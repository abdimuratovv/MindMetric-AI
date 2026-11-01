"""Real browser checks, using the existing explicitly disposable server fixture."""
import json
import os
import re
from playwright.sync_api import expect
import browser_cluster2_smoke as harness


def visible_text(value):
    return re.sub(r'```[^\n]*\n(.*?)```', lambda m: m[1].rstrip('\n'), value, flags=re.S)


def exercise_ui(page, output, root):
    sources = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((root / 'backend/apps/development/content/cluster3').glob('*.v1.json'))]
    sources.sort(key=lambda d: d['module']['order'])
    locales = {d['module']['key']: json.loads((root / 'backend/apps/development/content/translations' / f"{d['module']['key']}.v1.ru.json").read_text(encoding='utf-8')) for d in sources}
    language = 'uz'; answered = 0; downloads = 0

    def settle():
        page.wait_for_load_state('networkidle')
        expect(page.locator('.dev-heading h1')).to_be_visible()
        expect(page.locator('.dev-cluster-selector, .dev-module-title').first).to_be_visible()

    def button(key):
        return page.locator('.mm-dev').get_by_role('button', name=harness.LABELS[language][key], exact=False)

    def switch(value):
        nonlocal language
        page.locator('.mm-dev').get_by_role('button', name=value.upper(), exact=True).click()
        language = value; settle()
        if page.locator('.dev-module-title').count():
            expect(page.locator('.dev-module-title h2')).to_have_attribute('lang', value)
        else:
            expect(page.locator('.dev-module h2').first).to_have_attribute('lang', value)

    def catalogue():
        if page.locator('.dev-module-title').count():
            page.locator('.dev-heading-actions').get_by_role('button', name=harness.LABELS[language]['catalogue'], exact=False).click()
            settle()
        expect(page.locator('.dev-cluster-selector button')).to_have_count(3)

    def mobile(name):
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_function('document.querySelector(".mm-shell-sidebar").getBoundingClientRect().right <= 1')
        assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1')
        page.screenshot(path=str(output / name), full_page=True)
        page.set_viewport_size({'width': 1440, 'height': 1000})

    settle(); catalogue()
    for cluster, count in ((1, 6), (2, 6), (3, 4)):
        page.locator(f'.dev-cluster-selector button[data-cluster="{cluster}"]').click()
        expect(page.locator('.dev-module')).to_have_count(count)
    page.reload(); settle()
    expect(page.locator('.dev-cluster-selector button[data-cluster="3"]')).to_have_attribute('aria-pressed', 'true')
    page.screenshot(path=str(output / 'catalogue-uz.png'), full_page=True)
    mobile('catalogue-mobile.png')
    if os.environ.get('CLUSTER3_CATALOGUE_ONLY') == '1':
        switch('ru')
        expect(page.locator('.dev-module')).to_have_count(4)
        page.screenshot(path=str(output / 'catalogue-ru.png'), full_page=True)
        mobile('catalogue-ru-mobile.png')
        return {'passed': True, 'catalogue_only': True, 'clusters': 3, 'modules': 16, 'mobile_overflow': False}
    for data in sources:
        key = data['module']['key']; locale = locales[key]
        catalogue()
        page.locator('.dev-cluster-selector button[data-cluster="3"]').click()
        title = locale['title'] if language == 'ru' else data['module']['title_uz']
        page.locator('.dev-module').filter(has_text=title).get_by_role('button').click(); settle()
        expect(page.locator('.dev-study-files')).to_have_count(0)
        for purpose in ('precheck', 'practice', 'postcheck'):
            if purpose == 'practice':
                for lang in ('ru', 'uz'):
                    switch(lang)
                    for index, lesson in enumerate(data['lessons']):
                        page.locator('.dev-lesson-nav button').nth(index).click()
                        local = locale['lessons'][lesson['key']]
                        expect(page.locator('.dev-lesson h3')).to_have_text(local['title'] if lang == 'ru' else lesson['title_uz'])
                    expect(page.locator('.dev-project')).to_have_count(len(data['projects']))
                page.locator('.dev-lesson-nav button').first.click()
                page.locator('.dev-example summary').click()
                if key == 'code-debugging':
                    expect(page.locator('.dev-example pre code')).to_contain_text('if 4 > 2')
                    page.reload(); settle()
                    expect(page.locator('.dev-example pre code')).to_be_visible()
                    mobile('debugging-code-mobile.png')
                if data['projects']:
                    page.locator('.dev-project summary').first.click()
                    page.reload(); settle()
                    expect(page.locator('.dev-project').first).to_have_attribute('open', '')
                for index, file in enumerate(data['study_files']):
                    with page.expect_download() as info:
                        page.locator('.dev-study-files button').nth(index).click()
                    download = info.value
                    assert download.suggested_filename == file['filename']
                    assert download.path().read_text(encoding='utf-8') == file['content']
                    downloads += 1
                for index in range(5):
                    page.locator('.dev-lesson-nav button').nth(index).click()
                    button('study').click(); settle()
                if key == 'documentation-learning':
                    page.screenshot(path=str(output / 'documentation-study.png'), full_page=True)
                    mobile('documentation-study-mobile.png')
            button({'precheck': 'precheck', 'practice': 'practice', 'postcheck': 'postcheck'}[purpose]).click(); settle()
            if purpose != 'practice':
                expect(page.locator('.dev-study-files')).to_have_count(0)
                expect(page.locator('.dev-project')).to_have_count(0)
            questions = {q['key']: q for q in data['exercises']}
            for index, qkey in enumerate(data['blueprint'][purpose + '_order']):
                question = questions[qkey]
                prompt = locale['exercises'][qkey]['prompt'] if language == 'ru' else question['prompt_uz']
                expect(page.locator('.dev-question')).to_have_text(visible_text(prompt))
                if purpose == 'practice' and index == 0:
                    button('hint').click(); settle()
                form = page.locator('.dev-exercise form')
                correct = purpose != 'precheck'
                if question['format'] == 'numeric':
                    form.locator('input[type=text]').fill(question['answer_key']['value'] if correct else '999999')
                else:
                    chosen = question['answer_key']['option_id'] if correct else next(o['id'] for o in question['options'] if o['id'] != question['answer_key']['option_id'])
                    form.locator(f'input[type=radio][value="{chosen}"]').check()
                button('submit').click(); settle(); answered += 1
                if purpose == 'practice':
                    button('next').click(); settle()
            button('finish').click(); settle()
        expect(page.locator('.dev-metrics')).to_contain_text('100%')
    catalogue(); switch('ru')
    page.screenshot(path=str(output / 'catalogue-ru.png'), full_page=True)
    mobile('catalogue-ru-mobile.png')
    assert answered == 80 and downloads == 2
    return {'passed': True, 'clusters': 3, 'catalogue_modules': 16, 'cluster3_complete_modules': 4,
            'answered': answered, 'bilingual_lessons': 20, 'downloads_verified': downloads,
            'code_blocks': True, 'refresh_preserved': True, 'mobile_overflow': False}


if __name__ == '__main__':
    harness.exercise_ui = exercise_ui
    harness.main()

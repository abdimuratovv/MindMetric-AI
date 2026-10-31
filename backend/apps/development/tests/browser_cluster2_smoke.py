"""Real two-cluster UI checks on an explicitly disposable SQLite fixture."""
import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import expect, sync_playwright
from browser_smoke import free_port, wait_ready


LABELS = {
    'uz': {'catalogue': 'Modullar', 'start': 'Modulni boshlash', 'resume': 'Davom ettirish',
           'precheck': 'Boshlang‘ich tekshiruvni boshlash', 'submit': 'Javobni yuborish',
           'finish': 'Yakunlash va natijani ko‘rish', 'study': 'Darsni o‘rgandim',
           'practice': 'Mashqlarni boshlash', 'postcheck': 'Yakuniy tekshiruvni boshlash',
           'hint': 'Yordam olish', 'next': 'Keyingi savol', 'return': 'Davom etayotgan mashg‘ulotga qaytish'},
    'ru': {'catalogue': 'Модули', 'start': 'Начать модуль', 'resume': 'Продолжить',
           'precheck': 'Начать входную проверку', 'submit': 'Отправить ответ',
           'finish': 'Завершить и посмотреть результат', 'study': 'Урок изучен',
           'practice': 'Начать тренировку', 'postcheck': 'Начать итоговую проверку',
           'hint': 'Получить подсказку', 'next': 'Следующий вопрос', 'return': 'Вернуться к текущей сессии'},
}


def exercise_ui(page, output, root):
    sources, translations, questions = {}, {}, {}
    for directory in ('cluster1', 'cluster2'):
        for path in (root / 'backend/apps/development/content' / directory).glob('*.v1.json'):
            data = json.loads(path.read_text(encoding='utf-8'))
            key = data['module']['key']; sources[key] = data
            locale_path = path.parent.parent / 'translations' / (path.stem + '.ru.json')
            translated = json.loads(locale_path.read_text(encoding='utf-8')) if locale_path.exists() else None
            translations[key] = translated
            for q in data['exercises']:
                questions[q['prompt_uz']] = q
                if translated:
                    questions[translated['exercises'][q['key']]['prompt']] = q
    language = 'uz'
    answered = 0

    def settled():
        page.wait_for_load_state('networkidle')
        expect(page.locator('.dev-heading h1')).to_be_visible()

    def button(name):
        return page.locator('.mm-dev').get_by_role('button', name=LABELS[language][name], exact=False)

    def switch_language(value):
        nonlocal language
        page.locator('.mm-dev').get_by_role('button', name=value.upper(), exact=True).click()
        language = value; settled()

    def select_cluster(number):
        selector = page.locator(f'.dev-cluster-selector button[data-cluster="{number}"]')
        selector.click(); expect(selector).to_have_attribute('aria-pressed', 'true')

    def catalogue():
        if page.locator('.dev-module-title').count():
            page.locator('.dev-heading-actions').get_by_role('button', name=LABELS[language]['catalogue'], exact=False).click()
            settled()
        expect(page.locator('.dev-cluster-selector')).to_be_visible()

    def open_module(key):
        catalogue()
        source = sources[key]; select_cluster(source['module'].get('cluster', 1))
        title = translations[key]['title'] if language == 'ru' and translations[key] else source['module']['title_uz']
        card = page.locator('.dev-module').filter(has_text=title)
        card.get_by_role('button').click(); settled()
        expect(page.locator('.dev-module-title h2')).to_have_text(title)

    def answer_current(correct=True, refresh_draft=False):
        nonlocal answered
        heading = page.locator('.dev-question')
        prompt = heading.text_content()
        q = questions[prompt]
        form = page.locator('.dev-exercise form')
        if q['format'] == 'numeric':
            value = q['answer_key']['value'] if correct else '999999'
            form.locator('input[type=text]').fill(value)
            if refresh_draft:
                page.reload(); settled()
                expect(page.locator('.dev-exercise input[type=text]')).to_have_value(value)
        else:
            value = q['answer_key']['option_id'] if correct else next(o['id'] for o in q['options'] if o['id'] != q['answer_key']['option_id'])
            form.locator(f'input[value="{value}"]').check()
        button('submit').click()
        if q['purpose'] == 'practice':
            expect(page.locator('.dev-feedback')).to_be_visible()
        else:
            page.wait_for_function('(old) => !document.querySelector(".dev-question") || document.querySelector(".dev-question").textContent !== old', arg=prompt)
        answered += 1
        return q

    def finish():
        button('finish').click(); settled()

    def mobile_screenshot(name):
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_function('document.querySelector(".mm-shell-sidebar").getBoundingClientRect().right <= 1')
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), name + ': mobile overflow'
        page.screenshot(path=str(output / name), full_page=True)
        page.set_viewport_size({'width': 1440, 'height': 1000})

    settled()
    expect(page.locator('.dev-cluster-selector button')).to_have_count(2)
    print('Rendered cluster choices:', page.locator('.dev-cluster-selector button').all_text_contents(), flush=True)
    second = page.locator('.dev-cluster-selector button[data-cluster="2"]')
    second.focus(); page.keyboard.press('Enter')
    expect(second).to_have_attribute('aria-pressed', 'true')
    expect(page.locator('.dev-module')).to_have_count(6)
    assert [p.inner_text().split('/')[-1].strip() for p in page.locator('.dev-module > .dev-eyebrow').all()] == [f'2.{i}' for i in range(1, 7)]
    switch_language('ru')
    for key, data in sources.items():
        if data['module'].get('cluster') == 2:
            card = page.locator('.dev-module').filter(has_text=translations[key]['title'])
            expect(card.locator('h2')).to_have_attribute('lang', 'ru')
    page.screenshot(path=str(output / 'catalogue-ru.png'), full_page=True)
    mobile_screenshot('catalogue-ru-mobile.png')
    page.reload(); settled()
    expect(page.locator('.dev-cluster-selector button[data-cluster="2"]')).to_have_attribute('aria-pressed', 'true')

    creative = 'creative-mini-apps'
    ru = translations[creative]; uz = sources[creative]
    open_module(creative)
    expect(page.locator('.dev-notation')).to_be_visible()
    expect(page.locator('.dev-notation')).to_have_attribute('open', '')
    expect(page.locator('.dev-notation ul')).to_have_text(''.join(ru['notation']))
    expect(page.locator('.dev-project')).to_have_count(0)
    button('precheck').click()
    expect(page.locator('.dev-notation')).to_have_count(0)
    first = page.locator('.dev-exercise input[type=radio]').first
    first.check(); draft = first.get_attribute('value')
    switch_language('uz')
    expect(page.locator(f'.dev-exercise input[value="{draft}"]')).to_be_checked()
    page.reload(); settled()
    expect(page.locator(f'.dev-exercise input[value="{draft}"]')).to_be_checked()
    catalogue(); select_cluster(1)
    expect(page.locator('.dev-priority').first).to_contain_text('2.6')
    open_module('arithmetic-algebra')
    expect(button('precheck')).to_be_disabled()
    expect(page.locator('.dev-project, .dev-notation, .dev-lesson')).to_have_count(0)
    button('return').click(); settled()
    expect(page.locator(f'.dev-exercise input[value="{draft}"]')).to_be_checked()
    switch_language('ru')
    for _ in range(5): answer_current(False)
    finish()
    expect(page.locator('.dev-project')).to_have_count(2)
    for lang in ('uz', 'ru'):
        switch_language(lang)
        for index, lesson in enumerate(uz['lessons']):
            page.locator('.dev-lesson-nav button').nth(index).click()
            local = ru['lessons'][lesson['key']]
            expect(page.locator('.dev-lesson h3')).to_have_text(local['title'] if lang == 'ru' else lesson['title_uz'])
            if page.locator('.dev-example').get_attribute('open') is None:
                page.locator('.dev-example summary').click()
            expect(page.locator('.dev-example .dev-math').first).to_have_text(
                local['worked_example']['prompt'] if lang == 'ru' else lesson['worked_example']['prompt_uz'])
    page.locator('.dev-lesson-nav button').nth(2).click()
    if page.locator('.dev-example').get_attribute('open') is None:
        page.locator('.dev-example summary').click()
    page.locator('.dev-project summary').first.focus(); page.keyboard.press('Enter')
    page.locator('.dev-project summary').nth(1).click()
    expect(page.locator('.dev-project').first).to_have_attribute('open', '')
    expect(page.locator('.dev-project').first.locator('.dev-project-brief')).to_have_text(ru['projects']['project-study-planner']['brief'])
    expect(page.locator('.dev-project').first.locator('h4')).to_have_text(['Ограничения', 'Этапы работы', 'Материалы результата', 'Критерии самопроверки'])
    page.screenshot(path=str(output / 'creative-projects-ru.png'), full_page=True)
    switch_language('uz')
    expect(page.locator('.dev-lesson h3')).to_have_text(uz['lessons'][2]['title_uz'])
    expect(page.locator('.dev-project').first.locator('.dev-project-brief')).to_have_text(uz['projects'][0]['brief_uz'])
    page.reload(); settled()
    expect(page.locator('.dev-lesson h3')).to_have_text(uz['lessons'][2]['title_uz'])
    expect(page.locator('.dev-example')).to_have_attribute('open', '')
    expect(page.locator('.dev-project').first).to_have_attribute('open', '')
    switch_language('ru')
    mobile_screenshot('creative-projects-ru-mobile.png')

    # Reverse direction: a legacy check must also hide cluster-two study resources.
    open_module('arithmetic-algebra'); button('precheck').click()
    catalogue(); open_module(creative)
    expect(page.locator('.dev-project, .dev-notation, .dev-lesson')).to_have_count(0)
    switch_language('uz'); page.reload(); settled()
    expect(page.locator('.dev-project, .dev-notation, .dev-lesson')).to_have_count(0)
    button('return').click(); settled()
    for _ in range(5): answer_current(True)
    finish()

    open_module(creative); switch_language('ru')
    for i in range(5):
        page.locator('.dev-lesson-nav button').nth(i).click()
        button('study').click(); settled()
    button('practice').click()
    for i in range(10):
        if i == 0:
            button('hint').click(); settled()
            q = questions[page.locator('.dev-question').text_content()]
            expect(page.locator('.dev-exercise .dev-hint')).to_have_text(ru['exercises'][q['key']]['hint'])
            switch_language('uz')
            expect(page.locator('.dev-exercise .dev-hint')).to_have_text(q['hint_uz'])
            switch_language('ru')
        q = answer_current(True, refresh_draft=i == 3)
        if i == 0:
            switch_language('uz')
            expect(page.locator('.dev-feedback')).to_be_visible()
            expect(page.locator('.dev-feedback .dev-math').first).to_have_text(q['prompt_uz'])
            switch_language('ru')
        button('next').click()
    finish(); button('postcheck').click()
    expect(page.locator('.dev-project, .dev-notation, .dev-lesson')).to_have_count(0)
    for _ in range(5): answer_current(True)
    finish()
    expect(page.locator('.dev-metrics')).to_contain_text('100%')
    expect(page.locator('.dev-metrics')).to_contain_text('+100')
    page.screenshot(path=str(output / 'creative-completed-ru.png'), full_page=True)

    # Every other new module: real precheck, both-language lessons and examples.
    for key, data in sorted(sources.items(), key=lambda item: item[1]['module']['order']):
        if data['module'].get('cluster') != 2 or key == creative:
            continue
        open_module(key)
        expect(page.locator('.dev-notation')).to_be_visible()
        button('precheck').click()
        for _ in range(5): answer_current(True)
        finish()
        for lang in ('uz', 'ru'):
            switch_language(lang)
            for i, lesson in enumerate(data['lessons']):
                page.locator('.dev-lesson-nav button').nth(i).click()
                target = translations[key]['lessons'][lesson['key']]
                expect(page.locator('.dev-lesson h3')).to_have_text(target['title'] if lang == 'ru' else lesson['title_uz'])
                if not page.locator('.dev-example').get_attribute('open') == '':
                    page.locator('.dev-example summary').click()
                expect(page.locator('.dev-example .dev-math').first).to_have_text(
                    target['worked_example']['prompt'] if lang == 'ru' else lesson['worked_example']['prompt_uz'])
        if key == 'loops-recursion':
            expect(page.locator('.dev-pseudocode')).to_be_visible()
            page.screenshot(path=str(output / 'recursion-lesson-ru.png'), full_page=True)
            mobile_screenshot('recursion-lesson-ru-mobile.png')
    assert answered == 50, answered
    return {'passed': True, 'clusters': 2, 'catalogue_modules': 12, 'visible_topics_per_cluster': 6,
            'answered': answered, 'cluster2_prechecks': 6, 'bilingual_lessons_and_examples': 30,
            'creative_module_complete': True, 'self_review_projects': 2, 'keyboard_cluster_and_project_controls': True,
            'radio_and_numeric_drafts_after_refresh': True, 'draft_after_cluster_roundtrip': True,
            'selected_lesson_example_projects_after_refresh': True, 'cross_cluster_check_privacy': True,
            'hint_feedback_language_swap': True, 'mobile_overflow': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', required=True)
    parser.add_argument('--browser-executable', default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    output = Path(args.artifacts).resolve(); output.mkdir(parents=True, exist_ok=True)
    fixture = root / 'backups' / ('cluster2-browser-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    fixture.mkdir(parents=True)
    env = {**os.environ, 'DEVELOPMENT_BROWSER_DB_PATH': str(fixture / 'smoke.sqlite3'),
           'DEVELOPMENT_BROWSER_TOKEN_PATH': str(fixture / 'token.json'),
           'DJANGO_SETTINGS_MODULE': 'apps.development.tests.browser_settings', 'DEVELOPMENT_BROWSER_CLUSTERS': 'all'}
    python = root / 'backend/venv/Scripts/python.exe'
    subprocess.run([str(python), str(Path(__file__).with_name('browser_fixture.py'))], env=env, cwd=root, check=True)
    token = json.loads((fixture / 'token.json').read_text(encoding='utf-8'))
    backend_port, frontend_port = free_port(), free_port()
    env['API_PROXY_TARGET'] = f'http://127.0.0.1:{backend_port}'
    commands = [[str(python), 'backend/manage.py', 'runserver', f'127.0.0.1:{backend_port}', '--noreload'],
                [shutil.which('node'), str(root / 'frontend/node_modules/vite/bin/vite.js'), '--host', '127.0.0.1', '--port', str(frontend_port)]]
    processes, logs = [], []
    try:
        for label, command in zip(('backend', 'frontend'), commands):
            log = (fixture / f'{label}.log').open('w', encoding='utf-8'); logs.append(log)
            processes.append(subprocess.Popen(command, cwd=root if label == 'backend' else root / 'frontend', env=env,
                                             stdout=log, stderr=subprocess.STDOUT, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)))
        wait_ready(f'http://127.0.0.1:{backend_port}/api/development/capabilities/', processes[0])
        wait_ready(f'http://127.0.0.1:{frontend_port}/', processes[1])
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, executable_path=args.browser_executable)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            errors = []; page.on('pageerror', lambda error: errors.append(str(error)))
            page.add_init_script('localStorage.setItem("mindmetric_access_token", ' + json.dumps(token['access']) + '); if(!localStorage.getItem("mindmetric_language")) localStorage.setItem("mindmetric_language", "uz");')
            try:
                page.goto(f'http://127.0.0.1:{frontend_port}/#development')
                result = exercise_ui(page, output, root)
                assert not errors, errors
                result['javascript_errors'] = errors
                (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
                print(json.dumps(result), flush=True)
            except Exception:
                page.screenshot(path=str(output / 'failure.png'), full_page=True)
                raise
            finally:
                browser.close()
    finally:
        for process in reversed(processes):
            process.terminate()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait(timeout=5)
        for log in logs: log.close()


if __name__ == '__main__':
    main()

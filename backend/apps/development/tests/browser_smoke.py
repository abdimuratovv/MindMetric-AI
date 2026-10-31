"""Real React/Django learning flow against a disposable fixture database.

Run with a Python that has Playwright and its Chromium browser installed:
    python backend/apps/development/tests/browser_smoke.py --artifacts ABSOLUTE_DIRECTORY
"""

import argparse
import json
import os
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def free_port():
    with socket.socket() as server:
        server.bind(('127.0.0.1', 0))
        return server.getsockname()[1]


def wait_ready(url, process):
    deadline = time.monotonic() + 40
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError('Smoke server exited before becoming ready; inspect server logs.')
        try:
            urllib.request.urlopen(url, timeout=1).close()
            return
        except urllib.error.HTTPError:
            return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(.2)
    raise RuntimeError('Smoke server startup timed out.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', required=True)
    parser.add_argument('--browser-executable', default=None, help='Optional installed Chromium/Chrome executable.')
    parser.add_argument('--all-modules', action='store_true', help='Also verify the six-module catalogue and each new module entry.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    output = Path(args.artifacts).resolve()
    output.mkdir(parents=True, exist_ok=True)
    fixture = root / 'backups' / ('development-browser-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    fixture.mkdir(parents=True)
    environment = os.environ.copy()
    environment.update({
        'DEVELOPMENT_BROWSER_DB_PATH': str(fixture / 'smoke.sqlite3'),
        'DEVELOPMENT_BROWSER_TOKEN_PATH': str(fixture / 'token.json'),
        'DJANGO_SETTINGS_MODULE': 'apps.development.tests.browser_settings',
        'DEVELOPMENT_BROWSER_ALL_CONTENT': '1' if args.all_modules else '0',
    })
    python = root / 'backend/venv/Scripts/python.exe'
    subprocess.run([str(python), str(Path(__file__).with_name('browser_fixture.py'))], env=environment, cwd=root, check=True)
    token = json.loads((fixture / 'token.json').read_text(encoding='utf-8'))
    data = json.loads((root / 'backend/apps/development/content/cluster1/arithmetic-algebra.v1.json').read_text(encoding='utf-8'))
    by_prompt = {row['prompt_uz']: row for row in data['exercises']}
    russian = {key: json.loads((root / 'backend/apps/development/content/translations' / f'{key}.v1.ru.json').read_text(encoding='utf-8'))
               for key in ('arithmetic-algebra', 'mathematical-logic', 'sets-and-relations',
                           'number-theory-discrete-mathematics', 'functions-sequences-combinatorics', 'matrices-linear-algebra')}
    if args.all_modules:
        for source in (root / 'backend/apps/development/content/cluster1').glob('*.v1.json'):
            by_prompt.update({row['prompt_uz']: row for row in json.loads(source.read_text(encoding='utf-8'))['exercises']})
    backend_port, frontend_port = free_port(), free_port()
    environment['API_PROXY_TARGET'] = f'http://127.0.0.1:{backend_port}'
    commands = [
        [str(python), 'backend/manage.py', 'runserver', f'127.0.0.1:{backend_port}', '--noreload'],
        [shutil.which('node'), str(root / 'frontend/node_modules/vite/bin/vite.js'), '--host', '127.0.0.1', '--port', str(frontend_port)],
    ]
    processes, logs = [], []
    page_errors, requests = [], []
    try:
        for label, command in zip(('backend', 'frontend'), commands):
            log = (fixture / f'{label}.log').open('w', encoding='utf-8')
            logs.append(log)
            processes.append(subprocess.Popen(command, cwd=root if label == 'backend' else root / 'frontend', env=environment,
                stdout=log, stderr=subprocess.STDOUT, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)))
        # Vite executable is relative to its frontend working directory.
        wait_ready(f'http://127.0.0.1:{backend_port}/api/development/capabilities/', processes[0])
        wait_ready(f'http://127.0.0.1:{frontend_port}/', processes[1])
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, executable_path=args.browser_executable)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.on('pageerror', lambda error: page_errors.append(str(error)))
            page.on('request', lambda request: requests.append(request.post_data_json)
                    if request.url.endswith('/answers/') and request.method == 'POST' else None)
            page.add_init_script('localStorage.setItem("mindmetric_access_token", '+json.dumps(token['access'])+'); localStorage.setItem("mindmetric_language", "uz");')
            try:
                page.goto(f'http://127.0.0.1:{frontend_port}/#development')
                page.wait_for_load_state('networkidle')
                def switch_language(language):
                    page.locator('.mm-dev').get_by_role('button', name=language.upper(), exact=True).click()
                    page.wait_for_load_state('networkidle')

                expect(page.locator('.dev-module')).to_have_count(6 if args.all_modules else 1)
                switch_language('ru')
                expect(page.locator('.dev-module').filter(has_text=russian['arithmetic-algebra']['title'])).to_be_visible()
                if args.all_modules:
                    for translated in russian.values():
                        card = page.locator('.dev-module').filter(has_text=translated['title'])
                        expect(card).to_be_visible()
                        expect(card).to_contain_text('Учебный материал на русском языке')
                    expect(page.get_by_text('Учебный материал на узбекском языке', exact=True)).to_have_count(0)
                switch_language('uz')
                expect(page.locator('.dev-priority')).to_have_count(2 if args.all_modules else 1)
                page.set_viewport_size({'width': 390, 'height': 844})
                page.wait_for_function('document.querySelector(".mm-shell-sidebar").getBoundingClientRect().right <= 1')
                assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Plan mobile overflow'
                page.screenshot(path=str(output / 'plan-mobile.png'), full_page=True)
                page.set_viewport_size({'width': 1440, 'height': 1000})
                original = page.locator('.dev-module').filter(has_text=data['module']['title_uz'])
                expect(original.get_by_role('button', name='Modulni boshlash', exact=False)).to_be_visible()
                page.screenshot(path=str(output / 'catalogue.png'), full_page=True)
                original.get_by_role('button', name='Modulni boshlash', exact=False).click()
                page.get_by_role('button', name='Boshlang‘ich tekshiruvni boshlash', exact=False).click()
                draft=page.locator('.dev-exercise input[type=radio]').first
                draft.check()
                draft_id=draft.get_attribute('value')
                switch_language('ru')
                expect(page.locator('.dev-question')).to_have_text(russian['arithmetic-algebra']['exercises']['arith-precheck-01']['prompt'])
                expect(page.locator(f'.dev-exercise input[value="{draft_id}"]')).to_be_checked()
                assert page.locator('.dev-question').get_attribute('lang')=='ru'
                page.screenshot(path=str(output/'precheck-ru.png'),full_page=True)
                switch_language('uz')
                expect(page.locator(f'.dev-exercise input[value="{draft_id}"]')).to_be_checked()

                def answer_current(correct, *, lose_response=False, invalid_first=False):
                    heading = page.locator('.dev-question')
                    prompt = heading.inner_text()
                    question = by_prompt[prompt]
                    form = page.locator('.dev-exercise form')
                    if question['format'] == 'numeric':
                        field = form.locator('input[type=text]')
                        if invalid_first:
                            field.fill('1+2')
                            form.get_by_role('button', name='Javobni yuborish', exact=True).click()
                            expect(page.get_by_role('alert')).to_be_visible()
                            expect(field).to_be_enabled()
                        field.fill(question['answer_key']['value'] if correct else '999')
                    else:
                        option = question['answer_key']['option_id']
                        if not correct:
                            option = next(row['id'] for row in question['options'] if row['id'] != option)
                        form.locator(f'input[value="{option}"]').check()
                    if lose_response:
                        def lose(route):
                            route.fetch()  # Server commits, but the browser loses the response.
                            route.abort('failed')
                        page.route('**/api/development/sessions/*/answers/', lose, times=1)
                    form.get_by_role('button', name='Javobni yuborish', exact=True).click()
                    if lose_response:
                        expect(page.get_by_role('alert')).to_be_visible()
                        page.get_by_role('button', name='Shu javobni qayta yuborish', exact=True).click()
                        assert requests[-2]['idempotency_key'] == requests[-1]['idempotency_key']
                    if question['purpose'] == 'practice':
                        expect(page.locator('.dev-feedback')).to_be_visible()
                    else:
                        page.wait_for_function('(old) => !document.querySelector(".dev-question") || document.querySelector(".dev-question").textContent !== old', arg=prompt)

                for index in range(5):
                    answer_current(False, invalid_first=index == 1, lose_response=index == 2)
                    if index == 2:
                        page.reload()
                        page.wait_for_load_state('networkidle')
                        expect(page.locator('.dev-exercise-top')).to_contain_text('3 / 5')
                page.get_by_role('button', name='Yakunlash va natijani ko‘rish', exact=False).click()
                expect(page.locator('.dev-lesson')).to_be_visible()
                page.locator('.dev-lesson-nav button').nth(2).click()
                page.locator('.dev-example summary').click()
                switch_language('ru')
                translated_lesson=russian['arithmetic-algebra']['lessons']['arith-lesson-substitution']
                expect(page.locator('.dev-lesson h3')).to_have_text(translated_lesson['title'])
                expect(page.locator('.dev-example .dev-math').first).to_have_text(translated_lesson['worked_example']['prompt'])
                expect(page.locator('.dev-example')).to_have_attribute('open','')
                page.screenshot(path=str(output/'lesson-ru.png'),full_page=True)
                switch_language('uz')
                expect(page.locator('.dev-lesson h3')).to_have_text(data['lessons'][2]['title_uz'])
                page.locator('.dev-lesson-nav button').first.click()
                page.screenshot(path=str(output / 'lesson.png'), full_page=True)
                for index in range(5):
                    before = page.locator('.dev-lesson h3').inner_text()
                    page.get_by_role('button', name='Darsni o‘rgandim', exact=False).click()
                    if index < 4:
                        page.wait_for_function('(old) => document.querySelector(".dev-lesson h3").textContent !== old', arg=before)
                page.get_by_role('button', name='Mashqlarni boshlash', exact=True).click()
                for index in range(10):
                    if index == 0:
                        page.get_by_role('button', name='Yordam olish', exact=True).click()
                        expect(page.locator('.dev-exercise .dev-hint')).to_be_visible()
                        switch_language('ru')
                        expect(page.locator('.dev-exercise .dev-hint')).to_have_text(russian['arithmetic-algebra']['exercises']['arith-practice-01']['hint'])
                        switch_language('uz')
                    answer_current(True)
                    if index == 0:
                        switch_language('ru')
                        expect(page.locator('.dev-feedback')).to_be_visible()
                        expect(page.locator('.dev-feedback .dev-math').first).to_have_text(russian['arithmetic-algebra']['exercises']['arith-practice-01']['prompt'])
                        switch_language('uz')
                        page.set_viewport_size({'width': 390, 'height': 844})
                        page.wait_for_function('document.querySelector(".mm-shell-sidebar").getBoundingClientRect().right <= 1')
                        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile overflow'
                        page.screenshot(path=str(output / 'practice-mobile.png'), full_page=True)
                        page.set_viewport_size({'width': 1440, 'height': 1000})
                    page.get_by_role('button', name='Keyingi savol', exact=False).click()
                page.get_by_role('button', name='Yakunlash va natijani ko‘rish', exact=False).click()
                page.get_by_role('button', name='Yakuniy tekshiruvni boshlash', exact=False).click()
                for index in range(5):
                    answer_current(index != 0)
                page.get_by_role('button', name='Yakunlash va natijani ko‘rish', exact=False).click()
                expect(page.locator('.dev-metrics')).to_contain_text('80%')
                expect(page.locator('.dev-metrics')).to_contain_text('+80')
                page.screenshot(path=str(output / 'report.png'), full_page=True)
                page.locator('.mm-dev').get_by_role('button', name='RU', exact=True).click()
                expect(page.locator('.dev-heading h1')).to_have_text('От способностей к навыкам')
                expect(page.locator('.dev-module-title')).to_contain_text('Учебный материал на русском языке')
                page.screenshot(path=str(output / 'report-ru.png'), full_page=True)
                opened = 0
                if args.all_modules:
                    page.locator('.mm-dev').get_by_role('button', name='UZ', exact=True).click()
                    expect(page.locator('.dev-heading h1')).to_have_text('Qobiliyatdan ko‘nikmaga')
                    others = [json.loads(p.read_text(encoding='utf-8')) for p in
                              (root/'backend/apps/development/content/cluster1').glob('*.v1.json') if p.name != 'arithmetic-algebra.v1.json']
                    for other in sorted(others, key=lambda d:d['module']['order']):
                        page.locator('.dev-heading-actions').get_by_role('button', name='Modullar', exact=False).click()
                        card=page.locator('.dev-module').filter(has_text=other['module']['title_uz'])
                        expect(card.locator('.dev-eyebrow')).to_contain_text(f'1.{other["module"]["order"]}')
                        card.get_by_role('button', name='Modulni boshlash', exact=False).click()
                        page.get_by_role('button', name='Boshlang‘ich tekshiruvni boshlash', exact=False).click()
                        first_key=other['blueprint']['precheck_order'][0]
                        first=next(q for q in other['exercises'] if q['key']==first_key)
                        expect(page.locator('.dev-question')).to_have_text(first['prompt_uz'])
                        page.reload()
                        page.wait_for_load_state('networkidle')
                        expect(page.locator('.dev-module-title h2')).to_have_text(other['module']['title_uz'])
                        expect(page.locator('.dev-question')).to_have_text(first['prompt_uz'])
                        opened+=1
                        translated = russian[other['module']['key']]
                        switch_language('ru')
                        expect(page.locator('.dev-question')).to_have_text(translated['exercises'][first_key]['prompt'])
                        switch_language('uz')
                        expect(page.locator('.dev-question')).to_have_text(first['prompt_uz'])
                        if other['module']['order']==6:
                            switch_language('ru')
                            expect(page.locator('.dev-question')).to_have_text(russian['matrices-linear-algebra']['exercises'][first_key]['prompt'])
                            switch_language('uz')
                            page.set_viewport_size({'width':390,'height':844})
                            page.wait_for_function('document.querySelector(".mm-shell-sidebar").getBoundingClientRect().right <= 1')
                            bounds = page.evaluate('''() => Object.fromEntries(
                                [".mm-dev", ".dev-steps", ".dev-exercise", ".dev-exercise-top"].map(selector => {
                                  const r=document.querySelector(selector).getBoundingClientRect();
                                  return [selector, {left:r.left, right:r.right, width:r.width}];
                                }))''')
                            print('Matrix mobile content bounds:', json.dumps(bounds), flush=True)
                            assert all(row['left'] >= 0 and row['right'] <= 391 for row in bounds.values()), bounds
                            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                            page.screenshot(path=str(output/'matrix-mobile.png'),full_page=True)
                        for _ in range(5):
                            answer_current(True)
                        page.get_by_role('button', name='Yakunlash va natijani ko‘rish', exact=False).click()
                        for index,lesson in enumerate(other['lessons']):
                            page.locator('.dev-lesson-nav button').nth(index).click()
                            switch_language('ru')
                            target=translated['lessons'][lesson['key']]
                            expect(page.locator('.dev-lesson h3')).to_have_text(target['title'])
                            expect(page.locator('.dev-lesson')).to_have_attribute('lang','ru')
                            for paragraph in target['theory']:
                                expect(page.locator('.dev-lesson')).to_contain_text(paragraph)
                            if not page.locator('.dev-example').get_attribute('open') == '':
                                page.locator('.dev-example summary').click()
                            expect(page.locator('.dev-example .dev-math').first).to_have_text(target['worked_example']['prompt'])
                            for step in target['worked_example']['solution_steps']:
                                expect(page.locator('.dev-example')).to_contain_text(step)
                            switch_language('uz')
                            expect(page.locator('.dev-lesson h3')).to_have_text(lesson['title_uz'])
                            expect(page.locator('.dev-example .dev-math').first).to_have_text(lesson['worked_example']['prompt_uz'])
                        switch_language('ru')
                        expect(page.locator('.dev-lesson h3')).to_have_text(translated['lessons'][other['lessons'][-1]['key']]['title'])
                        page.screenshot(path=str(output/f'topic-1-{other["module"]["order"]}-lesson-ru.png'),full_page=True)
                        switch_language('uz')
                assert not page_errors, page_errors
                result = {'passed': True, 'answered': 20 + opened * 5, 'precheck': 0, 'postcheck': 80,
                          'delta_percentage_points': 80, 'refresh_resume': True, 'invalid_input_correction': True,
                          'lost_response_retry': True, 'mobile_overflow': False, 'russian_content_swap': True,
                          'localized_modules': list(range(1,7)) if args.all_modules else [1], 'draft_answer_preserved': True, 'hint_feedback_lesson_preserved': True,
                          'javascript_errors': page_errors, 'catalogue_modules': 6 if args.all_modules else 1,
                          'opened_additional_modules': opened}
                (output / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
                print(json.dumps(result))
            except Exception:
                page.screenshot(path=str(output / 'failure.png'), full_page=True)
                raise
            finally:
                browser.close()
    finally:
        for process in reversed(processes):
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        for log in logs:
            log.close()


if __name__ == '__main__':
    main()

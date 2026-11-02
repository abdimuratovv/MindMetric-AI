"""Real API, results card and requested-cluster navigation in a disposable DB."""
import os
from playwright.sync_api import expect
import browser_cluster2_smoke as harness


def exercise_ui(page, output, root):
    base = page.url.split('/#')[0]
    page.wait_for_load_state('networkidle')
    page.locator('nav').get_by_role('button', name='Mening natijalarim', exact=True).click()
    expect(page.locator('[data-recommended-cluster="3"]')).to_be_visible()
    card = page.locator('.cluster-recommendation')
    expect(card).to_contain_text('III klasterni')
    expect(card).to_contain_text('40/100')
    page.screenshot(path=str(output / 'results-uz.png'), full_page=True)
    # A remembered enrollment must not override an explicit card navigation.
    user_id = page.evaluate('JSON.parse(atob(localStorage.mindmetric_access_token.split(".")[1])).user_id')
    page.evaluate('(id) => sessionStorage.setItem(`mindmetric-development:${id}`, "999999")', user_id)
    card.get_by_role('button').click()
    expect(page.locator('.dev-cluster-selector button[data-cluster="3"]')).to_have_attribute('aria-pressed', 'true')
    expect(page.locator('.dev-module')).to_have_count(4)
    page.reload()
    expect(page.locator('.dev-cluster-selector button[data-cluster="3"]')).to_have_attribute('aria-pressed', 'true')
    page.locator('.mm-dev').get_by_role('button', name='RU', exact=True).click()
    expect(page.locator('.cluster-recommendation')).to_contain_text('развивать кластер III')
    page.locator('nav').get_by_role('button', name='Мои результаты', exact=True).click()
    expect(page.locator('.cluster-recommendation')).to_contain_text('развивать кластер III')
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_function('document.querySelector(".mm-shell-sidebar").getBoundingClientRect().right <= 1')
    assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1')
    page.screenshot(path=str(output / 'results-ru-mobile.png'), full_page=True)
    page.locator('.cluster-recommendation').get_by_role('button').click()
    expect(page.locator('.dev-cluster-selector button[data-cluster="3"]')).to_have_attribute('aria-pressed', 'true')
    return {'passed': True, 'real_api': True, 'bilingual': True, 'requested_cluster_overrides_saved_enrollment': True,
            'refresh_preserves_cluster': True, 'mobile_overflow': False}


if __name__ == '__main__':
    os.environ['CLUSTER_GUIDANCE_SMOKE'] = '1'
    harness.exercise_ui = exercise_ui
    harness.main()

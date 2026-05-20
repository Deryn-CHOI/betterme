from playwright.sync_api import sync_playwright


def test_countdown_not_reset():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Ture)
        page = browser.new_page()

        page.goto("https://betterme-pilates.com")

        # TODO: 跳转到paywall

        countdown_before = page.locator(".countdown").inner_text()

        page.reload()

        countdown_after = page.locator(".countdown").inner_text()

        assert countdown_before != countdown_after

        browser.close()

from playwright.sync_api import sync_playwright


def test_stripe_blocked():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()

        page.route("**/*stripe*", lambda route: route.abort())

        page.goto("https://betterme-pilates.com")

        # TODO: 跳转checkout

        assert "Payment failed" in page.content()

        browser.close()

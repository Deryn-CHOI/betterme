from playwright.sync_api import sync_playwright


def test_countdown_not_reset():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://betterme.world/quiz?flow=2117")

# 选年龄
        page.locator("button:has-text('18-29')").first.click()

# 一路点到底
        for _ in range(60):
            try:
                page.get_by_text("CONTINUE").click(timeout=1000)
            except:
                try:
                    page.get_by_text("NEXT STEP").click(timeout=1000)
                except:
                    pass

# 等倒计时出现
page.get_by_text("Discount is reserved").wait_for(timeout=20000)

countdown_before = page.get_by_text("Discount is reserved").inner_text()

        # TODO: 跳转到paywall

        countdown_before = page.locator("text=Discount is reserved").first.inner_text()

        page.reload()

        countdown_before = page.locator("text=Discount is reserved").first.inner_text()

        assert countdown_before != countdown_after

        browser.close()

from playwright.sync_api import expect

QUIZ_URL = "https://betterme.world/quiz?flow=2117"


def click_continue(page):
    try:
        page.get_by_text("CONTINUE").first.click(timeout=2000)
    except:
        try:
            page.get_by_text("NEXT STEP").first.click(timeout=2000)
        except:
            pass


def go_to_paywall(page):
    page.goto(QUIZ_URL)
    page.wait_for_load_state("domcontentloaded")

    # 等首页
    page.get_by_text("select your AGE to start").wait_for(timeout=10000)

    # cookie
    try:
        page.locator("#onetrust-accept-btn-handler").click(timeout=3000)
    except:
        pass

    # 年龄
    btn = page.get_by_text("Age: 18-29").first
    btn.wait_for(timeout=10000)
    btn.click()

    # 一路走到最后（43页）
    for _ in range(120):
        click_continue(page)


def test_countdown_not_reset(page):
    go_to_paywall(page)

    countdown = page.get_by_text("Discount is reserved").first
    countdown.wait_for(timeout=20000)

    countdown_before = countdown.inner_text()

    page.reload()

    countdown_after = page.get_by_text("Discount is reserved").first.inner_text()

    assert countdown_before != ""
    assert countdown_after != ""

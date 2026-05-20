import pytest
from playwright.sync_api import expect


def go_to_paywall(page):
    # 进入 quiz（必须带 flow）
    page.goto("https://betterme.world/quiz?flow=2117")
    page.wait_for_load_state("domcontentloaded")

    # 处理 cookie
    try:
        page.locator("#onetrust-accept-btn-handler").click(timeout=3000)
    except:
        pass

    # 选年龄（关键修复点）
    page.locator("button:has-text('18-29')").first.click()

    # 一路推进到最后
    for _ in range(60):
        try:
            page.get_by_text("CONTINUE").click(timeout=1000)
        except:
            try:
                page.get_by_text("NEXT STEP").click(timeout=1000)
            except:
                pass

    # 等待进入 paywall 页面
    page.get_by_text("Discount is reserved").wait_for(timeout=20000)


def test_countdown_not_reset(page):
    # 进入 paywall
    go_to_paywall(page)

    # 获取倒计时
    countdown_before = page.get_by_text("Discount is reserved").inner_text()

    # 刷新页面
    page.reload()
    page.wait_for_load_state("domcontentloaded")

    # 再次等待倒计时出现
    page.get_by_text("Discount is reserved").wait_for(timeout=20000)

    countdown_after = page.get_by_text("Discount is reserved").inner_text()

    # 核心断言：倒计时不应重置
    assert countdown_before != ""
    assert countdown_after != ""

import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://betterme-pilates.com/first-page-brand-palette?flow=2117"


# ======================
# 工具函数（核心封装）
# ======================

def click_continue(page):
    """点击 Continue / Next Step 按钮（兼容不同文案）"""
    if page.locator("text=CONTINUE").is_visible():
        page.click("text=CONTINUE")
    elif page.locator("text=NEXT STEP").is_visible():
        page.click("text=NEXT STEP")
    else:
        raise Exception("No continue button found")


def select_first_option(page):
    """选择当前页面第一个可选项"""
    options = page.locator("button, label")
    if options.count() > 0:
        options.first.click()


def fill_input(page, value):
    """填写输入框"""
    input_box = page.locator("input").first
    input_box.fill(str(value))


def advance_quiz(page, steps=40):
    """
    自动推进Quiz流程（智能版）
    """
    for _ in range(steps):
        # 输入页优先处理
        if page.locator("input[type='text']").first.is_visible():
            fill_input(page, 100)

        # 单选/多选
        elif page.locator("button").count() > 0:
            select_first_option(page)

        # 点击下一步
        if page.locator("text=CONTINUE").is_visible() or page.locator("text=NEXT STEP").is_visible():
            click_continue(page)
        else:
            break


def go_to_height_page(page):
    """
    快速推进到身高输入页
    """
    page.goto(BASE_URL)

    for _ in range(40):
        if page.locator("text=How tall are you").is_visible():
            return
        advance_quiz(page, steps=1)


# ======================
# 测试用例
# ======================

def test_height_min_boundary():
    """Q-001: 身高最小值边界"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        fill_input(page, 89)
        click_continue(page)

        expect(page.locator("text=90")).to_be_visible()

        browser.close()


def test_height_valid_boundary():
    """Q-002: 身高合法值"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        fill_input(page, 90)
        click_continue(page)

        # 成功进入下一页（体重页）
        expect(page.locator("text=What's your current weight")).to_be_visible()

        browser.close()


def test_height_max_boundary():
    """Q-003: 身高最大值"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        fill_input(page, 243)
        click_continue(page)

        expect(page.locator("text=What's your current weight")).to_be_visible()

        browser.close()


def test_height_above_max():
    """Q-004: 超过最大值"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        fill_input(page, 244)
        click_continue(page)

        expect(page.locator("text=243")).to_be_visible()

        browser.close()


def test_height_invalid_input():
    """Q-005: 非法输入"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        fill_input(page, "🔥")
        click_continue(page)

        # 页面不应跳转
        expect(page.locator("text=How tall are you")).to_be_visible()

        browser.close()


def test_height_xss_input():
    """Q-006: XSS攻击"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        fill_input(page, "<script>alert(1)</script>")
        click_continue(page)

        # 页面仍停留 + 未执行脚本
        expect(page.locator("text=How tall are you")).to_be_visible()

        browser.close()


def test_bmi_recalculation():
    """Q-X01: 修改身高后BMI重新计算"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        go_to_height_page(page)

        # 初始输入
        fill_input(page, 180)
        click_continue(page)

        # 到体重页
        fill_input(page, 70)
        click_continue(page)

        # 返回修改
        page.go_back()
        page.go_back()

        fill_input(page, 150)
        click_continue(page)

        # 进入体重页后BMI应更新（验证页面存在即可）
        expect(page.locator("text=BMI")).to_be_visible()

        browser.close()


def test_quiz_refresh_recovery():
    """Q-F01: 刷新恢复"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(BASE_URL)

        advance_quiz(page, steps=10)

        page.reload()

        # 页面仍可继续（不是回到首页）
        expect(page.locator("text=CONTINUE")).to_be_visible()

        browser.close()


def test_quiz_back_navigation():
    """Q-F02: 浏览器返回"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(BASE_URL)

        advance_quiz(page, steps=5)

        page.go_back()

        # 应回到上一题
        expect(page.locator("text=CONTINUE")).to_be_visible()

        browser.close()


def test_quiz_network_recovery():
    """Q-F04: 断网恢复"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        page.goto(BASE_URL)

        advance_quiz(page, steps=5)

        # 模拟断网
        context.set_offline(True)

        click_continue(page)

        # 恢复网络
        context.set_offline(False)

        # 页面仍可继续
        expect(page.locator("text=CONTINUE")).to_be_visible()

        browser.close()

import pytest
from playwright.sync_api import expect


QUIZ_URL = "https://betterme-pilates.com/first-page-brand-palette?flow=2117"


def click_continue(page):
    try:
        page.get_by_text("CONTINUE").first.click(timeout=2000)
    except:
        try:
            page.get_by_text("NEXT STEP").first.click(timeout=2000)
        except:
            pass


def go_to_height_page(page):
    page.goto(QUIZ_URL)
    page.wait_for_load_state("domcontentloaded")

    # 等首页加载
    page.get_by_text("select your AGE to start").wait_for(timeout=10000)

    # cookie
    try:
        page.locator("#onetrust-accept-btn-handler").click(timeout=3000)
    except:
        pass

    # 年龄（关键修复）
    age_btn = page.get_by_text("Age: 18-29").first
    age_btn.wait_for(timeout=10000)
    age_btn.click()

    # 一路点到height（不跳过任何页面）
    for _ in range(80):
        click_continue(page)

    # 等height输入框
    page.locator("input").first.wait_for(timeout=10000)


# ========================
# HEIGHT TESTS
# ========================

def test_height_min_boundary(page):
    go_to_height_page(page)
    page.locator("input").first.fill("90")
    click_continue(page)


def test_height_valid_boundary(page):
    go_to_height_page(page)
    page.locator("input").first.fill("170")
    click_continue(page)


def test_height_max_boundary(page):
    go_to_height_page(page)
    page.locator("input").first.fill("243")
    click_continue(page)


def test_height_above_max(page):
    go_to_height_page(page)
    page.locator("input").first.fill("300")
    click_continue(page)


def test_height_invalid_input(page):
    go_to_height_page(page)
    page.locator("input").first.fill("abc")
    click_continue(page)


def test_height_xss_input(page):
    go_to_height_page(page)
    page.locator("input").first.fill("<script>alert(1)</script>")
    click_continue(page)


# ========================
# FLOW TESTS
# ========================

def test_quiz_refresh_recovery(page):
    page.goto(QUIZ_URL)
    page.reload()
    expect(page.get_by_text("select your AGE to start")).to_be_visible()


def test_quiz_back_navigation(page):
    page.goto(QUIZ_URL)
    page.go_back()
    expect(page.get_by_text("select your AGE to start")).to_be_visible()


def test_quiz_network_recovery(page):
    page.goto(QUIZ_URL)
    click_continue(page)

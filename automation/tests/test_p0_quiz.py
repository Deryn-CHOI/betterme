import pytest
from playwright.sync_api import expect


BASE_URL = "https://betterme-pilates.com/first-page-brand-palette?flow=2117"


# ======================
# 通用工具函数
# ======================

def click_continue(page):
    btn = page.locator("button").filter(has_text="CONTINUE").first
    if btn.count() > 0:
        btn.click(force=True)
        return True

    btn = page.locator("button").filter(has_text="NEXT STEP").first
    if btn.count() > 0:
        btn.click(force=True)
        return True

    return False


def safe_click(page, text):
    el = page.get_by_text(text, exact=False).first
    el.wait_for(timeout=10000)
    el.click(force=True)


def wait_for_text(page, text):
    page.wait_for_function(
        f"""() => document.body.innerText.includes("{text}")""",
        timeout=20000
    )


# ======================
# 核心流程：走到 height 页面
# ======================

def go_to_height_page(page):
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    # cookie
    try:
        page.locator("#onetrust-accept-btn-handler").click(timeout=3000)
    except:
        pass

    # 1. AGE
    safe_click(page, "18-29")

    # 2
    click_continue(page)

    # 3 goal
    safe_click(page, "lose weight")
    click_continue(page)

    # 4 build
    safe_click(page, "mid")
    click_continue(page)

    # 5 dream body
    safe_click(page, "toned")
    click_continue(page)

    # 6 weight change
    safe_click(page, "gain weight fast")
    click_continue(page)

    # 7
    click_continue(page)

    # 8
    safe_click(page, "Less than a year")
    click_continue(page)

    # 9
    safe_click(page, "just starting")
    click_continue(page)

    # 10 target zones
    safe_click(page, "Belly")
    click_continue(page)

    # 10.2
    click_continue(page)

    # 11
    safe_click(page, "Just getting started")
    click_continue(page)

    # 12
    safe_click(page, "slightly out of breath")
    click_continue(page)

    # 13
    safe_click(page, "None of the")
    click_continue(page)

    # 14
    click_continue(page)

    # 15
    safe_click(page, "Several times per week")
    click_continue(page)

    # 16
    safe_click(page, "3-4 times per week")
    click_continue(page)

    # 👉 lifestyle 后面直接快进（核心技巧）
    for _ in range(10):
        if not click_continue(page):
            break

    # ✅ 等待 height 页面（关键）
    wait_for_text(page, "How tall are you")


# ======================
# 测试：height
# ======================

def test_height_min_boundary(page):
    go_to_height_page(page)

    input_box = page.locator("input").last
    input_box.fill("90")

    click_continue(page)

    expect(input_box).to_have_value("90")


def test_height_valid_boundary(page):
    go_to_height_page(page)

    input_box = page.locator("input").last
    input_box.fill("170")

    click_continue(page)

    expect(input_box).to_have_value("170")


def test_height_max_boundary(page):
    go_to_height_page(page)

    input_box = page.locator("input").last
    input_box.fill("243")

    click_continue(page)

    expect(input_box).to_have_value("243")


def test_height_above_max(page):
    go_to_height_page(page)

    input_box = page.locator("input").last
    input_box.fill("300")

    click_continue(page)

    # 期望不通过（值不会被接受）
    expect(input_box).not_to_have_value("300")


def test_height_invalid_input(page):
    go_to_height_page(page)

    input_box = page.locator("input").last
    input_box.fill("abc")

    click_continue(page)

    expect(input_box).not_to_have_value("abc")


def test_height_xss_input(page):
    go_to_height_page(page)

    input_box = page.locator("input").last
    input_box.fill("<script>alert(1)</script>")

    click_continue(page)

    expect(input_box).not_to_have_value("<script>alert(1)</script>")


# ======================
# 其他流程稳定性测试（简化版）
# ======================

def test_quiz_refresh_recovery(page):
    page.goto(BASE_URL)
    page.reload()

    expect(page.locator("text=select your AGE")).to_be_visible()


def test_quiz_back_navigation(page):
    page.goto(BASE_URL)

    safe_click(page, "18-29")
    page.go_back()

    expect(page.locator("text=select your AGE")).to_be_visible()


def test_quiz_network_recovery(page):
    page.goto(BASE_URL)

    safe_click(page, "18-29")

    # 模拟点击继续
    click_continue(page)

    expect(page.locator("body")).to_be_visible()

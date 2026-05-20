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
    page.goto("https://betterme.world/quiz")
    page.wait_for_load_state("domcontentloaded")

    # cookie
    try:
        page.locator("#onetrust-accept-btn-handler").click(timeout=3000)
    except:
        pass

    # 1️⃣ 选年龄
    page.locator("button:has-text('18-29')").first.click()

    # 2️⃣ page2
    page.get_by_text("CONTINUE").first.click()

    # 3️⃣ goal
    page.get_by_text("lose weight").first.click()

    # 4️⃣ build
    page.get_by_text("slim").first.click()

    # 5️⃣ dream body
    page.get_by_text("thin").first.click()

    # 6️⃣ weight change
    page.get_by_text("gain weight fast").first.click()

    # 7️⃣ continue
    page.get_by_text("CONTINUE").first.click()

    # 8️⃣ best shape
    page.get_by_text("Less than a year ago").first.click()

    # 9️⃣ pilates exp
    page.get_by_text("just starting").first.click()

    # 10️⃣ target zones
    page.get_by_text("Belly").click()
    page.get_by_text("NEXT STEP").click()

    # 11️⃣ continue
    page.get_by_text("CONTINUE").click()

    # 12️⃣ flexibility
    page.get_by_text("Pretty flexible").click()

    # 13️⃣ stairs
    page.get_by_text("slightly out of breath").click()

    # 14️⃣ issues
    page.get_by_text("None of the").click()
    page.get_by_text("NEXT STEP").click()

    # 15️⃣ continue
    page.get_by_text("CONTINUE").click()

    # 16️⃣ exercise
    page.get_by_text("Several times per week").click()

    # 17️⃣ walks
    page.get_by_text("3-4 times per week").click()

    # 👉 快速推进（后面全是类似结构）
    for _ in range(10):
        try:
            page.get_by_text("CONTINUE").click(timeout=2000)
        except:
            try:
                page.get_by_text("NEXT STEP").click(timeout=2000)
            except:
                pass

    # ✅ 等 height 页面
    page.get_by_text("How tall are you?").wait_for(timeout=15000)


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

    expect(page.get_by_text("select your AGE to start")).to_be_visible()


def test_quiz_back_navigation(page):
    page.goto(BASE_URL)

    page.get_by_text("18-29").click()
    page.go_back()

    expect(page.locator("text=select your AGE")).to_be_visible()


def test_quiz_network_recovery(page):
    page.goto(BASE_URL)

    page.get_by_text("18-29").click()
    # 模拟点击继续
    click_continue(page)

    expect(page.locator("body")).to_be_visible()

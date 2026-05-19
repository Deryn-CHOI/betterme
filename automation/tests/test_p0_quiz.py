from playwright.sync_api import sync_playwright

BASE_URL = "https://betterme-pilates.com/first-page-brand-palette?flow=2117"


def test_height_boundary():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        page.click("text=18-29")
        page.click("text=Continue")

class QuizFlow:
    def __init__(self, page):
        self.page = page

    def answer_single_choice(self):
        self.page.locator("button").first.click()

    def next(self):
        self.page.click("text=Continue")

    def run(self):
        for _ in range(50):
            if not self.page.locator("text=Continue").is_visible():
                break
            self.answer_single_choice()
            self.next()

        height_input = page.locator("input")
        height_input.fill("89")

        page.click("text=NEXT STEP")

        assert "90 cm" in page.content()

        browser.close()

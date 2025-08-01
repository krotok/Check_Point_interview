from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.message = page.locator("#message")

    #goto url and wait 1000msec
    def navigate(self, url: str):
        self.page.goto(url, wait_until="load", timeout = 1000)

    #login with usernamr and password
    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_message(self) -> str:
        return self.message.inner_text()
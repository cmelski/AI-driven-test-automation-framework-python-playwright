from page_objects.shop import ShopPage


class LoginPage:

    def __init__(self, page):
        self.page = page
        self.username_input = self.page.locator('#user-name')
        self.password_input = self.page.locator('#password')
        self.login_button = self.page.locator('#login-button')
        self.login_error = self.page.locator("h3[data-test='error']")

    def login(self, user_name, password):
        self.username_input.fill(user_name)
        self.password_input.fill(password)
        self.login_button.click()

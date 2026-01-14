from page_objects.shop import ShopPage


class LoginPage:

    def __init__(self, page):
        self.page = page
        self.username_login_input = self.page.locator('[data-test="username"]')
        self.password_login_input = self.page.locator('[data-test="password"]')
        self.login_button = self.page.locator('input[type="submit"]')
        self.login_error = self.page.locator('h3[data-test="error"]')

    def valid_login(self, user_name, password):
        self.username_login_input.fill(user_name)
        self.password_login_input.fill(password)
        self.login_button.click()
        shop_page = ShopPage(self.page)
        return shop_page

    def invalid_login(self, user_name, password):
        self.username_login_input.fill(user_name)
        self.password_login_input.fill(password)
        self.login_button.click()


class ShopPage:

    def __init__(self, page):
        self.page = page
        self.title = self.page.locator('.title')
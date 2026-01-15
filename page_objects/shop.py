class ShopPage:

    def __init__(self, page):
        self.page = page
        self.url = self.page.url
        self.title = self.page.locator('.title')
        self.inventory_items = self.page.locator('.inventory_item')

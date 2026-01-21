class CartPage:

    def __init__(self, page):
        self.page = page
        self.cart_icon = self.page.locator('.shopping_cart_badge')
        self.cart_items = self.page.locator('.cart_item')
        self.checkout_button = self.page.locator('#checkout')
        self.continue_shopping_button = self.page.locator('#continue-shopping')

    def remove_product_from_cart(self, product):
        items = self.cart_items
        items_count = items.count()

        for i in range(items_count):
            item = items.nth(i)
            product_name = item.locator('.inventory_item_name').inner_text().strip()
            if product_name == product:
                remove_button = item.locator('button')
                remove_button.click()

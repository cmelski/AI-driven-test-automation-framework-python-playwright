class ProductPage:

    def __init__(self, page):
        self.page = page
        self.product_details_panel_selector = 'div.inventory_details'
        self.product_name = self.page.locator('div[data-test="inventory-item-name"]')
        self.product_description = self.page.locator("div[data-test='inventory-item-desc']")
        self.product_price = self.page.locator("div[data-test='inventory-item-price']")
        self.back_to_shop_button = self.page.locator('#back-to-products')
        self.add_to_cart_button = self.page.locator('#add-to-cart')
        self.remove_from_cart_button = self.page.locator('#remove')

    def get_product_details(self):
        return {
            "name": self.product_name.inner_text(),
            "price": self.product_price.inner_text(),
            "description": self.product_description.inner_text(),
        }

    def add_to_cart(self):
        self.add_to_cart_button.click()


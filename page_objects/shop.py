class ShopPage:

    def __init__(self, page):
        self.page = page
        self.title = self.page.locator('.title')
        self.url = self.page.url
        self.inventory_items = self.page.locator('.inventory_item')
        self.inventory_item_name = self.page.locator('.inventory_item_name')
        self.add_to_cart_button_name = 'Add to cart'
        self.cart_link = self.page.locator('.shopping_cart_link')

    def get_product_details(self, product_to_view):
        product = self.inventory_items.filter(has_text=product_to_view)

        return {
            "name": product.locator(self.inventory_item_name).inner_text(),
            "price": product.locator(".inventory_item_price").inner_text(),
            "description": product.locator(".inventory_item_desc").inner_text(),
        }

    def open_product(self, product_to_view):
        product = self.inventory_items.filter(has_text=product_to_view)
        product.locator('a').first.click()

    def add_product_to_cart(self, product_name):
        # locate the specific product from the inventory by the product parameter

        product_to_add = self.inventory_items.filter(
            has=self.inventory_item_name, has_text=product_name)


        # find the button for this product and click to add it to cart

        product_to_add.get_by_role("button", name=self.add_to_cart_button_name).click()

    def open_cart(self):
        self.cart_link.click()

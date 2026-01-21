from page_objects.cart import CartPage
from page_objects.product import ProductPage


class ShopPage:

    def __init__(self, page):
        self.page = page
        self.title = self.page.locator('.title')
        self.url = self.page.url
        self.inventory_items = self.page.locator('.inventory_item')

    def get_product_info(self, product_to_view, product_inventory):
        product = self.page.locator(product_inventory).filter(has_text=product_to_view)
        product.locator('a').first.click()

    def add_product_to_cart(self, product_name, product_inventory, inventory_item_name, button_name):
        # locate the specific product from the inventory by the product parameter

        product_to_add = self.page.locator(product_inventory).filter(
            has=self.page.locator(inventory_item_name, has_text=product_name)
        )

        # find the button for this product and click to add it to cart

        product_to_add.get_by_role("button", name=button_name).click()

    def open_cart(self, cart_link):
        self.page.locator(cart_link).click()

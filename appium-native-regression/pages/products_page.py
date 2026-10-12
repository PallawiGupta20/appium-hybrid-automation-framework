import time

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_btn = ("xpath", "//*[@content-desc='Add To Cart button'] | //*[@text='Add To Cart']")
        self.cart_icon = ("xpath", "//android.view.ViewGroup[@content-desc='cart badge'] | //android.widget.ImageView[contains(@content-desc, 'cart')]")

    def add_all_products_to_cart(self, products):
        for index, product in enumerate(products):
            print(f"Targeting product catalog item: {product}")
            time.sleep(1.5)

            if index >= 4:
                self.driver.swipe(start_x=500, start_y=1800, end_x=500, end_y=800, duration=800)
                time.sleep(1.5)

            self.driver.find_element("xpath", f"//*[@text='{product}']").click()
            time.sleep(1.5)

            self.driver.find_element(*self.add_to_cart_btn).click()
            time.sleep(1)

            self.driver.back()
            time.sleep(1.5)

    def navigate_to_shopping_cart(self):
        self.driver.find_element(*self.cart_icon).click()
        time.sleep(1.5)

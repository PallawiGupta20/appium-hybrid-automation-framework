import time
from appium.webdriver.common.appiumby import AppiumBy

class CatalogPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_buttons = (AppiumBy.XPATH, "//android.widget.TextView[@text='ADD TO CART']")
        self.cart_icon = (AppiumBy.ID, "com.androidsample.generalstore:id/appbar_btn_cart")

    def add_first_two_items_to_cart(self):
        product_elements = self.driver.find_elements(*self.add_to_cart_buttons)
        if len(product_elements) >= 1:
            product_elements[0].click()
            time.sleep(1)
        if len(product_elements) >= 2:
            product_elements[1].click()
            time.sleep(1)

    def navigate_to_cart(self):
        self.driver.find_element(*self.cart_icon).click()
        time.sleep(3)

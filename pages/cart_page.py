import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_prices = (AppiumBy.ID, "com.androidsample.generalstore:id/productPrice")
        self.total_amount_label = (AppiumBy.ID, "com.androidsample.generalstore:id/totalAmountLbl")
        self.checkbox = (AppiumBy.CLASS_NAME, "android.widget.CheckBox")
        self.terms_link = (AppiumBy.XPATH, "//*[@text='Please read our terms of conditions']")
        self.dialog_close_button = (AppiumBy.ID, "android:id/button1")
        self.proceed_button = (AppiumBy.ID, "com.androidsample.generalstore:id/btnProceed")

    def verify_cart_total_calculation(self):
        price_elements = self.driver.find_elements(*self.product_prices)
        calculated_sum = sum(float(item.text.replace("$", "").strip()) for item in price_elements)
        
        raw_total_text = self.driver.find_element(*self.total_amount_label).text
        displayed_total_float = float(raw_total_text.replace("$", "").strip())
        
        assert calculated_sum == displayed_total_float, f"Math mismatch! Calculated {calculated_sum} but app says {displayed_total_float}"

    def accept_terms_and_proceed(self):
        self.driver.find_element(*self.checkbox).click()
        terms_element = self.driver.find_element(*self.terms_link)
        
        actions = ActionChains(self.driver)
        pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions.w3c_actions = ActionBuilder(self.driver, mouse=pointer)
        actions.w3c_actions.pointer_action.move_to(terms_element)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(2.0)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()
        time.sleep(1.5)

        try:
            self.driver.find_element(*self.dialog_close_button).click()
            time.sleep(1)
        except Exception:
            pass

        self.driver.find_element(*self.proceed_button).click()

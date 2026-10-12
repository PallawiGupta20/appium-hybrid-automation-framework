import time
from appium.webdriver.common.appiumby import AppiumBy

class FormPage:
    def __init__(self, driver):
        self.driver = driver
        self.country_dropdown = (AppiumBy.ID, "com.androidsample.generalstore:id/spinnerCountry")
        self.first_country_option = (AppiumBy.XPATH, "//android.widget.ListView/android.widget.TextView")
        self.name_field = (AppiumBy.ID, "com.androidsample.generalstore:id/nameField")
        self.female_radio_button = (AppiumBy.XPATH, "//android.widget.RadioButton[@text='Female']")
        self.lets_shop_button = (AppiumBy.ID, "com.androidsample.generalstore:id/btnLetsShop")

    def fill_registration_form(self, name):
        time.sleep(3)
        self.driver.find_element(*self.country_dropdown).click()
        time.sleep(1)
        self.driver.find_element(*self.first_country_option).click()
        time.sleep(1)
        self.driver.find_element(*self.name_field).send_keys(name)
        self.driver.find_element(*self.female_radio_button).click()
        self.driver.find_element(*self.lets_shop_button).click()
        time.sleep(4)

import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium_native_regression.pages.products_page import ProductsPage
from appium_native_regression.pages.checkout_page import CheckoutPage

@pytest.fixture(scope="function")
def native_driver_setup():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = "com.saucelabs.mydemoapp.rn"
    options.app_activity = ".MainActivity"
    options.automation_name = "UiAutomator2"
    options.set_capability("appium:connectHardwareKeyboard", True)

    local_driver_path = os.path.abspath("chromedriver")
    if os.path.exists(local_driver_path):
        options.set_capability("appium:chromedriverExecutable", local_driver_path)

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_native_app_e2e_checkout(native_driver_setup):
    driver = native_driver_setup
    
    products_catalog = [
        "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt"
    ]

    products_page = ProductsPage(driver)
    checkout_page = CheckoutPage(driver)

    products_page.add_all_products_to_cart(products_catalog)
    products_page.navigate_to_shopping_cart()
    
    checkout_page.initiate_checkout_with_autofill()
    checkout_page.fill_shipping_address(
        name="Pallawi Gupta", addr1="Rajouri Garden", addr2="New Delhi",
        city="New Delhi", state="New Delhi", zip_code="110064", country="India"
    )
    checkout_page.fill_payment_details_safely(
        name="Rebecca Winter", card_num="3258 1265 7568 7891", expiry="03/25", cvv="123"
    )
    checkout_page.submit_and_validate_order_confirmation()
    
    print("\n🎉 SUCCESS: Isolated Native POM Regression Test Passed! 🎉")

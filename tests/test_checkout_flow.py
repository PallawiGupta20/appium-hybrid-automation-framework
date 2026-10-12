import os
import time
import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.form_page import FormPage
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from pages.webview_page import WebViewPage

@pytest.fixture(scope="function")
def driver_setup(request):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = "com.androidsample.generalstore"
    options.app_activity = "com.androidsample.generalstore.SplashActivity"
    options.automation_name = "UiAutomator2"
    options.set_capability("appium:connectHardwareKeyboard", True)

    local_driver_path = os.path.abspath("chromedriver")
    if os.path.exists(local_driver_path):
        options.set_capability("appium:chromedriverExecutable", local_driver_path)
    else:
        raise FileNotFoundError(f"Chromedriver missing at root: {local_driver_path}")

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.implicitly_wait(10)
    request.node.driver = driver

    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            try:
                current_context = driver.current_context
                if "WEBVIEW" in current_context: 
                    driver.switch_to.context("NATIVE_APP")
                allure.attach(driver.get_screenshot_as_png(), name="Crash_State", attachment_type=allure.attachment_type.PNG)
                if "WEBVIEW" in current_context: 
                    driver.switch_to.context(current_context)
            except Exception as e: 
                print(f"⚠️ Snapshot triage failed: {e}")

@allure.feature("Enterprise POM Flow")
@allure.story("E-Commerce Hybrid E2E Verification Suite")
def test_general_store_checkout_e2e(driver_setup):
    driver = driver_setup
    
    form_page = FormPage(driver)
    catalog_page = CatalogPage(driver)
    cart_page = CartPage(driver)
    webview_page = WebViewPage(driver)

    form_page.fill_registration_form(name="Pallawi Gupta")
    catalog_page.add_first_two_items_to_cart()
    catalog_page.navigate_to_cart()
    
    cart_page.verify_cart_total_calculation()
    cart_page.accept_terms_and_proceed()
    
    webview_page.switch_to_webview_context()
    webview_page.perform_search(search_query="Appium POM Architecture Complete!")
    webview_page.return_to_native_context()
    print("\n🎉 SUCCESS: POM Architecture Workflow Passed Flawlessly! 🎉")

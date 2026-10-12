import os
import time
import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.keys import Keys

# ==========================================
# FIXTURES & HOOKS (Teardown & Screenshots)
# ==========================================

@pytest.fixture(scope="function")
def driver_setup(request):
    """Sets up the Appium driver capabilities and handles session lifecycle."""
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
        raise FileNotFoundError(f"Chromedriver missing at project root: {local_driver_path}")

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.implicitly_wait(10)
    request.node.driver = driver

    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook that captures screenshots automatically upon test failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            try:
                current_context = driver.current_context
                if "WEBVIEW" in current_context:
                    driver.switch_to.context("NATIVE_APP")
                
                screenshot_bytes = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot_bytes,
                    name=f"Failure_Triage_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                if "WEBVIEW" in current_context:
                    driver.switch_to.context(current_context)
            except Exception as e:
                print(f"⚠️ Failed to capture context screenshot: {e}")

# ==========================================
# CORE HYBRID AUTOMATION TEST Flow
# ==========================================

@allure.feature("Hybrid E-Commerce Flow")
@allure.story("Registration, Cart Calculation, and WebView Search Verification")
def test_general_store_hybrid_flow(driver_setup):
    driver = driver_setup
    try:
        # Phase 1: Registration Form
        time.sleep(3)
        driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/spinnerCountry").click()
        time.sleep(1)
        driver.find_element(AppiumBy.XPATH, "//android.widget.ListView/android.widget.TextView").click()
        time.sleep(1)
        driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/nameField").send_keys("Pallawi Gupta")
        driver.find_element(AppiumBy.XPATH, "//android.widget.RadioButton[@text='Female']").click()
        driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/btnLetsShop").click()
        time.sleep(4) 

        # Phase 2: Catalog & Multiple Items Selection
        product_elements = driver.find_elements(AppiumBy.XPATH, "//android.widget.TextView[@text='ADD TO CART']")
        product_elements[0].click()
        time.sleep(1)
        product_elements[1].click()
        time.sleep(1)
        driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/appbar_btn_cart").click()
        time.sleep(3) 

        # Phase 3: Dynamic Price Calculation Math Assertion Check
        price_elements = driver.find_elements(AppiumBy.ID, "com.androidsample.generalstore:id/productPrice")
        calculated_sum = sum(float(item.text.replace("$", "").strip()) for item in price_elements)
        raw_total_text = driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/totalAmountLbl").text
        displayed_total_float = float(raw_total_text.replace("$", "").strip())
        assert calculated_sum == displayed_total_float, f"Math mismatch! Calculated {calculated_sum} but app says {displayed_total_float}"

        # Phase 4: Terms and Conditions Gestures
        driver.find_element(AppiumBy.CLASS_NAME, "android.widget.CheckBox").click()
        terms_link = driver.find_element(AppiumBy.XPATH, "//*[@text='Please read our terms of conditions']")
        
        actions = ActionChains(driver)
        pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions.w3c_actions = ActionBuilder(driver, mouse=pointer)
        actions.w3c_actions.pointer_action.move_to(terms_link)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(2.0)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()
        time.sleep(1.5)

        try:
            driver.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(1)
        except Exception:
            pass

        driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/btnProceed").click()

        # Phase 5 & 6: Web Context Handshake & Input
        webview_context = None
        for retry in range(10):
            time.sleep(1.5)
            contexts = driver.contexts
            for context in contexts:
                if "WEBVIEW" in context:
                    webview_context = context
                    break
            if webview_context:
                break

        if not webview_context:
            raise Exception("Failed to discover WEBVIEW context framework channel within timeout limit.")

        driver.switch_to.context(webview_context)
        time.sleep(3)

        search_input_box = driver.find_element(AppiumBy.XPATH, "//input[@name='q'] | //textarea[@name='q']")
        search_input_box.send_keys("Appium Hybrid Context Automation Complete!")
        search_input_box.send_keys(Keys.ENTER)
        time.sleep(4)

        # Phase 7: Realignment Context Teardown
        driver.switch_to.context("NATIVE_APP")

    except Exception as error:
        raise error

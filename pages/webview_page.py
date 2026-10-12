import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys

class WebViewPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (AppiumBy.XPATH, "//input[@name='q'] | //textarea[@name='q']")

    def switch_to_webview_context(self):
        print("\nRedirecting to WebView framework layout... entering polling loop...")
        webview_context = None
        for retry in range(10):
            time.sleep(1.5)
            for context in self.driver.contexts:
                if "WEBVIEW" in context:
                    webview_context = context
                    break
            if webview_context:
                break

        if not webview_context:
            raise Exception("Failed to discover WEBVIEW context channel within timeout limit.")
            
        print(f"Targeting web layer -> Switching context to: {webview_context}...")
        self.driver.switch_to.context(webview_context)
        time.sleep(3)

    def perform_search(self, search_query):
        input_element = self.driver.find_element(*self.search_box)
        input_element.send_keys(search_query)
        input_element.send_keys(Keys.ENTER)
        time.sleep(4)

    def return_to_native_context(self):
        print("Returning execution controls back to Native OS sandbox...")
        self.driver.switch_to.context("NATIVE_APP")

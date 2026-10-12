import time

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_btn = ("xpath", "//*[@text='Proceed To Checkout'] | //*[@content-desc='Proceed To Checkout button']")
        self.username_option = ("xpath", "//*[@text='bob@example.com']")
        self.login_btn = ("xpath", '//android.view.ViewGroup[@content-desc="Login button"]')
        self.to_payment_btn = ("xpath", "//*[@text='To Payment'] | //*[@content-desc='To Payment button']")
        self.review_order_btn = ("xpath", '//android.widget.TextView[@text="Review Order"]')
        self.place_order_btn = ("xpath", '//android.widget.TextView[@text="Place Order"]')
        self.success_title = ("xpath", '//*[@text="Checkout Complete"]')
        self.continue_shopping_btn = ("xpath", '//android.widget.TextView[@text="Continue Shopping"]')

    def initiate_checkout_with_autofill(self):
        self.driver.find_element(*self.checkout_btn).click()
        time.sleep(1.5)
        self.driver.find_element(*self.username_option).click()
        time.sleep(2)
        self.driver.find_element(*self.login_btn).click()
        time.sleep(4)

    def fill_shipping_address(self, name, addr1, addr2, city, state, zip_code, country):
        address_form_fields = {
            "Full Name": name,
            "Address Line 1": addr1,
            "Address Line 2": addr2,
            "City": city,
            "State": state,
            "Zip": zip_code,
            "Country": country
        }
        for field_label, input_text in address_form_fields.items():
            input_box = self.driver.find_element("xpath", f"//*[contains(@content-desc, '{field_label}')] | //android.widget.EditText[contains(@content-desc, '{field_label}')]")
            input_box.clear()
            input_box.send_keys(input_text)
        
        self.driver.find_element(*self.to_payment_btn).click()
        time.sleep(4)

    def fill_payment_details_safely(self, name, card_num, expiry, cvv):
        card_name_field = self.driver.find_element("xpath", "//*[contains(@content-desc, 'Full Name')] | //android.widget.EditText[contains(@content-desc, 'Full Name')]")
        card_name_field.clear()
        card_name_field.send_keys(name)

        card_num_field = self.driver.find_element("xpath", "//*[contains(@content-desc, 'Card Number')] | //android.widget.EditText[contains(@content-desc, 'Card Number')]")
        card_num_field.clear()
        for _ in range(25): self.driver.press_keycode(67)
        for char in card_num:
            card_num_field.send_keys(char)
            time.sleep(0.1)

        exp_date_field = self.driver.find_element("xpath", "//*[contains(@content-desc, 'Expiration Date')] | //android.widget.EditText[contains(@content-desc, 'Expiration Date')]")
        exp_date_field.clear()
        for _ in range(10): self.driver.press_keycode(67)
        for char in expiry:
            exp_date_field.send_keys(char)
            time.sleep(0.1)

        cvv_field = self.driver.find_element("xpath", "//*[contains(@content-desc, 'Security Code')] | //android.widget.EditText[contains(@content-desc, 'Security Code')]")
        cvv_field.clear()
        for _ in range(5): self.driver.press_keycode(67)
        cvv_field.send_keys(cvv)
        time.sleep(1.5)

        self.driver.find_element(*self.review_order_btn).click()
        time.sleep(4)

    def submit_and_validate_order_confirmation(self):
        self.driver.find_element(*self.place_order_btn).click()
        time.sleep(4)
        
        success_message = self.driver.find_element(*self.success_title)
        assert success_message.is_displayed(), "Verification Error: Checkout complete validation failed!"
        print(f"Verified Confirmation Screen State: {success_message.text}")
        
        self.driver.find_element(*self.continue_shopping_btn).click()
        time.sleep(2)

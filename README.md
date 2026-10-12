# 📱 Mobile Hybrid E-Commerce Test Automation Framework

A production-grade mobile automation framework engineered from scratch with **Python**, **Appium (UiAutomator2)**, and **Pytest** using the **Page Object Model (POM)** design pattern. This layout validates end-to-end user lifecycles within hybrid Android applications (`General Store`), handling complex cross-context boundaries, hardware inputs, and advanced touch gestures.

## 🛠️ Key Architectural Solutions Implemented
* **Asynchronous Context Switching:** Custom polling engines designed to smoothly handshake execution parameters between `NATIVE_APP` boundaries and embedded `WEBVIEW` contexts without test synchronization failure.
* **Dynamic Price Sum Assertions:** Runtime data processing structures that natively scrape string metadata, strip out currency artifacts, type-cast raw objects into `float` variables, and execute automated mathematical sum checks against the application total.
* **Context-Aware Exception Triaging:** Built-in hooks within the test engine that catch unexpected runtime crashes, safely switch the context frame back to native, and capture visual framebuffers as Allure report attachments.
* **W3C Actions & Mobile Gestures:** Implementation of standard `ActionChains`, `PointerInput`, and `ActionBuilder` to simulate real-world physical touch parameters (e.g., a 2.0-second long-press gesture on legal terms dialog blocks).
* **Allure Dashboard Analytics:** Full integration with Allure Reporting to compile execution data streams and render rich, interactive HTML dashboards for cross-functional stakeholders.

## 📁 Repository Architecture
* `pages/` - Contains the isolated Page Object classes (`form_page.py`, `catalog_page.py`, etc.) encapsulating UI elements and procedural actions.
* `tests/` - Holds the clean, declarative test suite runner file (`test_checkout_flow.py`).
* `.gitignore` - Production-grade blocklist ensuring environment caches, system logs, and large binaries stay excluded from the codebase history.

## 🚀 Quick Execution Guide

1. **Activate local workspace dependencies:**
   ```bash
   source venv/bin/activate
   ```
2. **Execute the automated testing loop & log telemetry:**
   ```bash
   pytest -s --alluredir=allure-results tests/test_checkout_flow.py
   ```
3. **Spin up the interactive visual dashboard server:**
   ```bash
   allure serve allure-results
   ```

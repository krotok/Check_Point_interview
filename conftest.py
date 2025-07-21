import pytest
import logging
import os
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chromium", help="Browser to use: chromium, firefox, webkit")

@pytest.fixture(scope="session")
def browser_type(pytestconfig):
    return pytestconfig.getoption("browser")

@pytest.fixture(scope="function")
def page(request, browser_type):
    with sync_playwright() as p:
        browser_launcher = getattr(p, browser_type)
        browser = browser_launcher.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        # Check if the test failed
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{request.node.name}_{browser_type}.png"
            page.screenshot(path=screenshot_path)
            logger.error(f"Test failed. Screenshot saved to {screenshot_path}")
        context.close()
        browser.close()

@pytest.fixture(scope="function")
def base_url():
    import pathlib
    # Get the absolute path to your test file
    current_dir = pathlib.Path(__file__).parent.resolve()
    # Construct path to your HTML file relative to the test file
    html_path = current_dir / "static" / "fake_gmail_login.html"
    # Verify the file exists
    if not html_path.exists():
        raise FileNotFoundError(f"Could not find HTML file at {html_path}")
    return f"file://{html_path}"

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
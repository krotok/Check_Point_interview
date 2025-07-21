import pytest
from pages.login_page import LoginPage
import logging

logger = logging.getLogger(__name__)

@pytest.mark.parametrize("email,password,expected", [
    ("test@gmail.com", "password123", "Login successful"),
    ("test@gmail.com", "wrongpass", "Invalid credentials"),
    ("wrong@gmail.com", "password123", "Invalid credentials"),
    ("", "", "Fields cannot be empty"),
    ("noatsymbol.com", "password123", "Invalid email format"),
    ("test@gmail.com", "", "Fields cannot be empty"),
    ("", "password123", "Fields cannot be empty"),
])
def test_login_combinations(page, base_url, email, password, expected):
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.login(email, password)
    message = login_page.get_message()
    logger.info(f"Tested: ({email}, {password}) -> '{message}'")
    assert message == expected
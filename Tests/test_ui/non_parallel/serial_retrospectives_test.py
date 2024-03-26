import unittest
from Utils import users
from infra.infra_ui.browser_wrapper import WebDriverManager
from logic.logic_ui.login_page import LoginPage
from logic.logic_ui.Retrospectives_page import RetrospectivesPage
from logic.logic_ui.Home_page import HomePage
import pytest
from parameterized import parameterized_class
from Utils.configurations import ConfigurationManager

config_manager = ConfigurationManager()
settings = config_manager.load_settings()
browser_types = [(browser,) for browser in settings["browser_types"]]


@pytest.mark.serial
@parameterized_class(('browser',), [
    ('chrome',),
])
class SerialRetrospectivesTests(unittest.TestCase):
    VALID_USERS = users.authentic_users

    def setUp(self):
        self.browser_wrapper = WebDriverManager()
        default_browser = 'chrome'
        self.browser = getattr(self.__class__, 'browser', default_browser)
        self.driver = self.browser_wrapper.initialize_web_driver(browser_name=self.browser)
        self.login_page = LoginPage(self.driver)
        user = self.VALID_USERS[0]
        self.login_page.login(user['email'], user['password'])
        self.retrospective_Interface = RetrospectivesPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.home_page.changeEnvironment(environment_name="dev")

    def test_revert_bulk_deletion_of_retrospectives(self):
        outcome = self.retrospective_Interface.revertBulkDeletion()
        self.assertTrue(outcome, "Failed to undo the bulk deletion of retrospectives.")

    def tearDown(self):
        self.home_page.sign_out()
        if self.driver:
            self.driver.quit()
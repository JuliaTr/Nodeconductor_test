"""
1. Login NC
2. Add organization
3. Top-up balance
4. Remove organization
"""

import time
import unittest
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import (login_nodeconductor, get_driver, add_organization, top_up_organization_balance,
                     remove_organization, element_exists, make_screenshot, _back_to_list, _search,
                     get_private_parent, choose_organization, go_to_main_page)
from base import BaseSettings

private_parent = get_private_parent('OrganizationBalancePrivateSettings')


class Settings(BaseSettings, private_parent):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test org balance'
    balance = '$0.00'
    top_up_balance = '1'
    check_balance = '$1.00'
    time_wait_to_topup_balance = 10
    time_wait_to_go_back_to_list_of_organizations = 20
    time_wait_alert_is_present = 10
    time_wait_alert_invisibility = 10
    time_wait_to_swich_to_paypal = 20


class OrganizationBalanceTest(unittest.TestCase):

    def setUp(self):
        sys.exc_clear()
        self.driver = get_driver(Settings.site_url)
        self.organization_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)
        self.organization = Settings.get_unique_attribute('organization')

    def test_organization_balance(self):
        # Login NC
        print '%s is going to be logged in.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        print '%s was logged in successfully.' % Settings.username

        # Add organization
        print 'Organization is going to be added.'
        time.sleep(BaseSettings.click_time_wait)
        add_organization(self.driver, self.organization)
        print 'Existence check of added organization'
        xpath = '//span[@class="name" and contains(text(), "%s")]' % self.organization
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot add organization "%s"' % self.organization
        self.organization_exists = True
        print 'Organization exists: ', self.organization_exists
        print 'Organization was added successfully.'

        # Choose organization
        print 'Organization is going to be chosen.'
        go_to_main_page(self.driver)
        choose_organization(self.driver, self.organization)
        print 'Organization was chosen successfully.'

        # Top-up balance
        print 'Balance is going to be topped-up.'
        print 'Check "$0.00" balance'
        xpath = '//div[contains(text(), "%s")]' % Settings.balance
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot find balance "%s"' % Settings.balance
        print 'Top-up balance'
        top_up_organization_balance(self.driver, Settings.top_up_balance, Settings.payment_account_email,
                                    Settings.payment_account_password, Settings.time_wait_alert_is_present,
                                    Settings.time_wait_alert_invisibility, Settings.time_wait_to_swich_to_paypal)
        print 'Wait till balance will be topped-up'
        WebDriverWait(self.driver, Settings.time_wait_to_topup_balance).until(
            EC.invisibility_of_element_located((By.XPATH, '//div[contains(text(), "Payment is being proceeded, please wait")]')))
        print 'Check topped-up balance'
        xpath = '//div[contains(text(), "%s")]' % Settings.check_balance
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot find balance "%s"' % Settings.check_balance
        print 'Balance was topped-up successfully.'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver, name=self.__class__.__name__)
            print 'Organization exists: ', self.organization_exists
        if self.organization_exists:
            try:
                # Remove organization
                print 'Organization is going to be removed.'
                remove_organization(self.driver, self.organization)
                self.organization_exists = False
                print 'Organization exists: ', self.organization_exists
                print 'Wait till go back to list option will be possible'
                WebDriverWait(self.driver, Settings.time_wait_to_go_back_to_list_of_organizations).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'back-to-list')))
                _back_to_list(self.driver)
                print 'Existence check of removed organization'
                _search(self.driver, self.organization, css_selector='[ng-model="entityList.searchInput"]')
                assert not element_exists(self.driver, link_text=self.organization), (
                    'Error: Organization with name "%s" was not removed, it still exists' % self.organization)
                print 'Organization was removed successfully.'
            except Exception as e:
                print 'Organization cannot be removed. Error: "%s"' % e

        if self.organization_exists:
            print 'Warning! Test cannot remove organization "%s". It has to be removed manually.' % self.organization

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

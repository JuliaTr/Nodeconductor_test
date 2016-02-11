"""
1. Login NC
2. Create organization
3. Top-up balance
4. Delete organization
"""

import time
import unittest
import sys

from helpers import (login_nodeconductor, get_driver, create_organization, top_up_organization_balance,
                     delete_organization, element_exists, make_screenshot, _back_to_list, _search,
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


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        sys.exc_clear()
        self.driver = get_driver(Settings.site_url)
        self.organization_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)

    def test_organization_balance(self):
        # Login NC
        print '%s is going to be logged in.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        print '%s was logged in successfully.' % Settings.username

        # Create organization
        print 'Organization is going to be created.'
        time.sleep(BaseSettings.click_time_wait)
        create_organization(self.driver, Settings.organization)
        print 'Existence check of created organization'
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.organization
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create organization "%s"' % Settings.organization
        self.organization_exists = True
        print 'Organization exists: ', self.organization_exists
        print 'Organization was created successfully.'

        # Choose organization
        print 'Organization is going to be chosen.'
        go_to_main_page(self.driver)
        choose_organization(self.driver, Settings.organization)
        print 'Organization was chosen successfully.'

        # Top-up balance
        print 'Balance is going to be topped-up.'
        print 'Check "$0.00" balance'
        xpath = '//div[contains(text(), "%s")]' % Settings.balance
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot find balance "%s"' % Settings.balance
        print 'Top-up balance'
        top_up_organization_balance(self.driver, Settings.top_up_balance, Settings.payment_account_email, Settings.payment_account_password)
        time.sleep(BaseSettings.click_time_wait)
        print 'Check topped-up balance'
        xpath = '//div[contains(text(), "%s")]' % Settings.check_balance
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot find balance "%s"' % Settings.check_balance
        print 'Balance was topped-up successfully.'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver)
            print 'Organization exists: ', self.organization_exists
        if self.organization_exists:
            try:
                # Delete organization
                print 'Organization is going to be deleted.'
                delete_organization(self.driver, Settings.organization)
                self.organization_exists = False
                print 'Organization exists: ', self.organization_exists
                time.sleep(BaseSettings.click_time_wait)
                time.sleep(3)  # sometimes doen't want to work without additional time wait
                _back_to_list(self.driver)
                print 'Existence check of deleted organization'
                _search(self.driver, Settings.organization, css_selector='[ng-model="entityList.searchInput"]')
                assert not element_exists(self.driver, link_text=Settings.organization), (
                    'Error: Organization with name "%s" was not deleted, it still exists' % Settings.organization)
                print 'Organization was deleted successfully.'
            except Exception as e:
                print 'Organization cannot be deleted. Error: "%s"' % e

        if self.organization_exists:
            print 'Warning! Test cannot delete organization "%s". It has to be deleted manually.' % Settings.organization

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

"""
1. Login NC
2. Create organization
3. Top-up balance
4. Delete organization
"""


import sys
import time
import unittest

from helpers import (login_nodeconductor, get_driver, create_organization, top_up_organization_balance,
                     delete_organization, element_exists, make_screenshot, _back_to_list, choose_organization,
                     get_private_parent)
from base import BaseSettings

private_parent = get_private_parent('OrganizationBalancePrivateSettings')


class Settings(BaseSettings, private_parent):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test org balance1'
    new_organization = 'Test org balance2'  # should be only one organization. Blocker NC-1112
    balance = '$0.00'
    top_up_balance = '100'
    check_balance = '$100.00'


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.organization_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)

    def test_create_delete_project_provider_resource(self):
        # Login NC
        print '%s is going to be loggedin.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        print '%s was loggedin successfully.' % Settings.username

        # Test should work without this method. Blocker NC-1112
        # Choose organization
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, Settings.organization)
        print 'Organization was chosen successfully.'

        # Create organization
        print 'Organization is going to be created.'
        create_organization(self.driver, Settings.new_organization)
        print 'Existence check of created organization'
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.new_organization
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create organization "%s"' % Settings.new_organization
        self.organization_exists = True
        print 'Organization was created successfully.'

        # Top-up balance
        print 'Balance is going to be topped-up.'
        # Blocker NC-1112
        print 'Check "$0" balance'
        xpath = '//span[@visible="balance" and contains(text(), "%s")]' % Settings.balance
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot find balance "%s"' % Settings.balance
        print 'Top-up balance'
        top_up_organization_balance(self.driver, Settings.top_up_balance, Settings.email, Settings.password_account)
        print 'Check topped-up balance'
        xpath = '//span[@visible="balance" and contains(text(), "%s")]' % Settings.check_balance
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
                delete_organization(self.driver, Settings.new_organization)
                self.organization_exists = False
                _back_to_list(self.driver)
                print 'Existence check of deleted organization'
                search_field = self.driver.find_element_by_css_selector('[ng-change="entityList.search()"]')
                search_field.clear()
                search_field.send_keys(Settings.new_organization)
                time.sleep(BaseSettings.search_time_wait)
                assert not element_exists(self.driver, xpath='//span[contains(text(), "%s")]' % Settings.new_organization), (
                    'Error: Organization with name "%s" was not deleted, it still exists' % Settings.new_organization)
                print 'Organization was deleted successfully.'
            except Exception as e:
                print 'Organization cannot be deleted. Error: "%s"' % e

        if self.organization_exists:
            print 'Warning! Test cannot delete organization "%s". It has to be delete manually.' % Settings.new_organization

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

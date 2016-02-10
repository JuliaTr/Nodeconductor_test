"""
1. Login NC
2. Choose organization
3. Create project
4. Create provider
5. Import resource
6. Unlink resource
7. Delete provider
8. Delete project
"""


import time
import unittest
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_provider_digitalocean, import_resource, unlink_resource, delete_provider,
                     element_exists, go_to_main_page, make_screenshot, get_private_parent, _search)
from base import BaseSettings

private_parent = get_private_parent('DigitalOceanPrivateSettings')


class Settings(BaseSettings, private_parent):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'DO test project'
    provider_type_name = 'DigitalOcean'
    provider_name = 'DigitalOceanTest provider'
    category_name = 'VMs'
    resource_name = 'SIB-test'
    resource_cost = '$5.00'
    time_wait_for_provider_state = 30


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        sys.exc_clear()
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.provider_exists = False
        self.resource_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)

    def test_create_delete_project_provider_import_unlink_resource(self):
        # Login NC
        print '%s is going to be logged in.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        print '%s was logged in successfully.' % Settings.username

        # Choose organization
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, Settings.organization)
        print 'Organization was chosen successfully.'

        # Create project
        print 'Project is going to be created.'
        create_project(self.driver, Settings.project_name)
        time.sleep(BaseSettings.click_time_wait)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.project_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create project "%s"' % Settings.project_name
        self.project_exists = True
        print 'Project exists: ', self.project_exists
        print 'Project was created successfully.'

        # Create provider
        print 'Provider is going to be created.'
        time.sleep(BaseSettings.click_time_wait)
        create_provider_digitalocean(self.driver, Settings.provider_name, Settings.provider_type_name,
                                     Settings.digitalocean_access_token)
        _search(self.driver, Settings.provider_name)
        print 'Find provider in list'
        xpath = '//span[contains(text(), "%s")]' % Settings.provider_name
        assert element_exists(self.driver, xpath=xpath), 'Error: Provider with name "%s" is not found' % Settings.provider_name
        self.provider_exists = True
        print 'Provider exists: ', self.provider_exists
        print 'Find In Sync state of created provider'
        try:
            WebDriverWait(self.driver, Settings.time_wait_for_provider_state).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".status-circle.online")))
        except TimeoutException as e:
            print 'Error: Provider is not In Sync'
            raise e
        else:
            print 'Provider is in In Sync state'
        print 'Provider was created successfully.'

        # Import resource
        print 'Resource is going to be imported.'
        import_resource(self.driver, Settings.project_name, Settings.provider_name, Settings.category_name,
                        Settings.resource_name)
        _search(self.driver, Settings.resource_name)
        print 'Go to resource page'
        resource = self.driver.find_element_by_link_text(Settings.resource_name)
        resource.click()
        time.sleep(BaseSettings.click_time_wait)
        print 'Check imported resource existence'
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.resource_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot import resource "%s"' % Settings.resource_name
        self.resource_exists = True
        print 'Resource exists: ', self.resource_exists
        print 'Check imported resource state'
        xpath = '//div[contains(text(), "Online")]'
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Error: Imported resource "%s" is not online.' % Settings.resource_name
        print 'Imported resource is in online state'
        print 'Resource was imported successfully.'

        print '----- Cost is going to be checked----- '
        go_to_main_page(self.driver)
        costs = self.driver.find_element_by_link_text('Costs')
        costs.click()
        time.sleep(BaseSettings.click_time_wait)
        print 'Select resources tab'
        resources_list = self.driver.find_element_by_css_selector('[ng-class="{\'active\': row.selected && row.activeTab==\'resources\'}"]')
        resources_list.click()
        time.sleep(BaseSettings.click_time_wait)
        print 'Find row with the resource in a resource list'
        rows_list = self.driver.find_elements_by_css_selector('[ng-repeat="resource in row.resources"]')
        resource_cost_exists = False
        for row in rows_list:
            if Settings.resource_name in row.text:
                assert Settings.resource_cost in row.text, 'Error: Cannot find resource cost "%s" to check cost' % Settings.resource_cost
                resource_cost_exists = True
                print 'Resource cost "%s" was found on page' % Settings.resource_cost
        assert resource_cost_exists, 'Error: Cannot find resource with name "%s" ' % Settings.resource_name
        time.sleep(BaseSettings.click_time_wait)
        print '----- Cost was checked successfully----- '

        # Unlink resource
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, Settings.project_name, Settings.resource_name)
        _search(self.driver, Settings.resource_name)
        print 'Check unlinked resource existence'
        assert not element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % Settings.resource_name), (
            'Error: Resource with name "%s" was not unlinked, it still exists' % Settings.resource_name)
        self.resource_exists = False
        print 'Resource exists: ', self.resource_exists
        print 'Resource was unlinked successfully.'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver)
        print 'Provider exists: ', self.provider_exists
        # Blocker SAAS-1152
        if self.provider_exists:
            try:
                # Delete provider
                print 'Provider is going to be deleted.'
                delete_provider(self.driver, Settings.provider_name)
                self.provider_exists = False
                print 'Provider exists: ', self.provider_exists
                time.sleep(BaseSettings.click_time_wait)
                _search(self.driver, Settings.provider_name)
                assert not element_exists(self.driver, xpath='//span[contains(text(), "%s")]' % Settings.provider_name), (
                    'Error: Provider with name "%s" was not deleted, it still exists' % Settings.provider_name)
                print 'Provider was deleted successfully.'
            except Exception as e:
                print 'Provider cannot be deleted. Error: "%s"' % e

        if self.project_exists:
            try:
                # Delete project
                print 'Project is going to be deleted.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                time.sleep(BaseSettings.click_time_wait)
                _search(self.driver, Settings.project_name)
                if element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % Settings.project_name):
                    self.project_exists = True
                    print 'Project exists: ', self.project_exists
                print 'Project was deleted successfully.'
            except Exception as e:
                print 'Project cannot be deleted. Error: "%s"' % e

        if self.resource_exists:
            print 'Warning! Test cannot unlink resource "%s". It has to be unlinked manually.' % Settings.resource_name
        if self.provider_exists:
            print 'Warning! Test cannot delete provider "%s". It has to be deleted manually.' % Settings.provider_name
        if self.project_exists:
            print 'Warning! Test cannot delete project "%s". It has to be deleted manually.' % Settings.project_name

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

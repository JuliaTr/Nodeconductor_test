"""
1. Login NC
2. Choose organization
3. Create project
4. Create provider
5. Create resource
6. Delete resource
7. Delete provider
8. Delete project
"""

# Test is not ready yet. It was postponed.

import time
import unittest
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_resource_azure, element_exists, delete_resource, make_screenshot, get_private_parent,
                     _search)
from base import BaseSettings

private_parent = get_private_parent('AzurePrivateSettings')


class Settings(BaseSettings, private_parent):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'Azure test project'
    provider_name = 'Shared Azure'
    category_name = 'VMs'
    resource_name = 'AzureTestResource'
    image_name = 'Visual Studio Community 2013 Update 4 with Tools for Node.js on Windows Server 2012 R2'
    size_name = 'A2: Medium Instance'
    time_after_resource_creation = 180
    time_wait_after_resource_stopping = 60
    time_wait_after_resource_removal = 30


# TODO: Add method of provider creation and deletion.
class AzureResourceCreationTest(unittest.TestCase):

    def setUp(self):
        sys.exc_clear()
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.resource_exists = False
        self.driver.implicitly_wait(20)

    def test_create_delete_resource(self):
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

        # Create resource
        print 'Resource is going to be created.'
        create_resource_azure(self.driver, Settings.project_name, Settings.resource_name, Settings.category_name,
                              Settings.provider_name, Settings.image_name, Settings.username, Settings.azure_os_password,
                              Settings.size_name)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.resource_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create resource "%s"' % Settings.resource_name
        self.resource_exists = True
        print 'Resource exists: ', self.resource_exists
        print 'Find online state of created resource'
        try:
            WebDriverWait(self.driver, Settings.time_after_resource_creation).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Online")]')))
        except TimeoutException as e:
            print 'Error: Resource is not online'
            raise e
        else:
            print 'Resource is in online state'
        print 'Resource was created successfully.'

        # Method is not ready. Cannot check as resource cannot be purchased now
        # Delete resource
        print 'Resource is going to be deleted.'
        delete_resource(self.driver, Settings.resource_name, Settings.project_name,
                        Settings.time_wait_after_resource_stopping, Settings.time_wait_after_resource_removal)
        self.resource_exists = False
        print 'Resource was deleted successfully'
        time.sleep(10)

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver, name=self.__class__.__name__)
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
            print 'Warning! Test cannot delete resource %s. It has to be deleted manually.' % Settings.resource_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be deleted manually.' % Settings.project_name

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

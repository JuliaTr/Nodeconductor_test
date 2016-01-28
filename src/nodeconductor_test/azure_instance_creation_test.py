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


import time
import unittest

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_resource_azure, element_exists, delete_resource, is_in_list)

from base import BaseSettings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Settings(BaseSettings):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'Azure test project'
    provider_name = 'Shared Azure'
    category_name = 'VMs'
    os_password = 'Zi_lT6V0C9-~'
    resource_name = 'AzureTest'
    image_name = 'Visual Studio Community 2013 Update 4 with Tools for Node.js on Windows Server 2012 R2'
    size_name = 'Medium Instance'
    time_after_resource_creation = 180
    time_wait_after_resource_stopping = 60
    time_wait_after_resource_removal = 30


# Test is not ready because it's impossible to test resource deletion.
# Share Azure has disappeared.
# TODO: Add method of provider creation and deletion.
class AzureResourceCreationTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.resource_exists = False
        self.driver.implicitly_wait(20)

    def test(self):
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
        # goto main page:
        self.driver.get(Settings.site_url)
        create_project(self.driver, Settings.project_name)
        time.sleep(BaseSettings.click_time_wait)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.project_name
        self.project_exists = bool(self.driver.find_elements_by_xpath(xpath))
        assert self.project_exists, 'Cannot create project "%s"' % Settings.project_name
        print 'Prject was created successfully'

        # Create resource
        print 'Resource is going to be created.'
        # goto main page:
        self.driver.get(Settings.site_url)
        create_resource_azure(self.driver, Settings.project_name, Settings.resource_name, Settings.category_name,
                              Settings.provider_name, Settings.image_name, Settings.username, Settings.os_password,
                              Settings.size_name)
        element = WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.CLASS_NAME, "status-circle")))
        # time.sleep(Settings.time_after_resource_creation)
        # self.driver.refresh()
        # time.sleep(10)
        # back_to_list_field = self.driver.find_element_by_class_name('back-to-list')
        # back_to_list_field.click()
        # time.sleep(5)
        # vms = self.driver.find_element_by_css_selector('[visible="vms"]')
        # vms.click()
        # time.sleep(5)
        # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        # search_field.clear()
        # time.sleep(5)
        # search_field.send_keys(Settings.resource_name)
        # time.sleep(5)
        # assert element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
        #     'Error: Cannot find resource with name  %s ' % Settings.resource_name)
        self.resource_exists = True
        print 'Resource was created successfully.'

        # # Delete resource
        # print 'Resource is going to be deleted.'
        # delete_resource(self.driver, Settings.resource_name, Settings.project_name,
        #                 Settings.time_wait_after_resource_stopping, Settings.time_wait_after_resource_removal)
        # self.resource_exists = False
        # print 'Resource was deleted successfully'
        # time.sleep(10)

    # def tearDown(self):
    #     if self.project_exists:
    #         try:
    #             # Delete project
    #             print 'Project is going to be deleted.'
    #             delete_project(self.driver, Settings.project_name)
    #             self.project_exists = False
    #             time.sleep(10)
    #             if not element_exists(self.driver, xpath="//*[contains(text(), 'You have no projects yet.')]"):
    #                 search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    #                 search_field.clear()
    #                 time.sleep(5)
    #                 search_field.send_keys(Settings.project_name)
    #                 time.sleep(10)
    #                 if element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'):
    #                     self.project_exists = True
    #         except Exception as e:
    #             print 'Project cannot be deleted. Error: %s' % e

    #     if self.resource_exists:
    #         print 'Warning! Test cannot delete resource %s. It has to be deleted manually.' % Settings.resource_name
    #     if self.project_exists:
    #         print 'Warning! Test cannot delete project %s. It has to be deleted manually.' % Settings.project_name

    #     self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

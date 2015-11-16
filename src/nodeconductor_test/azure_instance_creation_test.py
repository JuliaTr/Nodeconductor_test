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

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, create_provider_azure,
                    choose_organization, create_resource_azure, element_exists, delete_resource, is_in_list,
                    delete_provider)


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    nec_organization = 'Ministry of Bells'
    project_name = 'xcghh'
    provider_name = 'AzureTest provider'
    provider_type_name = 'azure'
    subscription_id_name = '39e917e7-d6d4-4a01-ac7c-1ce78a63013f'
    category_name = 'VMs'
    os_password = 'Zi_lT6V0C9-~'
    resource_name = 'AzureTest'
    image_name = 'Visual Studio Community 2013 Update 4 with Tools for Node.js on Windows Server 2012 R2'
    size_name = 'Medium Instance'
    time_after_resource_creation = 180
    time_wait_after_resource_stopping = 60
    time_wait_after_resource_removal = 30


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.provider_exists = False
        self.resource_exists = False

    def test_create_delete_project_key_resource(self):
        # Login NC
        print '%s is going to be loggedin.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        time.sleep(5)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        print '%s was loggedin successfully.' % Settings.username
        time.sleep(10)

        # Choose organization
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, Settings.nec_organization)
        print 'Organization was chosen successfully.'
        time.sleep(10)

        # # Create project
        # print 'Project is going to be created.'
        # create_project(self.driver, Settings.project_name)
        # time.sleep(5)
        # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        # search_field.clear()
        # time.sleep(5)
        # search_field.send_keys(Settings.project_name)
        # time.sleep(5)
        # projects_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        # time.sleep(5)
        # assert is_in_list(projects_list, Settings.project_name), (
        #     'Error: Cannot find project with name  %s ' % Settings.project_name)
        self.project_exists = True
        # print 'Prject was created successfully'
        # time.sleep(10)

        # # Create provider
        # print 'Provider is going to be created.'
        # create_provider_azure(self.driver, Settings.provider_name, Settings.provider_type_name, Settings.subscription_id_name)
        # time.sleep(5)
        # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        # search_field.clear()
        # time.sleep(5)
        # search_field.send_keys(Settings.provider_name)
        # time.sleep(5)
        # provider_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        # assert is_in_list(provider_list, Settings.provider_name), (
        #     'Error: Cannot find provider with name  %s ' % Settings.provider_name)
        self.provider_exists = True
        # print 'Provider was created successfully.'
        # time.sleep(10)

        # Create resource
        print 'Resource is going to be created.'
        create_resource_azure(self.driver, Settings.project_name, Settings.resource_name, Settings.category_name,
                              Settings.provider_name, Settings.image_name, Settings.username, Settings.os_password,
                              Settings.size_name)
        time.sleep(Settings.time_after_resource_creation)
        self.driver.refresh()
        time.sleep(10)
        back_to_list_field = self.driver.find_element_by_class_name('back-to-list')
        back_to_list_field.click()
        time.sleep(5)
        vms = self.driver.find_element_by_css_selector('[visible="vms"]')
        vms.click()
        time.sleep(5)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.resource_name)
        time.sleep(5)
        assert element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
            'Error: Cannot find resource with name  %s ' % Settings.resource_name)
        self.resource_exists = True
        time.sleep(10)

    #     # Delete resource
    #     print 'Resource is going to be deleted.'
    #     delete_resource(self.driver, Settings.resource_name, Settings.project_name,
    #                     Settings.time_wait_after_resource_stopping, Settings.time_wait_after_resource_removal)
    #     self.resource_exists = False
    #     print 'Resource was deleted successfully'
    #     time.sleep(10)

    # def tearDown(self):
    #     print 'Provider exists: ', self.provider_exists
    #     if self.provider_exists:
    #         try:
    #             # Delete provider
    #             print 'Provider is going to be deleted.'
    #             time.sleep(10)
    #             delete_provider(self.driver, Settings.provider_name)
    #             self.provider_exists = False
    #             time.sleep(10)
    #             search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    #             search_field.clear()
    #             time.sleep(5)
    #             search_field.send_keys(Settings.provider_name)
    #             time.sleep(5)
    #             assert not element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
    #                 'Error: Provider with name %s is found' % Settings.provider_name)
    #         except Exception as e:
    #             print 'Provider cannot be deleted. Error: %s' % e
    #     time.sleep(10)

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
    #     if self.provider_exists:
    #         print 'Warning! Test cannot delete provider %s. It has to be deleted manually.' % Settings.provider_name
    #     if self.project_exists:
    #         print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name

    #     self.driver.quit()


if __name__ == "__main__":
    unittest.main()

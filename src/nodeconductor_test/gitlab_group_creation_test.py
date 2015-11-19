"""
1. Login NC
2. Choose organization
3. Create project
4. Create application
5. Delete application
6. Delete project
"""


import time
import unittest

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_application, element_exists, is_in_list, delete_application)


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'GitLab test project'
    category_name = 'APPLICATIONS'
    resource_type_name = 'Group'
    path_name = 'test-group-1'
    application_name = 'Test group 1'
    time_after_resource_creation = 60
    time_wait_after_resource_removal = 60


class ApplicationCreationTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.application_exists = False

    def test_create_delete_application(self):
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
        choose_organization(self.driver, Settings.organization)
        print 'Organization was chosen successfully.'
        time.sleep(10)

        # Create project
        print 'Project is going to be created.'
        create_project(self.driver, Settings.project_name)
        time.sleep(5)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.project_name)
        time.sleep(5)
        projects_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        time.sleep(5)
        assert is_in_list(projects_list, Settings.project_name), (
            'Error: Cannot find project with name  %s ' % Settings.project_name)
        self.project_exists = True
        print 'Prject was created successfully'
        time.sleep(10)

        # Create application
        print 'Application is going to be created.'
        create_application(self.driver, Settings.project_name, Settings.category_name, Settings.resource_type_name,
                           Settings.path_name, Settings.application_name)
        time.sleep(Settings.time_after_resource_creation)
        back_to_list_field = self.driver.find_element_by_class_name('back-to-list')
        back_to_list_field.click()
        time.sleep(5)
        vms = self.driver.find_element_by_css_selector('[visible="applications"]')
        vms.click()
        time.sleep(5)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.application_name)
        time.sleep(5)
        assert element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
            'Error: Cannot find application with name  %s ' % Settings.application_name)
        self.application_exists = True
        print 'Application was created successfully'
        time.sleep(10)

        # Delete application
        print 'Application is going to be deleted.'
        delete_application(self.driver, Settings.project_name, Settings.time_wait_after_resource_removal, Settings.application_name)
        self.application_exists = False
        print 'Application was deleted successfully'
        time.sleep(10)

    def tearDown(self):
        if self.project_exists:
            try:
                # Delete project
                print 'Project is going to be deleted.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                time.sleep(10)
                if not element_exists(self.driver, xpath="//*[contains(text(), 'You have no projects yet.')]"):
                    search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                    search_field.clear()
                    time.sleep(5)
                    search_field.send_keys(Settings.project_name)
                    time.sleep(10)
                    if element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'):
                        self.project_exists = True
            except Exception as e:
                print 'Project cannot be deleted. Error: %s' % e

        if self.resource_exists:
            print 'Warning! Test cannot delete application %s. It has to be deleted manually.' % Settings.application_nameapplication_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

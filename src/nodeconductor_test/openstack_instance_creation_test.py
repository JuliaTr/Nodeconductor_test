"""
1. Login NC
2. Choose organization
3. Create project
4. Create ssh key
5. Create resource
6. Delete resource
7. Delete project
8. Delete ssh key
"""


import time
import unittest

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, create_ssh_key,
                     delete_ssh_key, choose_organization, create_resource_openstack, delete_resource, is_in_list,
                     element_exists)


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'OpenStack test project'
    key_name = 'Openstack test key'
    category_name = 'VMs'
    provider_name_in_resource = 'Parnu LAB'
    image_name = 'Ubuntu 14.04 x86_64'
    flavor_name = 'm1.small'
    resource_name = 'OpenStack test instance'
    public_key_name = 'Openstack test key'
    time_after_resource_creation = 180
    time_wait_after_resource_stopping = 60
    time_wait_after_resource_removal = 30


# IMPORTANT: It's impossible to test resource deletion.
class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.ssh_key_exists = False
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

        # Create ssh key
        print 'Ssh key is going to be created.'
        create_ssh_key(self.driver, Settings.user_full_name, Settings.key_name)
        time.sleep(10)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.key_name)
        time.sleep(5)
        key_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        assert is_in_list(key_list, Settings.key_name), (
            'Error: Cannot find ssh key with name  %s ' % Settings.key_name)
        self.ssh_key_exists = True
        print 'Ssh key was created successfully'
        time.sleep(10)

        # Create resource
        print 'Resource is going to be created.'
        create_resource_openstack(self.driver, Settings.project_name, Settings.resource_name, Settings.category_name,
                                  Settings.provider_name_in_resource, Settings.image_name, Settings.flavor_name,
                                  Settings.public_key_name)
        time.sleep(Settings.time_after_resource_creation)
        self.driver.refresh()
        time.sleep(10)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.resource_name)
        time.sleep(5)
        assert element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
            'Error: Cannot find resource with name  %s ' % Settings.resource_name)
        self.resource_exists = True
        time.sleep(10)

        # Delete resource
        print 'Resource is going to be deleted.'
        delete_resource(self.driver, Settings.resource_name, Settings.project_name,
                        Settings.time_wait_after_resource_stopping, Settings.time_wait_after_resource_removal)
        self.resource_exists = False
        print 'Resource was deleted successfully'
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
        time.sleep(10)

        if self.ssh_key_exists:
            try:
                # Delete ssh key
                print 'Ssh key is going to be deleted.'
                delete_ssh_key(self.driver, Settings.key_name, Settings.user_full_name)
                self.ssh_key_exists = False
                time.sleep(10)
                search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                search_field.clear()
                time.sleep(5)
                search_field.send_keys(Settings.key_name)
                time.sleep(5)
                assert not element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
                    'Error: Ssh key with name %s is found' % Settings.key_name)
            except Exception as e:
                print 'Ssh key cannot be deleted. Error: %s' % e

        if self.resource_exists:
            print 'Warning! Test cannot delete resource %s. It has to be deleted manually.' % Settings.resource_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name
        if self.ssh_key_exists:
            print 'Warning! Test cannot delete ssh key %s. It has to be deleted manually.' % Settings.key_name

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

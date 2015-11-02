import time
import unittest

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_provider, import_resource, unlink_resource, delete_provider, is_in_list,
                     element_exists)


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    nec_organization = 'Ministry of Bells'
    project_name = 'DO test project'
    provider_name = 'DigitalOceanTest'
    resource_name = 'FFW3'


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.provider_exists = False
        self.resource_exists = False

    def test_create_delete_project_resource(self):
        # Login NC
        print '%s is going to be loggedin.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        time.sleep(10)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        time.sleep(10)
        print '%s was loggedin successfully.' % Settings.username

        # Choose organization
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, Settings.nec_organization)
        time.sleep(10)
        print 'Organization was chosen successfully.'

        # Create project
        print 'Project is going to be created.'
        create_project(self.driver, Settings.project_name)
        time.sleep(5)
        search_field = self.driver.find_element_by_css_selector('[ng-model="entityList.searchInput"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.project_name)
        time.sleep(5)
        projects_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        assert is_in_list(projects_list, Settings.project_name), (
            'Error: Cannot find project with name  %s ' % Settings.project_name)
        self.project_exists = True
        print 'Project was created successfully'
        time.sleep(10)

        # Create provider
        print 'Provider is going to be created.'
        create_provider(self.driver, Settings.project_name, Settings.provider_name)
        time.sleep(5)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.provider_name)
        time.sleep(5)
        provider_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        assert is_in_list(provider_list, Settings.provider_name), (
            'Error: Cannot find provider with name  %s ' % Settings.provider_name)
        self.provider_exists = True
        print 'Provider was created successfully.'
        time.sleep(10)

        # Import resource
        print 'Resource is going to be imported.'
        import_resource(self.driver, Settings.project_name, Settings.provider_name, Settings.resource_name)
        time.sleep(10)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.resource_name)
        time.sleep(5)
        resource_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        assert is_in_list(resource_list, Settings.resource_name), (
            'Error: Cannot find resource with name  %s ' % Settings.resource_name)
        self.resource_exists = True
        print 'Resource was imported successfully.'
        time.sleep(10)

        # Unlink resource
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, Settings.project_name, Settings.resource_name)
        time.sleep(10)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        time.sleep(5)
        search_field.send_keys(Settings.resource_name)
        time.sleep(10)
        assert not element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
            'Error: Resource with name %s is found' % Settings.resource_name)
        self.resource_exists = False
        print 'Resource was unlinked successfully.'
        time.sleep(10)

    def tearDown(self):
        print 'Provider exists: ', self.provider_exists
        if self.provider_exists:
            try:
                # Remove provider
                print 'Provider is going to be removed.'
                time.sleep(10)
                delete_provider(self.driver, Settings.project_name, Settings.provider_name)
                self.provider_exists = False
                time.sleep(10)
                search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                search_field.clear()
                time.sleep(5)
                search_field.send_keys(Settings.provider_name)
                time.sleep(5)
                assert not element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'), (
                    'Error: Provider with name %s is found' % Settings.provider_name)
            except Exception as e:
                print 'Provider cannot be removed. Error: %s' % e
        time.sleep(10)

        if self.project_exists:
            try:
                # Remove project
                print 'Project is going to be removed.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                time.sleep(10)
                if not element_exists(self.driver, xpath="//*[contains(text(), 'You have no projects yet.')]"):
                    search_field = self.driver.find_element_by_css_selector('[ng-model="entityList.searchInput"]')
                    search_field.clear()
                    time.sleep(5)
                    search_field.send_keys(Settings.project_name)
                    time.sleep(10)
                    if element_exists(self.driver, css_selector='[ng-repeat="entity in entityList.list"]'):
                        self.project_exists = True
            except Exception as e:
                print 'Project cannot be deleted. Error: %s' % e

        if self.resource_exists:
            print 'Warning! Test cannot unlink resource %s. It has to be unlinked manually.' % Settings.resource_name
        if self.provider_exists:
            print 'Warning! Test cannot delete provider %s. It has to be deleted manually.' % Settings.provider_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name

        # self.driver.quit()


if __name__ == "__main__":
    unittest.main()

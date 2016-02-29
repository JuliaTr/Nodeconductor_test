"""
1. Login NC
2. Choose organization
3. Add project
4. Add ssh key
5. Add resource
6. Remove resource
7. Remove project
8. Remove ssh key
"""


import time
import unittest
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import (login_nodeconductor, get_driver, add_project, remove_project, add_ssh_key,
                     remove_ssh_key, choose_organization, add_resource_openstack, remove_resource,
                     _search, element_exists, make_screenshot)

from base import BaseSettings


class Settings(BaseSettings):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'OpenStack test project1'
    key_name = 'Openstack test key'
    category_name = 'VMs'
    provider_name_in_resource = 'Parnu lab'
    image_name = 'Ubuntu 14.04 x86_64'
    flavor_name = 'm1.small'
    resource_name = 'OpenStack test instance1'
    public_key_name = 'Openstack test key'
    time_wait_for_resource_creation = 240
    time_wait_after_resource_stopping = 180
    time_wait_after_resource_removal = 60


class OpenStackCreationTest(unittest.TestCase):

    def setUp(self):
        sys.exc_clear()
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.ssh_key_exists = False
        self.resource_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)

    def test_add_remove_resource(self):
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

        # Add project
        print 'Project is going to be added.'
        add_project(self.driver, Settings.project_name)
        time.sleep(BaseSettings.click_time_wait)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.project_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot add project "%s"' % Settings.project_name
        self.project_exists = True
        print 'Project exists: ', self.project_exists
        print 'Project was added successfully.'

        # Add ssh key
        print 'SSH key is going to be added.'
        time.sleep(BaseSettings.click_time_wait)
        add_ssh_key(self.driver, Settings.user_full_name, Settings.key_name)
        _search(self.driver, Settings.key_name)
        print 'Find key in list'
        xpath = '//span[contains(text(), "%s")]' % Settings.key_name
        assert element_exists(self.driver, xpath=xpath), 'Error: Key with name "%s" is not found' % Settings.key_name
        self.ssh_key_exists = True
        print 'SSH key exists: ', self.ssh_key_exists
        print 'SSH key was added successfully'

        # Blocker SAAS-1141
        # Add resource
        print 'Resource is going to be added.'
        add_resource_openstack(self.driver, Settings.project_name, Settings.resource_name, Settings.category_name,
                               Settings.provider_name_in_resource, Settings.image_name, Settings.flavor_name,
                               Settings.public_key_name)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.resource_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot add resource "%s"' % Settings.resource_name
        self.resource_exists = True
        print 'Resource exists: ', self.resource_exists
        print 'Find online state of added resource'
        try:
            WebDriverWait(self.driver, Settings.time_wait_for_resource_creation).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Online")]')))
        except TimeoutException as e:
            print 'Error: Resource is not online'
            raise e
        else:
            print 'Resource is in online state'
        print 'Resource was added successfully.'

        # SAAS-1133
        # Remove resource
        print 'Resource is going to be removed.'
        remove_resource(self.driver, Settings.resource_name, Settings.project_name,
                        Settings.time_wait_after_resource_stopping)
        self.resource_exists = False
        print 'Resource exists: ', self.resource_exists
        # _search(self.driver, Settings.resource_name)
        # print 'Wait till resource will be removed'
        # try:
        #     WebDriverWait(self.driver, Settings.time_wait_after_resource_removal).until(
        #         EC.invisibility_of_element_located((By.XPATH, '//a[contains(text(), "%s")]' % Settings.resource_name)))
        # except TimeoutException as e:
        #     print 'Error: Resource with name "%s" was not removed, it still exists' % Settings.resource_name
        #     raise e
        # print 'Resource was removed successfully.'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver, name=self.__class__.__name__)
        if self.project_exists:
            try:
                # Remove project
                print 'Project is going to be removed.'
                remove_project(self.driver, Settings.project_name)
                self.project_exists = False
                print 'Project exists: ', self.project_exists
                time.sleep(BaseSettings.click_time_wait)
                _search(self.driver, Settings.project_name)
                if element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % Settings.project_name):
                    self.project_exists = True
                    print 'Project exists: ', self.project_exists
                print 'Project was removed successfully.'
            except Exception as e:
                print 'Project cannot be removed. Error: "%s"' % e

        if self.ssh_key_exists:
            try:
                # Remove ssh key
                print 'Ssh key is going to be removed.'
                remove_ssh_key(self.driver, Settings.key_name, Settings.user_full_name)
                self.ssh_key_exists = False
                print 'SSH key exists: ', self.ssh_key_exists
                _search(self.driver, Settings.key_name)
                assert not element_exists(self.driver, xpath='//span[contains(text(), "%s")]' % Settings.key_name), (
                    'Error: SSH key with name "%s" was not removed, it still exists' % Settings.key_name)
                print 'SSH key was removed successfully.'
            except Exception as e:
                print 'SSH key cannot be removed. Error: %s' % e

        if self.resource_exists:
            print 'Warning! Test cannot remove resource %s. It has to be removed manually.' % Settings.resource_name
        if self.project_exists:
            print 'Warning! Test cannot remove project %s. It has to be removed manually.' % Settings.project_name
        if self.ssh_key_exists:
            print 'Warning! Test cannot remove ssh key %s. It has to be deleted manually.' % Settings.key_name

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

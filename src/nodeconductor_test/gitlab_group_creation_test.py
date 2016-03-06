"""
1. Login NC
2. Choose organization
3. Add project
4. Add application group
5. Add application project
6. Remove application project
7. Remove application group
8. Remove project
"""


import time
import unittest
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import (login_nodeconductor, get_driver, add_project, remove_project, choose_organization,
                     add_application_group, element_exists, remove_application_group, add_application_project,
                     remove_application_project, make_screenshot, _search)
from base import BaseSettings


class Settings(BaseSettings):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'GitLab test project'
    category_name = 'APPLICATIONS'
    resource_type_name = 'Group'
    resource_type_name1 = 'Project'
    path_name = 'test-group'
    application_group_name = 'Test group'
    visibility_level_name = 'The project can be cloned by any logged in user.'
    application_project_name = 'Test project'
    time_wait_for_application_state = 240
    time_wait_to_remove_application = 180


class ApplicationCreationTest(unittest.TestCase):

    def setUp(self):
        sys.exc_clear()
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.application_group_exists = False
        self.application_project_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)
        self.project_name = Settings.get_unique_attribute('project_name')
        self.application_group_name = Settings.get_unique_attribute('application_group_name')
        self.application_project_name = Settings.get_unique_attribute('application_project_name')
        # TODO Add uuid for a path after SAAS-1185
        # self.path_name = Settings.get_unique_attribute('path_name')

    def test_add_remove_application(self):
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
        add_project(self.driver, self.project_name)
        time.sleep(BaseSettings.click_time_wait)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % self.project_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot add project "%s"' % self.project_name
        self.project_exists = True
        print 'Project exists: ', self.project_exists
        print 'Project was added successfully.'

        # Add application group
        print 'Application group is going to be added.'
        add_application_group(self.driver, self.project_name, Settings.category_name, Settings.resource_type_name,
                              Settings.path_name, self.application_group_name)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % self.application_group_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot add application group "%s"' % self.application_group_name
        self.application_group_exists = True
        print 'Application group exists: ', self.application_group_exists
        print 'Find online state of added application group'
        try:
            WebDriverWait(self.driver, Settings.time_wait_for_application_state).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Online")]')))
        except TimeoutException as e:
            print 'Error: Application group is not online'
            raise e
        else:
            print 'Application group is in online status'
        print 'Application group was added successfully'

        # Add application project
        print 'Application project is going to be added.'
        add_application_project(self.driver, self.project_name, Settings.category_name, Settings.resource_type_name1, self.application_project_name,
                                Settings.visibility_level_name, self.application_group_name)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % self.application_project_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot add application group "%s"' % self.application_project_name
        self.application_project_exists = True
        print 'Application project exists: ', self.application_project_exists
        print 'Find online state of added application group'
        try:
            WebDriverWait(self.driver, Settings.time_wait_for_application_state).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Online")]')))
        except TimeoutException as e:
            print 'Error: Application project is not online'
            raise e
        else:
            print 'Application project is in online status'
        print 'Application project was added successfully'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver, name=self.__class__.__name__)
        if self.application_project_exists:
            try:
                # Remove application project
                print 'Application project is going to be removed.'
                remove_application_project(self.driver, self.project_name, self.application_project_name)
                self.application_project_exists = False
                print 'Application project exists: ', self.application_project_exists
                _search(self.driver, self.application_project_name)
                print 'Wait till application project will be removed'
                try:
                    WebDriverWait(self.driver, Settings.time_wait_to_remove_application).until(
                        EC.invisibility_of_element_located((By.XPATH, '//a[contains(text(), "%s")]' % self.application_project_name)))
                except TimeoutException as e:
                    print 'Error: Application project with name "%s" was not removed, it still exists' % self.application_project_name
                    raise e
                else:
                    print 'Application project was removed successfully.'
            except Exception as e:
                print 'Application project cannot be removed. Error: %s' % e

        if self.application_group_exists:
            try:
                # Remove application group
                print 'Application group is going to be removed.'
                remove_application_group(self.driver, self.project_name, self.application_group_name)
                self.application_group_exists = False
                print 'Application group exists: ', self.application_group_exists
                _search(self.driver, self.application_group_name)
                print 'Wait till application group will be removed'
                try:
                    WebDriverWait(self.driver, Settings.time_wait_to_remove_application).until(
                        EC.invisibility_of_element_located((By.XPATH, '//a[contains(text(), "%s")]' % self.application_group_name)))
                except TimeoutException as e:
                    print 'Error: Application group with name "%s" was not removed, it still exists' % self.application_group_name
                    raise e
                else:
                    print 'Application group was removed successfully.'
            except Exception as e:
                print 'Application group cannot be removed. Error: %s' % e

        if self.project_exists:
            try:
                # Remove project
                print 'Project is going to be removed.'
                remove_project(self.driver, self.project_name)
                self.project_exists = False
                print 'Project exists: ', self.project_exists
                time.sleep(BaseSettings.click_time_wait)
                _search(self.driver, self.project_name)
                if element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % self.project_name):
                    self.project_exists = True
                print 'Project was removed successfully.'
            except Exception as e:
                print 'Project cannot be removed. Error: "%s"' % e

        if self.application_project_exists:
            print 'Warning! Test cannot remove application project %s. It has to be removed manually.' % self.application_project_name
        if self.application_group_exists:
            print 'Warning! Test cannot remove application group %s. It has to be removed manually.' % self.application_group_name
        if self.project_exists:
            print 'Warning! Test cannot remove project %s. It has to be removed manually.' % self.project_name

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()

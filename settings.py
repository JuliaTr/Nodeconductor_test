# site_url = "http://squ-test.nodeconductor.com"
# username = 'Julia'
# password = '123'
# user_full_name = 'Trygubniak'

# site_url = "http://web-test.nodeconductor.com"
# username = 'Alice'
# password = 'Alice'
# user_full_name = 'Alice Lebowski'
# nec_organization = 'Ministry of Bells'
# project_name = 'OpenStack test project'
# key_name = 'Openstack test key'
# resource_name = 'OpenStack test instance'
# time_after_resource_creation = 180
# time_wait_after_resource_stopping = 60
# time_wait_after_resource_removal = 30

# site_url = "http://web-test.nodeconductor.com"
# username = 'Alice'
# password = 'Alice'
# user_full_name = 'Alice Lebowski'
# nec_organization = 'Ministry of Bells'
# project_name = 'DO test project'
# provider_name = 'DigitalOceanTest'
# resource_name = 'FFW3'





def f(a, c, b, d='Hello!'):
    print locals()
    print d
    print a, b, c


f('b', 'c', 'a')

dashboard_field = self.driver.find_element_by_link_text('Dashboard')
dashboard_field.click()
time.sleep(5)
dashboard_project_field = self.driver.find_element_by_css_selector('a.project-context span.customer-name')
dashboard_project_field.click()
dashboard_project = self.driver.find_element_by_link_text('Manage projects')
dashboard_project.click()
time.sleep(5)

resource_list = self.driver.find_elements_by_css_selector('[ng-repeat="entity in entityList.list"]')
        for resource in resource_list:
            assert 'Online' in resource.text, (
                'Error: Resource with name  %s is not online. It will not be possible to delete it. ' % Settings.resource_name)
        print 'Resource was created successfully'
        time.sleep(10)
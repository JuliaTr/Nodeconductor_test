import os
from uuid import uuid4

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class BaseSettings(object):
    window_resolution = 1366, 768
    # Tests should run on 1024x768 resolution until agreed otherwise.
    # If changing these numbers make sure to change screen size in Jenkins job configuration.
    # Use 420x580 resolution to test mobile version (work in progress).
    # TODO: read resolution value from method parameters or configuration file.
    click_time_wait = 3  # time between normal user clicks
    search_time_wait = 8  # time for search
    tab_visible_time_wait = 10
    implicitly_wait = 30  # time to wait for element appears on the page
    screenshots_folder = os.path.join(project_path, 'screenshots')
    test_reports_dir = os.path.join(project_path, 'test_reports')  # unittest-xml-reporting must be installed

    @classmethod
    def get_unique_attribute(cls, attr):
        return '%s %s' % (getattr(cls, attr), uuid4().hex)

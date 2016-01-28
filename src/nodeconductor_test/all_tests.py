import os
import unittest

from base import BaseSettings


if __name__ == "__main__":
    tests = unittest.TestLoader().discover(os.path.dirname(os.path.abspath(__file__)), pattern='*_test.py')
    try:
        import xmlrunner
        xmlrunner.XMLTestRunner(output=BaseSettings.test_reports_dir).run(tests)
    except ImportError as e:
        unittest.runner.TextTestRunner().run(tests)

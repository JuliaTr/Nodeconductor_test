Setting up the environment
==========================

1. Set up dependencies from requirements.txt.
2. Create private_settings.py on the basis of private_settings.py.example.
3. Execute file python <test_name> for its launching.

Optional steps:

4. Install `unittest-xml-reporting <https://pypi.python.org/pypi/unittest-xml-reporting>`_ to enable generation of XML reports

Running tests
=============

Running a single test:

.. code:: sh

python src/nodeconductor_tests/<test_name>.py

::

Running all tests:

.. code:: sh

python src/nodeconductor_tests/all_tests.py

::

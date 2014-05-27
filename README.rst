Coverage Reporting for Python
=============================

Uploads code coverage data to `scrutinizer-ci.com <https://scrutinizer-ci.com>`_.

Installation
------------
To install the code coverage reporter, simply run:

.. code-block:: bash

    pip install scrutinizer-ocular

Integration with your CI server
-------------------------------
After your code coverage was generated, simply run the following command:

.. code-block:: bash

    ocular --access-token "your-access-token"

**For closed-source projects**, make sure to `generate an access token <https://scrutinizer-ci.com/profile/applications>`_.
For open-source projects, this is not necessary and should be avoided.

Customizing Locations of Coverage Data/Config
---------------------------------------------
If your coverage data or configuration is not placed in the current working directory, you need to pass these paths
as options to the ocular command:

.. code-block:: bash

    ocular --access-token "your-access-token" --data-file "../.coverage" --config-file "../.coveragerc"


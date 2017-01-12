# PyISAM

PyISAM is a Python framework for configuring an IBM Security Access Manager (ISAM) appliance via web service requests.

**Supported ISAM versions**
* IBM Security Access Manager 9.0.2.1
* IBM Security Access Manager 9.0.2.0

## Requirements

[Requests](http://docs.python-requests.org/en/master)

## Usage

```
import logging

from pyisam import Factory

logging.basicConfig(level=logging.DEBUG)

base_url = "https://isam.pyisam.ibm.com"
username = "admin"
password = "Passw0rd"

factory = Factory(base_url, username, password)
access_control = factory.get_access_control()
success, status, content = access_control.authentication.create_policy(...)
if success:
    print "Successfully created the policy"
else:
    print Failed to create the policy. status: %i, content: %s" % (status, content)
```

## Structure

The project is structured closely around the ISAM Local Management Interface mega menu.

```
pyisam -
    aux -
        {modules}
    core -
        {category} -
            {subcategory-module}
        {category-module}
    util -
        {module}
    factory.py
```

**Core:** functionality that is an exact, or close to, mapping of the available ISAM REST APIs.

**Auxiliary:** functionality that is not a specific ISAM REST API but is a common procedure to configuring appliances. This may include multiple calls for `Core` functionality.

**Utilities:** functionality that does not configure an ISAM appliance but aid in configuration tasks.

**Category:** maps to a mega menu category (e.g. Access Control) and contains all REST API functionality related to it.

**Category Module:** a master module for the category that defines public accessible variables for each subcategory. This module will contain multiple classes each for a specific ISAM firmware version.

**Subcategory Module:** a module that contains all REST API functionality for a given subcategory (e.g. API Protection). These modules will contain multiple classes, a base class implementing all methods, and additional classes specific to a version of ISAM which override any functionality that has been changed in that version.

**Factory:** the master module/class of the framework. This module handles the discovery and enforcement of supported ISAM versions, along with dynamic instantiation of version specific classes.

Discovery of the ISAM appliance's version and enforcement of supported versions are handled here, along with dynamic instantiation of version specific classes.

## Style Guide

[Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008)

[Idiomatic Python](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html)

*To be documented...*

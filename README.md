# ISAM PyConfig

ISAM PyConfig is a Python framework for issuing configuration based web service requests to an ISAM appliance.

## Requirements

[Requests](http://docs.python-requests.org/en/master)

## Structure

The project is structured closely around the ISAM Local Management Interface mega menu.

```
com -
    ibm -
        isam -
             pyconfig -
                      {category} -
                                 {category-module}
                                 {subcategory-module}
                      factory.py
             util -
                      {modules}
```

**Category:** a mega menu categories (e.g. Access Control) are separated by a directory, each holding all REST API functionality related to that category.

**Category Module:** a master module for the category that inherits all subcategory functionality. This module will contain multiple classes each for a specific version of ISAM.

**Subcategory Module:** a module that contains all REST API functionality for a given subcategory (e.g. Policy). These modules will contain multiple classes, a base class implementing all methods, and additional classes specific to a version of ISAM which override any functionality that has been changed in that version.

**Factory:** the master module/class of the framework. This module handles the discovery and enforcement of supported ISAM versions, along with dynamic instantiation of version specific classes.

Discovery of the ISAM appliance's version and enforcement of supported versions are handled here, along with dynamic instantiation of version specific classes.

**Utilities:** all functionality that is not a ISAM REST API is stored within modules under the `util` directory.

## Style Guide

[Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008)

[Idiomatic Python](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html)

*To be documented...*

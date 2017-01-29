======
PyISAM
======

PyISAM is a Python library that wraps the IBM Security Access Manager's RESTful Web services to provide a
quick and easy way to construct configuration scripts for appliances.

**Supported Versions**

- IBM Security Access Manager 9.0.2.1
- IBM Security Access Manager 9.0.2.0

Installation
============
*To be documented...*

Usage
=====
.. code-block:: python

    >>> import pyisam
    >>> factory = pyisam.Factory("https://isam.mmfa.ibm.com", "admin", "Passw0rd")
    >>> web = factory.get_web_settings()
    >>> resp = web.reverse_proxy.restart_instance("default")
    >>> if resp.success:
    ...     print "Successfully restarted the default instance."
    ... else:
    ...     print "Failed to restart the default instance. status_code: %s, data: %s" % (r.status_code, r.data)
    ...
    Successfully restarted the default instance.

Contribute
==========
1. `Identify an existing issue <https://github.ibm.com/benmarti/pyisam/issues>`_ or `create a new issue <https://help.github.com/enterprise/2.8/user/articles/creating-an-issue/>`_ that outlines the feature or bug you wish to address.
2. `Fork the repository <https://help.github.com/enterprise/2.8/user/articles/fork-a-repo/>`_ to your GitHub account.
3. Make the required changes to the **master** branch or another branch, if you wish.
4. Submit a `pull request <https://help.github.com/enterprise/2.8/user/articles/creating-a-pull-request-from-a-fork/>`_ to get your changes reviewed and merged.

Style Guidelines
----------------
*To be documented...*

`Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008>`_

`Idiomatic Python <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html>`_

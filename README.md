# PyISAM

PyISAM is a Python library that wraps the IBM Security Access Manager's RESTful Web services to provide a
quick and easy way to construct configuration scripts for appliances.

**Supported Versions**

- IBM Security Access Manager 9.0.2.1
- IBM Security Access Manager 9.0.2.0

## Installation

*To be documented...*

## Usage

```python
>>> import pyisam
>>> factory = pyisam.Factory("https://isam.mmfa.ibm.com", "admin", "*******")
>>> web = factory.get_web_settings()
>>> resp = web.reverse_proxy.restart_instance("default")
>>> if resp.success:
...     print "Successfully restarted the default instance."
... else:
...     print "Failed to restart the default instance. status_code: %s, data: %s" % (r.status_code, r.data)
...
Successfully restarted the default instance.
```

[![Build Status](https://travis-ci.org/OGCMetOceanDWG/wmo-cmp-ts.png?branch=master)](https://travis-ci.org/OGCMetOceanDWG/wmo-cmp-ts)

WMO Core Metadata Profile Test Suite
====================================

This library implements validation against [WMO Core Metadata Profile 1.3] (http://wis.wmo.int/2013/metadata/version_1-3-0/WMO_Core_Metadata_Profile_v1.3_Specification_Part_1_v1.0FINALcorrected.pdf), specifically [Part 2] (http://wis.wmo.int/2013/metadata/version_1-3-0/WMO_Core_Metadata_Profile_v1.3_Specification_Part_2_v1.0FINAL.pdf), Section 2.

Installation
------------

```bash
virtualenv wmo-cmp-ts
cd wmo-cmp-ts
. bin/activate
git clone git@github.com:OGCMetOceanDWG/wmo-cmp-ts.git
cd wmo-cmp-ts
pip install -r requirements.txt
python setup.py build
python setup.py install
```

Running
-------

From command line:
```bash
wmo-metadata-validate.py /path/to/file.xml
```

From Python:
```python
>>> test a file on disk
>>> from lxml import etree
>>> from wmo_cmp_ts import test_suite
>>> exml = etree.parse('/path/to/file.xml')
>>> ts = test_suite.WMOCoreMetadataProfileTestSuite13(exml)
>>> ts.run_tests()  # raises ValueError error stack on exception
```

```python
>>> test a URL
>>> from urllib2 import urlopen
>>> from StringIO import StringIO
>>> content = StringIO(urlopen('http://....').read())
>>> exml = etree.parse(content)
```

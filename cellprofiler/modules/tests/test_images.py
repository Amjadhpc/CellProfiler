'''test_images.py - test the Images module

CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Copyright (c) 2003-2009 Massachusetts Institute of Technology
Copyright (c) 2009-2014 Broad Institute
All rights reserved.

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
'''

import csv
import numpy as np
import os
from cStringIO import StringIO
import tempfile
import unittest
import urllib

import cellprofiler.measurements as cpmeas
import cellprofiler.pipeline as cpp
import cellprofiler.settings as cps
import cellprofiler.workspace as cpw
import cellprofiler.modules.images as I

class TestImages(unittest.TestCase):
    def setUp(self):
        # The Images module needs a workspace and the workspace needs
        # an HDF5 file.
        #
        self.temp_fd, self.temp_filename = tempfile.mkstemp(".h5")
        self.measurements = cpmeas.Measurements(
            filename = self.temp_filename)
        os.close(self.temp_fd)
        
    def tearDown(self):
        self.measurements.close()
        os.unlink(self.temp_filename)
        self.assertFalse(os.path.exists(self.temp_filename))
        
    def test_01_01_load_v1(self):
        data = r"""CellProfiler Pipeline: http://www.cellprofiler.org
Version:3
DateRevision:20120209212234
ModuleCount:1
HasImagePlaneDetails:False

Images:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:1|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)]
    :{"ShowFiltered"\x3A false}
    Filter based on rules:Yes
    Filter:or (directory does startwith "foo") (file does contain "bar")
"""
        pipeline = cpp.Pipeline()
        def callback(caller, event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO(data))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, I.Images))
        self.assertEqual(module.filter_choice, I.FILTER_CHOICE_CUSTOM)
        self.assertEqual(module.filter.value, 'or (directory does startwith "foo") (file does contain "bar")')
        
    def test_01_02_load_v2(self):
        data = r"""CellProfiler Pipeline: http://www.cellprofiler.org
Version:3
DateRevision:20120209212234
ModuleCount:1
HasImagePlaneDetails:False

Images:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:2|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)]
    :{"ShowFiltered"\x3A false}
    Filter choice:%s
    Filter:or (directory does startwith "foo") (file does contain "bar")
"""
        for fc, fctext in ((I.FILTER_CHOICE_CUSTOM, "Custom"),
                           (I.FILTER_CHOICE_IMAGES, "Images only"),
                           (I.FILTER_CHOICE_NONE, "No filtering")):
            pipeline = cpp.Pipeline()
            def callback(caller, event):
                self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
            pipeline.add_listener(callback)
            pipeline.load(StringIO(data % fctext))
            self.assertEqual(len(pipeline.modules()), 1)
            module = pipeline.modules()[0]
            self.assertTrue(isinstance(module, I.Images))
            self.assertEqual(module.filter_choice, fc)
            self.assertEqual(module.filter.value, 'or (directory does startwith "foo") (file does contain "bar")')
        
    def test_02_04_filter_url(self):
        module = I.Images()
        module.filter_choice.value = I.FILTER_CHOICE_CUSTOM
        for url, filter_value, expected in (
            ("file:/TestImages/NikonTIF.tif",
             'and (file does startwith "Nikon") (extension does istif)', True),
            ("file:/TestImages/NikonTIF.tif",
             'or (file doesnot startwith "Nikon") (extension doesnot istif)', False),
            ("file:/TestImages/003002000.flex",
             'and (directory does endwith "ges") (directory doesnot contain "foo")', True),
            ("file:/TestImages/003002000.flex",
             'or (directory doesnot endwith "ges") (directory does contain "foo")', False)):
            module.filter.value = filter_value
            self.assertEqual(module.filter_url(url), expected)
            
    def test_02_05_filter_standard(self):
        module = I.Images()
        module.filter_choice.value = I.FILTER_CHOICE_IMAGES
        for url, expected in (
            ("file:/TestImages/NikonTIF.tif", True),
            ("file:/foo/.bar/baz.tif", False),
            ("file:/TestImages/foo.bar", False)):
            self.assertEqual(module.filter_url(url), expected)
        
        
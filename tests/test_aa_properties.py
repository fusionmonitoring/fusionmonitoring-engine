#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2019: FusionSupervision team, see AUTHORS.md file for contributors
#
# This file is part of FusionSupervision engine.
#
# FusionSupervision is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FusionSupervision is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with FusionSupervision engine.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#  Copyright (C) 2015-2018: Alignak team, see AUTHORS.alignak.txt file for contributors
#
#  This file is part of Alignak.
#
#  Alignak is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Alignak is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
#  This file incorporates work covered by the following copyright and
#  permission notice:
#
#   Copyright (C) 2009-2014:
#      Jean Gabes, naparuba@gmail.com
#      Hartmut Goebel, h.goebel@goebel-consult.de
#      Grégory Starck, g.starck@gmail.com
#      Sebastien Coavoux, s.coavoux@free.fr
#      Christophe SIMON, christophe.simon@dailymotion.com
#
#   This file is part of Shinken.
#
#   Shinken is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Shinken is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

"""
Test fusionsupervision.property
"""

import fusionsupervision
from fusionsupervision.property import NONE_OBJECT

from .fusionsupervision_test import FusionsupervisionTest
import pytest


class PropertyTests:
    """Common tests for all property classes"""

    def test_no_default_value(self):
        p = self.prop_class()
        assert p.default is NONE_OBJECT
        assert not p.has_default
        assert p.required

    def test_default_value(self):
        default_value = object()
        p = self.prop_class(default=default_value)
        assert p.default is default_value
        assert p.has_default
        assert not p.required

    def test_fill_brok(self):
        p = self.prop_class()
        assert 'full_status' not in p.fill_brok
        p = self.prop_class(default='0', fill_brok=['full_status'])
        assert 'full_status' in p.fill_brok

    def test_unused(self):
        p = self.prop_class()
        assert not p.unused


class TestBoolProp(PropertyTests, FusionsupervisionTest):
    """Test the BoolProp class"""

    prop_class = fusionsupervision.property.BoolProp

    def test_pythonize(self):
        p = self.prop_class()
        # allowed strings for `True`
        assert p.pythonize("1") == True
        assert p.pythonize("yes") == True
        assert p.pythonize("true") == True
        assert p.pythonize("on") == True
        assert p.pythonize(["off", "on"]) == True
        # allowed strings for `False`
        assert p.pythonize("0") == False
        assert p.pythonize("no") == False
        assert p.pythonize("false") == False
        assert p.pythonize("off") == False
        assert p.pythonize(["on", "off"]) == False


class TestIntegerProp(PropertyTests, FusionsupervisionTest):
    """Test the IntegerProp class"""

    prop_class = fusionsupervision.property.IntegerProp

    def test_pythonize(self):
        p = self.prop_class()
        assert p.pythonize("1") == 1
        assert p.pythonize("0") == 0
        assert p.pythonize("1000.33") == 1000
        assert p.pythonize(["2000.66", "1000.33"]) == 1000


class TestFloatProp(PropertyTests, FusionsupervisionTest):
    """Test the FloatProp class"""

    prop_class = fusionsupervision.property.FloatProp

    def test_pythonize(self):
        p = self.prop_class()
        assert p.pythonize("1") == 1.0
        assert p.pythonize("0") == 0.0
        assert p.pythonize("1000.33") == 1000.33
        assert p.pythonize(["2000.66", "1000.33"]) == 1000.33


class TestStringProp(PropertyTests, FusionsupervisionTest):
    """Test the StringProp class"""

    prop_class = fusionsupervision.property.StringProp

    def test_pythonize(self):
        p = self.prop_class()
        assert p.pythonize("1") == "1"
        assert p.pythonize("yes") == "yes"
        assert p.pythonize("0") == "0"
        assert p.pythonize("no") == "no"
        assert p.pythonize(["yes", "no"]) == "no"


class TestCharProp(PropertyTests, FusionsupervisionTest):
    """Test the CharProp class"""

    prop_class = fusionsupervision.property.CharProp

    def test_pythonize(self):
        p = self.prop_class()
        assert p.pythonize("c") == "c"
        assert p.pythonize("cxxxx") == "c"
        assert p.pythonize(["bxxxx", "cxxxx"]) == "c"
        # this raises IndexError. is this intented?
        ## self.assertEqual(p.pythonize(""), "")


class TestPathProp(TestStringProp):
    """Test the PathProp class"""

    prop_class = fusionsupervision.property.PathProp

    # As of now, PathProp is a subclass of StringProp without any
    # relevant change. So no further tests are implemented here.


class TestConfigPathProp(TestStringProp):
    """Test the ConfigPathProp class"""

    prop_class = fusionsupervision.property.ConfigPathProp

    # As of now, ConfigPathProp is a subclass of StringProp without
    # any relevant change. So no further tests are implemented here.


class TestListProp(PropertyTests, FusionsupervisionTest):
    """Test the ListProp class"""

    prop_class = fusionsupervision.property.ListProp

    def test_pythonize(self):
        p = self.prop_class()
        assert p.pythonize("") == []
        assert p.pythonize("1,2,3") == ["1", "2", "3"]
        # Default is to split on coma for list also.
        assert p.pythonize(["1,2,3", "4,5,6"]) == ["1","2","3", "4","5","6"]

    def test_pythonize_nosplit(self):
        p = self.prop_class(split_on_comma=False)
        assert p.pythonize("") == []
        assert p.pythonize("1,2,3") == ["1,2,3"]
        # Default is to split on coma for list also.
        assert p.pythonize(["1,2,3", "4,5,6"]) == ["1,2,3", "4,5,6"]


class TestLogLevelProp(PropertyTests, FusionsupervisionTest):
    """Test the LogLevelProp class"""

    prop_class = fusionsupervision.property.LogLevelProp

    def test_pythonize(self):
        p = self.prop_class()
        assert p.pythonize("NOTSET") == 0
        assert p.pythonize("DEBUG") == 10
        assert p.pythonize("INFO") == 20
        assert p.pythonize("WARN") == 30
        assert p.pythonize("WARNING") == 30
        assert p.pythonize("ERROR") == 40
        ## 'FATAL' is not defined in std-module `logging._levelNames`
        #self.assertEqual(p.pythonize("FATAL"), 50)
        assert p.pythonize("CRITICAL") == 50
        assert p.pythonize(["NOTSET", "CRITICAL"]) == 50


class TestAddrProp(PropertyTests, FusionsupervisionTest):
    """Test the AddrProp class"""

    prop_class = fusionsupervision.property.AddrProp

    def test_pythonize_with_IPv4_addr(self):
        p = self.prop_class()
        assert p.pythonize("192.168.10.11:445") == \
                         {'address': "192.168.10.11",
                          'port': 445}
        # no colon, no port
        assert p.pythonize("192.168.10.11") == \
                         {'address': "192.168.10.11"}
        # colon but no port number
        with pytest.raises(ValueError):
            p.pythonize("192.168.10.11:")
        # only colon, no addr, no port number
        with pytest.raises(ValueError):
            p.pythonize(":")
        # no address, only port number
        assert p.pythonize(":445") == \
                         {'address': "",
                          'port': 445}

    def test_pythonize_with_hostname(self):
        p = self.prop_class()
        assert p.pythonize("host_123:445") == \
                         {'address': "host_123",
                          'port': 445}
        # no colon, no port
        assert p.pythonize("host_123") == \
                         {'address': "host_123"}
        # colon but no port number
        with pytest.raises(ValueError):
            p.pythonize("host_123:")
        # only colon, no addr, no port number
        with pytest.raises(ValueError):
            p.pythonize(":")
        # no address, only port number
        assert p.pythonize(":445") == \
                         {'address': "",
                          'port': 445}
        assert p.pythonize([":444", ":445"]) == \
                         {'address': "",
                          'port': 445}

    # :fixme: IPv6 addresses are no tested since they are not parsed
    # correcly

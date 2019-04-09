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

import unittest2
from fusionsupervision import common

class CommonPureTest(unittest2.TestCase):
    """Test functions in common file/class"""

    def test_convert_list_in_dict(self):
        """Test the pure funtion convert_list_in_dict"""
        data_list = [
            {
                "_id": "11",
                "name": "test1"
            },
            {
                "_id": "12",
                "name": "test2"
            },
            {
                "_id": "13",
                "name": "test3"
            }
        ]
        data_reference = {
            "11": {
                "_id": "11",
                "name": "test1"
            },
            "12": {
                "_id": "12",
                "name": "test2"
            },
            "13": {
                "_id": "13",
                "name": "test3"
            }
        }
        data_dict = common.convert_list_in_dict(data_list)
        self.assertDictEqual(data_reference, data_dict)

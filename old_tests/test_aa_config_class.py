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

"""
This file contains the test for the Alignak Config class
"""

import os
import re
import sys
import time
import unittest2
import pytest
import importlib

from .fusionsupervision_test import FusionsupervisionTest

from fusionsupervision.objects.config import Config

class TestConfigClassBase(FusionsupervisionTest):
    """
    This class tests the Config obhject initialization
    """
    def setUp(self):
        super(TestConfigClassBase, self).setUp()

    def test_config_ok(self):
        """Test the object initialization and base features"""
        # ---
        # print("Reference to Config: %s" % sys.getrefcount(Config))
        # mod = importlib.import_module("fusionsupervision.objects.config")
        # importlib.reload(mod)
        # #
        # # importlib.reload('fusionsupervision.objects.config')
        # print("Reference to Config: %s" % sys.getrefcount(Config))

        # Fresh initialized configuration
        fusionsupervision_cfg = Config()
        assert fusionsupervision_cfg.magic_hash
        next_instance_id = "Config_%s" % Config._next_id
        # assert str(fusionsupervision_cfg) == '<Config Config_1 - unknown />'

        # Another fresh initialized configuration
        fusionsupervision_cfg = Config()
        assert fusionsupervision_cfg.magic_hash
        # Config instance_id incremented!
        assert next_instance_id == fusionsupervision_cfg.instance_id
        # assert str(fusionsupervision_cfg) == '<Config Config_2 - unknown />'
        from pprint import pprint
        pprint(fusionsupervision_cfg.macros)

        # -----------------------------------------------------------------------------------------
        # Macro part
        # ---
        # Macro list is yet defined but the values are not yet set
        expected_macros = {
            # Main Config objects macros
            'ALIGNAK': 'fusionsupervision_name',
            'ALIGNAK_CONFIG': 'fusionsupervision_env',

            'ADMINEMAIL': '',
            'ADMINPAGER': '',

            'MAINCONFIGDIR': 'config_base_dir',
            'CONFIGFILES': 'config_files',
            'MAINCONFIGFILE': 'main_config_file',

            'OBJECTCACHEFILE': '', 'COMMENTDATAFILE': '', 'TEMPPATH': '', 'SERVICEPERFDATAFILE': '',
            'RESOURCEFILE': '', 'COMMANDFILE': '', 'DOWNTIMEDATAFILE': '',
            'HOSTPERFDATAFILE': '', 'LOGFILE': '', 'TEMPFILE': '', 'RETENTIONDATAFILE': '',
            'STATUSDATAFILE': '',
            'RETENTION_FILE': 'state_retention_file'
        }
        # The 64 "USER" macros.
        for i in range(1, 65):
            expected_macros['USER%d' % i] = '$USER%d$' % i
        assert fusionsupervision_cfg.macros == expected_macros

        # After several tests execution the Config object got imported several times and
        # has several python references. The properties object containing the macros is a
        # class object and has thus been updated because some configurations got loaded.
        # Because of this, a pure assertion is only valid when the test is the first one executed!
        compare_macros = {}
        for macro in list(fusionsupervision_cfg.macros.items()):
            compare_macros[macro[0]] = macro[1]
            # print(macro)
            # if macro[0] not in [
            #     'DIST', 'DIST_BIN', 'DIST_ETC', 'DIST_LOG', 'DIST_RUN', 'DIST_VAR',
            #     'VAR', 'RUN', 'ETC', 'BIN', 'USER', 'GROUP', 'LIBEXEC', 'LOG',
            #     'NAGIOSPLUGINSDIR', 'PLUGINSDIR', ''
            # ]:
            #     compare_macros[macro[0]] = macro[1]
        assert compare_macros == expected_macros
        assert fusionsupervision_cfg.macros == expected_macros

        # # Macro properties are not yet existing!
        # for macro in fusionsupervision_cfg.macros:
        #     print("Macro: %s" % macro)
        #     assert getattr(fusionsupervision_cfg, '$%s$' % macro, None) is None, \
        #         "Macro: %s property is still existing!" % ('$%s$' % macro)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        # Configuration parsing part
        # ---
        # Read and parse the legacy configuration files, do not provide environement file name
        legacy_cfg_files = ['../etc/fusionsupervision.cfg']
        raw_objects = fusionsupervision_cfg.read_config_buf\
            (fusionsupervision_cfg.read_legacy_cfg_files(legacy_cfg_files))
        assert isinstance(raw_objects, dict)
        for daemon_type in ['arbiter', 'broker', 'poller', 'reactionner', 'receiver', 'scheduler']:
            assert daemon_type in raw_objects
        # Make sure we got all the managed objects type
        for o_type in fusionsupervision_cfg.types_creations:
            assert o_type in raw_objects, 'Did not found %s in configuration ojbect' % o_type
        assert fusionsupervision_cfg.fusionsupervision_env == 'n/a'

        # Same parser that stores the environment files names
        env_filename = '../etc/fusionsupervision.ini'
        # It should be a list
        env_filename = [os.path.abspath(env_filename)]
        # Read and parse the legacy configuration files, do not provide environement file name
        raw_objects = fusionsupervision_cfg.read_config_buf(
            fusionsupervision_cfg.read_legacy_cfg_files(legacy_cfg_files, env_filename)
        )
        assert fusionsupervision_cfg.fusionsupervision_env == env_filename

        # Same parser that stores a string (not list) environment file name
        # as an absolute file path in a list
        env_filename = '../etc/fusionsupervision.ini'
        # Read and parse the legacy configuration files, do not provide environement file name
        raw_objects = fusionsupervision_cfg.read_config_buf(
            fusionsupervision_cfg.read_legacy_cfg_files(legacy_cfg_files, env_filename)
        )
        assert fusionsupervision_cfg.fusionsupervision_env == [os.path.abspath(env_filename)]

        # Same parser that stores the environment file name as an absolute file path
        env_filename = '../etc/fusionsupervision.ini'
        # Read and parse the legacy configuration files, do not provide environement file name
        raw_objects = fusionsupervision_cfg.read_config_buf(
            fusionsupervision_cfg.read_legacy_cfg_files(legacy_cfg_files, env_filename)
        )
        assert fusionsupervision_cfg.fusionsupervision_env == [os.path.abspath(env_filename)]
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        # Macro part
        # ---
        # The macros defined in the default loaded configuration
        expected_macros.update({
            # 'DIST': '$DIST$',
            # 'DIST_BIN': '$DIST_BIN$',
            # 'DIST_ETC': '$DIST_ETC$',
            # 'DIST_LOG': '$DIST_LOG$',
            # 'DIST_RUN': '$DIST_RUN$',
            # 'DIST_VAR': '$DIST_VAR$',
            # 'BIN': '$BIN$',
            # 'ETC': '$ETC$',
            # 'GROUP': '$GROUP$',
            # 'LIBEXEC': '$LIBEXEC$',
            # 'LOG': '$LOG$',
            # 'NAGIOSPLUGINSDIR': '',
            # 'PLUGINSDIR': '$',
            # 'RUN': '$RUN$',
            # 'USER': '$USER$',
            # 'USER1': '$NAGIOSPLUGINSDIR$',
            # 'VAR': '$VAR$'
        })
        assert sorted(fusionsupervision_cfg.macros) == sorted(expected_macros)
        assert fusionsupervision_cfg.resource_macros_names == []
        # Macro are not existing in the object attributes!
        for macro in fusionsupervision_cfg.macros:
            macro = fusionsupervision_cfg.macros[macro]
            assert getattr(fusionsupervision_cfg, '$%s$' % macro, None) is None, \
                "Macro: %s property is existing as an attribute!" % ('$%s$' % macro)
        # But as an attribute of the properties attribute!
        for macro in fusionsupervision_cfg.macros:
            macro = fusionsupervision_cfg.macros[macro]
            assert getattr(fusionsupervision_cfg.properties, '$%s$' % macro, None) is None, \
                "Macro: %s property is not existing as an attribute of properties!" % ('$%s$' % macro)

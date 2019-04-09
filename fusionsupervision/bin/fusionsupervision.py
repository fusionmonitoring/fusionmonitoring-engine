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

import argparse
from fusionsupervison import fusionsupervison

def main():
    #parser = argparse.ArgumentParser(description=__doc__)
    #parser.add_argument(
    #    'input_file',
    #    type=str,
    #    help="The spreadsheet file to pring the columns of"
    #)
    #args = parser.parse_args()
    #get_spreadsheet_cols(args.input_file, print_cols=True)
    fusionsupervison.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()

#!/usr/bin/env python3
"""
A quick and simple Python-based CMS

Copyright (C) 2014  George Bryant

This program is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

You should have received a copy of the GNU General Public License along with
    this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse

parser = argparse.ArgumentParser(
        description="LazyPyCMS - a simple Python-based web CMS")

parser.add_argument("-n", "--new", action="store_true",
        help="Create a new post")

parser.add_argument("-e", "--edit", type=str, action="append",
        metavar="N", default=None,
        help="Edit an existing post in the LazyPyCMS editor. Give the post number")

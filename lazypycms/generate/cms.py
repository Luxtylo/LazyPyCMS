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

This is LazyPyCMS' main python file.
It can be run with the arguments:
    new - this makes
"""

import sys
import os
import make_post, preview, gen_html

def posts_iterate():
    """Iterate through posts and get their information"""
    def get_post_folders():
        postFolderList = []

        for dirpath, dnames, fnames in os.walk("../posts"):
            for d in dnames:
                if dirpath == "../posts":
                    folder = "../posts" + slashChar + d + slashChar
                    postFolderList.append(folder)

        postFolderList.sort()
        return postFolderList

    postFolders = get_post_folders()

    for folder in postFolders:
        postNum = folder.split(slashChar)[-2]
        directory = os.path.realpath(folder) + slashChar
        contentLocation = directory + "content.txt"

        if os.path.isfile(contentLocation):
            with open(contentLocation) as post:
                postContent = post.readlines()
                postData = parse.post_parser(postContent)
        else:
            print("Excluding post " + postNum + " due to lack of a content.txt.")

def os_specifics():
    """OS-specific stuff"""
    slashChar = "/"
    if os.name == "nt":
        slashChar = "\\"
    #print("OS is detected as", os.name)

    return slashChar

def get_site_details():
    """Find necessary site details from siteDetails.txt"""
    with open("siteDetails.txt", "r") as detailsFile:
        details = detailsFile.readlines()
        siteName = details[0]
        siteCategories = details[2:-1]
        siteCategories = [cat.strip() for cat in siteCategories]
        
        return (siteName, siteCategories)

if __name__ == "__main__":
    slashChar = os_specifics()
    pythonFileLocation = os.path.dirname(os.path.realpath(__file__)) + slashChar

    (siteName, siteCategories) = get_site_details()

    if len(sys.argv) > 1:
        args = sys.argv[1:]

        if "new" in args:
            print("New post")
            post = make_post.newPost(siteName, siteCategories)
            post = preview.gen_preview(post)

            if post.isVisible:
                gen_html.gen(post)

        if "update" in args:
            print("Updating")
            posts_iterate()

        if not "new" in args and not "update" in args: # Unrecognised arguments
            print("\nUnrecognised arguments given. Give arguments:\n  \"new\" to make a new post\n  \"update\" to generate all posts and the front page")
            sys.exit("Unrecognised arguments. Exited.")

    else: # If no arguments given
        print("\nNo arguments given. Give arguments:\n  \"new\" to make a new post\n  \"update\" to generate all posts and the front page")
        sys.exit("No arguments given. Exited.")

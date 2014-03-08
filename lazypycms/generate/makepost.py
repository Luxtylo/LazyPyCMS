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

import tkinter as tk

class Post():
    def __init__(self):
        self.title = None
        self.postDate = None
        self.time = None
        self.visibility = None
        self.headerImage = None
        self.contents = None
        self.html = None
        self.preview = None
        self.tag = None

class PostMaker:
    def __init__(self, siteName, categories):
        self.siteName = siteName
        self.post = Post()

        self.postTags = categories

        self.post_write_ui()
    
    def post_write_ui(self):
        self.root = tk.Tk()
        self.root.wm_title("New post on " + self.siteName)

        self.postTag = tk.StringVar()
        self.postTag.set(self.postTags[0]) # Set default tag to first supplied

        # Row 0
        row0Frame = tk.Frame(self.root)
        row0Frame.pack(fill=tk.X, expand=0)

        titleLabel = tk.Label(row0Frame, text="Title:", width=5)
        titleLabel.pack(side=tk.LEFT, expand=0)

        titleBox = tk.Entry(row0Frame)
        titleBox.pack(side=tk.RIGHT, fill=tk.X, expand=1)

        # Row 1
        row1Frame = tk.Frame(self.root)
        row1Frame.pack(fill=tk.X, expand=0)

        imgLocSel = tk.Button(row1Frame, text="Select Image")
        imgLocSel.pack(side=tk.LEFT, expand=0)

        imgLocBox = tk.Entry(row1Frame)
        imgLocBox.pack(side=tk.RIGHT, expand=1, fill=tk.X)

        # Row 2
        row2Frame = tk.Frame(self.root)
        row2Frame.pack(fill=tk.X, expand=0)

        postLabel = tk.Label(row2Frame, text="Post:", width=5)
        postLabel.pack(side=tk.LEFT, expand=0)

        visibleCheck = tk.Checkbutton(
                row2Frame,
                text="Visible",
                variable = self.post.visibility)
        visibleCheck.pack(side=tk.RIGHT, expand=0)

        # Row 3
        postBox = tk.Text(self.root)
        postBox.pack(expand=1, fill=tk.BOTH)

        # Row 4
        row3Frame = tk.Frame(self.root)
        row3Frame.pack(fill=tk.X, expand=0)

        tagLabel = tk.Label(row3Frame, text="Category:", width=8)
        tagLabel.pack(side=tk.LEFT)

        tagSelect = tk.OptionMenu(
                row3Frame,
                self.postTag,
                *self.postTags)
        tagSelect.pack(side=tk.LEFT, fill=tk.X)

        submitButton = tk.Button(
                row3Frame,
                text="Submit",
                command=self.extract_post)
        submitButton.pack(side=tk.RIGHT)

        self.root.mainloop()

    def extract_post(self):
        pass

categories = ["None", "Design", "Photography", "Programming", "Videography"]
post = PostMaker("gbryant.co.uk", categories)

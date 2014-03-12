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
from datetime import datetime

class Post():
    def __init__(self):
        self.title = None
        self.postTime = None
        self.isVisible = None
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
        """UI for writing post"""
        self.root = tk.Tk()
        self.root.wm_title("New post on " + self.siteName)

        self.postTag = tk.StringVar()
        self.postTag.set(self.postTags[0]) # Set default tag to first supplied

        # Row 0
        self.row0Frame = tk.Frame(self.root)
        self.row0Frame.pack(fill=tk.X, expand=0)

        self.titleLabel = tk.Label(self.row0Frame, text="Title:", width=5)
        self.titleLabel.pack(side=tk.LEFT, expand=0)

        self.titleBox = tk.Entry(self.row0Frame)
        self.titleBox.pack(side=tk.RIGHT, fill=tk.X, expand=1)

        # Row 1
        self.row1Frame = tk.Frame(self.root)
        self.row1Frame.pack(fill=tk.X, expand=0)

        self.imgLocSel = tk.Button(self.row1Frame, text="Select Image")
        self.imgLocSel.pack(side=tk.LEFT, expand=0)

        self.imgLocBox = tk.Entry(self.row1Frame)
        self.imgLocBox.pack(side=tk.RIGHT, expand=1, fill=tk.X)

        # Row 2
        self.row2Frame = tk.Frame(self.root)
        self.row2Frame.pack(fill=tk.X, expand=0)

        self.postLabel = tk.Label(self.row2Frame, text="Post:", width=5)
        self.postLabel.pack(side=tk.LEFT, expand=0)

        self.postVisible = tk.IntVar()
        self.visibleCheck = tk.Checkbutton(
                self.row2Frame,
                text="Visible",
                variable = self.postVisible)
        self.visibleCheck.pack(side=tk.RIGHT, expand=0)

        # Row 3
        self.postBox = tk.Text(self.root)
        self.postBox.pack(expand=1, fill=tk.BOTH)

        # Row 4
        self.row3Frame = tk.Frame(self.root)
        self.row3Frame.pack(fill=tk.X, expand=0)

        self.tagLabel = tk.Label(self.row3Frame, text="Category:", width=8)
        self.tagLabel.pack(side=tk.LEFT)

        self.tagSelect = tk.OptionMenu(
                self.row3Frame,
                self.postTag,
                *self.postTags)
        self.tagSelect.pack(side=tk.LEFT, fill=tk.X)

        self.submitButton = tk.Button(
                self.row3Frame,
                text="Submit",
                command=self.extract_post)
        self.submitButton.pack(side=tk.RIGHT)

        self.root.mainloop()

    def extract_post(self):
        """Get the post's information from the UI and add it to the object"""
        self.post.title = self.titleBox.get()
        self.post.headerImage = self.imgLocBox.get()
        self.post.contents = self.postBox.get("1.0", tk.END)[:-1]
        self.post.tag = self.postTag.get()

        if self.postVisible.get() == 1:
            self.post.isVisible = True
        else:
            self.post.isVisible = False

        self.post.postTime = datetime.now()

        self.root.destroy()

def newPost(siteName, categories):
    """Create a new post using the post creation UI"""
    makePost = PostMaker(siteName, categories)
    try:
        post = makePost.post
        return post
    except AttributeError:
        return 0

if __name__ == "__main__":
    """Test newPost using a test siteName and categories"""
    siteName = "test.co.uk"
    categories = ["None", "Cat1", "Cat2", "Cat3"]
    newPost(siteName, categories)

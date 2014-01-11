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

import os
import subprocess


def osSpecifics():
    slashChar = "/"
    if os.name == "nt":
        slashChar = "\\"
    print("OS is detected as", os.name)

    return slashChar

slashChar = osSpecifics()
pythonFileLocation = os.path.dirname(os.path.realpath(__file__)) + slashChar

postFolderList = []

for dirpath, dnames, fnames in os.walk("./posts"):
    for d in dnames:
        #print(dirpath)
        if dirpath == "./posts":
            folder = "./posts" + slashChar + d + slashChar
            postFolderList.append(folder)

postFolderList.sort()

for directory in postFolderList:
    imageFolder = directory + "images" + slashChar
    contents = directory + "contents.txt"
    prvwPngName = imageFolder + "previewImage.png"
    prvwJpgName = imageFolder + "previewImage.jpg"
    prvwImgResName = imageFolder + "previewImageResized.png"

    if os.path.isfile(prvwPngName):
        print("Preview image of", directory, "recognised as PNG")
        imgConvertCmd = [
            "convert",
            prvwPngName,
            "-resize",
            "512",
            prvwImgResName]
        subprocess.call(imgConvertCmd)
    elif os.path.isfile(prvwJpgName):
        print("Preview image of", directory, "recognised as JPG")
        imgConvertCmd = [
            "convert",
            prvwJpgName,
            "-resize",
            "512",
            prvwImgResName]
        subprocess.call(imgConvertCmd)
    else:
        print("Preview image of post", directory, "not recognised.")
        quit()

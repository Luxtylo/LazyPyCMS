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

import os
import subprocess
from math import ceil


def osSpecifics():
    slashChar = "/"
    if os.name == "nt":
        slashChar = "\\"
    print("OS is detected as", os.name)

    return slashChar

def getPosts():
    postFolderList = []

    for dirpath, dnames, fnames in os.walk("./posts"):
        for d in dnames:
            #print(dirpath)
            if dirpath == "./posts":
                folder = "./posts" + slashChar + d + slashChar
                postFolderList.append(folder)

    postFolderList.sort()
    return postFolderList

def convertImages(postFolderList):
    print("\nConverting post preview images")
    for directory in postFolderList:
        imageFolder = directory + "images" + slashChar
        contents = directory + "contents.txt"
        prvwPngName = imageFolder + "previewImage.png"
        prvwJpgName = imageFolder + "previewImage.jpg"
        prvwImgResName = imageFolder + "previewImageResized.png"

        if os.path.isfile(prvwPngName):
            if not os.path.isfile(prvwImgResName):
                print("  Preview image of", directory, "recognised as PNG and converted")
                imgConvertCmd = [
                    "convert",
                    prvwPngName,
                    "-resize",
                    "512",
                    prvwImgResName]
                subprocess.call(imgConvertCmd)
            else:
                print("  Preview image of",directory,"already converted")
        elif os.path.isfile(prvwJpgName):
            if not os.path.isfile(prvwImgResName):
                print("  Preview image of", directory, "recognised as JPG and converted")
                imgConvertCmd = [
                    "convert",
                    prvwJpgName,
                    "-resize",
                    "512",
                    prvwImgResName]
                subprocess.call(imgConvertCmd)
            else:
                print("  Preview image of",directory,"already converted")
        else:
            print("\nError:\n  Preview image of post", directory, "not recognised.")
            quit()

        # Should use pngcrush here

    print("Preview images successfully converted")

def generatePostPages(postFolderList):
    print("\nGenerating post pages")

    def shortenPost(postContents):
        lineMaxLength = 92
        maxPreviewLines = 6

        previewList = []

        lineNum = 1
        for line in postContents:
            if lineNum < maxPreviewLines:
                if len(line) < lineMaxLength:
                    if line != "\n":
                        linesTakenByLine = 1
                        addToPreview = line
                        print("singleLine\n  " + addToPreview)
                else:
                    linesTakenByLine = round(len(line)/lineMaxLength, 0)
                    linesLeft = maxPreviewLines - lineNum

                    if linesLeft >= linesTakenByLine:
                        addToPreview = line
                        print("multiline\n  " + addToPreview)
                    else:
                        truncatePoint = int(linesLeft * lineMaxLength * 0.9)
                        lineTruncated = line[:truncatePoint]
                        addToPreview = ".".join(lineTruncated.split(".")[:-1])
                        print("multitrunc\n  " + addToPreview)

                previewList.append(addToPreview)
                lineNum += linesTakenByLine
            else:
                break

    def generateMainPage():
        pass

    for directory in postFolderList:
        postsDir = os.path.dirname(os.path.realpath(__file__))
        postsDir += slashChar + "posts" + slashChar
        currentPost = directory.split(slashChar)[-2] + slashChar
        imageDir = postsDir + currentPost + "images" + slashChar
        content = postsDir + currentPost + "content.txt"

        if os.path.isfile(content):
            print("  Generating static page for", directory)
            with open(content) as postFile:
                post = postFile.readlines()

                imageTag = "<|--Post image--|>\n"
                postTag = "<|--Begin Post--|>\n"

                if imageTag in post:
                    imageLine = post.index(imageTag) + 2
                else:
                    print("\nError:\n  Image line not found in", directory)
                    quit()

                if postTag in post:
                    postStartLine = post.index(postTag) + 1
                else:
                    print("\nError:\n  Post line not found in", directory)
                    quit()

                metadata = []
                postContents = []

                lineNum = 1
                for line in post:
                    if lineNum < (imageLine - 1):
                        metadata.append(line[:-1])
                    elif lineNum == imageLine:
                        imageLocation = "images/" + line
                    elif lineNum > postStartLine:
                        postContents.append(line[:-1])
                    lineNum += 1

                timeList = metadata[1].split("-")
                time = metadata[2].split(":")
                postTime = {
                    "year": timeList[0],
                    "month": timeList[1],
                    "day": timeList[2],
                    "hour": time[0],
                    "minute": time[1]}

                title = metadata[0]
                visibility = metadata[3]

                postPreview = shortenPost(postContents)
                # Useful things: title, visibility, postTime, postContents, imageLocation
        else:
            print("content.txt not found in", directory)

slashChar = osSpecifics()
pythonFileLocation = os.path.dirname(os.path.realpath(__file__)) + slashChar

postFolderList = getPosts()

convertImages(postFolderList)
generatePostPages(postFolderList)

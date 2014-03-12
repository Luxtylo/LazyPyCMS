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

def gen_preview(post):
    """Generates a preview of the post"""
    contents = post.contents.split("\n")

    lineMaxLength = 92
    maxPreviewLines = 6

    previewList = []

    lineNum = 1
    for line in contents:
        if lineNum < maxPreviewLines:
            if len(line) < lineMaxLength:
                if line != "\n":
                    linesTakenByLine = 1
                    addToPreview = line
                    #print("singleLine\n  " + addToPreview)
            else:
                linesTakenByLine = round(len(line)/lineMaxLength, 0)
                linesLeft = maxPreviewLines - lineNum

                if linesLeft >= linesTakenByLine:
                    addToPreview = line
                    #print("multiline\n  " + addToPreview)
                else:
                    truncatePoint = int(linesLeft * lineMaxLength * 0.9)
                    lineTruncated = line[:truncatePoint]
                    addToPreview = ".".join(lineTruncated.split(".")[:-1])
                    #print("multitrunc\n  " + addToPreview)

            previewList.append(addToPreview)
            lineNum += linesTakenByLine
        else:
            break

    preview = "\n".join(previewList)

    post.preview = preview
    return post

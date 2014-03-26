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

from make_post import Post
from datetime import datetime

def gen(post):
    """Generate HTML from the post passed to it"""
    def initial_layout():
        textList = []
        
        in_paragraph = False

        for inputLine in contents:
            # Paragraphs
            if inputLine != "" and not in_paragraph:
                textList.append("<p>" + inputLine)
                in_paragraph = True
            elif inputLine != "" and in_paragraph:
                textList.append("<br/>" + inputLine)
            elif inputLine == "" and in_paragraph:
                textList.append("</p>")
                in_paragraph = False
        
        # Close final paragraph
        if in_paragraph:
            textList.append("</p>")
            in_paragraph = False

        return textList

    def formatting_tags(textList):
        in_italics = False
        in_bold = False

        for lineIndex, line in enumerate(textList):
            line = list(line)
            tempLine = list()

            for index, char in enumerate(line):
                newChar = char

                if char == "*":
                    try:
                        nextChar = line[index + 1]
                    except IndexError:
                        nextChar = None

                    # Italics
                    if nextChar != "*":
                        if not in_italics:
                            newChar = "<i>"
                            in_italics = True
                            print("Italicised")
                        else:
                            newChar = "</i>"
                            in_italics = False
                            print("De-italicised")

                    # Bold
                    elif nextChar == "*":
                        if not in_bold:
                            newChar = "<b>"
                            in_bold = True
                            line[index + 1] = ""
                            print("Bolded")
                        else:
                            newChar = "</b>"
                            in_bold = False
                            line[index + 1] = ""
                            line[index] = ""
                            print("De-bolded")

                if newChar != "":
                    tempLine.append(newChar)
            
            # Cleaning up unclosed tags
            if in_italics:
                tempLine.append("</i>")
                in_italics = False

            textList[lineIndex] = "".join(tempLine)

        return textList

    def special_chars(finalList):
        pass

    def join_list(finalList):
        for lineIndex, line in enumerate(finalList):
            finalList[lineIndex] = "".join(line)
        return "".join(finalList)

    contents = post.contents.split("\n")

    layout = initial_layout()
    formatting = formatting_tags(layout)
    finalHTML = join_list(formatting)
    print(finalHTML)

def testRun():
    """Test HTML generation using a test post"""
    testPost = Post()
    testPost.title = "Test"
    testPost.postTime = datetime(2014, 3, 24, 16, 10, 21, 493135)
    testPost.isVisible = True
    testPost.headerImage = "HEADERIMG.jpg"
    testPost.tag = "Photography"
    testPost.made = True
    testPost.contents = """Hello.

This is a post.
This is a **very good** post.
Here are *some italics*"""

    gen(testPost)

if __name__ == "__main__":
    testRun()

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
import os

def gen(post, debug=False):
    """Generate HTML from the post passed to it"""
    def initial_layout():
        textList = []
        
        in_paragraph = False

        for inputLine in contents:
            # Paragraphs
            if inputLine != "" and not in_paragraph:
                textList.append("\n<p>")
                textList.append("\n" + inputLine)
                in_paragraph = True
            elif inputLine != "" and in_paragraph:
                textList.append("\n<br/>")
                textList.append("\n" + inputLine)
            elif inputLine == "" and in_paragraph:
                textList.append("\n</p>")
                in_paragraph = False
        
        # Close final paragraph
        if in_paragraph:
            textList.append("\n</p>")
            in_paragraph = False

        return textList

    def formatting_tags(textList):
        first_char = True
        in_italics = False
        in_bold = False
        in_underline = False
        in_ul = False
        in_code = False
        in_quote = False

        for lineIndex, line in enumerate(textList, 0):
            line = list(line)
            tempLine = list()

            for index, char in enumerate(line, 0):
                if index == 0:
                    first_char = True
                elif index == 1 and line[index-1] == "\n":
                    first_char == True
                else:
                    first_char = False

                newChar = char

                try:
                    nextChar = line[index + 1]
                except IndexError:
                    nextChar = None

                try:
                    prevChar = line[index - 1]
                except IndexError:
                    prevChar = None

                if char == "*":
                    # Bullet points (ie <ul>s)
                    if nextChar == " " and first_char:
                        if not in_ul:
                            newChar = "<ul>\n<li>"
                            in_ul = True
                            line[index + 1] = ""
                        else:
                            newChar = "<li>"
                            line[index + 1] = ""

                        tempLine.append(newChar)

                    # Bold
                    elif nextChar == "*" and nextChar != " ":
                        if not in_bold:
                            newChar = "<b>"
                            in_bold = True
                            line[index + 1] = ""
                        else:
                            newChar = "</b>"
                            in_bold = False
                            line[index + 1] = ""

                        tempLine.append(newChar)

                    # Italics
                    else:
                        if prevChar != "\\":
                            if not in_italics:
                                newChar = "<i>"
                                in_italics = True
                            elif in_italics:
                                newChar = "</i>"
                                in_italics = False
                        else:
                            del tempLine[-1]
                            newChar = "*"

                        tempLine.append(newChar)

                # Quotes
                elif char == ">" and first_char:
                    if not in_quote:
                        newChar = "<blockquote>"
                        in_quote = True
                    else:
                        newChar = ""
                    
                    tempLine.append(newChar)

                # Underlining
                elif char == "_":
                    if not in_underline and prevChar == " ":
                        newChar = "<u>"
                        in_underline = True
                    elif in_underline and nextChar == " " and prevChar != "\\":
                        newChar = "</u>"
                        in_underline = False
                    else:
                        if prevChar == "\\":
                            del tempLine[-1]
                        newChar = "_"

                    tempLine.append(newChar)
                
                # Headings
                elif char == "=":
                    if first_char:
                        textList[lineIndex-3] = ""
                        textList[lineIndex-2] = "\n<h4>" + textList[lineIndex-2][1:] + "</h4>\n<p>"
                        textList[lineIndex-1], textList[lineIndex], textList[lineIndex+1] = "", "", ""
                        if textList[lineIndex+2].startswith("\n"):
                            textList[lineIndex+2] = textList[lineIndex+2][1:]
                    elif prevChar == "\\":
                        del tempLine[-1]
                        tempLine.append("=")

                # Code tags
                elif char == "`":
                    if not in_code and prevChar != "\\":
                        newChar = "<code>"
                        in_code = True
                    elif in_code and prevChar != "\\":
                        newChar = "</code>"
                        in_code = False
                    else:
                        del tempLine[-1]
                        newChar = "`"

                    tempLine.append(newChar)

                else:
                    if newChar != "":
                        tempLine.append(newChar)

                # Close unclosed <ul>s, <li>s and <blockquote>s
                if index == len(line)-1:
                    if in_ul or in_quote:
                        try:
                            nextLine = textList[lineIndex+1]
                        except:
                            nextLine = []

                        try:
                            lineAfterNext = textList[lineIndex+2]
                        except:
                            lineAfterNext = []

                        lineBreak = list("\n<br/>")
                        listElement = "*"
                        quoteMarker = ">"

                    if in_ul:
                        try:
                            if nextLine[1] == listElement and nextLine[2] == " ":
                                continuingList = True
                            elif lineAfterNext[1] == listElement and lineAfterNext[2] == " ":
                                continuingList = True
                            else:
                                continuingList = False
                        except IndexError:
                            continuingList = False

                        if line != lineBreak and continuingList:
                            tempLine.append("</li>")
                        elif line != lineBreak:
                            tempLine.append("</li>\n</ul>")
                            in_ul = False
                        else:
                            tempLine = ""

                    elif in_quote:
                        try:
                            if nextLine[1] == quoteMarker and nextLine[2] == " ":
                                continuingQuote = True
                            elif lineAfterNext[1] == quoteMarker and lineAfterNext[2] == " ":
                                continuingQuote = True
                            else:
                                continuingQuote = False
                        except IndexError:
                            continuingQuote = False

                        if tempLine[1] == "" and tempLine[2] == " ":
                            tempLine = tempLine[3:]
                            tempLine.insert(0, "\n")

                        if line != lineBreak and continuingQuote:
                            tempLine.append("<br/>")
                        elif line != lineBreak:
                            tempLine.append("</blockquote>")
                            in_quote = False
                        elif line == lineBreak:
                            tempLine = ""

            # Cleaning up unclosed tags
            if in_italics:
                tempLine.append("</i>")
                in_italics = False

            if in_bold:
                tempLine.append("</b>")
                in_bold = False

            if tempLine != []:
                textList[lineIndex] = "".join(tempLine)

        return textList

    def special_chars(finalList):
        pass

    def join_list(finalList):
        for lineIndex, line in enumerate(finalList):
            if line != "":
                finalList[lineIndex] = "".join(line)
        return "".join(finalList)

    def get_templates():
        try:
            with open("../templates/testTemplate", "r") as testTemplate:
                template = testTemplate.read()
        except FileNotFoundError:
            template = None
        
        templateDict = {"test": template}
        
        return templateDict

    contents = post.contents.split("\n")
    number = post.number
    postNumString = str(number).zfill(4)

    layout = initial_layout()
    formatting = formatting_tags(layout)
    HTML = join_list(formatting)

    templates = get_templates()

    if debug:
        finalHTML = templates["test"].format(title=post.title, contents=HTML)
        with open("test.html", "w+") as testPost:
            testPost.write(finalHTML)
    else:
        finalHTML = templates["test"].format(title=post.title, contents=HTML)
        directory = "../posts/" + postNumString + "/"
        HTMLLocation = directory + postNumString + ".html"

        with open(HTMLLocation, "w+") as HTMLFile:
            HTMLFile.write(finalHTML)

    return finalHTML

def testRun():
    """Test HTML generation using a test post"""
    testPost = Post()
    testPost.title = "Test post please ignore."
    testPost.postTime = datetime(2014, 3, 24, 16, 10, 21, 493135)
    testPost.isVisible = True
    testPost.headerImage = "HEADERIMG.jpg"
    testPost.tag = "Photography"
    testPost.made = True
    testPost.number = 2
    testPost.contents = """Hello.

This is a post.
This is a **very good** post.
Here are *some italics* - So there.

A list:
* Blah
* Bloh
* Bluh

More _things_ go here. Underlines_in_middle_of_word
Escaped \*asterisk and \_underscore

Code
=
This is some code:
`Code here
Bwup
Bwop`

A famous quote
=
Here is a famous quote said by Mr Dude
>I am Mr Dude
> That is my name
> Now go away
What an insightful quote"""

    html = gen(testPost, True)
    #print(repr(html))

if __name__ == "__main__":
    testRun()

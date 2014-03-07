#Planning LazyPyCMS
##General goal
Generate a static blog site from individual post files.

##Rough overview
###Generating individual post
* new_post - Runs other post-writing functions
* post_write_ui - GUI in which post is written. Includes file manager for inserting image files.
* extract_post - Gets the post data from write_post
* save_post - Adds post (including images) in a new folder in the posts/ directory
* Optionally, can run img_compress and gen_html from next section to generate the post when it is first written.
###Generating blog
* posts_iterate - Iterate through posts in the posts/ directory, and call post_parser and gen_html each post which has not already been generated. Also should make list of posts in date order and pass it to gen_frontpage
* post_parser - Parses post file and returns object containing the post's information. Call img_compress to compress post's images
* img_compress - Takes post location as argument and resizes and compresses the images for web using Imagemagick and PNGCrush
* gen_html - Take object containing post's information and create html file for each post it is passed
* gen_frontpage - Takes list of posts in date order, gets their summaries and generates a front page from them

##More detailed function plan
class new_post:
    contains extract_post, save_post, post_write_ui
    def post_write_ui - starts post UI - text box, "insert image" button
    def extract_post - runs post_parser, then save_post
    def save_post - saves post data in new folder in posts/. Can also run img_compress and gen_html if box is checked (on by default)

posts_iterate:
    Uses os module to go through all post folders in posts/
    For each folder, gets post location and post contents
    Runs post_parser on post contents, then runs gen_html using this.
    Passes post location to img_compress
    Appends post contents to list
    After iterating through all posts, runs gen_frontpage on posts content list

post_parser
    Gets passed post contents, and parses them, creating a dict with:
        Post title, date, time, visibility, image, contents, preview

gen_html
    Parses post contents and generates HTML from this
    iterate - iterates through post line by line and char by char. Runs other functions and sets variables. Builds up list of html, which is then joined to make the html file.

img_compress
    Iterates through posts' images, running imagemagick to resize them and pngcrush to compress them. Posts' main images are left larger than the images contained in the posts.

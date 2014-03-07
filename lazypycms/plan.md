Planning LazyPyCMS
==================
General goal
------------
Generate a static blog site from individual post files.

Rough overview
--------------
* posts_iterate - Iterate through posts in the posts/ directory, and call post_parser and gen_html each post which has not already been generated. Also should make list of posts in date order and pass it to gen_frontpage
* post_parser - Parses post file and returns object containing the post's information. Call img_compress to compress post's images
* img_compress - Takes post location as argument and resizes and compresses the images for web using Imagemagick and PNGCrush
* gen_html - Take object containing post's information and create html file for each post it is passed
* gen_frontpage - Takes list of posts in date order, gets their summaries and generates a front page from them

from tumblrbotbegone.utils import tumblr_client
from .tumblr_api_classes import BlogInfo, Post
from .bot_detectors import is_it_a_silent_fella, is_it_a_one_trick_pony

def is_it_a_bot(blogname):
    client = tumblr_client()
    blog_info_and_posts = client.posts(blogname, filter="text")

    blog_info = BlogInfo(blog_info_and_posts)
    posts = []
    
    for post in blog_info_and_posts["posts"]:
        posts.append(Post(post))



    output = ""

    for bot_name, bot_func in [["silent fella", is_it_a_silent_fella], ["one trick pony", is_it_a_one_trick_pony]]:
        output += f"Checking for {bot_name}...<br>"
        info, chance = bot_func(blog_info, posts)
        output += "<br>".join(info) + "<br><br>"

    

    return output



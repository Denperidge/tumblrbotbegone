from ..tumblr_api_classes import BlogInfo
from .utils import check_for_bot, has_default_avatar, has_default_header, has_no_posts, has_default_ask_page_title, has_no_description, has_no_blog_title

def is_it_a_silent_fella(blog_info: BlogInfo, posts: list):
    return check_for_bot(
        blog_info,
        posts,
        "silent fella",
        [has_default_avatar,has_default_header, has_no_posts, has_default_ask_page_title, has_no_description,has_no_blog_title]
    )

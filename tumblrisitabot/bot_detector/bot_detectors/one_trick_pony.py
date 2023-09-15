from re import match

from .utils import check_for_bot, has_no_description, has_default_ask_page_title, has_default_header, has_low_post_number, has_only_suspicious_posts
from ..tumblr_api_classes import BlogInfo

def is_it_a_one_trick_pony(blog_info: BlogInfo, posts: list):
    return check_for_bot(
        blog_info,
        posts,
        "one trick pont",
        [has_no_description, has_default_ask_page_title, has_default_header, has_low_post_number, has_only_suspicious_posts]
    )
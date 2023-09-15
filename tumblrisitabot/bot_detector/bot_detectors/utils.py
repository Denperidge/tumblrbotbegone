from re import match

from ..tumblr_api_classes import BlogInfo, Post

def check_for_bot(blog_info: BlogInfo, posts: list, bot_type_name: str, checks: list):
    total_signs = 0
    found_signs = 0
    output = []

    for check in checks:
        total_signs += 1
        output, found_signs = check(blog_info, posts, output, found_signs)
    
    chance = found_signs * 100 / total_signs
    output.append(f"{chance}% chance for a {bot_type_name}")

    return output, chance

def check(condition, text, output: list, found_signs: int):
    if condition:
        found_signs += 1
        output.append(text)
    
    return output, found_signs


# Text/customisation
def has_no_blog_title(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    return check(
        blog_info.title == "Untitled", 
        f"Default blog title (display/non-url name) ({blog_info.title})", 
        output, found_signs)

def has_no_description(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    return check(
        blog_info.description == "", 
        f"Default description (\"{blog_info.description}\")", 
        output, found_signs)


def has_default_ask_page_title(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    return check(
        blog_info.ask_page_title == "Ask me anything",
        f"Default ask page title ({blog_info.ask_page_title})", 
        output, found_signs)


# Theme/visual
def has_default_avatar(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    for avatar in blog_info.avatar:
        if avatar["url"].startswith("https://assets.tumblr.com/images/default_avatar"):
            found_signs += 1
            output.append(f"Avatar url is a default ({avatar['url']})")
            break
    return output, found_signs

def has_default_header(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    return check(
        blog_info.theme["header_image"].startswith("https://assets.tumblr.com/images/default_header/"),
        f"Default header ({blog_info.theme['header_image']})",
        output,
        found_signs)


# Posts
def has_no_posts(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    return check(
        blog_info.posts == 0,
        f"No posts (Post count: {blog_info.posts})", 
        output, 
        found_signs)

def has_low_post_number(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    return check(
        blog_info.posts < 5,
        f"Low number of posts ({blog_info.posts})", 
        output, 
        found_signs)

def has_only_suspicious_posts(blog_info: BlogInfo, posts: list, output: list, found_signs: int):
    only_suspicious_posts = True
    the_same_url = None
    for post in posts:
        post: Post = post

        url = match(r"http[^ ]+", post.body)
        if the_same_url is None:
            the_same_url = url
        else:
            if the_same_url != url:
                only_suspicious_posts = False
                output.append(f"Posts with differing links found (First post: {the_same_url} --- Second post: {url})")
                break

        if len(post.tags) != 0:
            only_suspicious_posts = False
            output.append(f"Post with multiple tags found: ({', '.join(post.tags)})")
            break

    if only_suspicious_posts:
        found_signs += 1
        output.append("Only suspicious posts found")
    
    return output, found_signs
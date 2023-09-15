from tumblrbotbegone.utils import tumblr_client

from re import match

from json import dumps

class BlogInfo():
    def __init__(self, blogDict) -> None:
        blogDict = blogDict["blog"]

        self.ask: bool = blogDict["ask"]
        self.ask_anon: bool = blogDict["ask_anon"]
        self.ask_page_title: str = blogDict["ask_page_title"]
        self.asks_allow_media: bool = blogDict["asks_allow_media"]
        self.avatar: list = blogDict["avatar"]
        """The dict consists of dicts with width, height & url properties"""
        self.can_chat: bool = blogDict["can_chat"]
        self.can_subscribe: bool = blogDict["can_subscribe"]
        self.description: str = blogDict["description"]
        self.is_nsfw: bool = blogDict["is_nsfw"]
        self.name: str = blogDict["name"]
        self.posts: int = blogDict["posts"]
        self.share_likes: bool = blogDict["share_likes"]
        self.subscribed: bool = blogDict["subscribed"]
        self.theme: dict = blogDict["theme"]
        self.title: str = blogDict["title"]
        self.total_posts: int = blogDict["total_posts"]
        self.updated: int = blogDict["updated"]
        self.url: str = blogDict["url"]
        self.uuid: str = blogDict["uuid"]

class Post():
    def __init__(self, postDict) -> None:
        self.type: str = postDict["type"]
        self.is_blocks_post_format: bool = postDict["is_blocks_post_format"]
        self.blog_name: str = postDict["blog_name"]
        self.blog: dict = postDict["blog"],
        self.id: int = postDict["id"]
        """This might give issues IF an id on tumblr can start with 0. Use id_string if in doubt"""
        self.id_string: str = postDict["id_string"]
        self.is_blazed: bool = postDict["is_blazed"]
        self.is_blaze_pending: bool = postDict["is_blaze_pending"]
        self.can_blaze: bool = postDict["can_blaze"]
        self.post_url: str = postDict["post_url"]
        self.slug: str = postDict["slug"]
        self.date: str = postDict["date"]
        self.timestamp: int = postDict["timestamp"]
        self.state: str = postDict["state"]
        self.format: str = postDict["format"]
        self.reblog_key: str = postDict["reblog_key"]
        self.tags: list = postDict["tags"]
        self.short_url: str = postDict["short_url"]
        self.summary: str = postDict["summary"]
        self.should_open_in_legacy: bool = postDict["should_open_in_legacy"]
        self.recommended_source = postDict["recommended_source"]
        self.recommended_color = postDict["recommended_color"]
        self.note_count: int = postDict["note_count"]
        self.title: str = postDict["title"]
        self.body: str = postDict["body"]
        self.reblog: dict = postDict["reblog"]

def is_it_a_silent_fella(blog_info: BlogInfo, posts: list):
    TOTAL_SIGNS = 5
    found_signs = 0
    output = []

    # sign 1: default avatar
    for avatar in blog_info.avatar:
        if avatar["url"].startswith("https://assets.tumblr.com/images/default_avatar"):
            found_signs += 1
            output.append(f"Avatar url is a default ({avatar['url']})")
            break
    
    # Sign 2: default header
    if blog_info.theme["header_image"].startswith("https://assets.tumblr.com/images/default_header/"):
        found_signs += 1
        output.append("Default header")
    
    # sign 3: no posts
    if blog_info.posts == 0:
        found_signs += 1
        output.append(f"No posts (Post count: {blog_info.posts})")
    
    # sign 4: default Ask
    if blog_info.ask_page_title == "Ask me anything":
        found_signs += 1
        output.append(f"Default ask page title ({blog_info.ask_page_title})")
    
    # sign 5: no description
    if blog_info.description == "":
        found_signs += 1
        output.append(f"No description ('{blog_info.description}')")
    
    # sign 6: no blog title (display/non-url name)
    if blog_info.title == "Untitled":
        found_signs += 1
        output.append(f"Default blog title (display/non-url name) ({blog_info.title})")

    chance = found_signs * 100 / TOTAL_SIGNS
    output.append(f"{chance}% chance for a silent fella")

    return output, chance

def is_it_a_one_trick_pony(blog_info: BlogInfo, posts: list):
    TOTAL_SIGNS = 5
    found_signs = 0
    output = []

    if blog_info.ask_page_title == "Ask me anything":
        found_signs += 1
        output.append(f"Default ask page title")

    if blog_info.theme["header_image"].startswith("https://assets.tumblr.com/images/default_header/"):
        found_signs += 1
        output.append(f"Default header ({blog_info.theme['header_image']})")
    
    if blog_info.description == "":
        found_signs += 1
        output.append(f"Default description (\"{blog_info.description}\")")
    
    if blog_info.posts < 5:
        found_signs += 1
        output.append(f"Low number of posts ({blog_info.posts})")
    
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

    
    chance = found_signs * 100 / TOTAL_SIGNS
    output.append(f"{chance}% chance for a one trick pony")

    return output, chance

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
        output += "<br>".join(info) + "<br>"

    

    return output



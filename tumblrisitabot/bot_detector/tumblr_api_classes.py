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
        
        if hasattr(postDict, "title"):
            self.title: str = postDict["title"]
        else:
            self.title = ""
        if hasattr(postDict, "body"):
            self.body: str = postDict["body"]
        else:
            self.body = ""
        self.reblog: dict = postDict["reblog"]

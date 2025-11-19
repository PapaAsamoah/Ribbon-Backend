import os
import praw
from praw.models import MoreComments

def create_reddit_client():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )

def get_top_posts_with_comments(subreddit: str, limit: int = 50, max_comments: int = 10, time_filter: str = "day") -> list[dict]:
    reddit = create_reddit_client()
    sub = reddit.subreddit(subreddit)

    posts = []

    for post in sub.top(time_filter=time_filter, limit=limit):
        title = post.title or ""
        if len(title.split()) < 4:
            continue
        
        post_data = {
            "post_id": post.id,
            "title": title,
            "selftext": (post.selftext or "").strip(),
            "subreddit": subreddit,
            "author": str(post.author) if post.author else None,
            "score": int(post.score),
            #comes as float from praw
            "created_utc": int(post.created_utc),
            "url": post.url,
            "is_self": post.is_self,
            "num_comments": post.num_comments,
        }

        post.comment_sort = "top"

        top_comments = []

        for comment in post.comments[:max_comments]:
            # reddit makes comment objects for "load more" comments isinstance skips those
            if isinstance(comment, MoreComments):
                continue

            body_text = (comment.body or "").strip()
            if not body_text:
                continue

            top_comments.append({
                "body": body_text,
                "score": int(comment.score),
            })

        post_data["top_comments"] = top_comments
        post_data["cleaned_top_comment_count"] = len(top_comments)

        posts.append(post_data)

    return posts
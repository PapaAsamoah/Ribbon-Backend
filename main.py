from fastapi import FastAPI
from app.reddit_client import get_top_posts_with_comments
from app.supabase_client import upsert_posts, get_cleaned_posts

app = FastAPI()

@app.get("/api/sentiment")
def sentiment(subreddit: str = "wallstreetbets"):
    posts = get_top_posts_with_comments(
        subreddit=subreddit,
        limit=50,
        max_comments=5,
        time_filter="week"
    )

    upsert_posts(posts)

    cleaned = get_cleaned_posts()
    return cleaned
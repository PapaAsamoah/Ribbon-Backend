from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.reddit_client import get_top_posts_with_comments
from app.supabase_client import upsert_posts, get_cleaned_posts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

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
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

@app.get("/api/fetch_posts")
def fetch_posts(subreddit: str = "wallstreetbets", limit: int = 50):
    posts = get_top_posts_with_comments(subreddit=subreddit, limit=limit)
    upsert_result = upsert_posts(posts)
    return {"fetched_post_count": len(posts), "upsert_result": upsert_result}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/sentiment")
def sentiment(subreddit: str = "wallstreetbets"):
    cleaned: list[dict] = get_cleaned_posts()
    ticker_stats: dict[str, dict[str, float | int]] = {}

    for post in cleaned:
        tickers: list[str] = post.get("tickers", [])
        polarity: float = post.get("polarity", 0)

        for t in tickers:
            t = t.upper().strip()

            if t not in ticker_stats:
                ticker_stats[t] = {"count": 0, "sentiment_sum": 0}

            ticker_stats[t]["count"] += 1
            ticker_stats[t]["sentiment_sum"] += polarity

    results: list[dict[str, str | int | float]] = []

    for t, data in ticker_stats.items():
        avg: float = data["sentiment_sum"] / data["count"]
        results.append({
            "ticker": t,
            "mention_count": data["count"],
            "avg_sentiment": avg
        })

    results.sort(key=lambda x: (-x["mention_count"], -x["avg_sentiment"]))
    return results[:10]
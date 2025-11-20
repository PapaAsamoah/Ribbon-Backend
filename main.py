from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.reddit_client import get_top_posts_with_comments
from app.supabase_client import get_cleaned_posts, upsert_posts, get_raw_posts, save_cleaned_posts
from app.spacy_cleaner import process_post

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

@app.get("/api/reddit_load")
def load_reddit(subreddit: str = "wallstreetbets"):
    posts = get_top_posts_with_comments(subreddit=subreddit, limit=50, max_comments=10, time_filter="day")
    upsert_posts(posts)
    return {"inserted": len(posts)}

@app.get("/api/clean")
def clean():
    raw = get_raw_posts()
    cleaned_rows = []

    for post in raw:
        processed = process_post(post["title"] + " " + post["selftext"])
        cleaned_rows.append({
            "post_id": post["post_id"],
            "tickers": processed["tickers"],
            "polarity": processed["polarity"]
        })

    save_cleaned_posts(cleaned_rows)
    return {"cleaned": len(cleaned_rows)}

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
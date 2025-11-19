import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
sb = create_client(url, key)

def upsert_posts(rows):
    if not rows:
        return None

    data = []

    for r in rows:
        item = {}
        item["post_id"] = r["post_id"]
        item["title"] = r["title"]
        item["selftext"] = r["selftext"]
        item["created_utc"] = r["created_utc"]

        t = datetime.fromtimestamp(r["created_utc"], timezone.utc)
        item["created_at"] = t.isoformat()

        item["cleaned"] = False
        data.append(item)

    res = sb.table("reddit_posts").upsert(data).execute()
    return res.model_dump()

def get_cleaned_posts():
    query = (
        sb.table("reddit_posts_clean")
        .select("post_id, tickers, polarity, cleaned_at")
        .filter("tickers", "not.is", "null")
        .order("cleaned_at", desc=True)
    )

    res = query.execute()
    return res.data
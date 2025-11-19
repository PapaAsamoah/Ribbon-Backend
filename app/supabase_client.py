import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from supabase import create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(supabase_url, supabase_key)

def save_raw_posts(posts):
    if not posts:
        return None

    rows_to_save = []

    for post in posts:
        row = {}
        row["post_id"] = post["post_id"]
        row["title"] = post["title"]
        row["selftext"] = post["selftext"]
        row["created_utc"] = post["created_utc"]
        row["cleaned"] = False
        rows_to_save.append(row)

    result = supabase.table("reddit_posts").upsert(rows_to_save).execute()
    return result.model_dump()

def fetch_cleaned_posts():
    query = (
        supabase.table("reddit_posts_clean")
        .select("post_id, tickers, polarity, cleaned_at")
        .filter("tickers", "not.is", "null")
        .order("cleaned_at", desc=True)
    )

    response = query.execute()
    return response.data
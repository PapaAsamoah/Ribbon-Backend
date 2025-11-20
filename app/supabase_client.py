import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(supabase_url, supabase_key)

def get_raw_posts():
    response = (
        supabase.table("reddit_posts")
        .select("*")
        .eq("cleaned", False)
        .execute()
    )
    return response.data

def save_cleaned_posts(cleaned_rows):
    if not cleaned_rows:
        return None

    supabase.table("reddit_posts_clean").upsert(cleaned_rows, on_conflict="post_id").execute()

    ids = [row["post_id"] for row in cleaned_rows]
    supabase.table("reddit_posts").update({"cleaned": True}).in_("post_id", ids).execute()

def upsert_posts(posts):
    if not posts:
        return None

    rows_to_save = []

    for post in posts:
        row = {}
        row["post_id"] = post["post_id"]
        row["title"] = post["title"]
        row["selftext"] = post["selftext"]
        #row["created_utc"] = post["created_utc"]
        row["cleaned"] = False
        rows_to_save.append(row)

    result = supabase.table("reddit_posts").upsert(rows_to_save, on_conflict="post_id").execute()
    return result.model_dump()

def get_cleaned_posts():
    query = (
        supabase.table("reddit_posts_clean")
        .select("post_id, tickers, polarity, cleaned_at")
        .filter("tickers", "not.is", "null")
        .order("cleaned_at", desc=True)
    )

    response = query.execute()
    return response.data
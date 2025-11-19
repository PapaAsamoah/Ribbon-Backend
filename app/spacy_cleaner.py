import os
from dotenv import load_dotenv
import spacy
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
sb = create_client(SUPABASE_URL, SUPABASE_KEY)

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

def remove_urls(text):
    cleaned_words = []
    for word in text.split():
        if word.startswith("http") or word.startswith("www."):
            continue
        cleaned_words.append(word)
    return " ".join(cleaned_words)

def find_tickers(text):
    tickers = []
    for word in text.split():
        if word.startswith("$") and len(word) > 1 and word[1:].isalpha():
            tickers.append(word[1:].upper())
    return tickers

def replace_tickers(text):
    new_words = []
    for word in text.split():
        if word.startswith("$") and word[1:].isalpha():
            new_words.append("<TICKER>")
        else:
            new_words.append(word)
    return " ".join(new_words)

def remove_extra_spaces(text):
    return " ".join(text.split())

slang = {
    "stonk": "stock",
    "tendies": "profit",
    "yolo": "risky_trade",
    "hodl": "hold",
    "to the moon": "big_gain_expected",
    "ape": "retail_trader",
    "rocket": "bullish",
    "moon": "bullish",
    "fomo": "fear_missing_out"
}

def replace_slang(text):
    cleaned_text = text.lower()
    for word, replacement in slang.items():
        cleaned_text = cleaned_text.replace(word, replacement)
    return cleaned_text

def normalize_text(text):
    if not text:
        return "", []

    text = text.strip()
    tickers = find_tickers(text)

    cleaned = remove_urls(text)
    cleaned = replace_slang(cleaned)
    cleaned = replace_tickers(cleaned)
    cleaned = remove_extra_spaces(cleaned).lower()

    doc = nlp(cleaned)
    final_words = []

    for token in doc:
        if token.text == "<TICKER>":
            final_words.append("<TICKER>")
        elif token.is_alpha:
            final_words.append(token.lemma_)

    cleaned_text = " ".join(final_words)
    return cleaned_text, tickers

def get_sentiment(text):
    if not text:
        return 0
    doc = nlp(text)
    return doc._.blob.polarity

def process_post(text):
    cleaned_text, tickers = normalize_text(text)
    polarity = get_sentiment(cleaned_text)
    return {
        "cleaned_text": cleaned_text,
        "tickers": tickers,
        "polarity": polarity
    }
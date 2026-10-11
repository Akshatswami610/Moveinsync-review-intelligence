
from google_play_scraper import Sort, reviews
import pandas as pd
from pathlib import Path

# Output directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "moveinsync_reviews.csv"

# Collect public Google Play Store reviews
result, continuation_token = reviews(
    "com.moveinsync.ets",
    lang="en",
    country="in",
    sort=Sort.NEWEST,
    count=500
)

df = pd.DataFrame(result)

# Keep relevant fields when available
columns = [
    "score",
    "content",
    "at",
    "thumbsUpCount",
    "reviewId",
    "appVersion"
]

df = df[[column for column in columns if column in df.columns]]

# Remove duplicate reviews
if "reviewId" in df.columns:
    df = df.drop_duplicates(subset="reviewId")

# Save collected data
df.to_csv(OUTPUT_FILE, index=False)

print(f"Reviews collected: {len(df)}")
print(f"Saved to: {OUTPUT_FILE}")
print(df.head(10).to_string(index=False))

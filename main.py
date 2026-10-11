
from pathlib import Path
import re

import pandas as pd
import matplotlib.pyplot as plt


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "moveinsync_reviews.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# 1. Load and clean the reviews
def load_reviews():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"CSV not found: {DATA_FILE}\n"
            "Place moveinsync_reviews.csv inside the data folder."
        )

    data = pd.read_csv(DATA_FILE)

    required = {"score", "content", "at"}
    missing = required - set(data.columns)

    if missing:
        raise ValueError(f"Missing CSV columns: {missing}")

    if "reviewId" in data.columns:
        data = data.drop_duplicates(subset="reviewId")

    data["score"] = pd.to_numeric(data["score"], errors="coerce")
    data["at"] = pd.to_datetime(data["at"], errors="coerce")
    data["content"] = data["content"].fillna("").astype(str)

    data = data[data["score"].between(1, 5)].copy()
    data = data[data["at"].notna()].copy()

    return data


# 2. Define complaint categories
THEMES = {
    "Booking and scheduling": [
        r"\bbook\w*", r"\bschedul\w*", r"\bcancel\w*",
        r"\btrip\b", r"\bno.show\b"
    ],
    "GPS, ETA and tracking": [
        r"\bgps\b", r"\blocation\b", r"\btrack\w*",
        r"\beta\b", r"\broute\b", r"\bmap\b",
        r"\blate\b", r"\bdelay\w*"
    ],
    "App stability": [
        r"\bcrash\w*", r"\bfreez\w*", r"\bstuck\b",
        r"\bslow\b", r"\bnot opening\b", r"\bnot working\b"
    ],
    "Login and OTP": [
        r"\blogin\b", r"\bsign in\b", r"\botp\b",
        r"\bpassword\b"
    ],
    "Notifications": [
        r"\bnotification\w*", r"\balert\w*"
    ],
    "Transport and support": [
        r"\bdriver\w*", r"\bcab\b", r"\bshuttle\b",
        r"\btransport\b", r"\bsupport\b", r"\bcomplaint\w*"
    ],
    "UI and usability": [
        r"\bconfus\w*", r"\binterface\b", r"\bdesign\b",
        r"\bupdate\w*", r"\bbutton\b"
    ]
}


def classify_review(text):
    text = text.lower()
    matches = []

    for theme, patterns in THEMES.items():
        if any(re.search(pattern, text) for pattern in patterns):
            matches.append(theme)

    return matches


# 3. Analyze ratings
def analyze_ratings(df):
    counts = (
        df["score"]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
        .sort_index()
    )

    summary = pd.DataFrame({
        "rating": counts.index,
        "review_count": counts.values,
        "percentage": (counts.values / len(df) * 100).round(2)
    })

    summary.to_csv(OUTPUT_DIR / "rating_summary.csv", index=False)

    average = df["score"].mean()
    low_count = int((df["score"] <= 2).sum())

    print("\n--- RATING SUMMARY ---")
    print(summary.to_string(index=False))
    print(f"\nReviews analyzed: {len(df)}")
    print(f"Average rating: {average:.2f}/5")
    print(f"1-2 star reviews: {low_count} "
          f"({low_count / len(df) * 100:.1f}%)")

    plt.figure(figsize=(8, 5))
    plt.bar(summary["rating"].astype(str), summary["review_count"])
    plt.title("MoveInSync Review Rating Distribution")
    plt.xlabel("Star rating")
    plt.ylabel("Number of reviews")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rating_distribution.png", dpi=150)
    plt.close()


# 4. Analyze common issues in low-rated reviews
def analyze_themes(df):
    negative = df[df["score"] <= 2].copy()
    negative["themes"] = negative["content"].apply(classify_review)

    exploded = negative.explode("themes").dropna(subset=["themes"])

    if exploded.empty:
        print("\nNo themes matched the low-rated reviews.")
        return

    summary = (
        exploded.groupby("themes")
        .size()
        .sort_values(ascending=False)
        .rename("review_mentions")
        .reset_index()
    )

    summary["percent_of_low_rated_reviews"] = (
        summary["review_mentions"] / len(negative) * 100
    ).round(1)

    summary.to_csv(OUTPUT_DIR / "theme_analysis.csv", index=False)

    negative[["score", "at", "content", "themes"]].to_csv(
        OUTPUT_DIR / "negative_reviews_analysis.csv", index=False
    )

    print("\n--- COMPLAINT THEMES ---")
    print(summary.to_string(index=False))

    summary.sort_values("review_mentions").plot(
        x="themes", y="review_mentions",
        kind="barh", legend=False, figsize=(9, 5)
    )
    plt.title("Themes in 1-2 Star Reviews")
    plt.xlabel("Number of review mentions")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "complaint_themes.png", dpi=150)
    plt.close()


# 5. Analyze trends over time
def analyze_trends(df):
    df = df.copy()
    df["month"] = df["at"].dt.to_period("M").astype(str)

    monthly = df.groupby("month").agg(
        reviews=("score", "size"),
        average_rating=("score", "mean"),
        low_rating_percentage=(
            "score", lambda x: (x <= 2).mean() * 100
        )
    ).round(2).reset_index()

    monthly.to_csv(OUTPUT_DIR / "monthly_trends.csv", index=False)

    print("\n--- MONTHLY TRENDS ---")
    print(monthly.to_string(index=False))

    plt.figure(figsize=(9, 5))
    plt.plot(
        monthly["month"],
        monthly["average_rating"],
        marker="o"
    )
    plt.title("Average Review Rating by Month")
    plt.xlabel("Month")
    plt.ylabel("Average rating")
    plt.ylim(0, 5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_trends.png", dpi=150)
    plt.close()


# 6. Run the complete analysis
def main():
    df = load_reviews()

    print("MoveInSync Review Intelligence")
    print(f"Date range: {df['at'].min()} to {df['at'].max()}")

    analyze_ratings(df)
    analyze_themes(df)
    analyze_trends(df)

    print(f"\nAnalysis complete. Results saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

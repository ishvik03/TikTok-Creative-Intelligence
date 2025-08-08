import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")
output_dir = "../insights/plots"
os.makedirs(output_dir, exist_ok=True)

# --- 1. Hooks Distribution ---
try:
    hooks = pd.read_csv("../insights/hooks.csv")
    plt.figure(figsize=(6, 4))
    sns.countplot(data=hooks, x="hook_type", order=hooks["hook_type"].value_counts().index, palette="viridis")
    plt.title("Distribution of Hook Types")
    plt.xlabel("Hook Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/hook_type_distribution.png")
    plt.close()
except Exception as e:
    print("❌ Could not plot hook types:", e)

# --- 2. Hashtag Frequency ---
try:
    hashtags = pd.read_csv("../insights/hashtags.csv").head(20)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=hashtags, y="hashtag", x="count", palette="rocket")
    plt.title("Top 20 Hashtags")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_hashtags.png")
    plt.close()
except Exception as e:
    print("❌ Could not plot hashtags:", e)

# --- 3. Keyword Viral Ratio ---
try:
    keywords = pd.read_csv("../insights/viral_keywords.csv")
    keywords = keywords[keywords["count"] >= 10]  # Filter for meaningful keywords
    top_viral_keywords = keywords.sort_values("viral_ratio", ascending=False).head(15)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=top_viral_keywords, y="keyword", x="viral_ratio", palette="mako")
    plt.title("Top Viral Keywords (min 10 mentions)")
    plt.xlabel("Viral Ratio")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_viral_keywords.png")
    plt.close()
except Exception as e:
    print("❌ Could not plot viral keywords:", e)

# --- 4. Duration Bin ---
try:
    cleaned = pd.read_csv("../data/processed/cleaned_tiktok_data.csv")
    plt.figure(figsize=(6, 4))
    sns.countplot(data=cleaned, x="duration_bin", order=cleaned["duration_bin"].value_counts().index, palette="Set2")
    plt.title("Video Duration Bins")
    plt.xlabel("Duration")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/duration_bins.png")
    plt.close()
except Exception as e:
    print("❌ Could not plot duration bins:", e)

# --- 5. Post Time Patterns ---
try:
    # Hour of Day
    plt.figure(figsize=(8, 4))
    sns.countplot(data=cleaned, x="hour_of_day", palette="Blues")
    plt.title("Post Hour Distribution")
    plt.xlabel("Hour of Day")
    plt.ylabel("Post Count")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/post_hours.png")
    plt.close()

    # Day of Week
    plt.figure(figsize=(8, 4))
    sns.countplot(
        data=cleaned,
        x="day_of_week",
        order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        palette="coolwarm"
    )
    plt.title("Post Day of Week")
    plt.xlabel("Day")
    plt.ylabel("Post Count")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/post_days.png")
    plt.close()
except Exception as e:
    print("❌ Could not plot post time patterns:", e)

# --- 6. Video Format Types ---
try:
    formats = pd.read_csv("../insights/formats.csv")
    plt.figure(figsize=(7, 4))
    sns.countplot(data=formats, y="video_format", order=formats["video_format"].value_counts().index, palette="flare")
    plt.title("Detected Video Formats")
    plt.xlabel("Count")
    plt.ylabel("Format")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/video_formats.png")
    plt.close()
except Exception as e:
    print("❌ Could not plot formats:", e)

print("✅ All visualizations saved to:", output_dir)

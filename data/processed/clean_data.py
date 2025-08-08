import pandas as pd
import os
import re

# File paths
raw_dir = "creative-intel-tiktok/data/raw"
processed_dir = "creative-intel-tiktok/data/processed"
output_path = os.path.join(processed_dir, "cleaned_tiktok_data.csv")

# Helper functions
def clean_hashtags(ht):
    if pd.isna(ht):
        return []
    tags = re.findall(r"#\w+", ht)
    return [tag.lower().strip("#") for tag in tags]

def duration_bin(seconds):
    if pd.isna(seconds):
        return None
    if seconds < 15:
        return "<15s"
    elif seconds < 30:
        return "15–30s"
    elif seconds < 60:
        return "30–60s"
    elif seconds < 90:
        return "60–90s"
    else:
        return ">90s"

def add_country_column(df, country_name):
    df["country"] = country_name
    return df

# Read and process all 4 files
file_map = {
    "Japan": "JapanTikTokData_with_Transcripts.xlsx",
    "UK": "UKTikTokData_with_Transcripts-2.xlsx",
    "Italy": "ItalyTikTokData_with_Transcripts.xlsx",
    "USA": "USATikTokData_with_Transcripts-2.xlsx"
}

cleaned_dfs = []

for country, filename in file_map.items():
    path = os.path.join(raw_dir, filename)
    df = pd.read_excel(path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Print columns for debugging
    print(f"\nColumns in {filename} ({country}):")
    print(df.columns.tolist())

    # Add country column
    df = add_country_column(df, country)

    # Extract all hashtag name columns
    hashtag_cols = [col for col in df.columns if re.match(r"hashtags/\d+/name", col)]
    
    if hashtag_cols:
        df["cleaned_hashtags"] = df[hashtag_cols].apply(
            lambda row: [str(tag).lower().strip("#") for tag in row if pd.notna(tag)],
            axis=1
        )
    else:
        print(f"Skipping {filename} due to missing hashtag name columns.")
        continue

    # Extract hour and day
    df["post_time"] = pd.to_datetime(df.get("createtimeiso", None), errors="coerce")
    df["hour_of_day"] = df["post_time"].dt.hour
    df["day_of_week"] = df["post_time"].dt.day_name()

    # Bin durations
    df["duration_bin"] = df.get("videometa/duration", None).apply(duration_bin)

    # Viral flag
    df["is_viral"] = (df.get("diggcount", 0) / df.get("playcount", 1)).fillna(0) > 0.15

    cleaned_dfs.append(df)


# Merge all
final_df = pd.concat(cleaned_dfs, ignore_index=True)

# Save cleaned file
final_df.to_csv(output_path, index=False)

print(f"\n✅ Cleaned data saved to: {output_path}")

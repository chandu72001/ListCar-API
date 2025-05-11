import pandas as pd
import re
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load raw CSV
df = pd.read_csv("data/raw/vehicle_data.csv")

# 1. Extract model year from Car name
df["Model Year"] = df["Car name"].str.extract(r"^(\d{4})")
df["Car name"] = df["Car name"].str.replace(r"^\d{4}\s*", "", regex=True)

# 2. Clean Car Price → integer
def clean_price(price):
    if pd.isna(price):
        return None
    return int(re.sub(r"[^\d]", "", price))

df["Car Price"] = df["Car Price"].apply(clean_price)

# 3. Simplify Price Badge
def simplify_price_badge(badge):
    if pd.isna(badge):
        return None
    return badge.split("|")[0].strip()

df["Car Price Badge"] = df["Car Price Badge"].apply(simplify_price_badge)

# 4. Convert MPG range to average
def avg_mpg(mpg):
    if pd.isna(mpg):
        return None
    try:
        parts = re.findall(r"\d+", mpg)
        parts = list(map(int, parts))
        if len(parts) == 2:
            return round(sum(parts) / 2)
        elif len(parts) == 1:
            return parts[0]
        else:
            return None
    except Exception as e:
        logger.warning(f"Error processing MPG: {mpg} - {e}")
        return None

df["MPG"] = df["MPG"].apply(avg_mpg)

# 5. Convert Mileage
def clean_mileage(mileage):
    if pd.isna(mileage):
        return None
    return int(re.sub(r"[^\d]", "", mileage))

df["Mileage"] = df["Mileage"].apply(clean_mileage)

# 6. Keep nulls as-is (already handled by pd.isna() checks above)

# 7. Convert Seller Rating to float
def clean_rating(rating):
    if pd.isna(rating):
        return None
    try:
        return float(rating)
    except ValueError:
        return None

df["Seller Rating"] = df["Seller Rating"].apply(clean_rating)

# Final strip of all string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# Reordering columns if "Model Year" exists
cols = df.columns.tolist()
if "Model Year" in cols and "Car name" in cols:
    cols.remove("Model Year")
    Car_name_index = cols.index("Car name")
    cols.insert(Car_name_index + 1, "Model Year")
    df = df[cols]

# Save cleaned version
df.to_csv("data/processed/vehicle_data_cleaned.csv", index=False)
logger.info("Cleaned data saved to 'vehicle_data_cleaned.csv'")
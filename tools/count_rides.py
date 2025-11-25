import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================ UTILS (Dari skrip preprocessing.py) ===================
def to_snake(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s

# ================= 1. LOAD & AGREGASI PELANGGAN =================
INPUT_CSV = "ncr_ride_bookings.csv"
print(f"📥 Loading: {INPUT_CSV}")
df = pd.read_csv(INPUT_CSV, dtype=str)
df.columns = [to_snake(c) for c in df.columns]
NULL_LIKE = {"", "null", "none", "na", "n/a", "nan", "Nil", "NULL", "NaN"}
for c in df.columns:
    if df[c].dtype == "object":
        df[c] = df[c].str.strip().replace(list(NULL_LIKE), np.nan)

for c in ("booking_id", "customer_id"):
    if c in df.columns:
        df[c] = df[c].str.replace(r'^"|"$', "", regex=True)

df["datetime"] = pd.to_datetime(df["date"].astype(str) + ' ' + df["time"].astype(str), errors="coerce")
df["booking_value"] = pd.to_numeric(df["booking_value"], errors="coerce").fillna(0)
df["ride_distance"] = pd.to_numeric(df["ride_distance"], errors="coerce").fillna(0)
df["is_cancelled"] = df["booking_status"].apply(lambda x: int("cancel" in str(x).lower() or "no driver" in str(x).lower())).astype(int)

observation_date = df['datetime'].max() + pd.Timedelta(days=1)
df_valid_rides = df[df['booking_status'].isin(['Completed', 'Incomplete', 'No Driver Found'])].copy()

customer_df = df_valid_rides.groupby('customer_id').agg(
    recency=('datetime', lambda x: (observation_date - x.max()).days),
    frequency=('booking_id', 'nunique'),
    monetary=('booking_value', 'sum'),
).reset_index()

print("\n🔄 Agregasi Pelanggan Selesai.")


# ================= 2. ANALISIS FREKUENSI =================
total_customers = len(customer_df)
single_transaction_count = (customer_df['frequency'] == 1).sum()
single_transaction_percentage = (single_transaction_count / total_customers) * 100

print(f"\n==================== ANALISIS FREKUENSI ====================")
print(f"Total Pelanggan: {total_customers}")
print(f"Pelanggan dengan 1 Transaksi (F=1): {single_transaction_count}")
print(f"Persentase Pelanggan dengan F=1: {single_transaction_percentage:.2f}%")
print("============================================================")

# --- Visualisasi Distribusi Frequency ---
# Kita batasi frekuensi plot untuk melihat distribusi yang miring (skewed)
plt.figure(figsize=(10, 6))
sns.histplot(customer_df['frequency'], bins=range(1, customer_df['frequency'].max() + 2), kde=False, stat="count")

plt.title('Distribusi Frekuensi Transaksi Pelanggan')
plt.xlabel('Jumlah Transaksi (Frequency)')
plt.ylabel('Jumlah Pelanggan')
plt.xlim(0, customer_df['frequency'].quantile(0.99) + 1) # Batasi sumbu X pada kuantil ke-99 agar tidak didominasi oleh outlier ekstrem
plt.xticks(range(1, int(customer_df['frequency'].quantile(0.99)) + 2))
plt.grid(axis='y', linestyle='--')
plt.savefig('outputs/frekuensi_distribusi.png')
plt.show()
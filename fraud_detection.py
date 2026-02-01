import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("transactions_uncleaned.csv")
print("\nInitial Data Loaded:")
print(df.head())

# -----------------------------
# CLEANING
# -----------------------------
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['transaction_time'] = pd.to_datetime(df['transaction_time'])

print("\nAfter Cleaning:")
print(df[['amount', 'transaction_time']].head())

# -----------------------------
# RULE 1: HIGH AMOUNT
# -----------------------------
df['high_amount_flag'] = np.where(df['amount'] > 50000, 1, 0)

print("\nRule 1 – High Amount Flag (> 50,000):")
print(df[['amount', 'high_amount_flag']].head(10))

# -----------------------------
# RULE 2: LATE NIGHT TRANSACTIONS
# -----------------------------
df['hour'] = df['transaction_time'].dt.hour
df['late_night_flag'] = np.where((df['hour'] >= 0) & (df['hour'] <= 5), 1, 0)

print("\nRule 2 – Late Night Flag (12 AM – 5 AM):")
print(df[['transaction_time', 'hour', 'late_night_flag']].head(10))

# -----------------------------
# RULE 3: RAPID TRANSACTIONS
# -----------------------------
df = df.sort_values(['card_id', 'transaction_time'])
df['time_diff'] = df.groupby('card_id')['transaction_time'].diff().dt.total_seconds()
df['rapid_txn_flag'] = np.where(df['time_diff'] <= 300, 1, 0)

print("\nRule 3 – Rapid Transactions (within 5 minutes):")
print(df[['card_id', 'transaction_time', 'time_diff', 'rapid_txn_flag']].head(10))

# -----------------------------
# RULE 4: CITY CHANGE
# -----------------------------
df['prev_city'] = df.groupby('card_id')['city'].shift(1)
df['city_change_flag'] = np.where(
    (df['city'] != df['prev_city']) & (df['time_diff'] <= 600),
    1,
    0
)

print("\nRule 4 – City Change within 10 minutes:")
print(df[['card_id', 'prev_city', 'city', 'time_diff', 'city_change_flag']].head(10))

# -----------------------------
# RULE 5: MISSING DATA
# -----------------------------
df['missing_data_flag'] = np.where(df['amount'].isna() | df['city'].isna(), 1, 0)

print("\nRule 5 – Missing Amount or City:")
print(df[['amount', 'city', 'missing_data_flag']].head(10))

# -----------------------------
# FRAUD SCORE & FINAL FLAG
# -----------------------------
df['fraud_score'] = (
    df['high_amount_flag'] +
    df['late_night_flag'] +
    df['rapid_txn_flag'] +
    df['city_change_flag'] +
    df['missing_data_flag']
)

df['fraud_flag'] = np.where(df['fraud_score'] >= 2, 1, 0)

print("\nFinal Fraud Score & Flag:")
print(df[['fraud_score', 'fraud_flag']].head(10))

# -----------------------------
# SAVE TO SQLITE
# -----------------------------
conn = sqlite3.connect("fraud_detection.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)

# -----------------------------
# FRAUD TRANSACTIONS QUERY
# -----------------------------
query = """
SELECT
    transaction_id,
    card_id,
    amount,
    city,
    fraud_score,
    fraud_flag
FROM transactions
WHERE fraud_flag = 1
"""
fraud_df = pd.read_sql(query, conn)
print("\n--- FRAUD TRANSACTIONS ---")
print(fraud_df.head())

# -----------------------------
# FRAUD SUMMARY QUERY
# -----------------------------
summary_query = """
SELECT
    fraud_flag,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY fraud_flag
"""
summary_df = pd.read_sql(summary_query, conn)
print("\n--- FRAUD SUMMARY ---")
print(summary_df)

fraud_df.to_csv("fraud_transactions.csv", index=False)
summary_df.to_csv("fraud_summary.csv", index=False)

conn.close()

# -----------------------------
# FRAUD DETECTION GRAPH
# -----------------------------

summary_df.set_index('fraud_flag')['total_transactions'].plot(kind='bar')
plt.title("Fraud vs Non-Fraud Transactions")
plt.xlabel("Fraud Flag (0 = No, 1 = Yes)")
plt.ylabel("Number of Transactions")
plt.show()

print("\n✅ Fraud detection completed successfully!")

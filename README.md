# Fraud-Detection-Rule-Based-
Identify suspicious transactions using rule-based logic (Python + NumPy + SQL + Matplotlib)

# Fraud Detection – Rule Based System (Python + NumPy + SQL)

## 📌 Project Overview
This project demonstrates a **rule-based fraud detection system** similar to what is used in real-world banking and payment systems.

Instead of machine learning, we apply **business rules** to detect suspicious transactions and store results in a SQL database.

---

## 🛠️ Tools & Technologies
- Python
- Pandas
- NumPy
- SQLite (SQL)
- SQL Queries for analysis

---

## 📂 Dataset
- Simulated real-time **uncleaned transaction dataset**
- 100,000+ transaction records
- Includes missing values, high amounts, rapid transactions, and city changes

---

## 🚨 Fraud Detection Rules

| Rule | Description |
|----|------------|
| Rule 1 | High transaction amount (> ₹50,000) |
| Rule 2 | Late night transaction (12 AM – 5 AM) |
| Rule 3 | Rapid transactions within 5 minutes |
| Rule 4 | City change within 10 minutes |
| Rule 5 | Missing critical data (amount or city) |

Each rule generates a **flag (0 or 1)**.

---

## 🧮 Fraud Logic
```text
Fraud Score = Sum of all rule flags
If Fraud Score ≥ 2 → Marked as Fraud

## 📊** Outcome**
- Identified suspicious transactions using rule-based logic
- Generated fraud scores and fraud flags
- Stored results in SQL database
- Fraud summary and transaction-level analysis ready for dashboard creation

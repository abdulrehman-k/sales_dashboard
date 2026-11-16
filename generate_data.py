import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 5000

prices = {
    "Starter Plan": 19.99,
    "Pro Plan": 49.99,
    "Business Plan": 99.99,
    "Enterprise Plan": 299.00,
    "Analytics Add-on": 14.99,
    "Support Add-on": 29.99,
}

df = pd.DataFrame({
    "order_id": np.arange(1001, 1001 + n),
    "date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 680, n), unit="D"),
    "product": rng.choice(list(prices), n, p=[0.30, 0.25, 0.18, 0.07, 0.12, 0.08]),
    "region": rng.choice(["Asia", "Europe", "North America", "Middle East", "Africa"], n),
    "salesperson": rng.choice(["Ayesha", "Bilal", "Carlos", "Dana", "Elena", "Farid"], n),
    "quantity": rng.integers(1, 6, n),
})
df["unit_price"] = df["product"].map(prices)

df.sort_values("date").to_csv("data/sales.csv", index=False)
print("Saved", len(df), "rows")
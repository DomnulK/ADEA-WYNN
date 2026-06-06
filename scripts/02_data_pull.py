"""
WYNN Resorts - Date intra-day (5 minute) pentru ADEA Partea 2

Descarca date la 5 minute pe ultimele 60 de zile (maximul permis de yfinance
pentru intervale intra-day), apoi construieste seria contoarelor orare:
pentru fiecare interval de o ora, numarul de modificari ale pretului intre
observatii consecutive de 5 minute din interiorul acelui interval.
"""
import yfinance as yf
import numpy as np
import pandas as pd
from pathlib import Path

TICKER = "WYNN"
INTERVAL = "1m"
PERIOD = "7d"  # maximul yfinance pentru intra-day

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

print(f"Descarcare {TICKER} la {INTERVAL} pe {PERIOD}...")
data = yf.download(
    TICKER,
    period=PERIOD,
    interval=INTERVAL,
    auto_adjust=False,
    progress=False,
)

# Flatten multi-index daca apare
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

print(f"\nShape brut: {data.shape}")
print(f"Interval: {data.index.min()} -> {data.index.max()}")
print(f"\nPrimele randuri:")
print(data.head(3))

# Pastram doar pretul Close (pentru numararea modificarilor)
df = data[["Close"]].copy()
df = df.dropna()

# IMPORTANT: filtram doar orele de tranzactionare regulate (9:30-16:00 ET)
# yfinance returneaza timestamp-uri in fus orar; verificam
print(f"\nFus orar index: {df.index.tz}")

# Salvam datele brute de 5 minute
df.to_csv(DATA_DIR / "wynn_intraday_1m.csv")
print(f"\nSalvat {len(df)} observatii de 1 min -> wynn_intraday_1m.csv")

# ============================================
# Construim seria contoarelor orare
# ============================================
# Pentru fiecare ora calendaristica, numaram cate modificari de pret
# (close_t != close_{t-1}) au avut loc intre observatiile consecutive

# Adaugam coloana: modificarea fata de observatia anterioara
df["price_changed"] = (df["Close"].diff() != 0).astype(int)
# Prima observatie din serie are diff = NaN -> 0 (nu o numaram)
df.loc[df.index[0], "price_changed"] = 0

# Grupam pe ore calendaristice si numaram modificarile
# floor("h") rotunjeste timestamp-ul la ora
df["hour_bucket"] = df.index.floor("h")
hourly_counts = df.groupby("hour_bucket")["price_changed"].sum()

# Eliminam orele cu prea putine observatii (de ex. ultima ora partiala)
# Numaram si cate observatii sunt in fiecare ora
obs_per_hour = df.groupby("hour_bucket").size()

# Pastram doar orele cu cel putin 6 observatii (jumatate dintr-o ora de 5m=12)
# ca sa evitam orele partiale de la deschidere/inchidere
valid_hours = obs_per_hour[obs_per_hour >= 6].index
hourly_counts = hourly_counts[hourly_counts.index.isin(valid_hours)]

print(f"\n=== Seria contoarelor orare ===")
print(f"Numar de ore (contoare): {len(hourly_counts)}")
print(f"Statistici:")
print(f"  Media:    {hourly_counts.mean():.4f}")
print(f"  Varianta: {hourly_counts.var(ddof=1):.4f}")
print(f"  Min:      {hourly_counts.min()}")
print(f"  Max:      {hourly_counts.max()}")
print(f"\nDistributia valorilor:")
print(hourly_counts.value_counts().sort_index())

# Salvam contoarele orare
hourly_counts.to_frame("count").to_csv(DATA_DIR / "wynn_hourly_counts.csv")
print(f"\nSalvat {len(hourly_counts)} contoare orare -> wynn_hourly_counts.csv")
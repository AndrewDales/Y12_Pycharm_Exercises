
#!/usr/bin/env python3
"""
Fetch past 30 days of hourly temperature from Open-Meteo Archive API
and plot with matplotlib—no pandas required.

Change LATITUDE / LONGITUDE and TIMEZONE as needed.
"""

import datetime as dt
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -----------------------------
# User settings
# -----------------------------
LATITUDE = 51.5072       # London (example)
LONGITUDE = -0.1276
TIMEZONE = "Europe/London"   # or "auto"
TEMP_UNIT = "celsius"        # "celsius" or "fahrenheit"
# -----------------------------

# Compute the last 30 complete days (end = yesterday, start = 29 days before)
today = dt.date.today()
end_date = today - dt.timedelta(days=1)
start_date = end_date - dt.timedelta(days=29)

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "hourly": "temperature_2m",
    "timezone": TIMEZONE,
    "temperature_unit": TEMP_UNIT,  # optional; defaults to celsius
}

print(f"Requesting {params['start_date']} → {params['end_date']} "
      f"for lat={LATITUDE}, lon={LONGITUDE}")

resp = requests.get(BASE_URL, params=params, timeout=30)
resp.raise_for_status()
payload = resp.json()

# Basic validation
if "hourly" not in payload or "time" not in payload["hourly"] or "temperature_2m" not in payload["hourly"]:
    raise RuntimeError("Unexpected response format from Open-Meteo Archive API")

# Parse into Python lists
time_strings = payload["hourly"]["time"]              # e.g. "2026-01-18T23:00"
temps = payload["hourly"]["temperature_2m"]           # numeric list

# Convert ISO 8601 strings → datetime objects for plotting
times = [dt.datetime.fromisoformat(t) for t in time_strings]

# ---- Optional: compute simple daily means (no pandas) ----
# Group by date
daily_sums = {}
daily_counts = {}
for ts, temp in zip(times, temps):
    d = ts.date()
    daily_sums[d] = daily_sums.get(d, 0.0) + float(temp)
    daily_counts[d] = daily_counts.get(d, 0) + 1
daily_dates = sorted(daily_sums.keys())
daily_means = [daily_sums[d] / daily_counts[d] for d in daily_dates]

# ---- Plot ----
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots(figsize=(11, 5))

# Hourly series
ax.plot(times, temps, color="#1f77b4", linewidth=1.0, label="Hourly temperature")

# Daily mean series (overlay)
ax.plot(
    [dt.datetime.combine(d, dt.time(12, 0)) for d in daily_dates],
    daily_means,
    color="#d62728",
    linewidth=2.0,
    label="Daily mean"
)

unit_label = "°C" if TEMP_UNIT.lower().startswith("c") else "°F"
ax.set_title(
    f"Hourly Air Temperature — Past 30 Days\n"
    f"London  —  {start_date} to {end_date}"
)
ax.set_xlabel("Date / time")
ax.set_ylabel(f"Temperature ({unit_label})")
ax.grid(True, alpha=0.3)
ax.legend()

# Nice date formatting
ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=12))
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
fig.autofmt_xdate()

plt.tight_layout()
plt.show()

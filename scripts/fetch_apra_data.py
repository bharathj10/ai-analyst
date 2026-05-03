"""
APRA superannuation statistics fetcher.

Downloads and parses publicly available APRA publications into
reference DataFrames saved to data/reference/.

Run manually or scheduled quarterly when APRA updates their statistics.

Data sources:
- Annual Fund-Level Superannuation Statistics (AFLSS) — published January each year
- Quarterly Superannuation Statistics — published ~6 weeks after quarter end
- APRA Heatmap data — published November each year

Usage:
    python scripts/fetch_apra_data.py              # fetch all
    python scripts/fetch_apra_data.py --quarterly  # quarterly stats only
    python scripts/fetch_apra_data.py --annual     # annual AFLSS only
"""

from __future__ import annotations
import argparse
import datetime
import json
import sys
from pathlib import Path

import pandas as pd
import requests

OUTPUT_DIR = Path("data/reference")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.date.today()
DATE_STR = TODAY.strftime("%Y-%m-%d")


# ── APRA publication URLs ─────────────────────────────────────────────────────
# These are stable landing pages; the actual Excel/CSV links change each release.
# The fetch functions use requests to download whatever is currently linked.

APRA_BASE = "https://www.apra.gov.au"
APRA_SUPER_STATS_PAGE = f"{APRA_BASE}/statistics/superannuation-statistics"

# Known direct download URLs (update these after each APRA release)
# As of early 2025 — check apra.gov.au for current links
KNOWN_URLS = {
    "quarterly_summary": (
        "https://www.apra.gov.au/sites/default/files/2025-02/"
        "Quarterly%20superannuation%20statistics%20December%202024.xlsx"
    ),
    "annual_aflss": (
        "https://www.apra.gov.au/sites/default/files/2025-01/"
        "Annual%20fund-level%20superannuation%20statistics%20June%202024.xlsx"
    ),
}

# ASFA Retirement Standard (updated quarterly; hardcoded current values as fallback)
ASFA_STANDARDS = {
    "as_of": "September 2024",
    "comfortable_single_pa": 51_630,
    "comfortable_couple_pa": 72_663,
    "modest_single_pa": 32_030,
    "modest_couple_pa": 46_494,
    "comfortable_lump_sum_single": 595_000,  # rough present value estimate
    "comfortable_lump_sum_couple": 690_000,
}

# APRA industry benchmarks (from AFLSS June 2024 — update annually)
APRA_BENCHMARKS_2024 = {
    "as_of_year": "June 2024",
    "source": "APRA Annual Fund-Level Superannuation Statistics",
    "industry_fund": {
        "return_1yr_median_pct": 8.5,
        "return_5yr_median_pct": 6.8,
        "return_7yr_median_pct": 7.4,
        "return_10yr_median_pct": 7.9,
        "total_fee_50k_median_pct": 0.82,
        "total_fee_50k_top_quartile_pct": 0.70,
        "admin_fee_flat_median_aud": 78,
        "nps_median": 35,
        "salary_sacrifice_participation_pct": 22.1,
    },
    "retail_fund": {
        "return_1yr_median_pct": 7.8,
        "return_5yr_median_pct": 6.0,
        "return_7yr_median_pct": 6.6,
        "return_10yr_median_pct": 7.0,
        "total_fee_50k_median_pct": 1.12,
        "total_fee_50k_top_quartile_pct": 0.95,
    },
    "system_totals": {
        "total_fum_bn_aud": 3900,
        "total_accounts_millions": 22.4,
        "total_contributions_bn_aud": 165,
        "mysuper_funds_count": 62,
        "median_account_balance_aud": 72_000,
        "mean_account_balance_aud": 115_000,
    },
}

# SG rate schedule (legislated)
SG_RATE_SCHEDULE = {
    2013: 9.25, 2014: 9.50, 2015: 9.50, 2016: 9.50, 2017: 9.50,
    2018: 9.50, 2019: 9.50, 2020: 9.50, 2021: 9.50,
    2022: 10.00, 2023: 10.50, 2024: 11.00, 2025: 11.50, 2026: 12.00,
}

# Contribution caps (FY)
CONTRIBUTION_CAPS = {
    2021: {"cc": 25_000, "ncc": 100_000},
    2022: {"cc": 27_500, "ncc": 110_000},
    2023: {"cc": 27_500, "ncc": 110_000},
    2024: {"cc": 27_500, "ncc": 110_000},
    2025: {"cc": 30_000, "ncc": 120_000},
    2026: {"cc": 30_000, "ncc": 120_000},  # to be confirmed
}

# Transfer Balance Cap
TRANSFER_BALANCE_CAP = {
    2021: 1_700_000,
    2022: 1_700_000,
    2023: 1_900_000,
    2024: 1_900_000,
    2025: 1_900_000,
}

# ASFA retirement standards (quarterly, AUD p.a.)
ASFA_HISTORY = {
    "Sep-2024": {"comfortable_single": 51_630, "comfortable_couple": 72_663,
                 "modest_single": 32_030, "modest_couple": 46_494},
    "Jun-2024": {"comfortable_single": 51_278, "comfortable_couple": 72_148,
                 "modest_single": 31_752, "modest_couple": 46_096},
    "Mar-2024": {"comfortable_single": 50_981, "comfortable_couple": 71_723,
                 "modest_single": 31_323, "modest_couple": 45_808},
}


# ── Fetch functions ───────────────────────────────────────────────────────────

def save_reference_json(name: str, data: dict) -> Path:
    path = OUTPUT_DIR / f"{DATE_STR}_{name}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved: {path}")
    return path


def save_reference_csv(name: str, df: pd.DataFrame) -> Path:
    path = OUTPUT_DIR / f"{DATE_STR}_{name}.csv"
    df.to_csv(path, index=False)
    print(f"  Saved: {path} ({len(df):,} rows)")
    return path


def fetch_apra_excel(url: str, sheet_name: str = None) -> pd.DataFrame | None:
    """Download an APRA Excel file and return a DataFrame."""
    try:
        print(f"  Downloading: {url}")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        local = OUTPUT_DIR / "_temp_apra.xlsx"
        local.write_bytes(resp.content)

        if sheet_name:
            df = pd.read_excel(local, sheet_name=sheet_name, skiprows=4)
        else:
            df = pd.read_excel(local, skiprows=4)

        local.unlink()
        return df
    except Exception as e:
        print(f"  Warning: Could not fetch APRA data ({e}). Using cached benchmarks.")
        return None


def build_sg_rate_table() -> pd.DataFrame:
    """Build a clean SG rate reference table."""
    rows = []
    for fy, rate in SG_RATE_SCHEDULE.items():
        rows.append({
            "financial_year": fy,
            "fy_label": f"FY{fy}",
            "sg_rate_pct": rate,
            "sg_rate_decimal": rate / 100,
        })
    return pd.DataFrame(rows)


def build_contribution_caps_table() -> pd.DataFrame:
    rows = []
    for fy, caps in CONTRIBUTION_CAPS.items():
        rows.append({
            "financial_year": fy,
            "fy_label": f"FY{fy}",
            "concessional_cap_aud": caps["cc"],
            "non_concessional_cap_aud": caps["ncc"],
            "bring_forward_3yr_aud": caps["ncc"] * 3,
        })
    return pd.DataFrame(rows)


def build_asfa_table() -> pd.DataFrame:
    rows = []
    for period, values in ASFA_HISTORY.items():
        rows.append({"period": period, **values})
    return pd.DataFrame(rows)


def fetch_all(fetch_live: bool = True) -> dict:
    """
    Build the complete reference dataset.
    fetch_live=True: attempt to download latest APRA data.
    fetch_live=False: use hardcoded benchmarks only (safe offline mode).
    """
    print("\n── APRA Reference Data Fetch ─────────────────────────────────")
    results = {}

    print("\n[1] SG rate schedule")
    df_sg = build_sg_rate_table()
    results["sg_rates"] = save_reference_csv("sg_rate_schedule", df_sg)

    print("\n[2] Contribution caps")
    df_caps = build_contribution_caps_table()
    results["contribution_caps"] = save_reference_csv("contribution_caps", df_caps)

    print("\n[3] APRA benchmarks (hardcoded current values)")
    results["apra_benchmarks"] = save_reference_json("apra_benchmarks", APRA_BENCHMARKS_2024)

    print("\n[4] ASFA retirement standards history")
    df_asfa = build_asfa_table()
    results["asfa_standards"] = save_reference_csv("asfa_standards", df_asfa)
    results["asfa_current"] = save_reference_json("asfa_current", ASFA_STANDARDS)

    print("\n[5] Transfer Balance Cap history")
    results["tbc"] = save_reference_json("transfer_balance_cap", TRANSFER_BALANCE_CAP)

    if fetch_live:
        print("\n[6] Attempting live APRA quarterly statistics download...")
        url = KNOWN_URLS.get("quarterly_summary")
        if url:
            df_qly = fetch_apra_excel(url)
            if df_qly is not None:
                results["quarterly_live"] = save_reference_csv("apra_quarterly_raw", df_qly)
        else:
            print("  No quarterly URL configured — skip.")

        print("\n[7] Attempting live APRA annual AFLSS download...")
        url = KNOWN_URLS.get("annual_aflss")
        if url:
            df_aflss = fetch_apra_excel(url)
            if df_aflss is not None:
                results["annual_live"] = save_reference_csv("apra_aflss_raw", df_aflss)
        else:
            print("  No AFLSS URL configured — skip.")

    print(f"\n── Complete. Files written to {OUTPUT_DIR}/ ──")
    return results


def load_benchmarks() -> dict:
    """
    Load the most recent APRA benchmarks from data/reference/.
    Falls back to hardcoded values if no local file exists.
    """
    files = sorted(OUTPUT_DIR.glob("*_apra_benchmarks.json"), reverse=True)
    if files:
        with open(files[0]) as f:
            return json.load(f)
    return APRA_BENCHMARKS_2024


def load_sg_rates() -> dict:
    """Return the SG rate schedule as a dict {year: rate}."""
    return SG_RATE_SCHEDULE


def load_contribution_caps(fy: int = None) -> dict:
    """Return contribution caps for a given FY, or all caps if fy=None."""
    if fy:
        return CONTRIBUTION_CAPS.get(fy, CONTRIBUTION_CAPS[2025])
    return CONTRIBUTION_CAPS


def load_asfa_current() -> dict:
    """Return current ASFA Retirement Standard values."""
    files = sorted(OUTPUT_DIR.glob("*_asfa_current.json"), reverse=True)
    if files:
        with open(files[0]) as f:
            return json.load(f)
    return ASFA_STANDARDS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch APRA reference data")
    parser.add_argument("--offline", action="store_true",
                        help="Use hardcoded benchmarks only (no web requests)")
    parser.add_argument("--quarterly", action="store_true",
                        help="Fetch quarterly stats only")
    parser.add_argument("--annual", action="store_true",
                        help="Fetch annual AFLSS only")
    args = parser.parse_args()

    fetch_all(fetch_live=not args.offline)

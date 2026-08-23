"""Product-style Streamlit interface for the Tashkent apartment model."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data import FINGERPRINT_COLUMNS, TARGET_COLUMN, VALID_RANGES
from src.model import load_artifact, predict_price

ARTIFACT_PATH = Path(os.getenv("MODEL_ARTIFACT_PATH", "artifacts/apartment_price_pipeline.joblib"))
MARKET_DATA_PATH = Path(os.getenv("MARKET_DATA_PATH", "data/apartment_listings_2026.csv"))

st.set_page_config(
    page_title="Tashkent Apartment Market",
    page_icon="🏙️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(145deg, #f7faff 0%, #edf4ff 55%, #f7fbff 100%);}
    .block-container {max-width: 1180px; padding-top: 2rem;}
    .hero {padding: 1.6rem 1.7rem; border-radius: 22px; color: white;
           background: linear-gradient(120deg, #061846, #0d5bff 68%, #00a6a6);
           margin-bottom: 1rem; box-shadow: 0 16px 38px rgba(13,91,255,.18);}
    .hero h1 {margin: 0; font-size: 2.45rem; line-height: 1.12;}
    .hero p {margin: .65rem 0 0; opacity: .94; font-size: 1.05rem;}
    .result {padding: 1.35rem; border: 1px solid #0d9d59; border-radius: 18px;
             background: #effcf5; text-align: center; box-shadow: 0 10px 25px rgba(8,122,68,.08);}
    .result-label {color: #52627e; font-size: .95rem;}
    .result-value {color: #087a44; font-size: 2.45rem; font-weight: 780;}
    .result-range {color: #245643; margin-top: .25rem;}
    .status {display:inline-block; padding:.28rem .65rem; border-radius:999px;
             background:#e7f7ef; color:#087a44; font-weight:650; font-size:.86rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_artifact():
    return load_artifact(ARTIFACT_PATH)


@st.cache_data
def get_market_data(path: str, modified_ns: int) -> pd.DataFrame:
    del modified_ns
    frame = pd.read_csv(path)
    required = {*FINGERPRINT_COLUMNS, TARGET_COLUMN, "listing_date"}
    if missing := sorted(required.difference(frame.columns)):
        raise ValueError(f"Market dataset is missing: {', '.join(missing)}")
    valid = pd.Series(True, index=frame.index)
    for column, (minimum, maximum) in VALID_RANGES.items():
        valid &= pd.to_numeric(frame[column], errors="coerce").between(minimum, maximum)
    valid &= pd.to_numeric(frame["level"], errors="coerce") <= pd.to_numeric(
        frame["max_levels"], errors="coerce"
    )
    valid &= pd.to_numeric(frame["is_new_building"], errors="coerce").isin([0, 1])
    clean = frame.loc[valid].drop_duplicates([*FINGERPRINT_COLUMNS, TARGET_COLUMN]).copy()
    clean["listing_date"] = pd.to_datetime(clean["listing_date"], errors="coerce")
    clean["price_per_m2"] = clean[TARGET_COLUMN] / clean["size_m2"]
    return clean


def similar_listings(
    market: pd.DataFrame,
    *,
    district: str,
    rooms: int,
    size_m2: float,
    is_new_building: int,
) -> pd.DataFrame:
    size_margin = max(size_m2 * 0.25, 10)
    strict = market[
        (market["district"] == district)
        & (market["rooms"] == rooms)
        & (market["is_new_building"] == is_new_building)
        & (market["size_m2"].between(size_m2 - size_margin, size_m2 + size_margin))
    ]
    if len(strict) >= 5:
        return strict
    return market[
        (market["district"] == district)
        & (market["size_m2"].between(size_m2 - size_margin, size_m2 + size_margin))
    ]


artifact = get_artifact()
metadata = artifact["metadata"]
audit = metadata.get("data_audit", {})
market = get_market_data(str(MARKET_DATA_PATH), MARKET_DATA_PATH.stat().st_mtime_ns)
latest_listing = market["listing_date"].max().date()
earliest_listing = market["listing_date"].min().date()
age_days = max((date.today() - latest_listing).days, 0)
reference_period = (
    latest_listing.strftime("%B %Y")
    if latest_listing.replace(day=1) == earliest_listing.replace(day=1)
    else f"{earliest_listing:%b %Y}–{latest_listing:%b %Y}"
)
freshness_label = "Fresh snapshot" if age_days <= 14 else f"Snapshot is {age_days} days old"

st.markdown(
    f"""
    <div class="hero">
      <h1>Tashkent Apartment Market</h1>
      <p>AI asking-price estimate + comparable listing evidence<br>
      Reference period: {reference_period}</p>
    </div>
    <span class="status">● {freshness_label}</span>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "Decision-support product prototype — estimates advertised USD asking prices, not completed "
    "sales, guarantees, or legal appraisals."
)

estimate_tab, market_tab, method_tab = st.tabs(
    ["Estimate a property", "Market snapshot", "Model & data"]
)

with estimate_tab:
    with st.form("prediction_form"):
        left, middle, right = st.columns(3)
        with left:
            district = st.selectbox("District", metadata["known_districts"], index=1)
            size_m2 = st.number_input("Apartment size (m²)", 15.0, 1000.0, 70.0, 1.0)
        with middle:
            rooms = st.number_input("Rooms", 1, 20, 3, 1)
            level = st.number_input("Apartment floor", 1, 50, 3, 1)
        with right:
            max_levels = st.number_input("Building floors", 1, 50, 5, 1)
            building_type = st.radio("Building type", ["Resale", "New building"], horizontal=True)
        submitted = st.form_submit_button("Estimate and compare", type="primary", width="stretch")

    if submitted:
        try:
            is_new_building = int(building_type == "New building")
            price, prediction_warnings = predict_price(
                artifact,
                district=district,
                size_m2=size_m2,
                rooms=rooms,
                level=level,
                max_levels=max_levels,
                is_new_building=is_new_building,
            )
            error_quantiles = metadata.get("protected_test_absolute_error_quantiles", {})
            reference_error = float(
                error_quantiles.get(
                    "p80_usd",
                    metadata["protected_test_comparison"][metadata["model_name"]]["mae_usd"],
                )
            )
            lower = max(price - reference_error, 0)
            upper = price + reference_error
            st.markdown(
                f"""
                <div class="result">
                  <div class="result-label">Estimated advertised asking price</div>
                  <div class="result-value">${price:,.0f} USD</div>
                  <div class="result-range">Reference band: ${lower:,.0f}–${upper:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(
                f"Estimated ${price / size_m2:,.0f}/m². The reference band uses the protected-test "
                "80th-percentile absolute error; it is not a guaranteed prediction interval."
            )
            comparable = similar_listings(
                market,
                district=district,
                rooms=rooms,
                size_m2=size_m2,
                is_new_building=is_new_building,
            )
            st.subheader("Comparable listing evidence")
            if comparable.empty:
                st.warning("No sufficiently similar records exist in the current snapshot.")
            else:
                comp_1, comp_2, comp_3, comp_4 = st.columns(4)
                comp_1.metric("Comparable listings", f"{len(comparable):,}")
                comp_2.metric("Median asking price", f"${comparable[TARGET_COLUMN].median():,.0f}")
                comp_3.metric("Median price/m²", f"${comparable['price_per_m2'].median():,.0f}")
                comp_4.metric(
                    "Middle 50%",
                    f"${comparable[TARGET_COLUMN].quantile(0.25):,.0f}–"
                    f"${comparable[TARGET_COLUMN].quantile(0.75):,.0f}",
                )
            for warning in prediction_warnings:
                st.warning(warning)
            st.info(
                "Use recent verified comparables and a qualified human before making a decision."
            )
        except ValueError as error:
            st.error(str(error))

with market_tab:
    st.subheader("Current snapshot overview")
    overview_1, overview_2, overview_3, overview_4 = st.columns(4)
    overview_1.metric("Usable listings", f"{len(market):,}")
    overview_2.metric("Districts", f"{market['district'].nunique()}")
    overview_3.metric("Median asking price", f"${market[TARGET_COLUMN].median():,.0f}")
    overview_4.metric("Median price/m²", f"${market['price_per_m2'].median():,.0f}")
    district_market = (
        market.groupby("district", observed=True)
        .agg(
            listings=(TARGET_COLUMN, "size"),
            median_price_usd=(TARGET_COLUMN, "median"),
            median_price_per_m2_usd=("price_per_m2", "median"),
        )
        .sort_values("median_price_per_m2_usd", ascending=False)
    )
    st.bar_chart(district_market["median_price_per_m2_usd"], color="#0d5bff")
    st.dataframe(
        district_market.style.format(
            {
                "listings": "{:,.0f}",
                "median_price_usd": "${:,.0f}",
                "median_price_per_m2_usd": "${:,.0f}",
            }
        ),
        width="stretch",
    )

with method_tab:
    test_metrics = metadata["protected_test_comparison"][metadata["model_name"]]
    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Protected-test MAE", f"${test_metrics['mae_usd']:,.0f}")
    metric_2.metric("Protected-test R²", f"{test_metrics['r2']:.3f}")
    metric_3.metric("Protected-test MAPE", f"{test_metrics['mape_percent']:.2f}%")
    metric_4.metric("Modeling rows", f"{metadata['row_count']:,}")
    st.markdown(
        f"""
        **Data window:** {earliest_listing:%d %B %Y} to {latest_listing:%d %B %Y}

        **Last collection age:** {age_days} day(s)

        **Model:** {metadata["model_name"].replace("_", " ").title()}

        **Target:** advertised asking price in USD

        The product accepts future approved-source exports through the standard ingestion schema,
        but the committed model remains geographically limited to Tashkent and temporally tied to
        its training window until new snapshots are collected, evaluated, and retrained.
        """
    )
    with st.expander("Important limitations"):
        st.markdown(
            """
            - Asking prices are not verified transaction prices.
            - Exact address, renovation, building year, amenities, and legal status are unavailable.
            - Reliability varies by district and is weaker for unusual or luxury properties.
            - The data snapshot must be refreshed and the model re-evaluated as the market changes.
            - Do not use for lending, taxation, legal appraisal, or automated high-impact decisions.
            """
        )

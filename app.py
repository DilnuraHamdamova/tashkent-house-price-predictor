"""Streamlit web demo for the 2026 Tashkent apartment asking-price model."""

from pathlib import Path

import streamlit as st

from src.model import load_artifact, predict_price

ARTIFACT_PATH = Path("artifacts/apartment_price_pipeline.joblib")

st.set_page_config(
    page_title="Tashkent Apartment Price Predictor",
    page_icon="🏙️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg, #f7faff 0%, #edf4ff 100%);}
    .hero {padding: 1.2rem 1.4rem; border-radius: 18px; color: white;
           background: linear-gradient(120deg, #061846, #0d5bff); margin-bottom: 1rem;}
    .hero h1 {margin: 0; font-size: 2.35rem;}
    .hero p {margin: .45rem 0 0; opacity: .92;}
    .result {padding: 1.25rem; border: 1px solid #0d9d59; border-radius: 16px;
             background: #effcf5; text-align: center;}
    .result-label {color: #52627e; font-size: .95rem;}
    .result-value {color: #087a44; font-size: 2.35rem; font-weight: 750;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_artifact():
    """Load the committed preprocessing and model pipeline once per app process."""
    return load_artifact(ARTIFACT_PATH)


artifact = get_artifact()
metadata = artifact["metadata"]

st.markdown(
    """
    <div class="hero">
      <h1>Tashkent Apartment Price Predictor</h1>
      <p>Estimate an August 2026 advertised asking price from observable apartment attributes.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Educational reference only — not a completed sale price, guarantee, or legal appraisal."
)

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

    submitted = st.form_submit_button(
        "Estimate asking price", type="primary", use_container_width=True
    )

if submitted:
    try:
        price, prediction_warnings = predict_price(
            artifact,
            district=district,
            size_m2=size_m2,
            rooms=rooms,
            level=level,
            max_levels=max_levels,
            is_new_building=int(building_type == "New building"),
        )
        st.markdown(
            f"""
            <div class="result">
              <div class="result-label">Estimated August 2026 advertised asking price</div>
              <div class="result-value">${price:,.0f} USD</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for warning in prediction_warnings:
            st.warning(warning)
        st.info("Compare this estimate with recent listings and use human review.")
    except ValueError as error:
        st.error(str(error))

st.divider()
metric_1, metric_2, metric_3, metric_4 = st.columns(4)
test_metrics = metadata["protected_test_comparison"]["random_forest"]
metric_1.metric("Protected-test MAE", f"${test_metrics['mae_usd']:,.0f}")
metric_2.metric("Protected-test R²", f"{test_metrics['r2']:.3f}")
metric_3.metric("Protected-test MAPE", f"{test_metrics['mape_percent']:.2f}%")
metric_4.metric("Modeling rows", f"{metadata['row_count']:,}")

with st.expander("Model scope and limitations"):
    st.markdown(
        """
        - Target: advertiser's USD asking price, not a verified transaction price.
        - Source: privacy-minimized public HATA apartment listing snapshot from August 2026.
        - Missing exact address, condition, renovation, building year, amenities, and legal status.
        - Reliability varies by district and is weaker for unusual luxury listings.
        - Do not use for lending, taxation, legal appraisal, or automated high-stakes decisions.
        """
    )

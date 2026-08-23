"""FastAPI inference service for the apartment asking-price model."""

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.model import load_artifact, predict_price

ARTIFACT_PATH = Path("artifacts/apartment_price_pipeline.joblib")


class ApartmentInput(BaseModel):
    """Validated raw apartment attributes accepted by the API."""

    district: str = Field(min_length=2, max_length=80, examples=["Chilonzor"])
    size_m2: float = Field(ge=15, le=1000, examples=[70])
    rooms: int = Field(ge=1, le=20, examples=[3])
    level: int = Field(ge=1, le=50, examples=[3])
    max_levels: int = Field(ge=1, le=50, examples=[5])
    is_new_building: bool = Field(default=False)


class PredictionOutput(BaseModel):
    """Stable JSON response contract for one asking-price estimate."""

    estimated_asking_price_usd: float
    currency: str = "USD"
    data_window: dict[str, str | None]
    reference_error_p80_usd: float
    warnings: list[str]
    disclaimer: str


@lru_cache(maxsize=1)
def get_artifact():
    """Load the serialized preprocessing/model pipeline once per worker."""
    return load_artifact(ARTIFACT_PATH)


app = FastAPI(
    title="Tashkent Apartment Price API",
    summary="Validated inference for a versioned Tashkent asking-price model.",
    version="1.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return service and model readiness."""
    artifact = get_artifact()
    return {"status": "ok", "model": artifact["metadata"]["model_name"]}


@app.get("/model-info")
def model_info() -> dict[str, object]:
    """Expose non-sensitive model scope and protected-test metrics."""
    metadata = get_artifact()["metadata"]
    return {
        "model": metadata["model_name"],
        "target": metadata["target"],
        "row_count": metadata["row_count"],
        "known_districts": metadata["known_districts"],
        "data_window": {
            "from": metadata["data_audit"].get("listing_date_min"),
            "to": metadata["data_audit"].get("listing_date_max"),
        },
        "reference_error_p80_usd": metadata["protected_test_absolute_error_quantiles"]["p80_usd"],
        "protected_test": metadata["protected_test_comparison"]["random_forest"],
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(payload: ApartmentInput) -> PredictionOutput:
    """Validate a raw record and return one asking-price estimate."""
    try:
        price, prediction_warnings = predict_price(
            get_artifact(),
            district=payload.district,
            size_m2=payload.size_m2,
            rooms=payload.rooms,
            level=payload.level,
            max_levels=payload.max_levels,
            is_new_building=int(payload.is_new_building),
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    metadata = get_artifact()["metadata"]
    return PredictionOutput(
        estimated_asking_price_usd=round(price, 2),
        data_window={
            "from": metadata["data_audit"].get("listing_date_min"),
            "to": metadata["data_audit"].get("listing_date_max"),
        },
        reference_error_p80_usd=round(
            metadata["protected_test_absolute_error_quantiles"]["p80_usd"], 2
        ),
        warnings=prediction_warnings,
        disclaimer="Advertised asking-price reference only; not a sale price or appraisal.",
    )

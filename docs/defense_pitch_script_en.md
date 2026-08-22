# Tashkent Apartment Price Predictor — exact five-minute speech

**Presenter:** Dilnura Hamdamova  
**Target duration:** 4:40–5:00  
**Main route:** PPT slides 1–7 → Colab during slide 6 → return to slide 7  
**Appendix:** Slides 8–10 only when evidence or Q&A is requested

## Slide 1 — Opening (0:00–0:30)

Good morning. I am Dilnura Hamdamova. My project is the Tashkent Apartment Price Predictor. It
estimates the advertised asking price of a Tashkent apartment using current August 2026 listing
attributes. The result is a reference for comparing advertisements; it is not a completed sale
price, a guarantee, or a legal appraisal.

## Slide 2 — User and ML task (0:30–1:15)

The intended users are buyers, sellers, agents, and analysts who need a consistent reference when
comparing apartment advertisements. This is a supervised regression task. The inputs are district,
apartment size, number of rooms, apartment floor, total building floors, and whether it is a new
building or resale property. The output is one estimated asking price in US dollars, together with
warnings for unseen or out-of-range values.

## Slide 3 — Data and preprocessing (1:15–2:10)

I collected a privacy-minimized snapshot from public HATA apartment listing pages on 22 August
2026. HATA did not provide a ready-made official CSV; the project collector created the dataset
from public listing pages. It excludes names, phone numbers, descriptions, and images. From 4,867
complete listings, fixed validation rules removed 257 invalid or misclassified rows. I then
removed 396 exact feature-and-target duplicates, leaving 4,214 modeling rows in 3,840
feature-fingerprint groups. Identical fingerprints remain in one split, and price per square metre
is excluded because it would leak the target.

<!-- PAGEBREAK -->

## Slide 4 — Models and selection (2:10–2:45)

I compared a median baseline, Log Ridge, Random Forest, and Gradient Boosting. Model selection used
five-fold group-safe cross-validation only on the development data. Random Forest had the lowest
cross-validation MAE at 31,298 dollars, compared with 33,545 for Gradient Boosting, 38,301 for Log
Ridge, and 55,604 for the median baseline. Therefore, Random Forest was selected before opening the
protected test result.

## Slide 5 — Unseen result and weakness (2:45–3:25)

On 835 protected unseen listings from 768 groups, Random Forest achieved MAE of 27,195 dollars,
RMSE of 58,887 dollars, R-squared of 0.681, and MAPE of 24.58 percent. The baseline test MAE was
50,900 dollars, so the selected model reduced MAE by 46.6 percent. However, the largest error was a
one-million-dollar Shayhontohur listing predicted near 234,461 dollars. This shows that luxury
premiums and property condition are not captured well. District reliability is also unequal.

## Slide 6 — Live Colab demo (3:25–4:20)

Say before leaving the PPT:

> Now I will show one real end-to-end prediction using the saved preprocessing and model pipeline.

Switch to the already-open Colab notebook. Show and run this input:

- District: Chilonzor
- Size: 70 square metres
- Rooms: 3
- Apartment floor: 3
- Building floors: 5
- Building type: resale

Then say:

> For this input, the model estimates an August 2026 asking price of approximately 97,098 US
> dollars. If I change the property to a new building, the result is approximately 103,647 dollars.
> The same pipeline also validates input: level 9 in a five-floor building produces a clear
> ValueError instead of a misleading prediction.

Return immediately to PPT slide 7.

## Slide 7 — Limitations, next step, and question (4:20–5:00)

The model is limited by a dated asking-price snapshot, source noise, market drift, missing exact
location, condition, renovation, building year, amenities, and legal status. It must not be used
for lending, taxation, or legal appraisal. The strongest next improvement is verified transaction
data with richer property features and a later time-based holdout. In conclusion, the project
provides a reproducible current asking-price reference with honest limitations. Thank you. I am
ready for one evidence-based question.

<!-- PAGEBREAK -->

## Offline backup sentence and command

If Colab or the internet fails, say:

> The network route is unavailable, so I will use the verified offline backup with the same saved
> pipeline.

Then run:

```bash
python -m src.predict --district Chilonzor --size 70 --rooms 3 --level 3 --max-levels 5
```

Expected output: `Estimated listing price: $97,098 USD`.

## One-line Q&A formula

Answer in this order: **direct answer → exact evidence path → limitation or next step**.

Example:

> I selected Random Forest because it had the lowest group-safe development CV MAE at 31,298
> dollars. The exact comparison is in reports/model_comparison.csv. Its trade-off is lower
> interpretability and a larger model size than Ridge.

## After the pitch — record real evidence

- Actual duration: ______ min ______ sec
- Demo: PASS / FAIL
- Question received: __________________________________________
- My live answer: ______________________________________________
- One answer weakness or revision: _____________________________

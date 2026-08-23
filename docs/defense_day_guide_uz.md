# Bugungi pitch uchun to‘liq qo‘llanma

Bu fayl EXTC4 worksheet tartibiga mos. Asosiy prezentatsiyada 1–7-slaydlar ishlatiladi;
8–10-slaydlar faqat savol yoki dalil so‘ralganda ochiladi. Maqsad: 4:40–5:00.

## Pitchdan oldin ochib qo‘yiladigan fayllar

1. `presentation/Tashkent_Apartment_Price_Defense.pptx` — Slide Show rejimida.
2. `demo.ipynb` — Colab’da ochilgan va runtime ulangan.
3. `docs/capstone_evidence_matrix.md` — dalil so‘ralsa ko‘rsatish uchun.
4. `reports/model_comparison.csv`, `reports/protected_test_metrics.csv` va
   `reports/largest_errors.csv` — savol-javob uchun.
5. Terminal — internet ishlamasa backup demo uchun.

Colab’da pitchdan oldin **Runtime → Run all** bosing. Natijalar ko‘ringach, demo input va output
celllariga qaytib qo‘ying. Pitch davomida kodni qatorma-qator tushuntirmang.

## Aynan aytiladigan 5 daqiqalik speech

### 0:00–0:30 — Slide 1: Opening

> Good morning. I am Dilnura Hamdamova. My project is the Tashkent Apartment Price Predictor.
> It estimates the advertised asking price of a Tashkent apartment using current August 2026
> listing attributes. The result is a reference for comparing advertisements; it is not a
> completed sale price, a guarantee, or a legal appraisal.

Ko‘rsatish: loyiha nomi, 4,214 modeling rows, Random Forest, test R² 0.681 va MAE $27,195.

### 0:30–1:15 — Slide 2: User and ML task

> The intended users are buyers, sellers, agents, and analysts who need a consistent reference
> when comparing apartment advertisements. This is a supervised regression task. The inputs are
> district, apartment size, number of rooms, apartment floor, total building floors, and whether
> it is a new building or resale property. The output is one estimated asking price in US dollars,
> together with warnings for unseen or out-of-range values.

Muhim jumla: target — **advertised asking price**, real sotilgan narx emas.

### 1:15–2:10 — Slide 3: Data and preprocessing

> I collected a privacy-minimized snapshot from public HATA apartment listing pages on 22 August
> 2026. HATA did not provide a ready-made official CSV; the project collector created the dataset
> from public listing pages. It excludes names, phone numbers, descriptions, and images. From
> 4,867 complete listings, fixed validation rules removed 257 invalid or misclassified rows. I
> then removed 396 exact feature-and-target duplicates, leaving 4,214 modeling rows in 3,840
> feature-fingerprint groups. Identical fingerprints remain in one split, and price per square
> metre is excluded because it would leak the target.

Dalil: `data/README.md`, `reports/data_audit.md`, `src/data.py`.

### 2:10–2:45 — Slide 4: Models

> I compared a median baseline, Log Ridge, Random Forest, and Gradient Boosting. Model selection
> used five-fold group-safe cross-validation only on the development data. Random Forest had the
> lowest cross-validation MAE at 31,298 dollars, compared with 33,545 for Gradient Boosting,
> 38,301 for Log Ridge, and 55,604 for the median baseline. Therefore, Random Forest was selected
> before opening the protected test result.

Dalil: `reports/model_comparison.csv`.

### 2:45–3:25 — Slide 5: Unseen result and weakness

> On 835 protected unseen listings from 768 groups, Random Forest achieved MAE of 27,195 dollars,
> RMSE of 58,887 dollars, R-squared of 0.681, and MAPE of 24.58 percent. The baseline test MAE was
> 50,900 dollars, so the selected model reduced MAE by 46.6 percent. However, the largest error
> was a one-million-dollar Shayhontohur listing predicted near 234,461 dollars. This shows that
> luxury premiums and property condition are not captured well. District reliability is also
> unequal.

Dalil: `reports/protected_test_metrics.csv`, `reports/largest_errors.csv`.

### 3:25–4:20 — Slide 6 + Colab: Live demo

Ayting:

> Now I will show one real end-to-end prediction using the saved preprocessing and model pipeline.

PPT’dan Colab’ga o‘ting. Quyidagi input cellini ko‘rsating:

- District: Chilonzor
- Size: 70 m²
- Rooms: 3
- Floor: 3
- Building floors: 5
- Building type: resale

Cellni ishga tushirib, natijani ko‘rsating:

> For this input, the model estimates an August 2026 asking price of approximately 97,098 US
> dollars. If I change the property to a new building, the result is approximately 103,647
> dollars. The same pipeline also validates input: level 9 in a five-floor building produces a
> clear ValueError instead of a misleading prediction.

So‘ng PPT’ga, 7-slaydga qayting.

### 4:20–5:00 — Slide 7: Limitations, next step, question

> The model is limited by a dated asking-price snapshot, source noise, market drift, missing exact
> location, condition, renovation, building year, amenities, and legal status. It must not be used
> for lending, taxation, or legal appraisal. The strongest next improvement is verified
> transaction data with richer property features and a later time-based holdout. In conclusion,
> the project provides a reproducible current asking-price reference with honest limitations.
> Thank you. I am ready for one evidence-based question.

## Live demo ishlamasa

Internet yoki Colab ishlamasa, buni yashirmang. Ayting:

> The network route is unavailable, so I will use the verified offline backup with the same saved
> pipeline.

Terminalda ishga tushiring:

```bash
python -m src.predict --district Chilonzor --size 70 --rooms 3 --level 3 --max-levels 5
```

Kutiladigan natija: `Estimated listing price: $97,098 USD`.

## Eng ehtimoliy savollar va qisqa javoblar

### Why did you choose Random Forest?

> It had the lowest group-safe development CV MAE at $31,298. The exact comparison is in
> `reports/model_comparison.csv`. Its trade-off is lower interpretability and larger model size
> than Ridge.

### Is this a real sale-price model?

> No. The target is the advertiser's asking price, not a verified completed transaction. This is
> stated in `data/README.md`. Verified transaction data is the main next improvement.

### Where did the dataset come from?

> I created a privacy-minimized snapshot from public HATA Tashkent apartment listing pages on 22
> August 2026. HATA did not give me an official ready-made CSV. The source and collector are in
> `data/README.md` and `scripts/collect_current_listings.py`.

### How did you prevent leakage?

> Identical apartment feature fingerprints stay in one holdout split and one CV fold. Recorded
> holdout and CV overlap are both zero in `artifacts/metrics.json`. I also excluded price per square
> metre because it directly contains the target.

### What is the biggest failure?

> A $1,000,000 Shayhontohur listing was predicted near $234,461. The exact row is in
> `reports/largest_errors.csv`. Missing luxury, condition, and exact-location signals are plausible
> limitations, but I cannot claim a single verified cause.

### Can the model predict future prices?

> No. It estimates asking prices relative to an August 2026 snapshot. A later market requires a
> new snapshot, retraining, and new evaluation, preferably with a time-based holdout.

## “Show Me Where” uchun uchta tayyor dalil

1. Current 2026 data: `data/apartment_listings_2026.csv` → `listing_date`, `collected_at_utc`;
   `data/README.md` → source and snapshot.
2. No identical-feature split leakage: `src/model.py` → group split and
   `StratifiedGroupKFold`; `artifacts/metrics.json` → `holdout_group_overlap: 0` and
   `cv_group_overlap_max: 0`.
3. Baseline improvement and failure: `reports/protected_test_metrics.csv` and first row of
   `reports/largest_errors.csv`.

Peer tekshirganidan keyin `docs/capstone_evidence_matrix.md` ichidagi jadvalga uning haqiqiy ismi,
sana va PASS/FAIL natijalarini yozing.

## Pitch tugashi bilan to‘ldiriladi

- Actual duration: ______ min ______ sec
- Demo: PASS / FAIL
- Question received: __________________________________________
- My live answer: ______________________________________________
- What I must improve or verify: _______________________________
- Partner name and three challenge results: ____________________

Bu joylar pitchdan oldin taxmin bilan to‘ldirilmaydi.

## EXTC4 yakuniy tekshiruv

- [x] Besh daqiqalik aniq pitch route tayyor.
- [x] User, input, target va output aniq.
- [x] Dataset, preprocessing, baseline va final approach ko‘rsatilgan.
- [x] Unseen-test natijasi, baseline taqqoslash, real xato va limitation bor.
- [x] Colab demo va offline backup route tayyor.
- [x] Sakkiz mezon exact evidence yo‘llariga bog‘langan.
- [x] Essential model, evaluation, demo va documentation dalillari mavjud.
- [x] Uchta peer challenge uchun dalillar tayyor.
- [x] Kamida uchta emas, oltitadan ko‘p Q&A javobi tayyor.
- [ ] Haqiqiy pitch vaqti va savol pitchdan keyin yoziladi.
- [ ] Peer/mentor/CI kabi tashqi dalillar faqat real bajarilgach belgilanadi.

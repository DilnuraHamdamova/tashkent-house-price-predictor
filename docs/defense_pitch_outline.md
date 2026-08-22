# Five-minute defense pitch — 2026 apartment listing prices

Use slides 1–7 as navigation, not a script. Target 4:40–5:00.

**Pitch package status for 22 August 2026: GREEN — READY TO PRESENT.** Open the PDF or PPTX,
keep `demo.ipynb` ready, and use the local CLI command under “Backup route” if the network fails.

| Time | Block | Exact note / evidence route | Rubric |
|---|---|---|---|
| 0:00–0:30 | Opening | “I am Dilnura Hamdamova. My project estimates the current advertised USD asking price of a Tashkent apartment from August 2026 listing attributes. It helps buyers, sellers, agents, and analysts compare advertisements; it is not a completed sale price or legal appraisal.” | 1 + 8 |
| 0:30–1:15 | User + ML task | “This is supervised regression. Inputs are district, size, rooms, apartment floor, building floors, and new-build/resale status. The output is one estimated 2026 asking price in USD plus an out-of-range warning.” | 1 + 5 + 8 |
| 1:15–2:10 | Data + approach | “I collected a privacy-minimized public HATA snapshot on 22 August 2026. From 4,867 complete listings, validity checks and 396 exact feature-plus-target duplicate removals leave 4,214 rows in 3,840 feature groups. Identical fingerprints stay in one split. I compare a median baseline, Log Ridge, Random Forest, and Gradient Boosting using five-fold group-safe development CV.” | 2 + 3 |
| 2:10–3:10 | Results + weakness | “Random Forest had the best CV MAE at $31,298. On 835 protected unseen listings it achieved MAE $27,195, RMSE $58,887, R² 0.681, and MAPE 24.58%, versus baseline MAE $50,900—a 46.6% improvement. Its largest miss is a $1 million Shayhontohur listing predicted near $234,461. Mirobod and Shayhontohur remain difficult.” | 4 + 7 + 8 |
| 3:10–4:20 | Showcase + live demo | Open `demo.ipynb` in Colab → Run all → show Chilonzor resale input → show about $97,098 → switch to new build → show about $103,647 → run invalid floor example → show clear validation error. Open README/demo evidence only if asked. | 5 + 6 + 8 |
| 4:20–5:00 | Close + question | “The strongest improvement is verified transaction data with exact neighborhood, condition, renovation, building year, legal status, and a later time-based holdout. This model is an August 2026 asking-price reference requiring human review. I am ready for one question.” | 7 + 8 |

## Backup route

If Colab/network is unavailable, open the committed notebook output and
`reports/clean_run_check.md`, then run:

```bash
python -m src.predict --district Chilonzor --size 70 --rooms 3 --level 3 --max-levels 5
```

Do not claim a failed live link works; state that the offline route is the backup evidence.

## Pitch log

| Attempt | Date | Duration | Demo | Question received | Answer weakness / revision |
|---|---|---:|---|---|---|
| 1 | __________ | _____ | PASS / FAIL | ____________________ | ____________________ |
| 2 | __________ | _____ | PASS / FAIL | ____________________ | ____________________ |

Immediately after today's pitch, fill Attempt 1 with the real duration, demo result, received
question, and one improvement. Do not estimate these in advance.

# Five-minute defense pitch

Use the deck as navigation, not as a script. Target 4:40–5:00 so one short question fits.

| Time | Block | Spoken line / action | Rubric link |
|---|---|---|---|
| 0:00–0:30 | Opening | “I am Dilnura Hamdamova. My Individual Project estimates historical Tashkent apartment asking prices. It supports buyers, sellers, agents, and analysts with a reference estimate; it is not a legal appraisal or current sale-price guarantee.” | Criteria 1, 7, 8 |
| 0:30–1:15 | User + ML task | “This is supervised regression. The raw inputs are district, size, rooms, apartment floor, building floors, latitude, and longitude. The output is one estimated 2019 listing price in USD, plus a warning for unseen or out-of-range input.” | Criteria 1, 5 |
| 1:15–2:10 | Data + approach | “The CC0 dataset has 7,421 uybor.uz listings from 2019. I remove 696 exact duplicates before splitting, leaving 6,725 rows. I protect 20% for final testing, stratify by district, and compare a median baseline, Log Ridge, Random Forest, and Gradient Boosting with five-fold training-only CV. Encoding and scaling remain inside sklearn pipelines to prevent leakage.” | Criteria 2, 3 |
| 2:10–3:10 | Results + weakness | “Random Forest had the best CV MAE at $11,108. On 1,345 unseen test rows it achieved MAE $10,573, RMSE $23,162, R² 0.745, and MAPE 16.66%, versus baseline MAE $24,217. The largest weakness is unusual luxury data: one $800,000 Mirobod listing was predicted near $354,962. Bektemir and Yangihayot are also too sparse for strong conclusions.” | Criteria 4, 7, 8 |
| 3:10–4:20 | Live demo | Open `demo.ipynb` in Colab → run setup/load cells → show the Chilonzor 70 m² input → run prediction → show about $53,532 and no warnings → run invalid floor example → show the clear validation error. Do not tour source code unless asked. | Criteria 5, 6, 8 |
| 4:20–5:00 | Close + question | “The strongest improvement is current transaction data with condition, building age, legal status, and time-aware evaluation. The current model is an educational historical reference and requires human review. I am ready for one question.” | Criteria 7, 8 |

## Backup route

If Colab/network is unavailable, open the committed `demo.ipynb` and `reports/clean_run_check.md`, then run the same `python -m src.predict ...` command locally. Explain that the backup proves the route but does not justify claiming a failed live link works.

## Rehearsal log

| Attempt | Date | Duration | Demo worked? | Main correction |
|---|---|---:|---|---|
| 1 | __________ | _____ | PASS / FAIL | ____________________ |
| 2 | __________ | _____ | PASS / FAIL | ____________________ |

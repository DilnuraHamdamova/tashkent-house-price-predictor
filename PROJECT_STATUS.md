# Capstone readiness status

**Project:** 2026 Tashkent Apartment Listing Price Predictor
**Track:** Individual Project Track
**Technical model status:** GREEN
**Today's pitch package:** GREEN — READY TO PRESENT
**Overall defense readiness:** YELLOW

## Latest verified model evidence

**Snapshot date:** 22 August 2026 (Asia/Samarkand)

- Collected a privacy-minimized current HATA apartment-sale snapshot.
- Parsed 4,867 unique complete-feature listings dated 4–21 August 2026.
- Removed 257 invalid/category/currency/unit rows and 396 exact feature+target duplicates.
- Used 4,214 modeling rows in 3,840 identical-feature groups.
- Kept identical feature fingerprints in one holdout and CV group.
- Compared Median, Log Ridge, Random Forest, and Gradient Boosting using group-safe CV.
- Selected Random Forest by development CV MAE ($31,298).
- Protected 835-row test: MAE $27,195; RMSE $58,887; R² 0.681; MAPE 24.58%.
- Baseline test MAE $50,900; selected model improves MAE by 46.6%.
- Checked resale demo example at approximately $97,098 USD.
- Eight automated tests pass, Ruff passes, and all three notebook code-cell sequences complete locally.

## Completed repository evidence

- [x] Current dated apartment asking-price problem, user, task, scope, and measurable criteria
- [x] Privacy-minimized source snapshot and collector
- [x] Asking-price target named honestly; no sale-price claim
- [x] Validity, missing-field, duplicate, and feature-group leakage controls
- [x] Baseline plus three trained approaches
- [x] Group-safe development CV and protected unseen test
- [x] MAE, RMSE, R², MAPE, baseline comparison, largest errors, and district slices
- [x] Saved preprocessing/model pipeline with input validation and OOD warnings
- [x] Official filename set for pitch, evidence matrix, question bank, and action plan
- [x] Exact English speech, Uzbek presenter instructions, Colab handoff, and offline demo backup
- [x] Project-specific Responsible AI and limitations

## Remaining external or final-build confirmations

- [ ] Written source-use/redistribution confirmation or mentor-approved private snapshot handling
- [x] Updated Individual Project Brief generated for the 2026 apartment scope
- [ ] Mentor approval of the revised Project Brief
- [ ] Fresh browser-based Colab run by a named peer
- [x] Current 2026 revision committed/pushed; public CI run 32561644942 passed
- [ ] Two timed pitch rehearsals
- [ ] One three-claim “Show Me Where” peer challenge
- [ ] Final defense attendance and personal Q&A

## Honest gate

**YELLOW.** The current-data model and protected evaluation are implemented. Source-use handling,
fresh external reproduction, presentation rehearsal, peer challenge, mentor confirmation, and the
live defense require real external evidence and cannot be pre-marked Green.

The pitch package itself is **GREEN** for today's presentation: the timed route, deck, local demo,
backup route, results, failure example, evidence matrix, and Q&A answers are present and verified.
After the live session, record the actual duration, received question, and peer result; those facts
determine whether the official final gate can be changed from YELLOW to GREEN.

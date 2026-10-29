# Synthetic Source Data — Provenance and Reproduction

This portfolio does **not** use an external public dataset. `data/orders_raw.csv` and the six dimension CSVs were supplied as synthetic fictional-business inputs in the project archive. They model a two-year FMCG activity sample with plausible product, customer, channel, geography, distributor, discount and return fields. Sixty exact duplicate source records were intentionally included to support a repeatable data-quality exercise.

The archive did not include an original data-generation script or a verifiable seed. To avoid inventing a generation algorithm or seed after the fact, this project does not claim byte-for-byte regeneration of the original source data. The checked-in source CSVs are the authoritative baseline inputs. Re-run `python python/aarohan_analysis.py` to reproduce the cleaning, KPI calculations, summaries, and validation checks from the provided inputs; the script reads the raw source and does not overwrite it.

For interview or public portfolio use, state that the dataset is **synthetic**, not actual employer/client data. Do not present the findings as real company performance or the monetary values as a specific currency.

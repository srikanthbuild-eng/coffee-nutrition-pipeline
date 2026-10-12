# Drink Nutrition Pipeline

Calculates the true nutrition of any customized Starbucks drink on Databricks.

The Starbucks app recalculates nutrition when you change the size, but not when you change the
number of syrup pumps. This project models every drink as a recipe of components (espresso, milk,
syrup, sauce, toppings), like a bill of materials, so nutrition is always **calculated** from what
was actually ordered rather than looked up from a fixed label.

Phase 2 joins logged intake (caffeine, sugar, timing) to Whoop sleep, HRV and recovery data.

## Status

| Step | What | State |
| --- | --- | --- |
| Weeks 1-2 | Foundation: bundle, schemas, landing volume, bronze load, CI | in progress |
| Weeks 3-4 | Silver pipeline with expectations, modification logic, gold nutrition | planned |
| Week 5 | Streamlit order builder as a Databricks App | planned |
| Week 6 | Label capture, validation, calibration, dashboard | planned |

## Stack

Databricks (Free Edition, serverless) · Unity Catalog · Delta Lake · COPY INTO ·
Databricks Asset Bundles · GitHub Actions · pytest

## Repo layout

```
databricks.yml            bundle definition (targets, variables)
resources/                one YAML file per job
src/setup/                schemas and landing volume
src/bronze/               raw loads into Delta
seed_data/                drinks, recipes, ingredients + generate_seed.py
scripts/                  helper scripts (upload to the volume)
tests/                    pytest checks run locally and in CI
docs/                     runbooks and design notes
```

## Run it

See [docs/week1_runbook.md](docs/week1_runbook.md).

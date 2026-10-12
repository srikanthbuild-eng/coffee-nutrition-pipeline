# Week 1 runbook: from seed files to bronze tables

By the end you will have three schemas, a landing volume, eight bronze Delta tables,
a job that loads them without ever duplicating rows, and the repo on GitHub with CI.

Run every command from the project root (`~/projects/drink-nutrition-pipeline`).

---

## Step 1 · Point the bundle at your workspace

Open `databricks.yml` and replace the `host:` line with your workspace URL:

```yaml
      host: https://dbc-xxxxxxxx-xxxx.cloud.databricks.com
```

Then check the bundle is valid:

```bash
databricks bundle validate
```

**Notice:** it prints the bundle name, the target (`dev`) and your workspace. If it complains
about the host or authentication, re-run `databricks auth login --host <your-url>`.

## Step 2 · Run the local tests

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

**Notice:** 9 tests pass. They are the seed data's foreign keys and unique constraints,
checked before anything leaves your laptop.

## Step 3 · Deploy

```bash
databricks bundle deploy
```

**Notice:** in the workspace, open **Jobs & Pipelines**. You'll see two jobs named
`[dev <your name>] drink_nutrition_setup` and `[dev <your name>] drink_nutrition_bronze_load`.
The prefix comes from `mode: development` in `databricks.yml`.

## Step 4 · Create the schemas and volume

```bash
databricks bundle run setup_job
```

**Notice:** open **Catalog → workspace**. You now have `bronze`, `silver` and `gold` schemas,
and under `bronze` a volume called `landing`.

## Step 5 · Upload the seed files

```bash
chmod +x scripts/upload_seeds.sh
./scripts/upload_seeds.sh
```

**Notice:** in **Catalog → workspace → bronze → landing**, the files sit in a folder
named `seed/load_date=<today>`.

## Step 6 · Load bronze

```bash
databricks bundle run bronze_load_job
```

**Notice:** the run output shows rows inserted per table, then "All bronze tables match the seed files."

## Step 7 · Look at the data

Open the **SQL editor** and run:

```sql
SELECT * FROM workspace.bronze.drinks LIMIT 10;

DESCRIBE workspace.bronze.recipes;

SELECT drink_id, size_id, ingredient_id, quantity
FROM workspace.bronze.recipes
WHERE drink_id = 'caramel_macchiato' AND size_id = 'grande';
```

**Notice:** every column is a `string`, including `quantity`. That is deliberate: bronze keeps
data exactly as it arrived. Silver will cast types and reject bad values.

## Step 8 · Prove it is idempotent

Run the load again without uploading anything new:

```bash
databricks bundle run bronze_load_job
```

**Notice:** every table shows **0 rows inserted**, and the row-count check still passes.
`COPY INTO` remembered the files it already loaded.

## Step 9 · Put it on GitHub

```bash
git add .
git commit -m "Week 1: bundle, schemas, landing volume, bronze load, CI"
gh repo create drink-nutrition-pipeline --public --source=. --push
```

**Notice:** on GitHub, open the **Actions** tab. The `ci` workflow runs the same pytest checks
on every push.

---

## Check your understanding

Try answering these before week 2; they are the questions an interviewer would ask.

1. Why are bronze columns all strings instead of numbers?
2. What would happen if you ran `./scripts/upload_seeds.sh` again **tomorrow** and then the load job?
   What about running both again **today**?
3. The SSIS equivalent of `COPY INTO`'s file tracking is usually a control table you build yourself.
   What does having it built in save you?
4. Why does the job fail on a row-count mismatch instead of just printing a warning?

## If something goes wrong

| Symptom | Likely cause |
| --- | --- |
| `bundle validate` mentions host or auth | Host in `databricks.yml` differs from the one you logged in to |
| Upload script says the path doesn't exist | Step 4 (setup job) hasn't run yet |
| Load job fails with a row-count mismatch | Seed files changed; regenerate with `python3 seed_data/generate_seed.py` and update `EXPECTED_ROWS` |
| Daily compute limit reached | Free Edition quota; work resumes when it resets |

Paste any error into the chat and we'll fix it together.

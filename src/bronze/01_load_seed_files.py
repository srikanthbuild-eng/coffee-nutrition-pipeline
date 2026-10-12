# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Load seed files into bronze
# MAGIC
# MAGIC Loads each CSV from the landing volume into its own bronze Delta table with `COPY INTO`.
# MAGIC
# MAGIC **Why COPY INTO:** it remembers which files it has already loaded and skips them on the
# MAGIC next run. Re-running the job never duplicates rows, which makes it *idempotent*: the same
# MAGIC idea as an SSIS package that tracks processed files, but built into the SQL engine.
# MAGIC
# MAGIC **Bronze rules:**
# MAGIC - Every column is loaded as a string, exactly as it appears in the file. Typing happens in silver.
# MAGIC - Three metadata columns are added: `_load_date` (from the folder name), `_source_file`, `_ingested_at`.
# MAGIC - Each upload lands in a new `load_date=YYYY-MM-DD` folder, so bronze keeps every version
# MAGIC   of the seed data. Silver will pick the latest one.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace")
catalog = dbutils.widgets.get("catalog")

landing = f"/Volumes/{catalog}/bronze/landing/seed"

# bronze table name -> file name in each load_date folder
TABLES = {
    "sizes": "sizes.csv",
    "ingredients": "ingredients.csv",
    "drinks": "drinks.csv",
    "recipes": "recipes.csv",
    "modifiers": "modifiers.csv",
    "orders": "orders_sample.csv",
    "order_modifications": "order_modifications_sample.csv",
    "captured_labels": "published_labels_template.csv",
}

print(f"Reading from: {landing}")
display(dbutils.fs.ls(landing))

# COMMAND ----------

results = []

for table, file_name in TABLES.items():
    target = f"{catalog}.bronze.{table}"

    # A table with no columns: COPY INTO infers the columns from the file on the first load.
    spark.sql(f"CREATE TABLE IF NOT EXISTS {target}")

    copy_result = spark.sql(
        f"""
        COPY INTO {target}
        FROM (
            SELECT
                *,
                regexp_extract(_metadata.file_path, 'load_date=([0-9-]+)', 1) AS _load_date,
                _metadata.file_name                                         AS _source_file,
                current_timestamp()                                         AS _ingested_at
            FROM '{landing}'
        )
        FILEFORMAT = CSV
        PATTERN = 'load_date=*/{file_name}'
        FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false')
        COPY_OPTIONS ('mergeSchema' = 'true')
        """
    ).first().asDict()

    inserted = copy_result.get("num_inserted_rows", copy_result.get("num_affected_rows"))
    results.append((table, file_name, int(inserted or 0)))
    print(f"{target:45} <- {file_name:35} rows inserted: {inserted}")

display(spark.createDataFrame(results, "table string, file string, rows_inserted long"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Check: latest load matches the seed files
# MAGIC
# MAGIC Counts rows in the most recent `_load_date` of each table and compares them with the
# MAGIC row counts of the files `generate_seed.py` produced. A mismatch fails the job, so a bad
# MAGIC load never goes unnoticed.

# COMMAND ----------

EXPECTED_ROWS = {
    "sizes": 10,
    "ingredients": 64,
    "drinks": 70,
    "recipes": 736,
    "modifiers": 8,
    "orders": 5,
    "order_modifications": 9,
    "captured_labels": 33,
}

problems = []
for table, expected in EXPECTED_ROWS.items():
    actual = spark.sql(
        f"""
        SELECT count(*) AS n
        FROM {catalog}.bronze.{table}
        WHERE _load_date = (SELECT max(_load_date) FROM {catalog}.bronze.{table})
        """
    ).first()["n"]
    status = "ok" if actual == expected else "MISMATCH"
    print(f"{table:22} expected {expected:4}  actual {actual:4}  {status}")
    if actual != expected:
        problems.append(table)

if problems:
    raise ValueError(f"Row counts do not match the seed files for: {problems}")
print("All bronze tables match the seed files.")

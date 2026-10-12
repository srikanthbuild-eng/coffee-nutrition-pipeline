# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Create schemas and the landing volume
# MAGIC
# MAGIC Creates the three medallion schemas inside the catalog, plus a **volume**: a governed
# MAGIC folder in Unity Catalog where raw files land before they are loaded into tables.
# MAGIC
# MAGIC Every statement uses `IF NOT EXISTS`, so this notebook is safe to run any number of times.
# MAGIC
# MAGIC | Object | Purpose |
# MAGIC | --- | --- |
# MAGIC | `bronze` schema | raw data exactly as it arrived, plus load metadata |
# MAGIC | `silver` schema | cleaned, typed tables and the order-modification logic |
# MAGIC | `gold` schema | analytics tables: nutrition per order, daily intake, label validation |
# MAGIC | `bronze.landing` volume | where the upload script puts CSV files |

# COMMAND ----------

# Widgets are notebook parameters. The job passes `catalog` in from databricks.yml,
# and the default lets you also run this notebook by hand.
dbutils.widgets.text("catalog", "workspace")
catalog = dbutils.widgets.get("catalog")
print(f"Using catalog: {catalog}")

# COMMAND ----------

schemas = {
    "bronze": "Raw data exactly as received, with load metadata. Append-only.",
    "silver": "Cleaned, typed tables and final recipes per order.",
    "gold": "Analytics tables: nutrition per order, daily intake, label validation.",
}

for schema, comment in schemas.items():
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema} COMMENT '{comment}'")
    print(f"Schema ready: {catalog}.{schema}")

# COMMAND ----------

spark.sql(
    f"""
    CREATE VOLUME IF NOT EXISTS {catalog}.bronze.landing
    COMMENT 'Landing zone for raw files. Each upload goes into its own load_date=YYYY-MM-DD folder.'
    """
)
print(f"Volume ready: /Volumes/{catalog}/bronze/landing")

# COMMAND ----------

display(spark.sql(f"SHOW SCHEMAS IN {catalog}"))

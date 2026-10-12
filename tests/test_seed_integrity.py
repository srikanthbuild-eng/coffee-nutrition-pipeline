"""
Local checks on the seed CSVs, run with `pytest` before anything is uploaded.

These are the same rules a database would enforce with foreign keys and unique
constraints. Catching a broken seed file here is cheaper than finding it in a
failed Databricks job.
"""
import csv
from collections import Counter
from pathlib import Path

import pytest

SEED = Path(__file__).resolve().parents[1] / "seed_data"


def read(name):
    with open(SEED / name, newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def seed():
    return {
        "sizes": read("sizes.csv"),
        "ingredients": read("ingredients.csv"),
        "drinks": read("drinks.csv"),
        "recipes": read("recipes.csv"),
        "modifiers": read("modifiers.csv"),
        "orders": read("orders_sample.csv"),
        "order_mods": read("order_modifications_sample.csv"),
        "labels": read("published_labels_template.csv"),
    }


def ids(rows, key):
    return {r[key] for r in rows}


def test_primary_keys_are_unique(seed):
    for table, key in [("sizes", "size_id"), ("ingredients", "ingredient_id"),
                       ("drinks", "drink_id"), ("orders", "order_id")]:
        dupes = [k for k, n in Counter(r[key] for r in seed[table]).items() if n > 1]
        assert not dupes, f"duplicate {key} in {table}: {dupes}"


def test_recipe_grain_is_unique(seed):
    keys = Counter((r["drink_id"], r["size_id"], r["ingredient_id"]) for r in seed["recipes"])
    dupes = [k for k, n in keys.items() if n > 1]
    assert not dupes, f"duplicate drink/size/ingredient rows: {dupes[:5]}"


def test_recipes_reference_existing_rows(seed):
    drinks, sizes, ingredients = ids(seed["drinks"], "drink_id"), ids(seed["sizes"], "size_id"), ids(seed["ingredients"], "ingredient_id")
    for r in seed["recipes"]:
        assert r["drink_id"] in drinks, r
        assert r["size_id"] in sizes, r
        assert r["ingredient_id"] in ingredients, r


def test_every_available_size_has_a_recipe(seed):
    have = {(r["drink_id"], r["size_id"]) for r in seed["recipes"]}
    for d in seed["drinks"]:
        for size in d["available_sizes"].split("|"):
            assert (d["drink_id"], size) in have, f"{d['drink_id']} has no recipe for {size}"


def test_default_milk_is_in_the_recipe(seed):
    recipe_ingredients = {(r["drink_id"], r["ingredient_id"]) for r in seed["recipes"]}
    for d in seed["drinks"]:
        if d["default_milk_id"]:
            assert (d["drink_id"], d["default_milk_id"]) in recipe_ingredients, d["drink_id"]


def test_quantities_and_nutrition_are_not_negative(seed):
    for r in seed["recipes"]:
        assert float(r["quantity"]) > 0, r
    for i in seed["ingredients"]:
        for col in ["calories", "total_fat_g", "saturated_fat_g", "carbs_g", "sugar_g", "protein_g", "caffeine_mg"]:
            assert float(i[col]) >= 0, (i["ingredient_id"], col)


def test_confidence_values_are_known(seed):
    assert ids(seed["ingredients"], "confidence") <= {"high", "medium", "low"}


def test_sample_orders_reference_valid_drinks_sizes_and_modifiers(seed):
    drinks, ingredients = ids(seed["drinks"], "drink_id"), ids(seed["ingredients"], "ingredient_id")
    modifier_types = ids(seed["modifiers"], "modifier_type")
    available = {d["drink_id"]: set(d["available_sizes"].split("|")) for d in seed["drinks"]}
    order_ids = ids(seed["orders"], "order_id")
    for o in seed["orders"]:
        assert o["drink_id"] in drinks, o
        assert o["size_id"] in available[o["drink_id"]], o
    for m in seed["order_mods"]:
        assert m["order_id"] in order_ids, m
        assert m["modifier_type"] in modifier_types, m
        assert m["ingredient_id"] in ingredients, m


def test_row_counts_match_bronze_expectations(seed):
    # Keep in sync with EXPECTED_ROWS in src/bronze/01_load_seed_files.py
    expected = {"sizes": 10, "ingredients": 64, "drinks": 70, "recipes": 736, "modifiers": 8,
                "orders": 5, "order_mods": 9, "labels": 33}
    actual = {k: len(v) for k, v in seed.items()}
    assert actual == expected

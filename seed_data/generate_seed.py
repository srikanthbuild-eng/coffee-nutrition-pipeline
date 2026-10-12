"""
Seed data generator for the Drink Nutrition Pipeline (phase 1).

Builds component-level seed tables for the Starbucks US beverage menu:
  sizes.csv, ingredients.csv, drinks.csv, recipes.csv, modifiers.csv,
  orders_sample.csv, order_modifications_sample.csv,
  published_labels_template.csv

All nutrition values are per unit of the ingredient and are ESTIMATES.
`confidence` says how much to trust each one; the pipeline's calibration
step compares calculated defaults with official labels you capture and
corrects these values over time.
"""
import csv
import os

OUT = "seed_data"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- sizes
SIZES = [
    # size_id, size_name, volume_fl_oz, size_family
    ("short", "Short", 8, "cup"),
    ("tall", "Tall", 12, "cup"),
    ("grande", "Grande", 16, "cup"),
    ("venti_hot", "Venti (hot)", 20, "cup"),
    ("venti_iced", "Venti (iced)", 24, "cup"),
    ("trenta", "Trenta", 30, "cup"),
    ("solo", "Solo", 1, "espresso"),
    ("doppio", "Doppio", 2, "espresso"),
    ("triple", "Triple", 3, "espresso"),
    ("quad", "Quad", 4, "espresso"),
]

# ---------------------------------------------------------------- ingredients
# id, name, category, unit, kcal, fat, sat_fat, carbs, sugar, protein, caffeine_mg, confidence, note
I = []
def ing(*row):
    I.append(row)

# espresso
ing("espresso_signature", "Signature Espresso", "espresso", "shot", 5, 0, 0, 1, 0, 0, 75, "high", "")
ing("espresso_blonde", "Blonde Espresso", "espresso", "shot", 5, 0, 0, 1, 0, 0, 85, "high", "")
ing("espresso_decaf", "Decaf Espresso", "espresso", "shot", 5, 0, 0, 1, 0, 0, 10, "low", "decaf caffeine varies")
ing("espresso_ristretto", "Signature Espresso (ristretto pull)", "espresso", "shot", 5, 0, 0, 1, 0, 0, 75, "medium", "used in flat white")
# brewed / cold coffee (per fl oz of finished coffee)
ing("brewed_pike_place", "Pike Place Roast", "coffee_base", "fl_oz", 0.3, 0, 0, 0, 0, 0.05, 19.4, "high", "grande ~310 mg")
ing("brewed_blonde", "Blonde Roast", "coffee_base", "fl_oz", 0.3, 0, 0, 0, 0, 0.05, 22.5, "high", "grande ~360 mg")
ing("brewed_dark", "Dark Roast", "coffee_base", "fl_oz", 0.3, 0, 0, 0, 0, 0.05, 16.25, "high", "grande ~260 mg")
ing("brewed_decaf", "Decaf Pike Place Roast", "coffee_base", "fl_oz", 0.3, 0, 0, 0, 0, 0.05, 1.6, "medium", "")
ing("iced_coffee_base", "Iced Coffee", "coffee_base", "fl_oz", 0.4, 0, 0, 0, 0, 0, 13.75, "medium", "grande ~165 mg")
ing("cold_brew_base", "Cold Brew", "coffee_base", "fl_oz", 0.4, 0, 0, 0, 0, 0, 17.1, "medium", "grande ~205 mg")
ing("nitro_cold_brew_base", "Nitro Cold Brew", "coffee_base", "fl_oz", 0.3, 0, 0, 0, 0, 0, 16.6, "medium", "grande ~265 mg")
ing("hot_water", "Hot Water", "water", "fl_oz", 0, 0, 0, 0, 0, 0, 0, "high", "")
ing("cold_water", "Water", "water", "fl_oz", 0, 0, 0, 0, 0, 0, 0, "high", "")
# milks (per fl oz)
ing("milk_whole", "Whole Milk", "milk", "fl_oz", 18.6, 1.0, 0.57, 1.5, 1.5, 0.96, 0, "high", "")
ing("milk_2pct", "2% Milk", "milk", "fl_oz", 15.3, 0.6, 0.38, 1.5, 1.5, 1.0, 0, "high", "default milk for most espresso drinks")
ing("milk_nonfat", "Nonfat Milk", "milk", "fl_oz", 10.4, 0.03, 0.02, 1.5, 1.5, 1.0, 0, "high", "")
ing("milk_breve", "Half & Half (Breve)", "milk", "fl_oz", 39, 3.5, 2.2, 1.3, 1.3, 0.9, 0, "medium", "")
ing("heavy_cream", "Heavy Cream", "milk", "fl_oz", 100, 11, 7, 0.8, 0.8, 0.85, 0, "medium", "")
ing("milk_oat", "Oatmilk", "milk", "fl_oz", 17.5, 0.88, 0.1, 2.0, 0.88, 0.38, 0, "medium", "")
ing("milk_almond", "Almondmilk", "milk", "fl_oz", 7.5, 0.31, 0, 1.0, 0.5, 0.13, 0, "medium", "")
ing("milk_coconut", "Coconutmilk", "milk", "fl_oz", 10, 0.63, 0.56, 1.0, 0.88, 0.06, 0, "medium", "")
ing("milk_soy", "Soymilk", "milk", "fl_oz", 16.3, 0.5, 0.06, 1.9, 1.6, 0.88, 0, "medium", "vanilla soy")
ing("vanilla_sweet_cream", "Vanilla Sweet Cream", "cream", "fl_oz", 65, 5, 3.5, 4, 4, 1, 0, "low", "also the base of cold foam")
# syrups (per pump)
for sid, name in [("syrup_classic", "Classic Syrup"), ("syrup_vanilla", "Vanilla Syrup"),
                  ("syrup_caramel", "Caramel Syrup"), ("syrup_hazelnut", "Hazelnut Syrup"),
                  ("syrup_toffee_nut", "Toffee Nut Syrup"), ("syrup_cinnamon_dolce", "Cinnamon Dolce Syrup"),
                  ("syrup_raspberry", "Raspberry Syrup"), ("syrup_peppermint", "Peppermint Syrup")]:
    ing(sid, name, "syrup", "pump", 20, 0, 0, 5, 5, 0, 0, "medium", "")
ing("syrup_brown_sugar", "Brown Sugar Syrup", "syrup", "pump", 20, 0, 0, 5, 5, 0, 0, "low", "label suggests fewer kcal per pump")
ing("syrup_sf_vanilla", "Sugar-Free Vanilla Syrup", "syrup", "pump", 0, 0, 0, 0.5, 0, 0, 0, "medium", "")
# sauces (per pump)
ing("sauce_mocha", "Mocha Sauce", "sauce", "pump", 25, 0.75, 0.5, 6, 5, 1, 6, "medium", "")
ing("sauce_white_mocha", "White Chocolate Mocha Sauce", "sauce", "pump", 45, 1.0, 0.7, 8.5, 8.5, 0.5, 0, "low", "")
ing("sauce_pumpkin_spice", "Pumpkin Spice Sauce", "sauce", "pump", 33, 0.2, 0.1, 7.5, 7, 0.2, 0, "low", "seasonal")
ing("sauce_dark_caramel", "Dark Caramel Sauce", "sauce", "pump", 30, 1, 0.6, 5, 5, 0, 0, "low", "")
# toppings (per serving, sized to a grande)
ing("whipped_cream", "Whipped Cream", "topping", "serving", 90, 9, 6, 3, 3, 0.5, 0, "medium", "1 serving = grande portion")
ing("caramel_drizzle", "Caramel Drizzle", "topping", "serving", 15, 0.5, 0.3, 2, 2, 0, 0, "medium", "")
ing("mocha_drizzle", "Mocha Drizzle", "topping", "serving", 10, 0.3, 0.2, 2, 1.5, 0, 0, "low", "")
ing("cinnamon_dolce_topping", "Cinnamon Dolce Topping", "topping", "serving", 5, 0, 0, 1, 1, 0, 0, "low", "")
ing("pumpkin_spice_topping", "Pumpkin Spice Topping", "topping", "serving", 0, 0, 0, 0, 0, 0, 0, "medium", "")
ing("cinnamon_powder", "Cinnamon Powder", "topping", "serving", 0, 0, 0, 0, 0, 0, 0, "high", "")
ing("cookie_crumble_topping", "Chocolate Cookie Grind", "topping", "serving", 30, 1.5, 0.5, 4, 2, 0, 0, "low", "")
ing("caramel_crunch_topping", "Caramel Crunch Topping", "topping", "serving", 30, 1, 0.5, 5, 4, 0, 0, "low", "")
ing("frap_chips", "Frappuccino Chips", "inclusion", "scoop", 30, 1.5, 1, 4, 3, 0.5, 2, "low", "")
# frappuccino components
ing("frap_coffee_base", "Coffee Frappuccino Syrup", "frap_base", "pump", 35, 0, 0, 9, 9, 0, 0, "medium", "")
ing("frap_creme_base", "Creme Frappuccino Syrup", "frap_base", "pump", 35, 0, 0, 9, 9, 0, 0, "medium", "")
ing("frap_roast", "Frappuccino Roast", "coffee_base", "pump", 5, 0, 0, 1, 0, 0, 32, "medium", "grande coffee frap ~95 mg")
ing("vanilla_bean_powder", "Vanilla Bean Powder", "inclusion", "scoop", 20, 0, 0, 5, 5, 0, 0, "low", "")
ing("strawberry_puree", "Strawberry Puree", "inclusion", "pump", 25, 0, 0, 6, 5, 0, 0, "low", "")
# tea
ing("chai_concentrate", "Chai Concentrate", "tea", "pump", 27, 0, 0, 7, 7, 0, 24, "medium", "")
ing("matcha_powder", "Matcha Powder (unsweetened)", "tea", "scoop", 5, 0, 0, 1, 0, 0.3, 20, "low", "recipe reportedly moved to unsweetened matcha + classic in 2025; verify")
ing("tea_bag_black", "Black Tea Bag (Royal English Breakfast / Earl Grey)", "tea", "bag", 0, 0, 0, 0, 0, 0, 40, "medium", "")
ing("tea_bag_green", "Green Tea Bag (Emperor's Clouds & Mist / Jade Citrus Mint)", "tea", "bag", 0, 0, 0, 0, 0, 0, 16, "low", "")
ing("tea_bag_herbal", "Herbal Tea Bag (Mint Majesty / Peach Tranquility)", "tea", "bag", 0, 0, 0, 0, 0, 0, 0, "high", "")
ing("iced_black_tea_base", "Iced Black Tea", "tea", "fl_oz", 0, 0, 0, 0, 0, 0, 3.1, "medium", "grande ~25 mg")
ing("iced_green_tea_base", "Iced Green Tea", "tea", "fl_oz", 0, 0, 0, 0, 0, 0, 3.1, "medium", "grande ~25 mg")
ing("iced_passion_tango_base", "Iced Passion Tango Tea", "tea", "fl_oz", 0, 0, 0, 0, 0, 0, 0, "high", "")
ing("lemonade", "Lemonade", "juice", "fl_oz", 12, 0, 0, 3, 3, 0, 0, "medium", "")
# refreshers
ing("refresher_strawberry_acai", "Strawberry Acai Refresher Base", "refresher_base", "fl_oz", 15, 0, 0, 3.5, 3.2, 0, 7.5, "medium", "grande ~45 mg")
ing("refresher_mango_dragonfruit", "Mango Dragonfruit Refresher Base", "refresher_base", "fl_oz", 15, 0, 0, 3.5, 3.2, 0, 7.5, "medium", "grande ~45 mg")
ing("strawberry_inclusion", "Freeze-Dried Strawberries", "inclusion", "scoop", 5, 0, 0, 1, 1, 0, 0, "medium", "")
ing("dragonfruit_inclusion", "Freeze-Dried Dragonfruit", "inclusion", "scoop", 5, 0, 0, 1, 1, 0, 0, "medium", "")

ING_IDS = {r[0] for r in I}
ING_UNIT = {r[0]: r[3] for r in I}

# ---------------------------------------------------------------- drinks + recipes
DRINKS = []   # drink_id, name, category, temperature, default_milk_id, sizes, menu_status, verify_current_menu, notes
RECIPES = []  # drink_id, size_id, ingredient_id, quantity, unit, component_role

HOT = ["short", "tall", "grande", "venti_hot"]
ICED = ["tall", "grande", "venti_iced"]
COLD = ["tall", "grande", "venti_iced", "trenta"]
ESP = ["solo", "doppio"]

def drink(did, name, cat, temp, sizes, comps, milk=None, status="core", verify="N", notes=""):
    """comps: list of (ingredient_id, role, {size: qty})"""
    DRINKS.append((did, name, cat, temp, milk or "", "|".join(sizes), status, verify, notes))
    for ing_id, role, qty in comps:
        assert ing_id in ING_IDS, ing_id
        for s in sizes:
            q = qty.get(s, 0)
            if q:
                RECIPES.append((did, s, ing_id, q, ING_UNIT[ing_id], role))

def q(sizes, *vals):
    return dict(zip(sizes, vals))

# shared quantity patterns
LATTE_SHOTS_H = q(HOT, 1, 1, 2, 2)
LATTE_MILK_H = q(HOT, 6.5, 9.5, 12, 15.5)
PUMPS_H = q(HOT, 2, 3, 4, 5)
WHIP_H = q(HOT, 0.6, 0.75, 1, 1.2)
SHOTS_I = q(ICED, 1, 2, 3)
PUMPS_I = q(ICED, 3, 4, 6)
WHIP_I = q(ICED, 0.75, 1, 1.2)
FRAP_BASE = q(ICED, 2, 3, 4)
FRAP_MILK = q(ICED, 4.5, 6, 8)
TOP1_H = q(HOT, 0.6, 0.75, 1, 1.25)
TOP1_I = q(ICED, 0.75, 1, 1.25)

# --- hot brewed coffee
for did, name, base in [("pike_place_roast", "Pike Place Roast", "brewed_pike_place"),
                        ("blonde_roast", "Blonde Roast", "brewed_blonde"),
                        ("dark_roast", "Dark Roast", "brewed_dark"),
                        ("decaf_pike_place_roast", "Decaf Pike Place Roast", "brewed_decaf")]:
    drink(did, name, "hot_coffee", "hot", HOT, [(base, "base", q(HOT, 8, 12, 16, 20))])
drink("caffe_misto", "Caffe Misto", "hot_coffee", "hot", HOT,
      [("brewed_pike_place", "base", q(HOT, 4, 6, 8, 10)), ("milk_2pct", "milk", q(HOT, 4, 6, 8, 10))], milk="milk_2pct")

# --- hot espresso
drink("caffe_latte", "Caffe Latte", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("milk_2pct", "milk", LATTE_MILK_H)], milk="milk_2pct")
drink("cappuccino", "Cappuccino", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("milk_2pct", "milk", q(HOT, 5, 7, 9, 11.5))], milk="milk_2pct")
drink("flat_white", "Flat White", "hot_espresso", "hot", HOT,
      [("espresso_ristretto", "espresso", q(HOT, 2, 2, 3, 3)), ("milk_whole", "milk", q(HOT, 5, 8, 10.5, 13.5))], milk="milk_whole")
drink("caramel_macchiato", "Caramel Macchiato", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("syrup_vanilla", "flavor", q(HOT, 2, 2, 3, 4)),
       ("milk_2pct", "milk", q(HOT, 6.5, 9.5, 11.5, 15)), ("caramel_drizzle", "topping", TOP1_H)], milk="milk_2pct")
drink("caffe_mocha", "Caffe Mocha", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("sauce_mocha", "flavor", PUMPS_H),
       ("milk_2pct", "milk", q(HOT, 6, 9, 11, 14.5)), ("whipped_cream", "topping", WHIP_H)], milk="milk_2pct")
drink("white_chocolate_mocha", "White Chocolate Mocha", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("sauce_white_mocha", "flavor", PUMPS_H),
       ("milk_2pct", "milk", q(HOT, 6, 9, 11, 14.5)), ("whipped_cream", "topping", WHIP_H)], milk="milk_2pct")
drink("caffe_americano", "Caffe Americano", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", q(HOT, 1, 2, 3, 4)), ("hot_water", "base", q(HOT, 7, 10, 13, 16))])
drink("blonde_vanilla_latte", "Blonde Vanilla Latte", "hot_espresso", "hot", HOT,
      [("espresso_blonde", "espresso", LATTE_SHOTS_H), ("syrup_vanilla", "flavor", PUMPS_H),
       ("milk_2pct", "milk", LATTE_MILK_H)], milk="milk_2pct")
drink("cinnamon_dolce_latte", "Cinnamon Dolce Latte", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("syrup_cinnamon_dolce", "flavor", PUMPS_H),
       ("milk_2pct", "milk", q(HOT, 6, 9, 11, 14.5)), ("whipped_cream", "topping", WHIP_H),
       ("cinnamon_dolce_topping", "topping", TOP1_H)], milk="milk_2pct")
drink("pumpkin_spice_latte", "Pumpkin Spice Latte", "hot_espresso", "hot", HOT,
      [("espresso_signature", "espresso", LATTE_SHOTS_H), ("sauce_pumpkin_spice", "flavor", PUMPS_H),
       ("milk_2pct", "milk", q(HOT, 6, 9, 11, 14.5)), ("whipped_cream", "topping", WHIP_H),
       ("pumpkin_spice_topping", "topping", TOP1_H)], milk="milk_2pct", status="seasonal")
drink("espresso", "Espresso", "hot_espresso", "hot", ["solo", "doppio", "triple", "quad"],
      [("espresso_signature", "espresso", {"solo": 1, "doppio": 2, "triple": 3, "quad": 4})])
drink("espresso_macchiato", "Espresso Macchiato", "hot_espresso", "hot", ESP,
      [("espresso_signature", "espresso", q(ESP, 1, 2)), ("milk_2pct", "milk", q(ESP, 0.3, 0.6))], milk="milk_2pct")
drink("espresso_con_panna", "Espresso con Panna", "hot_espresso", "hot", ESP,
      [("espresso_signature", "espresso", q(ESP, 1, 2)), ("whipped_cream", "topping", q(ESP, 0.25, 0.3))])

# --- iced espresso
drink("iced_caffe_latte", "Iced Caffe Latte", "iced_espresso", "iced", ICED,
      [("espresso_signature", "espresso", SHOTS_I), ("milk_2pct", "milk", q(ICED, 6, 8, 11))], milk="milk_2pct")
drink("iced_caramel_macchiato", "Iced Caramel Macchiato", "iced_espresso", "iced", ICED,
      [("espresso_signature", "espresso", SHOTS_I), ("syrup_vanilla", "flavor", q(ICED, 2, 3, 4)),
       ("milk_2pct", "milk", q(ICED, 7, 9.5, 12.5)), ("caramel_drizzle", "topping", TOP1_I)], milk="milk_2pct")
drink("iced_caffe_mocha", "Iced Caffe Mocha", "iced_espresso", "iced", ICED,
      [("espresso_signature", "espresso", SHOTS_I), ("sauce_mocha", "flavor", PUMPS_I),
       ("milk_2pct", "milk", q(ICED, 6, 8, 10.5)), ("whipped_cream", "topping", WHIP_I)], milk="milk_2pct")
drink("iced_white_chocolate_mocha", "Iced White Chocolate Mocha", "iced_espresso", "iced", ICED,
      [("espresso_signature", "espresso", SHOTS_I), ("sauce_white_mocha", "flavor", PUMPS_I),
       ("milk_2pct", "milk", q(ICED, 6, 8, 10.5)), ("whipped_cream", "topping", WHIP_I)], milk="milk_2pct")
drink("iced_caffe_americano", "Iced Caffe Americano", "iced_espresso", "iced", ICED,
      [("espresso_signature", "espresso", q(ICED, 2, 3, 4)), ("cold_water", "base", q(ICED, 6, 8, 11))])
drink("iced_flat_white", "Iced Flat White", "iced_espresso", "iced", ICED,
      [("espresso_ristretto", "espresso", q(ICED, 2, 3, 4)), ("milk_whole", "milk", q(ICED, 6, 8, 11))], milk="milk_whole")
drink("iced_shaken_espresso", "Iced Shaken Espresso", "iced_espresso", "iced", ICED,
      [("espresso_signature", "espresso", q(ICED, 2, 3, 4)), ("syrup_classic", "sweetener", q(ICED, 3, 4, 6)),
       ("milk_2pct", "milk", q(ICED, 2, 3, 4))], milk="milk_2pct")
drink("iced_brown_sugar_oatmilk_shaken_espresso", "Iced Brown Sugar Oatmilk Shaken Espresso", "iced_espresso", "iced", ICED,
      [("espresso_blonde", "espresso", q(ICED, 2, 3, 4)), ("syrup_brown_sugar", "flavor", q(ICED, 3, 4, 6)),
       ("milk_oat", "milk", q(ICED, 2.5, 3.5, 5)), ("cinnamon_powder", "topping", TOP1_I)], milk="milk_oat")

# --- cold coffee
drink("iced_coffee", "Iced Coffee", "cold_coffee", "iced", COLD,
      [("iced_coffee_base", "base", q(COLD, 9, 12, 17.5, 21)), ("syrup_classic", "sweetener", q(COLD, 3, 4, 6, 7))])
drink("iced_coffee_with_milk", "Iced Coffee with Milk", "cold_coffee", "iced", COLD,
      [("iced_coffee_base", "base", q(COLD, 8, 11, 16, 19)), ("syrup_classic", "sweetener", q(COLD, 3, 4, 6, 7)),
       ("milk_2pct", "milk", q(COLD, 1, 1.5, 2, 2.5))], milk="milk_2pct")
drink("cold_brew", "Cold Brew", "cold_coffee", "iced", COLD,
      [("cold_brew_base", "base", q(COLD, 9, 12, 18, 21))])
drink("vanilla_sweet_cream_cold_brew", "Vanilla Sweet Cream Cold Brew", "cold_coffee", "iced", COLD,
      [("cold_brew_base", "base", q(COLD, 8, 11, 16, 19)), ("syrup_vanilla", "flavor", q(COLD, 1, 2, 3, 4)),
       ("vanilla_sweet_cream", "cream", q(COLD, 0.75, 1, 1.5, 1.75))])
drink("salted_caramel_cream_cold_brew", "Salted Caramel Cream Cold Brew", "cold_coffee", "iced", COLD,
      [("cold_brew_base", "base", q(COLD, 8, 11, 16, 19)), ("syrup_vanilla", "flavor", q(COLD, 1, 2, 3, 4)),
       ("vanilla_sweet_cream", "cold_foam", q(COLD, 1.5, 2, 2.5, 3)), ("syrup_caramel", "cold_foam", q(COLD, 1, 2, 2, 3))])
drink("pumpkin_cream_cold_brew", "Pumpkin Cream Cold Brew", "cold_coffee", "iced", COLD,
      [("cold_brew_base", "base", q(COLD, 8, 11, 16, 19)), ("syrup_vanilla", "flavor", q(COLD, 1, 2, 3, 4)),
       ("vanilla_sweet_cream", "cold_foam", q(COLD, 1.5, 2, 2.5, 3)), ("sauce_pumpkin_spice", "cold_foam", q(COLD, 1, 2, 2, 3)),
       ("pumpkin_spice_topping", "topping", q(COLD, 0.75, 1, 1.25, 1.5))], status="seasonal")
drink("nitro_cold_brew", "Nitro Cold Brew", "cold_coffee", "iced", ["tall", "grande"],
      [("nitro_cold_brew_base", "base", {"tall": 12, "grande": 16})], verify="Y", notes="availability varies by store")

# --- frappuccinos (default whole milk)
def frap(did, name, base, extras, milk_qty=FRAP_MILK, coffee=True, whip=True):
    comps = [(base, "frap_base", FRAP_BASE), ("milk_whole", "milk", milk_qty)]
    if coffee:
        comps.append(("frap_roast", "base", FRAP_BASE))
    comps += extras
    if whip:
        comps.append(("whipped_cream", "topping", WHIP_I))
    drink(did, name, "frappuccino", "blended", ICED, comps, milk="milk_whole")

frap("coffee_frappuccino", "Coffee Frappuccino", "frap_coffee_base", [], whip=False)
frap("mocha_frappuccino", "Mocha Frappuccino", "frap_coffee_base", [("sauce_mocha", "flavor", FRAP_BASE)])
frap("caramel_frappuccino", "Caramel Frappuccino", "frap_coffee_base",
     [("syrup_caramel", "flavor", q(ICED, 2, 3, 3)), ("caramel_drizzle", "topping", TOP1_I)])
frap("java_chip_frappuccino", "Java Chip Frappuccino", "frap_coffee_base",
     [("sauce_mocha", "flavor", FRAP_BASE), ("frap_chips", "inclusion", FRAP_BASE), ("mocha_drizzle", "topping", TOP1_I)])
frap("mocha_cookie_crumble_frappuccino", "Mocha Cookie Crumble Frappuccino", "frap_coffee_base",
     [("sauce_mocha", "flavor", FRAP_BASE), ("frap_chips", "inclusion", FRAP_BASE), ("cookie_crumble_topping", "topping", TOP1_I)])
frap("caramel_ribbon_crunch_frappuccino", "Caramel Ribbon Crunch Frappuccino", "frap_coffee_base",
     [("sauce_dark_caramel", "flavor", FRAP_BASE), ("caramel_drizzle", "topping", TOP1_I), ("caramel_crunch_topping", "topping", TOP1_I)])
frap("white_chocolate_mocha_frappuccino", "White Chocolate Mocha Frappuccino", "frap_coffee_base",
     [("sauce_white_mocha", "flavor", FRAP_BASE)])
frap("vanilla_bean_creme_frappuccino", "Vanilla Bean Creme Frappuccino", "frap_creme_base",
     [("vanilla_bean_powder", "flavor", FRAP_BASE)], milk_qty=q(ICED, 5, 6.5, 8.5), coffee=False)
frap("strawberry_creme_frappuccino", "Strawberry Creme Frappuccino", "frap_creme_base",
     [("strawberry_puree", "flavor", q(ICED, 1, 2, 3)), ("syrup_classic", "sweetener", q(ICED, 1, 1, 2))],
     milk_qty=q(ICED, 5, 6.5, 8.5), coffee=False)
frap("double_chocolaty_chip_creme_frappuccino", "Double Chocolaty Chip Creme Frappuccino", "frap_creme_base",
     [("sauce_mocha", "flavor", FRAP_BASE), ("frap_chips", "inclusion", FRAP_BASE), ("mocha_drizzle", "topping", TOP1_I)],
     milk_qty=q(ICED, 5, 6.5, 8.5), coffee=False)
frap("matcha_creme_frappuccino", "Matcha Creme Frappuccino", "frap_creme_base",
     [("matcha_powder", "flavor", FRAP_BASE), ("syrup_classic", "sweetener", q(ICED, 2, 3, 4))],
     milk_qty=q(ICED, 5, 6.5, 8.5), coffee=False)

# --- tea lattes
drink("chai_tea_latte", "Chai Tea Latte", "tea_latte", "hot", HOT,
      [("chai_concentrate", "base", PUMPS_H), ("milk_2pct", "milk", q(HOT, 5, 7, 8.5, 11))], milk="milk_2pct")
drink("iced_chai_tea_latte", "Iced Chai Tea Latte", "tea_latte", "iced", ICED,
      [("chai_concentrate", "base", q(ICED, 3, 4, 6)), ("milk_2pct", "milk", q(ICED, 5, 7, 10))], milk="milk_2pct")
drink("matcha_tea_latte", "Matcha Tea Latte", "tea_latte", "hot", HOT,
      [("matcha_powder", "base", PUMPS_H), ("syrup_classic", "sweetener", PUMPS_H),
       ("milk_2pct", "milk", LATTE_MILK_H)], milk="milk_2pct", verify="Y", notes="matcha recipe changed in 2025")
drink("iced_matcha_tea_latte", "Iced Matcha Tea Latte", "tea_latte", "iced", ICED,
      [("matcha_powder", "base", q(ICED, 2, 3, 4)), ("syrup_classic", "sweetener", q(ICED, 2, 3, 4)),
       ("milk_2pct", "milk", q(ICED, 6.5, 8.5, 12))], milk="milk_2pct", verify="Y", notes="matcha recipe changed in 2025")
drink("london_fog_tea_latte", "London Fog Tea Latte", "tea_latte", "hot", HOT,
      [("tea_bag_black", "base", q(HOT, 1, 1, 2, 2)), ("syrup_vanilla", "flavor", PUMPS_H),
       ("milk_2pct", "milk", q(HOT, 4, 6, 8, 10)), ("hot_water", "base", q(HOT, 3.5, 5.5, 7.5, 9.5))], milk="milk_2pct")

# --- hot tea
for did, name, bag in [("royal_english_breakfast_tea", "Royal English Breakfast Tea", "tea_bag_black"),
                       ("earl_grey_tea", "Earl Grey Tea", "tea_bag_black"),
                       ("emperors_clouds_mist_tea", "Emperor's Clouds & Mist", "tea_bag_green"),
                       ("jade_citrus_mint_tea", "Jade Citrus Mint Tea", "tea_bag_green"),
                       ("mint_majesty_tea", "Mint Majesty", "tea_bag_herbal"),
                       ("peach_tranquility_tea", "Peach Tranquility", "tea_bag_herbal")]:
    drink(did, name, "hot_tea", "hot", HOT,
          [(bag, "base", q(HOT, 1, 1, 1, 2)), ("hot_water", "base", q(HOT, 8, 12, 16, 20))])

# --- iced tea (unsweetened by default; verify)
for did, name, base in [("iced_black_tea", "Iced Black Tea", "iced_black_tea_base"),
                        ("iced_green_tea", "Iced Green Tea", "iced_green_tea_base"),
                        ("iced_passion_tango_tea", "Iced Passion Tango Tea", "iced_passion_tango_base")]:
    drink(did, name, "iced_tea", "iced", COLD, [(base, "base", q(COLD, 6, 8, 12, 15))],
          verify="Y", notes="default sweetening varies; verify")
    drink(did + "_lemonade", name + " Lemonade", "iced_tea", "iced", COLD,
          [(base, "base", q(COLD, 3, 4, 6, 7.5)), ("lemonade", "juice", q(COLD, 3, 4, 6, 7.5))],
          verify="Y", notes="default sweetening varies; verify")

# --- refreshers
for prefix, name, base, fruit, coco_name in [
        ("strawberry_acai", "Strawberry Acai", "refresher_strawberry_acai", "strawberry_inclusion", "pink_drink"),
        ("mango_dragonfruit", "Mango Dragonfruit", "refresher_mango_dragonfruit", "dragonfruit_inclusion", "dragon_drink")]:
    base_q = q(COLD, 4.5, 6, 9, 11)
    fruit_q = q(COLD, 1, 1, 1.5, 2)
    top_q = q(COLD, 3, 4, 6, 7.5)
    drink(prefix + "_refresher", name + " Refresher", "refresher", "iced", COLD,
          [(base, "base", base_q), ("cold_water", "base", top_q), (fruit, "inclusion", fruit_q)])
    drink(prefix + "_lemonade", name + " Lemonade", "refresher", "iced", COLD,
          [(base, "base", base_q), ("lemonade", "juice", top_q), (fruit, "inclusion", fruit_q)])
    drink(coco_name, "Pink Drink" if coco_name == "pink_drink" else "Dragon Drink", "refresher", "iced", COLD,
          [(base, "base", base_q), ("milk_coconut", "milk", top_q), (fruit, "inclusion", fruit_q)], milk="milk_coconut")

# --- hot chocolate & steamers
drink("hot_chocolate", "Hot Chocolate", "hot_chocolate_steamer", "hot", HOT,
      [("sauce_mocha", "flavor", PUMPS_H), ("milk_2pct", "milk", LATTE_MILK_H),
       ("whipped_cream", "topping", WHIP_H), ("mocha_drizzle", "topping", TOP1_H)], milk="milk_2pct")
drink("steamed_milk", "Steamed Milk", "hot_chocolate_steamer", "hot", HOT,
      [("milk_2pct", "milk", q(HOT, 7.5, 11.5, 15, 19))], milk="milk_2pct")
drink("vanilla_creme", "Vanilla Creme", "hot_chocolate_steamer", "hot", HOT,
      [("syrup_vanilla", "flavor", PUMPS_H), ("milk_2pct", "milk", q(HOT, 6.5, 9.5, 12.5, 16)),
       ("whipped_cream", "topping", WHIP_H)], milk="milk_2pct")

# ---------------------------------------------------------------- modifiers
MODIFIERS = [
    ("swap_milk", "Replace the drink's milk with another milk; quantity unchanged", "milk", "Oatmilk instead of 2%"),
    ("set_quantity", "Set pumps/shots/scoops of an ingredient already in the recipe (0 removes it)", "any", "2 pumps vanilla instead of 4"),
    ("add_ingredient", "Add an ingredient not in the default recipe", "any", "Add 1 pump hazelnut"),
    ("remove_ingredient", "Remove an ingredient entirely", "any", "No whipped cream"),
    ("swap_espresso", "Replace espresso type; shot count unchanged", "espresso", "Blonde instead of Signature"),
    ("add_cold_foam", "Add vanilla sweet cream cold foam at the size's foam quantity (1.5/2/2.5/3 fl oz)", "cream", "Add cold foam to cold brew"),
    ("scale_quantity", "Light (x0.5) or extra (x1.5) of an ingredient", "any", "Light caramel drizzle"),
    ("ice_level", "Light / extra / no ice; not modeled in phase 1 (changes liquid volume)", "none", "Light ice"),
]

# ---------------------------------------------------------------- sample orders
ORDERS = [
    ("ord_0001", "2026-10-06T08:12:00-04:00", "caramel_macchiato", "grande"),
    ("ord_0002", "2026-10-06T14:40:00-04:00", "iced_brown_sugar_oatmilk_shaken_espresso", "venti_iced"),
    ("ord_0003", "2026-10-07T09:05:00-04:00", "pumpkin_spice_latte", "tall"),
    ("ord_0004", "2026-10-08T15:20:00-04:00", "cold_brew", "grande"),
    ("ord_0005", "2026-10-09T08:30:00-04:00", "caffe_latte", "grande"),
]
ORDER_MODS = [
    # order_id, seq, modifier_type, ingredient_id, quantity, replaces_ingredient_id
    ("ord_0001", 1, "swap_milk", "milk_oat", "", "milk_2pct"),
    ("ord_0001", 2, "set_quantity", "syrup_vanilla", 2, ""),
    ("ord_0002", 1, "set_quantity", "syrup_brown_sugar", 3, ""),
    ("ord_0003", 1, "remove_ingredient", "whipped_cream", 0, ""),
    ("ord_0003", 2, "set_quantity", "sauce_pumpkin_spice", 2, ""),
    ("ord_0004", 1, "add_cold_foam", "vanilla_sweet_cream", "", ""),
    ("ord_0004", 2, "add_ingredient", "syrup_caramel", 2, ""),
    ("ord_0005", 1, "swap_espresso", "espresso_blonde", "", "espresso_signature"),
    ("ord_0005", 2, "add_ingredient", "syrup_sf_vanilla", 2, ""),
]

# ---------------------------------------------------------------- label capture template
LABEL_KEYS = [(d, "grande") for d in [
    "caffe_latte", "cappuccino", "flat_white", "caramel_macchiato", "caffe_mocha", "white_chocolate_mocha",
    "caffe_americano", "pumpkin_spice_latte", "iced_caffe_latte", "iced_caramel_macchiato",
    "iced_brown_sugar_oatmilk_shaken_espresso", "iced_shaken_espresso", "iced_coffee", "cold_brew",
    "vanilla_sweet_cream_cold_brew", "salted_caramel_cream_cold_brew", "pumpkin_cream_cold_brew",
    "coffee_frappuccino", "mocha_frappuccino", "caramel_frappuccino", "java_chip_frappuccino",
    "vanilla_bean_creme_frappuccino", "chai_tea_latte", "iced_chai_tea_latte", "matcha_tea_latte",
    "strawberry_acai_refresher", "pink_drink", "hot_chocolate", "pike_place_roast"]] + [
    ("caffe_latte", "tall"), ("caffe_latte", "venti_hot"), ("iced_caffe_latte", "venti_iced"), ("cold_brew", "trenta")]

# ---------------------------------------------------------------- write
def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

write("sizes.csv", ["size_id", "size_name", "volume_fl_oz", "size_family"], SIZES)
write("ingredients.csv", ["ingredient_id", "ingredient_name", "category", "unit", "calories", "total_fat_g",
                          "saturated_fat_g", "carbs_g", "sugar_g", "protein_g", "caffeine_mg", "confidence", "note"], I)
write("drinks.csv", ["drink_id", "drink_name", "category", "temperature", "default_milk_id", "available_sizes",
                     "menu_status", "verify_current_menu", "notes"], DRINKS)
write("recipes.csv", ["drink_id", "size_id", "ingredient_id", "quantity", "unit", "component_role"], RECIPES)
write("modifiers.csv", ["modifier_type", "description", "applies_to", "example"], MODIFIERS)
write("orders_sample.csv", ["order_id", "ordered_at", "drink_id", "size_id"], ORDERS)
write("order_modifications_sample.csv", ["order_id", "seq", "modifier_type", "ingredient_id", "quantity",
                                         "replaces_ingredient_id"], ORDER_MODS)
dmilk = {d[0]: d[4] for d in DRINKS}
write("published_labels_template.csv", ["drink_id", "size_id", "milk_id", "calories", "total_fat_g", "sugar_g",
                                        "protein_g", "caffeine_mg", "source_url", "captured_on"],
      [(d, s, dmilk[d], "", "", "", "", "", "", "") for d, s in LABEL_KEYS])

print(f"ingredients={len(I)} drinks={len(DRINKS)} recipe_rows={len(RECIPES)}")

# Seed data: Drink Nutrition Pipeline (phase 1)

Component-level model of the Starbucks US beverage menu: 70 drinks, 64 ingredients, 736 recipe rows.
Regenerate any time with `python generate_seed.py`.

| File | Grain | Purpose |
| --- | --- | --- |
| sizes.csv | one row per size | Cup sizes (short to trenta) and espresso sizes (solo to quad) |
| ingredients.csv | one row per ingredient | Nutrition per unit (pump, shot, fl oz, scoop, serving) plus a confidence level |
| drinks.csv | one row per drink | Category, default milk, available sizes, seasonal flag, "verify current menu" flag |
| recipes.csv | drink x size x ingredient | Default quantity of each ingredient (the bill of materials) |
| modifiers.csv | one row per modifier type | Allowed customization actions (swap milk, set pumps, add foam...) |
| orders_sample.csv | one row per order | Sample logged orders for testing |
| order_modifications_sample.csv | order x change | Sample customizations applied to those orders |
| published_labels_template.csv | drink x size | Blank template: capture official labels here to calibrate the model |

## How to trust these numbers

All ingredient values are estimates; `confidence` is high, medium or low.
Default recipes reproduce 24 of 26 well-known grande labels (approximate published values) within 15% on calories.
The two misses are Iced Brown Sugar Oatmilk Shaken Espresso (+30%) and Matcha Tea Latte (+18%); start calibration there.
Drinks flagged `verify_current_menu = Y` may have changed or left the menu since mid-2026.

## Calculation rule

nutrition(order) = sum over final ingredients of (quantity x per-unit value),
where final ingredients = default recipe for drink + size, with the order's modifications applied in `seq` order.

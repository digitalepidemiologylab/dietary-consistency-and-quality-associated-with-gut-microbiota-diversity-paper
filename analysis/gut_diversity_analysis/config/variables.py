# config/variables.py

"""Configuration file containing all variable definitions."""

NUTRI_MACRO_VARS = [
    "protein_eaten",
    "fat_eaten",
    "carb_eaten",
    "fiber_eaten",
    "alcohol_eaten",
]

PERSONAL_VARS = [
    "age",
    "bmi",
    "bmr",
    "height",
    "weight",
    "language",
    "urbanity",
    "swiss_citizen",
]

AMOUNT_VARS = ["eaten_quantity_in_gram", "energy_kcal_eaten"]

NUTRI_MICRO_VARS = [
    "beta_carotene_eaten",
    "folate_eaten",
    "iron_eaten",
    "magnesium_eaten",
    "niacin_eaten",
    "pantothenic_acid_eaten",
    "cholesterol_eaten",
    "fatty_acids_monounsaturated_eaten",
    "fatty_acids_polyunsaturated_eaten",
    "fatty_acids_saturated_eaten",
    "calcium_eaten",
    "phosphorus_eaten",
    "potassium_eaten",
    "sodium_eaten",
    "zinc_eaten",
    "vitamin_b1_eaten",
    "vitamin_b12_eaten",
    "vitamin_b2_eaten",
    "vitamin_b6_eaten",
    "vitamin_c_eaten",
    "vitamin_d_eaten",
    "salt_eaten",
    "sugar_eaten",
]

NUTRI_CFG_VARS = [
    "dairy_products_meat_fish_eggs_tofu",
    "vegetables_fruits",
    "sweets_salty_snacks_alcohol",
    "non_alcoholic_beverages",
    "grains_potatoes_pulses",
    "oils_fats_nuts",
]

NUTRI_FG_VARS = [
    "meat_fg_eaten",
    "fruits_fg_eaten",
    "vegetables_fg_eaten",
    "dairy_fg_eaten",
    "bread_fg_eaten",
    "oils_nuts_fg_eaten",
    "coffee_fg_eaten",
    "others_fg_eaten",
    "sugary_fg_eaten",
    "grains_cereals_fg_eaten",
    "fast_food_fg_eaten",
    "water_fg_eaten",
    "tea_fg_eaten",
    "alcohol_fg_eaten",
    "vegan_fg_eaten",
]

NUTRI_DI_VARS = [
    "daily_HEI",
    "HEI",
    "aMED",
    "DASH",
    "mean_dds",
    "mean_shannon_diversity_kcal",
    "mean_berger_parker_kcal",
    "mean_simpson_diversity_kcal",
    "mean_gini_simpson_diversity_kcal",
    "mean_quantidd_kcal",
    "mean_mfad_jaccard_kcal",
]


# Function to get CV vars from metadata
def get_cv_vars(meta_df):
    """Get coefficient of variation variables from metadata DataFrame."""
    return [col for col in meta_df.columns if "CV_" in col]


# Combine all variables except CV vars (which need to be obtained from metadata)
ALL_VARS = (
    NUTRI_DI_VARS
    + NUTRI_MACRO_VARS
    + NUTRI_MICRO_VARS
    + NUTRI_CFG_VARS
    + NUTRI_FG_VARS
    + PERSONAL_VARS
    + AMOUNT_VARS
)

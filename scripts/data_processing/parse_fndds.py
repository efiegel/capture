import csv
import json


def parse_fndds():
    # FNDDS dataset https://fdc.nal.usda.gov/download-datasets.html
    with open("fndds.json", "r") as file:
        data = json.load(file)

    with open("fndds.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        headers = [
            "food",
            "portion",
            "portion_grams",
            "calories",
            "protein_grams",
            "fat_grams",
            "carbs_grams",
            "sodium_mg",
        ]
        writer.writerow(headers)

        for food in data["SurveyFoods"]:
            description = food.get("description")
            portion = None
            portion_grams = None
            calories = None
            protein = None
            fat = None
            carbs = None
            sodium = None

            try:
                portion = food.get("foodPortions", [{}])[0].get("portionDescription")
                portion_grams = food.get("foodPortions", [{}])[0].get("gramWeight")
            except IndexError:
                pass

            for nutrient in food.get("foodNutrients"):
                if nutrient.get("nutrient", {}).get("name") == "Energy":
                    calories = nutrient.get("amount")
                elif nutrient.get("nutrient", {}).get("name") == "Protein":
                    protein = nutrient.get("amount")
                elif nutrient.get("nutrient", {}).get("name") == "Total lipid (fat)":
                    fat = nutrient.get("amount")
                elif (
                    nutrient.get("nutrient", {}).get("name")
                    == "Carbohydrate, by difference"
                ):
                    carbs = nutrient.get("amount")
                elif nutrient.get("nutrient", {}).get("name") == "Sodium, Na":
                    sodium = nutrient.get("amount")

            writer.writerow(
                [
                    description,
                    portion,
                    portion_grams,
                    calories,
                    protein,
                    fat,
                    carbs,
                    sodium,
                ]
            )


if __name__ == "__main__":
    parse_fndds()

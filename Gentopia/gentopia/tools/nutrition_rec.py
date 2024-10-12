from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from gentopia.tools.basetool import *
import requests
import json

# Nutrition Recommendation Class
class NutritionRecommendationArgs(BaseModel):
    query: str = Field(
        ..., description="Name of the food item or nutrition requirement, e.g., 'apple' or 'high-protein diet'."
    )


class NutritionRecommendation(BaseTool):
    """Tool that provides nutritional information or suggestions."""

    name = "nutrition_recommendation"
    description = (
        "A tool that provides nutritional information based on a given query. "
        "Input should be a food item or nutrition-related query."
    )

    args_schema: Optional[Type[BaseModel]] = NutritionRecommendationArgs

    def _run(self, query: str) -> str:
        try:
            # Nutritionix API for food information (example usage)
            api_url = "https://api.nutritionix.com/v1_1/search/"
            params = {
                "query": query,
                "appId": "your_app_id_here",
                "appKey": "your_app_key_here",
            }

            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data["hits"]:
                    food_info = data["hits"][0]["fields"]
                    return f"Nutritional Information for {query}:\nCalories: {food_info['nf_calories']}\nProtein: {food_info['nf_protein']}g\nFat: {food_info['nf_total_fat']}g\nCarbohydrates: {food_info['nf_total_carbohydrate']}g"
                else:
                    return "No nutritional information found for the given query."
            else:
                return "Failed to retrieve nutritional information."

        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Example usage of NutritionRecommendation tool
    nutrition_tool = NutritionRecommendation()
    nutrition_ans = nutrition_tool._run("apple")
    print(nutrition_ans)

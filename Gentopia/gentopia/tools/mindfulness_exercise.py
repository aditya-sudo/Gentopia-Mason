from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from gentopia.tools.basetool import *

# Mindfulness Exercises and Meditation Class
class MindfulnessExerciseArgs(BaseModel):
    exercise_type: str = Field(
        ..., description="Type of mindfulness exercise (e.g., 'breathing', 'meditation', 'guided visualization')."
    )


class MindfulnessExercise(BaseTool):
    """Tool that provides mindfulness exercises and guided meditation."""

    name = "mindfulness_exercise"
    description = (
        "A tool that provides mindfulness exercises or guided meditation based on the specified exercise type. "
        "Input should specify the type of mindfulness exercise (e.g., 'breathing', 'meditation')."
    )

    args_schema: Optional[Type[BaseModel]] = MindfulnessExerciseArgs

    def _run(self, exercise_type: str) -> str:
        try:
            # Predefined mindfulness exercise suggestions
            exercises = {
                "breathing": "Breathing Exercise: Sit comfortably. Inhale deeply for 4 seconds, hold for 4 seconds, exhale for 6 seconds. Repeat for 5-10 minutes.",
                "meditation": "Meditation Exercise: Sit comfortably and close your eyes. Focus on your breathing. Observe each inhale and exhale for 10 minutes.",
                "guided visualization": "Guided Visualization: Imagine yourself in a peaceful environment, like a forest or beach. Visualize the details and focus on the sounds, smells, and sights for 10-15 minutes."
            }

            return exercises.get(exercise_type.lower(), "No mindfulness exercise found for the given type.")

        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Example usage of MindfulnessExercise tool
    mindfulness_tool = MindfulnessExercise()
    mindfulness_ans = mindfulness_tool._run("breathing")
    print(mindfulness_ans)
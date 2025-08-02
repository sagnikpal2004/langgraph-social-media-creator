import os
import pandas as pd
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

import model

# --- LangGraph State Definition ---

class ContentCreatorState(TypedDict):
    """Represents the state of the content generation process, using a DataFrame.

    Attributes:
        brand_theme (str): The high-level theme for content generation.
        num_days (int): The number of days to plan content for.
        topics (List[str]): A list of generated topic ideas.
        content_plan (pd.DataFrame): The final content plan stored in a DataFrame.
        current_day_index (int): Tracks the current day being processed.
    """
    brand_theme: str
    num_days: int
    current_day_index: int
    topics: list[str]
    captions: list[str]
    hashtags: list[list[str]]
    content_plan: pd.DataFrame


# --- Node Implementations ---

def day_planner(state: ContentCreatorState):
    """
    Day Planner Node: Generates a list of topic ideas and initializes the DataFrame.
    
    Args:
        state (ContentCreatorState): The current state of the graph.
        
    Returns:
        Dict: A dictionary to update the state with the generated topics and the DataFrame.
    """
    print("\n--- Day Planner Node: Generating topic ideas ---\n")

    brand_theme = state["brand_theme"]
    num_days = state["num_days"]

    topics = model.generate_topics(brand_theme, num_days)

    return {
        "topics": topics,
        "current_day_index": 0
    }


def content_generator(state: ContentCreatorState):
    """
    Content Generator Node: For the current topic, generates a caption and hashtags
    and updates the DataFrame.

    Args:
        state (ContentCreatorState): The current state of the graph.

    Returns:
        Dict: An updated content plan and the incremented day index.
    """
    print(f"--- Content Generator Node: Processing Day {state['current_day_index'] + 1} ---")

    topics = state["topics"]
    current_day_index = state["current_day_index"]

    state["captions"].append(model.generate_caption(topics[current_day_index]))
    state["hashtags"].append(model.generate_hashtags(topics[current_day_index]))

    return {
        "captions": state["captions"],
        "hashtags": state["hashtags"],
        "current_day_index": current_day_index + 1
    }

def should_continue(state: ContentCreatorState) -> str:
    """
    Conditional edge to check if more content needs to be generated.
    """
    if state["current_day_index"] < state["num_days"]:
        return "continue"
    else:
        print("\n--- All content generated. Moving to formatting. ---")
        return "end_generation"

def formatter(state: ContentCreatorState):
    """
    Formatter Node: Formats the content plan into a DataFrame.
    Args:
        state (ContentCreatorState): The current state of the graph.
    Returns:
        Dict: A DataFrame containing the content plan.
    """
    num_days = state["num_days"]
    topics = state["topics"]
    captions = state["captions"]
    hashtags = state["hashtags"]

    content_plan = pd.DataFrame({
        "Day": range(1, num_days+1),
        "Topic": topics,
        "Caption": captions,
        "Hashtags": hashtags
    })

    return {
        "content_plan": content_plan
    }

def save(state: ContentCreatorState):
    """
    Save Node: Saves the content plan DataFrame to a CSV file.
    """
    csv_path = "results/content_calendar.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    state["content_plan"].to_csv(csv_path, index=False)
    print(f"Content calendar saved to {csv_path}")

    return {}


# --- Agent Creation and Running ---

def create_agent():
    workflow = StateGraph(ContentCreatorState)

    # Add the nodes to the workflow
    workflow.add_node("day_planner", day_planner)
    workflow.add_node("content_generator", content_generator)
    workflow.add_node("formatter", formatter)
    workflow.add_node("save_csv", save)

    # Set the entry point for the graph
    workflow.set_entry_point("day_planner")

    # Define the edges (flow of execution)
    workflow.add_edge("day_planner", "content_generator")
    workflow.add_conditional_edges("content_generator", should_continue, {
        "continue": "content_generator", 
        "end_generation": "formatter"
    })
    workflow.add_edge("formatter", "save_csv")

    workflow.set_finish_point("save_csv")
    return workflow.compile()

def run_agent(brand_theme: str, num_days: int = 30):
    """
    Run the content creation agent with the specified brand theme and number of days.
    
    Args:
        brand_theme (str): The theme for the content generation.
        num_days (int): The number of days to plan content for.
        
    Returns:
        pd.DataFrame: The final content plan DataFrame.
    """
    app = create_agent()
    init_state = {
        "brand_theme": brand_theme,
        "num_days": num_days,
        "captions": [],
        "hashtags": [],
    }

    final_state = app.invoke(init_state)
    return final_state["content_plan"], "results/content_calendar.csv"


if __name__ == "__main__":
    brand_theme = input("Enter brand theme: ")
    num_days = int(input("Enter number of days: "))

    content_plan = run_agent(brand_theme, num_days)
    print(f"\nFinal content plan:\n{content_plan}")
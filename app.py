import os
import json
import pandas as pd
from flask import Flask, request, jsonify
from together import Together
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# -----------------------------
# Utility Functions
# -----------------------------

def load_dataset(filename="Dataset.xlsx"):
    """
    Loads the dataset from an Excel file.
    Expected columns: Visualization, Memory, Association, Reasoning, Age, 
    Activity name, Activity description, Zone, Time.
    """
    try:
        df = pd.read_excel(filename, engine="openpyxl")
        # Standardize column names (strip extra whitespace)
        df.columns = [col.strip() for col in df.columns]
        return df
    except Exception as e:
        raise Exception(f"Error loading Excel file: {e}")

def create_knowledge_base(df, num_examples=3):
    """
    Creates a knowledge base snippet by selecting a few example rows from the dataset.
    Each example includes details such as the activity title, description, cognitive aspects,
    age, zone, and duration.
    """
    examples = []
    for _, row in df.head(num_examples).iterrows():
        summary = (
            f"Title: {row['Activity name']}\n"
            f"Description: {row['Activity description']}\n"
            f"Categories: Visualization={row['Visualization']}, Memory={row['Memory']}, "
            f"Association={row['Association']}, Reasoning={row['Reasoning']}\n"
            f"Age: {row['Age']}, Zone: {row['Zone']}, Duration: {row['Time']} minutes\n"
        )
        examples.append(summary)
    return "\n".join(examples)

def generate_activity_recommendations(category: str, zone: str, age_range: str, knowledge_base: str) -> list:
    """
    Uses the Together API to generate three new cognitive activity recommendations.
    
    The prompt instructs the model to output a valid JSON array containing three JSON objects.
    Each object must have the following keys: "name", "description", "instructions",
    "materials_required", "time_required", "zone", and "objective".
    """
    prompt = (
        "You are a creative expert in designing engaging cognitive activities for children. "
        "Using the following knowledge base examples solely for inspiration, generate three completely new, original, and positive cognitive activity recommendations that are engaging and age-appropriate. "
        "Output your recommendations as a valid JSON array containing exactly three JSON objects. Each JSON object must have the following keys: "
        "\"name\", \"description\", \"instructions\", \"materials_required\", \"time_required\", \"zone\", and \"objective\". "
        "Do not include any additional commentary or text; output only the JSON array.\n\n"
        "Knowledge Base Examples:\n"
        f"{knowledge_base}\n\n"
        "Parameters:\n"
        f"Category: {category}\n"
        f"Zone: {zone}\n"
        f"Age Range: {age_range}\n\n"
        "Now, please generate the JSON array:"
    )
    
    # Initialize Together API client with API key from .env
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    
    # Make a single API call that returns a JSON array.
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        n=1
    )
    
    raw_output = response.choices[0].message.content.strip()
    try:
        recommendations = json.loads(raw_output)
    except Exception as e:
        recommendations = [{"error": "Failed to parse JSON output", "raw_output": raw_output, "exception": str(e)}]
    return recommendations

# -----------------------------
# Global Initialization
# -----------------------------

# Load the dataset and create the knowledge base when the app starts.
try:
    dataset_df = load_dataset("Dataset.xlsx")
    KNOWLEDGE_BASE = create_knowledge_base(dataset_df, num_examples=3)
except Exception as e:
    KNOWLEDGE_BASE = ""
    print(f"Error initializing knowledge base: {e}")

# -----------------------------
# Flask API Endpoints
# -----------------------------

@app.route("/recommend", methods=["GET"])
def recommend():
    # Retrieve query parameters
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "The 'category' parameter is required."}), 400
    zone = request.args.get("zone", "")   # optional; default to empty string
    age_range = request.args.get("age_range", "")  # optional; default to empty string

    # Generate recommendations using the global KNOWLEDGE_BASE
    recommendations = generate_activity_recommendations(category, zone, age_range, KNOWLEDGE_BASE)
    return jsonify({"recommendations": recommendations})

# -----------------------------
# Run the Flask App
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# Cognitive Activity Recommendations API

This project provides a Flask-based RESTful API that generates cognitive activity recommendations using the Together AI API. The recommendations are generated based on a dataset of cognitive activities provided in an Excel file named `Dataset.xlsx`. The API accepts parameters such as category, zone, and age range, and returns a JSON response with a list of recommended activities.

## Demo

https://github.com/user-attachments/assets/cbf3dd05-ab03-4250-b96f-91e79832d08d

## Features

- **Dataset Integration:**  
  Loads an Excel file (`Dataset1.xlsx`) containing cognitive activity details. The expected columns are:
  - `Visualization`
  - `Memory`
  - `Association`
  - `Reasoning`
  - `Age`
  - `Activity name`
  - `Activity description`
  - `Zone`
  - `Time`

- **Knowledge Base:**  
  Creates a snippet of example activities from the dataset to serve as inspiration for generating recommendations.

- **Recommendation Generation:**  
  Uses the Together AI API (with the `meta-llama/Llama-3.3-70B-Instruct-Turbo` model) to generate a valid JSON array containing recommendations. Each recommendation includes:
  - **name**: Title of the activity.
  - **description**: Brief summary of the activity.
  - **instructions**: Clear, step-by-step instructions.
  - **materials_required**: List of necessary materials.
  - **time_required**: Estimated time needed (in minutes).
  - **zone**: Recommended cognitive level (e.g., "red", "yellow", "green").
  - **objective**: The educational objective of the activity.

- **Flask API Endpoint:**  
  Provides a single endpoint (`/recommend`) that accepts the following query parameters:
  - `category` (required): The category of cognitive activity (e.g., "Memory", "Reasoning", "Attention").
  - `zone` (optional): The cognitive level of the user (e.g., "red", "yellow", "green").
  - `age_range` (optional): The age range of the user (e.g., "4-10", "11-18", "18-65").  
  The API returns a JSON response containing a list of recommended activities.

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine.

### 2. Install Dependencies

Install the required Python packages by running the following command:
```bash
    pip install pandas openpyxl together flask python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following content:
```
 TOGETHER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Together API key.


### 4. Run the Flask API

Run the Flask API using the following command:
```bash
python app.py
```

The API will start on port 5000 (accessible at `http://0.0.0.0:5000`).

### 5. Test the API

Send a GET request to the `/recommend` endpoint. For example, open your browser or use a tool to access:

```
http://127.0.0.1:5000/recommend?category=Memory&zone=Green&age_range=11-18
```


The API will return a JSON response with a list of recommended activities.

## Code Overview

- **app.py:**  
  Contains the Flask API code:
  - `load_dataset()`: Loads the Excel dataset from `Dataset1.xlsx`.
  - `create_knowledge_base()`: Creates a snippet of examples from the dataset.
  - `generate_activity_recommendations()`: Builds a detailed prompt and calls the Together API to generate a JSON array of recommendations.
  - `/recommend`: The Flask endpoint that accepts query parameters and returns generated recommendations as JSON.

- **.env:**  
  Contains the environment variable `TOGETHER_API_KEY`.

- **Dataset.xlsx:**  
  Your dataset file (not included in the repository).

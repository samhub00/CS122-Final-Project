# Final Project for CS122 at SJSU

## Authors
- **Sam Hubler** (Author #1) — Data Collection & Storage
- **Alan Xiao** (Author #2) — Data Analysis & Visualization

---

## Project Description

This project is a recipe application that leverages the [Spoonacular API](https://spoonacular.com/food-api) to provide users with a powerful and intuitive culinary assistant. Users can search for recipes by name or keyword, or generate personalized recipe suggestions based on the ingredients they already have on hand. The app also surfaces detailed nutritional information for each recipe, helping users make informed dietary decisions. In addition to nutrition data, the application retrieves estimated pricing data so users can plan meals within a budget. Together, these features make the app a comprehensive tool for everyday meal planning, grocery management, and healthy eating.

---

## Project Outline / Plan

### Interface Plan
The application will feature a clean, user-friendly interface with the following key views:
- **Home / Search Page** — A search bar where users can look up recipes by name or keyword.
- **Ingredient-Based Generator** — An input panel where users enter available ingredients to receive AI-assisted recipe suggestions from the Spoonacular API.
- **Recipe Detail Page** — Displays full recipe instructions, ingredient lists, nutritional facts, and estimated cost per serving.
- **Nutrition & Pricing Dashboard** — A visual summary panel showing charts and breakdowns of macronutrients and pricing data.

The interface will be built with simplicity and accessibility in mind, ensuring the app is easy to navigate for all users.

---

### Data Collection and Storage Plan
*Written by Author #1 — Sam Hubler*

The data collection and storage layer will take in, sort, and store the data from the Spoonacular API depending on the call for easy access in the visualization step. 

- **API Access** - When the website is accessed, the Spoonacular API will be accessed with our API key.
- **Searching** - When the user selects an option, the Flask apps will perform their duties whether that is to search for a recipe, get nutritional information or otherwise.
- **JSON Handling** - The Spoonacular API returns results in JSON form which will be handled comprehensively and efficiently, yielding the correct information for the user.
- **User Login and Data Storage** - We will be using DynamoDB from AWS to store user data such as login, preferences and more.
- **User Data Passing** - When a user logs in, their data will be accessed and passed through to the visualization layer. If a user is not logged in, no long term data will be stored, they will still be able to use the basic recipe gathering features.

---

### Data Analysis and Visualization Plan
*Written by Author #2 — Alan Xiao*

The visualization layer will transform raw recipe, nutrition, and pricing data from the Spoonacular API into clear and meaningful visual summaries for the user.

- **Nutritional Breakdown Charts** — For each recipe, a bar chart or pie chart will display the macronutrient breakdown (calories, protein, fat, carbohydrates) so users can quickly assess dietary fit.
- **Price Comparison Visuals** — When multiple recipes are returned in a search, a comparative bar chart will display estimated cost per serving side-by-side, helping users identify budget-friendly options.
- **Ingredient Overlap Heatmap** — When using the ingredient-based generator, a visual summary will highlight which suggested recipes make the best use of the provided ingredients.
- **Trend Summaries** — If a user searches multiple recipes in a session, aggregate nutrition and pricing stats will be displayed to give a holistic view of their selections.

Visualizations will be implemented using a Python library such as `matplotlib` or `plotly`, and will be embedded directly into the application interface for a seamless experience.



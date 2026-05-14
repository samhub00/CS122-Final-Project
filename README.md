# Final Project for CS122 at SJSU

## Authors
- **Sam Hubler** (Author #1) — Data Collection & Storage
- **Alan Xiao** (Author #2) — Data Analysis & Visualization

---

## Project Description

This project is a recipe application website that leverages the [Spoonacular API](https://spoonacular.com/food-api) to provide users with a powerful and intuitive culinary assistant. Users can search for recipes by name or keyword, or generate personalized recipe suggestions based on the ingredients they already have on hand. The website also surfaces detailed nutritional information for each recipe, helping users make informed dietary decisions. Together, these features make the website a comprehensive tool for everyday meal planning, and healthy eating.

---

## Project Outline / Plan

### Interface Plan
The website will feature a clean, user-friendly interface with the following key views:
- **Login Page** - A login page that is optional to users who would like to store their favorite data.
- **Home / Search Page** — A search bar where users can look up recipes by name or keyword.
- **Favorites Page** - A page that displays the favorites of the users. Favorites can be added from the recipe information page.
- **Recipe Detail Page** — Displays full recipe instructions, ingredient lists, nutritional facts, and estimated cost per serving.
- **Nutrition Dashboard** — A visual summary panel showing charts and breakdowns of macronutrients and pricing data.

The interface will be built with simplicity and accessibility in mind, ensuring the app is easy to navigate for all users.

---

### Data Collection and Storage Plan
*Written by Author #1 — Sam Hubler*

The data collection and storage layer will take in, sort, and store the data from the Spoonacular API depending on the call for easy access in the visualization step. 

- **API Access** - When the website is accessed, the Spoonacular API will be accessed with our API key.
- **Searching** - When the user selects an option, the Flask apps will perform their duties whether that is to search for a recipe, get nutritional information or otherwise.
- **JSON Handling** - The Spoonacular API returns results in JSON form which will be handled comprehensively and efficiently, yielding the correct information for the user.
- **User Login and Data Storage** - We will be using a MySQL server hosted on Aiven online free database hosting to store user data such as login, preferences and more.
- **User Data Passing** - When a user logs in, their data will be accessed and passed through to the visualization layer. If a user is not logged in, no long term data will be stored, they will still be able to use the basic recipe gathering features.

---

### Data Analysis and Visualization Plan
*Written by Author #2 — Alan Xiao*

The visualization layer will transform raw recipe, nutrition, and pricing data from the Spoonacular API into clear and meaningful visual summaries for the user.

- **Overall Website Design** - The website is designed to be visually appealing, enhancing user experience and ease of use.
- **Recipe Display** - For each recipe, when selected from search, there will be a visually appealing recipe page including picture, formatted nutrition, recipe details and instructions.
- **Favorite Feature** — The user is able to add recipes to their favorites list. The nutritional data will be pulled from the users favorite recipes data.
- **Nutrition Trend Summaries** — Based on the average of the user's favorite recipes, the selected recipes nutritional value will be displayed in comparison.

Visualizations will be implemented using a Python library such as `matplotlib` or `plotly`, and will be embedded directly into the application interface for a seamless experience.



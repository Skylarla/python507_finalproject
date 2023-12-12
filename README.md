# README for Flask Web Application

## Description
This Flask application serves as a web interface for a Restaurant Recommendation System. It helps users find restaurants based on criteria such as price, location, and cuisine type.

## Requirements
- Python 3.x
- Flask
- requests

## Setup and Installation
1. **Clone the repository**:

2. **Install dependencies**:
- Ensure Python 3.x is installed on your system.
- Install Flask and requests:
  ```
  pip install Flask 
  pip install requests
  ```

3. **API Keys and Configuration**:
-  This application does not require you to configure the API key, because I have already configured it in the code in advance.

## Interacting with the Program
- Once the application is running, open a web browser and navigate to http://127.0.0.1:5000.
- Interact with the application through its web interface, which includes forms for entering your preferences like price range, preferred location, and cuisine type. Submit your preferences to get tailored restaurant recommendations.

## Data Structure Overview
- **Graph Structure**:
  - Used to represent relationships between restaurants.
  - Nodes represent restaurants; edges represent connections based on the rating of each restaurant. 

## Data Representation
- Data is stored in a JSON format and organized into the above data structures within the application.
- The `restaurant_data.json` file contains raw restaurant data.

## Utilization in the Application
- Graphs are used to find related restaurants and suggest alternatives.

## Additional Files
- `restaurants_data.json`: cache file, it contains the raw restaurant data.

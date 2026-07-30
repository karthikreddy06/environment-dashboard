import joblib
import pandas as pd

# Load the trained model
model = joblib.load("environment/ml/model.pkl")

# Load the encoder
encoder = joblib.load("environment/ml/encoder.pkl")

# Sample input
country = "India"

# Convert country name into number
country_encoded = encoder.transform([country])[0]

# Create input data
input_data = pd.DataFrame({
    "Country": [country_encoded],
    "Year": [2024],
    "Population_Millions": [1440],
    "GDP_per_Capita_USD": [2800],
    "Forest_Area_Percent": [24.5],
    "Renewable_Energy_Percent": [30],
    "PM2_5": [48],
    "Average_Temperature_C": [25.2]
})

# Predict
prediction = model.predict(input_data)

print("Predicted CO2 Emissions:")
print(round(prediction[0], 2), "Million Tons")
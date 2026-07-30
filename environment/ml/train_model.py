import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Read dataset
data = pd.read_excel("dataset/Environmental_AI_Dataset_Starter.xlsx")

# Encode Country
encoder = LabelEncoder()
data["Country"] = encoder.fit_transform(data["Country"]) #type: ignore

# Features (Input)
X = data.drop("CO2_Emissions_Mt", axis=1)

# Target (Output)
y = data["CO2_Emissions_Mt"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model trained successfully!")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 4))

# Save model
joblib.dump(model, "environment/ml/model.pkl")

# Save encoder
joblib.dump(encoder, "environment/ml/encoder.pkl")

print("\nModel saved as model.pkl")
print("Encoder saved as encoder.pkl")
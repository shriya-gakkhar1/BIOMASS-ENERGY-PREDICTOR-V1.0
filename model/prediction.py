import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load data
data = pd.read_csv("data/sample_data.csv")

# Features and target
X = data[['biomass_type', 'quantity', 'temp', 'humidity']]
y = data['energy_output']

# One-hot encode biomass_type
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), ['biomass_type'])],
    remainder='passthrough'
)

# Build model pipeline
model = Pipeline(steps=[
    ('preprocess', preprocessor),
    ('regressor', LinearRegression())
])

# Train model
model.fit(X, y)

# Prediction function
def predict_energy(biomass_type, quantity, temp, humidity):
    X_input = pd.DataFrame([[biomass_type, quantity, temp, humidity]],
                           columns=['biomass_type', 'quantity', 'temp', 'humidity'])
    return model.predict(X_input)[0]

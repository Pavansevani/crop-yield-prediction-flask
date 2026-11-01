import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

dataset = pd.read_csv("india_farm_dataset.csv")

target = dataset["yield_q_per_ha"]
features = dataset.drop(columns=["farm_id", "yield_q_per_ha"])

Xtrain, Xtest, Ytrain, Ytest = train_test_split(features, target, train_size=0.8, random_state=42)

model = RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=42, n_jobs=-1)
print("Model training started...")
model.fit(Xtrain, Ytrain)
print("Model training completed...")

pred = model.predict(Xtest)
print("R2:", r2_score(Ytest, pred))
print("MAE:", mean_absolute_error(Ytest, pred))

joblib.dump(model, "trainedmodel.joblib")
print("Model saved to disk...")

sample = [[3,4,4,21,1,3,2,1,4.95,7.35,0.79,220.3,29.7,165.5,31.5,25.8,1174.9,62.6,7.9,10,368,5859.9,246.9,7.3,1.55,16,227.9,1]]
prediction = model.predict(pd.DataFrame(sample, columns=features.columns))
print(f"Predicted Yield: {prediction[0]:.1f} q/ha")
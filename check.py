import pandas as pd 

data = pd.read_csv("predicted_results.csv")

data["difference"] = data["Actual"] -  data['Predicted']
data["difference"] = abs(data["difference"])
data.to_csv("difference.csv")


newdata = data[data["Predicted"]<60]

print(len(newdata))
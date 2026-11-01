from flask import Flask, request, render_template
import pandas as pd
import joblib
from pymongo import MongoClient   # NEW

model = joblib.load('trainedmodel.joblib')

# NEW: connect to MongoDB Atlas
client = MongoClient("mongodb+srv://pavansevani2116_db_user:AeyHPUKPUY3hyA6W@cluster0.brjqkg0.mongodb.net/")
collection = client["crop_yield_db"]["predictions"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        state_code = float(request.form.get("state_code"))
        agro_climatic_zone_code = float(request.form.get("agro_climatic_zone_code"))
        season_code = float(request.form.get("season_code"))
        crop_code = float(request.form.get("crop_code"))
        soil_type_code = float(request.form.get("soil_type_code"))
        irrigation_type_code = float(request.form.get("irrigation_type_code"))
        seed_type_code = float(request.form.get("seed_type_code"))
        mechanization_code = float(request.form.get("mechanization_code"))
        farm_size_ha = float(request.form.get("farm_size_ha"))
        soil_ph = float(request.form.get("soil_ph"))
        organic_carbon_pct = float(request.form.get("organic_carbon_pct"))
        nitrogen_kg_ha = float(request.form.get("nitrogen_kg_ha"))
        phosphorus_kg_ha = float(request.form.get("phosphorus_kg_ha"))
        potassium_kg_ha = float(request.form.get("potassium_kg_ha"))
        soil_moisture_pct = float(request.form.get("soil_moisture_pct"))
        avg_temp_c = float(request.form.get("avg_temp_c"))
        rainfall_mm = float(request.form.get("rainfall_mm"))
        humidity_pct = float(request.form.get("humidity_pct"))
        sunshine_hours = float(request.form.get("sunshine_hours"))
        sowing_month = float(request.form.get("sowing_month"))
        crop_duration_days = float(request.form.get("crop_duration_days"))
        seed_rate_kg_ha = float(request.form.get("seed_rate_kg_ha"))
        fertilizer_kg_ha = float(request.form.get("fertilizer_kg_ha"))
        organic_manure_t_ha = float(request.form.get("organic_manure_t_ha"))
        pesticide_l_ha = float(request.form.get("pesticide_l_ha"))
        num_irrigations = float(request.form.get("num_irrigations"))
        labour_days_ha = float(request.form.get("labour_days_ha"))
        pest_disease_code = float(request.form.get("pest_disease_code"))

        input_data = [[
            state_code, agro_climatic_zone_code, season_code,
            crop_code, soil_type_code, irrigation_type_code,
            seed_type_code, mechanization_code, farm_size_ha,
            soil_ph, organic_carbon_pct, nitrogen_kg_ha,
            phosphorus_kg_ha, potassium_kg_ha, soil_moisture_pct,
            avg_temp_c, rainfall_mm, humidity_pct,
            sunshine_hours, sowing_month, crop_duration_days,
            seed_rate_kg_ha, fertilizer_kg_ha, organic_manure_t_ha,
            pesticide_l_ha, num_irrigations, labour_days_ha,
            pest_disease_code
        ]]

        prediction = model.predict(input_data)

        result = round(float(prediction[0]), 1)

        # NEW: save this prediction to MongoDB
        collection.insert_one({
            "state_code": state_code,
            "agro_climatic_zone_code": agro_climatic_zone_code,
            "season_code": season_code,
            "crop_code": crop_code,
            "soil_type_code": soil_type_code,
            "irrigation_type_code": irrigation_type_code,
            "seed_type_code": seed_type_code,
            "mechanization_code": mechanization_code,
            "farm_size_ha": farm_size_ha,
            "soil_ph": soil_ph,
            "organic_carbon_pct": organic_carbon_pct,
            "nitrogen_kg_ha": nitrogen_kg_ha,
            "phosphorus_kg_ha": phosphorus_kg_ha,
            "potassium_kg_ha": potassium_kg_ha,
            "soil_moisture_pct": soil_moisture_pct,
            "avg_temp_c": avg_temp_c,
            "rainfall_mm": rainfall_mm,
            "humidity_pct": humidity_pct,
            "sunshine_hours": sunshine_hours,
            "sowing_month": sowing_month,
            "crop_duration_days": crop_duration_days,
            "seed_rate_kg_ha": seed_rate_kg_ha,
            "fertilizer_kg_ha": fertilizer_kg_ha,
            "organic_manure_t_ha": organic_manure_t_ha,
            "pesticide_l_ha": pesticide_l_ha,
            "num_irrigations": num_irrigations,
            "labour_days_ha": labour_days_ha,
            "pest_disease_code": pest_disease_code,
            "predicted_yield": result
        })

        return render_template('index.html', result=result)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
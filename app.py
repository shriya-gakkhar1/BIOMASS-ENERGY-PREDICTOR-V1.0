import streamlit as st
import requests

from model.prediction import predict_energy


# --------------------- CONFIG ---------------------
st.set_page_config(page_title="BioPredict", page_icon="🌱")

# --------------------- HEADER ---------------------
st.title("🌱 BioPredict – Bioenergy Forecasting App")
st.markdown("Predict how much bioenergy (biogas or biofuel) you can produce based on biomass and weather data.")

# --------------------- INPUT SECTION ---------------------
name=st.text_input("Enter your name")
st.header(" Enter Biomass and Location")

biomass_type = st.selectbox("Select Biomass Type", ["Cow Dung", "Rice Husk", "Bagasse", "Kitchen Waste", "Other"])
quantity = st.number_input("Enter Quantity (in kg)", min_value=1, step=1)
location = st.text_input("Enter Your Location (City or Village)")

# --------------------- WEATHER FETCH FUNCTION ---------------------
def get_weather(city):
    API_KEY = "d9bcc47362649d83870a6bbd0946b5c8" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        return temp, humidity
    except:
        return None, None

# --------------------- ACTION BUTTON ---------------------
if st.button("Predict Energy Output"):
    if location:
        temp, humidity = get_weather(location)

        if temp is not None:
            st.success(f"📍 Weather in {location}: {temp}°C, {humidity}% humidity")

            #
            # Energy = (Quantity × Type Factor) adjusted by temp & humidity
            biomass_factors = {
                "Cow Dung": 0.45,
                "Rice Husk": 0.52,
                "Bagasse": 0.50,
                "Kitchen Waste": 0.48,
                "Other": 0.40
            }

            base_energy = quantity * biomass_factors.get(biomass_type, 0.40)
            temp_factor = 1 + ((temp - 30) * 0.01)  # Increase if temp > 30
            humidity_factor = 1 - ((humidity - 60) * 0.005)  # Slight decrease if very humid

            predicted_energy = base_energy * temp_factor * humidity_factor

            st.subheader("🔋 Estimated Energy Output")
            st.info(f"🌿 You can produce approximately **{predicted_energy:.2f} kWh** from {quantity} kg of {biomass_type}.")
            st.success(f"Thank you {name} for using BioPredict!🌎")
        else:
            st.error("❌ Could not fetch weather data. Please check your location.")
    else:
        st.warning("Please enter a valid location.")

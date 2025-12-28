import streamlit as st
import sys
import os

# Ensure the project root is in the path so we can import our layers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.charging.application.services.ChargingStationService import ChargingStationService
from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository

# Initialize components
repo = ChargingStationRepository()
service = ChargingStationService(repo)

st.title("⚡ Berlin Charging Station Finder")
st.subheader("Find stations by Postal Code (PLZ)")

zip_input = st.text_input("Enter a 5-digit Berlin ZIP code (e.g., 10117):", "")

if st.button("Search"):
    try:
        # The service uses the PostalCode Value Object, 
        # so it will raise a ValueError if the input is invalid.
        results = service.find_charging_stations(zip_input)
        
        if results:
            st.success(f"Found {len(results)} stations in {zip_input}")
            st.table(results)
        else:
            st.warning("No stations found for this ZIP code.")
            
    except ValueError as e:
        st.error(f"⚠️ {e}")
import sys
import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from pathlib import Path

# --- DYNAMIC PATH SETUP ---
current_file = Path(__file__).resolve()
# app.py(0) -> presentation(1) -> src(2) -> Root(3)
project_root = current_file.parents[2]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.charging.application.services.ChargingStationService import ChargingStationService
from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository
from src.maintenance.application.services.MalfunctionService import MalfunctionService
from src.maintenance.infrastructure.repositories.MalfunctionRepository import MalfunctionRepository

# ... (Include the rest of the main() function from my previous full code block)

# ==========================================
# 🚨 PERFORMANCE & BOUNDARY CONFIG
# ==========================================
pd.set_option("styler.render.max_elements", 500000)

# Berlin Bounding Box for Geofencing
LAT_MIN, LAT_MAX = 52.33, 52.68
LON_MIN, LON_MAX = 13.08, 13.76

# Initialize backend services
search_repo = ChargingStationRepository()
search_service = ChargingStationService(search_repo)
malfunction_repo = MalfunctionRepository() 
malfunction_service = MalfunctionService(malfunction_repo)

@st.cache_data
def load_and_filter_berlin():
    """Loads dataset and applies physical boundary filter for Berlin."""
    df = pd.read_csv(search_repo.path, sep=';', encoding='utf-8-sig', low_memory=False)
    df.columns = [c.strip().strip("'").strip('"') for c in df.columns]
    
    # Coordinate Conversion
    df['lat'] = pd.to_numeric(df['Breitengrad'].astype(str).str.replace(',', '.'), errors='coerce')
    df['lon'] = pd.to_numeric(df['Längengrad'].astype(str).str.replace(',', '.'), errors='coerce')
    
    # Filter for Berlin Bounding Box
    mask = (df['lat'] >= LAT_MIN) & (df['lat'] <= LAT_MAX) & (df['lon'] >= LON_MIN) & (df['lon'] <= LON_MAX)
    df = df[mask].dropna(subset=['lat', 'lon']).copy()
    
    # Clean Postal Codes
    df['Postleitzahl'] = df['Postleitzahl'].astype(str).str.split('.').str[0].str.zfill(5)
    return df

def main():
    st.set_page_config(page_title="Berlin Charging Hub", layout="wide", page_icon="⚡")
    st.title("⚡ Berlin Charging Hub")

    # --- 🔔 SUCCESS MESSAGES ---
    if 'report_success' in st.session_state:
        st.success(st.session_state['report_success'])
        del st.session_state['report_success']

    role = st.sidebar.radio("Select User Mode:", ["🚗 Driver", "👮 Operator"])
    st.sidebar.markdown("---")

    # --- 🔎 STEP 1: DATA SELECTION ---
    st.sidebar.header("1. Selection")
    view_all = st.sidebar.checkbox("Show All Berlin Stations")
    zip_input = st.sidebar.text_input("OR Enter 5-digit ZIP:", placeholder="e.g. 10117")

    display_df = pd.DataFrame()
    if view_all:
        display_df = load_and_filter_berlin()
    elif zip_input:
        try:
            stations = search_service.find_charging_stations(zip_input)
            if stations:
                temp_df = pd.DataFrame(stations)
                temp_df.columns = [c.strip().strip("'").strip('"') for c in temp_df.columns]
                temp_df['lat'] = pd.to_numeric(temp_df['Breitengrad'].astype(str).str.replace(',', '.'), errors='coerce')
                temp_df['lon'] = pd.to_numeric(temp_df['Längengrad'].astype(str).str.replace(',', '.'), errors='coerce')
                display_df = temp_df[(temp_df['lat'] >= LAT_MIN) & (temp_df['lat'] <= LAT_MAX)].copy()
        except ValueError as e:
            st.sidebar.error(f"⚠️ {e}")

    # --- 🛠️ STEP 2: DATA PROCESSING & ID SEQUENCING ---
    all_valid_ids = []
    if not display_df.empty:
        str_col = 'Straße' if 'Straße' in display_df.columns else 'Strasse'
        display_df['Street'] = display_df[str_col].astype(str) + " " + display_df['Hausnummer'].astype(str)
        display_df = display_df.rename(columns={'Betreiber': 'Operator'})
        
        # ID Generation (BER-PLZ-Rank)
        display_df['Postleitzahl'] = display_df['Postleitzahl'].astype(str).str.split('.').str[0].str.zfill(5)
        display_df['station_rank'] = display_df.groupby('Postleitzahl').cumcount() + 1
        display_df['Station ID'] = "BER-" + display_df['Postleitzahl'] + "-" + display_df['station_rank'].astype(str)
        all_valid_ids = display_df['Station ID'].tolist()

        # Status Logic
        reports = malfunction_repo.get_all()
        broken_ids = [str(r.get('station_id')) for r in reports]
        display_df['Availability'] = display_df.apply(
            lambda x: "Not Available" if str(x.get('Station ID')) in broken_ids else "Available", axis=1
        )
        
        display_df['tip_color'] = display_df['Availability'].map({"Available": "#27ae60", "Not Available": "#e74c3c"})

        # Filters
        st.sidebar.markdown("---")
        st.sidebar.header("2. Filters")
        st_filter = st.sidebar.multiselect("Status:", ["Available", "Not Available"], default=["Available", "Not Available"])
        display_df = display_df[display_df['Availability'].isin(st_filter)]
        
        unique_ops = sorted([str(op) for op in display_df['Operator'].unique() if pd.notna(op)])
        if unique_ops:
            op_filter = st.sidebar.multiselect("Operator:", unique_ops, default=unique_ops)
            display_df = display_df[display_df['Operator'].astype(str).isin(op_filter)]

    # --- 🗺️ STEP 3: VISUALIZATION ---
    view_state = pdk.ViewState(latitude=52.5200, longitude=13.4050, zoom=10 if view_all else 12)
    
    if not display_df.empty:
        # Overlap Jitter
        display_df['lat_j'] = display_df['lat'] + [random.uniform(-0.0001, 0.0001) for _ in range(len(display_df))]
        display_df['lon_j'] = display_df['lon'] + [random.uniform(-0.0001, 0.0001) for _ in range(len(display_df))]
        
        # Visual Styling
        display_df['fill'] = display_df['Availability'].apply(lambda x: [46, 204, 113, 200] if x == "Available" else [231, 76, 60, 200])
        display_df['border'] = [[0, 0, 0, 255]] * len(display_df)

        st.pydeck_chart(pdk.Deck(
            map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
            initial_view_state=view_state,
            layers=[pdk.Layer(
                "ScatterplotLayer",
                data=display_df,
                get_position="[lon_j, lat_j]",
                get_fill_color="fill",
                get_line_color="border",
                stroked=True,
                get_line_width=2,
                get_radius=120,
                pickable=True
            )],
            tooltip={
                "html": "<b>ID:</b> {Station ID}<br/>"
                        "<b>Status:</b> <span style='color: {tip_color}; font-weight: bold;'>{Availability}</span>"
            }
        ))
        
        st.markdown(f"### 📋 {len(display_df)} Stations Found")
        st.dataframe(
            display_df[['Station ID', 'Availability', 'Operator', 'Street']].rename(columns={'Availability': 'Status'}).style.applymap(
                lambda v: f"color: {'#e74c3c' if v == 'Not Available' else '#27ae60'}; font-weight: bold", subset=['Status']
            ), use_container_width=True
        )
    else:
        st.pydeck_chart(pdk.Deck(map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', initial_view_state=view_state))

    # --- 🔧 STEP 4: ACTIONS ---
    st.markdown("---")
    if role == "🚗 Driver":
        st.subheader("🔧 Report a Malfunction")
        with st.form("report_form", clear_on_submit=True):
            in_id = st.text_input("Enter Station ID")
            desc = st.text_area("Issue Details")
            if st.form_submit_button("🚨 Submit"):
                if in_id not in all_valid_ids:
                    st.error(f"❌ Invalid ID: '{in_id}'.")
                elif len(desc) < 5:
                    st.error("❌ Description too short.")
                else:
                    if malfunction_service.report_malfunction(in_id, desc):
                        st.session_state['report_success'] = f"🎉 Reported! Station {in_id} updated."
                        st.rerun()
    else:
        st.subheader("👮 Operator Admin")
        reps = malfunction_repo.get_all()
        if reps:
            df_reps = pd.DataFrame(reps).rename(columns={'station_id': 'Station ID', 'description': 'Description'})
            df_reps['Status'] = 'Open'
            st.dataframe(df_reps[['Station ID', 'Description', 'Status']].style.applymap(lambda x: "color: #e74c3c; font-weight: bold", subset=['Status']), use_container_width=True)
            
            target = st.selectbox("Resolve ID:", df_reps['Station ID'].unique())
            if st.button("✅ Resolve"):
                full_csv = pd.read_csv(malfunction_repo.path)
                full_csv = full_csv[full_csv['station_id'] != target]
                full_csv.to_csv(malfunction_repo.path, index=False)
                st.session_state['report_success'] = f"✅ Resolved {target}!"
                st.rerun()
        else:
            st.info("No active reports.")

if __name__ == "__main__":
    main()
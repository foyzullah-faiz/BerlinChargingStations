import sys
import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from pathlib import Path

# ==========================================
# 🚨 PERFORMANCE & BOUNDARY CONFIG
# ==========================================
pd.set_option("styler.render.max_elements", 500000)

LAT_MIN, LAT_MAX = 52.33, 52.68
LON_MIN, LON_MAX = 13.08, 13.76

# ==========================================
# 🚨 PATH & LAYER SETUP
# ==========================================
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.charging.application.services.ChargingStationService import ChargingStationService
from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository
from src.maintenance.application.services.MalfunctionService import MalfunctionService
from src.maintenance.infrastructure.repositories.MalfunctionRepository import MalfunctionRepository

# Initialize backend services
search_repo = ChargingStationRepository()
search_service = ChargingStationService(search_repo)
malfunction_repo = MalfunctionRepository() 
malfunction_service = MalfunctionService(malfunction_repo)

@st.cache_data
def load_and_filter_berlin():
    df = pd.read_csv(search_repo.path, sep=';', encoding='utf-8-sig', low_memory=False)
    df.columns = [c.strip().strip("'").strip('"') for c in df.columns]
    df['lat'] = pd.to_numeric(df['Breitengrad'].astype(str).str.replace(',', '.'), errors='coerce')
    df['lon'] = pd.to_numeric(df['Längengrad'].astype(str).str.replace(',', '.'), errors='coerce')
    berlin_mask = (df['lat'] >= LAT_MIN) & (df['lat'] <= LAT_MAX) & (df['lon'] >= LON_MIN) & (df['lon'] <= LON_MAX)
    df = df[berlin_mask].dropna(subset=['lat', 'lon']).copy()
    df['Postleitzahl'] = df['Postleitzahl'].astype(str).str.split('.').str[0].str.zfill(5)
    return df

def main():
    st.set_page_config(page_title="Berlin Charging Hub", layout="wide", page_icon="⚡")
    st.title("⚡ Berlin Charging Hub")

    if 'report_success' in st.session_state:
        st.success(st.session_state['report_success'])
        del st.session_state['report_success']

    role = st.sidebar.radio("Select User Mode:", ["🚗 Driver", "👮 Operator"])
    st.sidebar.markdown("---")

    # --- 🔎 DATA SELECTION ---
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

    # --- 🛠️ DATA PROCESSING ---
    all_valid_ids = []
    if not display_df.empty:
        str_col = 'Straße' if 'Straße' in display_df.columns else 'Strasse'
        display_df['Street'] = display_df[str_col].astype(str) + " " + display_df['Hausnummer'].astype(str)
        display_df = display_df.rename(columns={'Betreiber': 'Operator'})
        
        display_df['Postleitzahl'] = display_df['Postleitzahl'].astype(str).str.split('.').str[0].str.zfill(5)
        display_df['station_rank'] = display_df.groupby('Postleitzahl').cumcount() + 1
        display_df['Station ID'] = "BER-" + display_df['Postleitzahl'] + "-" + display_df['station_rank'].astype(str)
        
        all_valid_ids = display_df['Station ID'].tolist()

        reports = malfunction_repo.get_all()
        broken_ids = [str(r.get('station_id')) for r in reports]
        display_df['Availability'] = display_df.apply(
            lambda x: "Not Available" if str(x.get('Station ID')) in broken_ids else "Available", axis=1
        )

        # 🎨 Tooltip Color Logic (Helper column for HTML color)
        display_df['status_color'] = display_df['Availability'].apply(
            lambda x: "#27ae60" if x == "Available" else "#e74c3c"
        )

        # Filters
        st.sidebar.markdown("---")
        status_filter = st.sidebar.multiselect("Filter Availability:", ["Available", "Not Available"], default=["Available", "Not Available"])
        display_df = display_df[display_df['Availability'].isin(status_filter)]
        unique_ops = sorted([str(op) for op in display_df['Operator'].unique() if pd.notna(op)])
        if unique_ops:
            op_filter = st.sidebar.multiselect("Filter Operator:", unique_ops, default=unique_ops)
            display_df = display_df[display_df['Operator'].astype(str).isin(op_filter)]

    # --- 🗺️ VISUALIZATION ---
    view_state = pdk.ViewState(latitude=52.5200, longitude=13.4050, zoom=10 if view_all else 12)
    if not display_df.empty:
        display_df['lat_j'] = display_df['lat'] + [random.uniform(-0.0001, 0.0001) for _ in range(len(display_df))]
        display_df['lon_j'] = display_df['lon'] + [random.uniform(-0.0001, 0.0001) for _ in range(len(display_df))]
        display_df['fill_color'] = display_df['Availability'].apply(lambda x: [46, 204, 113, 200] if x == "Available" else [231, 76, 60, 200])
        display_df['line_color'] = [[0, 0, 0, 255]] * len(display_df)

        st.pydeck_chart(pdk.Deck(
            map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
            initial_view_state=view_state,
            layers=[pdk.Layer(
                "ScatterplotLayer", 
                data=display_df, 
                get_position="[lon_j, lat_j]", 
                get_fill_color="fill_color", 
                get_line_color="line_color", 
                stroked=True, 
                get_line_width=2, 
                get_radius=120, 
                pickable=True
            )],
            # 💡 HTML TOOLTIP WITH COLOR LOGIC
            tooltip={
                "html": "<b>ID:</b> {Station ID}<br/>"
                        "<b>Status:</b> <span style='color: {status_color}; font-weight: bold;'>{Availability}</span>",
                "style": {"color": "white"}
            }
        ))
        
        st.markdown(f"### 📋 Showing {len(display_df)} Stations in Berlin")
        def color_status(val):
            return f"color: {'#e74c3c' if val == 'Not Available' else '#27ae60'}; font-weight: bold"
        st.dataframe(display_df[['Station ID', 'Availability', 'Operator', 'Street']].rename(columns={'Availability': 'Status'}).style.applymap(color_status, subset=['Status']), use_container_width=True)
    else:
        st.pydeck_chart(pdk.Deck(map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', initial_view_state=view_state))

    # --- 🔧 ACTIONS ---
    st.markdown("---")
    if role == "🚗 Driver":
        st.subheader("🔧 Report a Malfunction")
        with st.form("report_form", clear_on_submit=True):
            input_id = st.text_input("Enter Station ID")
            description = st.text_area("Issue Details")
            if st.form_submit_button("🚨 Submit Report"):
                if input_id not in all_valid_ids:
                    st.error(f"❌ Invalid station ID: '{input_id}'")
                elif len(description) < 5:
                    st.error("❌ Description too short.")
                else:
                    try:
                        if malfunction_service.report_malfunction(input_id, description):
                            st.session_state['report_success'] = f"🎉 Reported {input_id}!"
                            st.rerun()
                    except ValueError as e: st.error(f"❌ {e}")
    else:
        st.subheader("👮 Operator Admin")
        reports_data = malfunction_repo.get_all()
        if reports_data:
            df_ops = pd.DataFrame(reports_data)
            df_ops = df_ops.rename(columns={'station_id': 'Station ID', 'description': 'Description'})
            df_ops['Status'] = 'Open'
            st.dataframe(df_ops[['Station ID', 'Description', 'Status']].style.applymap(lambda x: "color: #e74c3c; font-weight: bold" if x == 'Open' else "", subset=['Status']), use_container_width=True)
            
            target_id = st.selectbox("Resolve Station ID:", df_ops['Station ID'].unique())
            if st.button("✅ Resolve"):
                full_csv_df = pd.read_csv(malfunction_repo.path)
                full_csv_df = full_csv_df[full_csv_df['station_id'] != target_id]
                full_csv_df.to_csv(malfunction_repo.path, index=False)
                st.session_state['report_success'] = f"✅ Resolved {target_id}!"
                st.rerun()
        else:
            st.info("No active reports.")

if __name__ == "__main__": main()
import streamlit as st
import pandas as pd
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

# 🛠 Google Sheets Setup
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

# ✅ OPEN SHEET BY URL (your shared link)
sheet_url = "https://docs.google.com/spreadsheets/d/1CF3KJBtkwYC0g8oP4FOCrwfTwAESVoADgFa8aFyiKE0/edit?gid=0"
sheet = client.open_by_url(sheet_url).sheet1

# 🚀 App Setup
st.set_page_config(page_title="ESUAE Attendance Register")
st.title("📘 ESUAE Attendance Register")

# 📥 Load athlete data
try:
    athlete_df = pd.read_excel("Ballers_athletes.xlsx")
    st.write("✅ Excel file loaded")
except Exception as e:
    st.error(f"❌ Could not load Excel file: {e}")
    st.stop()

athlete_df.columns = athlete_df.columns.str.strip()

# 🧠 Session State
if "attendance" not in st.session_state:
    st.session_state.attendance = {}

# 📅 Date Input
selected_date = st.date_input("📅 Select date for attendance", date.today())

# 🏅 Sport Selection
sports = athlete_df["Sport"].unique()
selected_sport = st.selectbox("🏅 Select sport", sports)

# ✅ Athlete Selection
filtered_athletes = athlete_df[athlete_df["Sport"] == selected_sport]["Athlete list"].tolist()
st.write("👥 **Mark Attendance**")

for athlete in filtered_athletes:
    if athlete not in st.session_state.attendance:
        st.session_state.attendance[athlete] = {"present": True, "status": "Present"}

    col1, col2 = st.columns([3, 2])
    with col1:
        present = st.checkbox(f"{athlete}", value=st.session_state.attendance[athlete]["present"], key=f"{athlete}_check")
    with col2:
        if not present:
            status = st.selectbox(
                "Reason",
                ["Unknown", "Work Commitment", "School Commitment", "Family Commitment", "Injury", "Illness", "Club Training", "Competition"],
                key=f"{athlete}_dropdown"
            )
            st.session_state.attendance[athlete] = {"present": False, "status": status}
        else:
            st.session_state.attendance[athlete] = {"present": True, "status": "Present"}

# 💾 Save to Google Sheets
if st.button("💾 Save Attendance"):
    new_records = [
        [str(selected_date), selected_sport, athlete, st.session_state.attendance[athlete]["status"]]
        for athlete in filtered_athletes
    ]
    sheet.append_rows(new_records)
    st.success("✅ Attendance saved to Google Sheets!")


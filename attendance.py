import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

# -------------------------------
# ✅ App setup
# -------------------------------
st.set_page_config(page_title="ESUAE Attendance Register")
st.title("📘 ESUAE Attendance Register")

st.write("👋 App started...")

# -------------------------------
# ✅ Load athlete data
# -------------------------------
try:
    athlete_df = pd.read_excel("Ballers_athletes.xlsx")
    st.write("✅ Excel file loaded successfully")
except Exception as e:
    st.error(f"❌ Failed to load Excel file: {e}")
    st.stop()

athlete_df.columns = athlete_df.columns.str.strip()

# -------------------------------
# ✅ Session state setup
# -------------------------------
if "attendance" not in st.session_state:
    st.session_state.attendance = {}

# -------------------------------
# 🗓 Step 1: Select Date
# -------------------------------
selected_date = st.date_input("📅 Select date for attendance", date.today())

# -------------------------------
# 🏅 Step 2: Select Sport
# -------------------------------
sports = athlete_df["Sport"].unique()
selected_sport = st.selectbox("🏅 Select sport", sports)

# -------------------------------
# 👥 Step 3: Athlete checkboxes
# -------------------------------
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

# -------------------------------
# 💾 Step 4: Save & Download
# -------------------------------
if st.button("💾 Save Attendance"):
    new_records = [
        {
            "Date": selected_date,
            "Sport": selected_sport,
            "Athlete": athlete,
            "Status": st.session_state.attendance[athlete]["status"]
        }
        for athlete in filtered_athletes
    ]

    new_df = pd.DataFrame(new_records)

    # Convert to Excel in memory
    output = BytesIO()
    new_df.to_excel(output, index=False)

    st.success("✅ Attendance file created successfully")
    st.download_button(
        label="📥 Download Attendance File",
        data=output.getvalue(),
        file_name=f"attendance_{selected_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

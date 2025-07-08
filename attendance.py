import streamlit as st
import pandas as pd
from datetime import date
import os


# App Title
st.set_page_config(page_title="ESUAE Attendance Register")
st.title("📘 ESUAE Attendance Register")

# Load athlete data
athlete_df = pd.read_excel("Ballers_athletes.xlsx")
 # adjust path as needed
athlete_df.columns = athlete_df.columns.str.strip()

# Initialize session state
if "attendance" not in st.session_state:
    st.session_state.attendance = {}

# Step 1: Select Date
selected_date = st.date_input("📅 Select date for attendance", date.today())

# Step 2: Select Sport
sports = athlete_df["Sport"].unique()
selected_sport = st.selectbox("🏅 Select sport", sports)

# Step 3: Get list of athletes
filtered_athletes = athlete_df[athlete_df["Sport"] == selected_sport]["Athlete list"].tolist()

# Step 4: Loop through each athlete with checkbox + optional dropdown
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

# Step 5: Save Attendance
if st.button("💾 Save Attendance"):
    # Prepare records
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

    # Save path – change this if needed
    output_path = r"C:\Users\User\OneDrive - General Authority of sports\For ALL\Documents\Data Management\Attendance"
    output_file = os.path.join(output_path, "attendance_record.xlsx")

    # Ensure the folder exists (optional but safe)
    os.makedirs(output_path, exist_ok=True)

    # Append to or create the file
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    updated_df.to_excel(output_file, index=False)
    st.success(f"✅ Attendance saved to: {output_file}")

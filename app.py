import streamlit as st
from homie.files.csv import FlatCSVUploader


def load_data():
    st.subheader("Load Data from CSV")
    csv_uploader = FlatCSVUploader()
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        csv_uploader.populate(uploaded_file)

def find_flat_coordinates():
    st.subheader("Find Flat Coordinates")
    # Add your code to find flat coordinates here
    # For example:
    flat_address = st.text_input("Enter flat address:")
    st.write(f"Coordinates for {flat_address}: (latitude, longitude)")

def match_flats_with_services():
    st.subheader("Match Flats with Services")
    # Add your code to match flats with services here
    # For example:
    flats = ["Flat A", "Flat B", "Flat C"]
    services = ["Service 1", "Service 2", "Service 3"]
    st.write("Matching flats with services:")
    for flat in flats:
        for service in services:
            st.write(f"{flat} - {service}")


# Main app
st.title("Apartment Scoring")
st.subheader("Looking for an apartment? We can help you find the best one!")
menu_options = [
    "Home",
    "Load Data from CSV",
    "Find Flat Coordinates",
    "Match Flats with Services"
]
selected_option = st.sidebar.selectbox("Menu", menu_options)

if selected_option == "Load Data from CSV":
    load_data()
elif selected_option == "Find Flat Coordinates":
    find_flat_coordinates()
elif selected_option == "Match Flats with Services":
    match_flats_with_services()
import streamlit as st

from homie.db.engine import create_db_and_tables

create_db_and_tables()



# Main app
st.title("Apartment Scoring")
st.subheader("Looking for an apartment? We can help you find the best one!")


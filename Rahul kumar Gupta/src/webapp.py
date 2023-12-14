import streamlit as st
import requests
import pandas as pd
from io import StringIO

st.title("Scraping Leads From Apollo.io Database")

# Get user input (URL)
link = st.text_input("Enter URL:")

if st.button("Scrape"):
    # Send request to FastAPI with JSON payload
    fastapi_url = "http://127.0.0.1:8000/scrape"
    st.info("Scraping in progress... Please wait.")
    response = requests.post(fastapi_url, json={"link": link})  # Use json parameter for JSON payload

    # Check if the request was successful
    if response.status_code == 200:
        st.success("Scraping successful!")
           # Read CSV content from the response
        csv_content = response.content.decode("utf-8")
        print(csv_content)
        # Convert CSV content to DataFrame
        df = pd.read_csv(StringIO(csv_content))
        # Increase the display size of the DataFrame
        st.dataframe(df, height=800, width=1400)
        

        st.download_button(
            "Download CSV",
            csv_content,
            key="download_button",
            file_name="scraped_data.csv",
            mime="text/csv",
        )
    else:
        st.error(f"Error: {response.text}")

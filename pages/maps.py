from turtledemo.forest import start

import numpy
import streamlit as st
import data_storage
import pandas as pd
import pydeck as pdk

from pages.user import address, height

# Fetch coordinate data from storage
data = data_storage.get_data("email, ph_no, address, lat, long, postcode, city, state, country, breadth, length, height,status")
cord=[]
for i in data:
    cord.append((i[3],i[4]))


# Convert to DataFrame
df = pd.DataFrame(cord, columns=["lat", "lon"])
df_data = pd.DataFrame(data,columns=[
    "email",
    "ph_no",
    "address",
    "lat",
    "long",
    "postcode",
    "city",
    "state",
    "country",
    "breadth",
    "length",
    "height",
    "status"
])

df_data.index = numpy.arange(1, len(df_data)+1)

# Initialize session state for clicked info
if "clicked_info" not in st.session_state:
    st.session_state.clicked_info = "Click on a pin to see details."

# Define an icon for constant size
ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/e/ed/Map_pin_icon.svg"

icon_data = {
    "url": ICON_URL,
    "width": 128,
    "height": 128,
    "anchorY": 128  # Ensures the pin's tip is on the location
}

df["icon"] = [icon_data] * len(df)  # Apply icon settings to all rows

# Pydeck Icon Layer (to keep pin size constant)
layer = pdk.Layer(
    "IconLayer",
    df,
    get_position=["lon", "lat"],
    get_icon="icon",
    get_size=20,  # Keeps size fixed across zoom levels
    pickable=True  # Makes markers clickable
)

# View centered at first coordinate
view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=6
)

# Pydeck Map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11",
    tooltip={"text": "Latitude: {lat}\nLongitude: {lon}"}
)

# Display Map
st.pydeck_chart(r)

# Display clicked info
st.subheader("📍 Selected Location Details")
st.write(st.session_state.clicked_info)
with st.expander("📊 Click to Expand Data Table"):

    st.dataframe(df_data)

import streamlit as st
import data_storage
import location_raj
from streamlit_js_eval import get_geolocation
try:
    location = get_geolocation()["coords"]
except:
    address=0
    pass

from streamlit_geolocation import streamlit_geolocation
st.title("FULL STACK ATTACK")



enable = st.checkbox("enable camera")
picture = st.camera_input("Take a picture",disabled=not enable)


if picture:
    st.image(picture)
location_button = st.button("Get Location")
if location_button:
    lat=location['latitude']
    long=location['longitude']
    address = location_raj.reverse_location(lat, long)["display_name"]
    st.write(lat,long)
    st.write(f'''

latitude: {lat}
longitude: {long}
address: {address}


''')
email= st.text_input("Email")
ph_no= st.text_input("Phone No")


st.subheader("optional part")
metrics=st.radio("choose metrics :",["ft","cm","m"],horizontal=True)
breadth=st.number_input("breadth",step=0.2)
length=st.number_input("length",step=0.2)
height=st.number_input("height",step=0.2)
submit=st.button("Submit")
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_indian_number(phone):
    pattern = r'^(?:\+91|91|0)?[6-9]\d{9}$'
    return re.match(pattern, phone) is not None


# location = streamlit_geolocation()




if submit:
    errors = []


    if not email or not is_valid_email(email):
        errors.append("Invalid or missing email.")

    if not ph_no or not is_valid_indian_number(ph_no):
        errors.append("Invalid or missing phone number.")

    if not picture:
        errors.append("Please take a picture.")


    if errors:
        for error in errors:
            st.error(error)
    else:
        # Convert dimensions to meters if needed
        conversion_factor = {"ft": 0.3048, "cm": 0.01, "m": 1}
        factor = conversion_factor[metrics]

        breadth = round(breadth * factor, 3)
        height = round(height * factor, 3)
        length = round(length * factor, 3)

        st.write(f"Converted Dimensions - Breadth: {breadth}m, Height: {height}m, Length: {length}m")

        # Save image
        lat=location['latitude']
        long=location['longitude']
        pic_name = f"images/{lat}-{long}.jpg"
        a=picture.getbuffer()
        with open(pic_name, "wb") as f:
            f.write(a)
        address = location_raj.reverse_location(lat, long)

        st.success(f"Successfully uploaded the picture! address = {address["display_name"]} ")
        data_storage.insert_data(email,ph_no,address,pic_name,a,breadth,height,length)

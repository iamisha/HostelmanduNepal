import pyrebase
import streamlit as st

# firebase
firebaseConfig = {
  'apiKey': "AIzaSyBwdU7h0etn8hQ955FayCHp17y493izszE",
  'authDomain': "hostelmandunepal-e2d8b.firebaseapp.com",
  'databaseURL': "https://hostelmandunepal-e2d8b-default-rtdb.firebaseio.com/",
  'projectId': "hostelmandunepal-e2d8b",
  'storageBucket': "hostelmandunepal-e2d8b.appspot.com",
  'messagingSenderId': "819533083882",
  'appId': "1:819533083882:web:f3d783c52c85e5acea5393",
  'measurementId': "G-KL2YP4EWRP"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
if st.session_state.signout:
        st.success('You are logged in as ' + st.session_state.username +", Welcome!", icon="✅")
        st.sidebar.text(f"Email id: {st.session_state.useremail}")
        if st.sidebar.button('Sign out'):
            st.session_state.signout = False
            st.session_state.signedout = False
            st.session_state.username = ''
            st.session_state.useremail = ''
else:
    st.warning('Please login first', icon="⚠️")

def insert_data_to_database(data):
    hostel_name = data[0]
    college = data[1]
    location = data[2]
    gender = data[9]
    email = data[10]
    userid = data[11]

    hostel_data = {
        "hostel_name": hostel_name,
        "location": location,
        "gender": gender,
        "contact_email": email,
        "registered_by": userid
    }

    db.child("colleges").child(college).child("hostels").child(hostel_name).set(hostel_data)

    room_data = {
        "1_person": {
            "price": data[3],
            "capacity": data[6],
            "availability": True
        },
        "2_sharing": {
            "price": data[4],
            "capacity": data[7],
            "availability": True
        },
        "3_sharing": {
            "price": data[5],
            "capacity": data[8],
            "availability": True
        }
    }

    db.child("colleges").child(college).child("hostels").child(hostel_name).child("rooms info").set(room_data)

def main():
    st.markdown(
        "<h1 style='text-align: center; color: teal;'>Hostel Registration</h1>",
        unsafe_allow_html=True
    )

    hostel_name = st.text_input("Enter Hostel Name:")
    college = st.text_input("Enter Nearest College:")
    location = st.text_input("Enter Location:")
    Email = st.text_input("Contact Email ID:")
    gender = st.selectbox("Select your gender:", ["Male", "Female"])

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        price_per_person = st.number_input("Enter Price of single-room:", step=500, value=0)
        capacity_1_person = st.number_input("Enter Total No. of single-room available slot(s):", min_value=0, value=0)
    with col2:   
        price_2_sharing = st.number_input("Enter Price of 2-sharing:", step=500, value=0)
        capacity_2_sharing = st.number_input("Enter Total No. of 2-sharing rooms available slot(s):", min_value=0, value=0)
    with col3:
        price_3_sharing = st.number_input("Enter Price of 3-sharing:", step=500, value=0)
        capacity_3_sharing = st.number_input("Enter Total No. of 3-sharing rooms available slot(s):", min_value=0, value=0)

    if st.button("Insert Data",disabled= not st.session_state.signout ):
        if hostel_name and college and location and price_per_person and price_2_sharing and price_3_sharing and capacity_1_person and capacity_2_sharing and capacity_3_sharing:
            data = (
                hostel_name, college, location, price_per_person, price_2_sharing, price_3_sharing,
                capacity_1_person, capacity_2_sharing, capacity_3_sharing, gender,Email, st.session_state.username
            )
            insert_data_to_database(data)
            st.success("Data inserted successfully!")
        else:
            st.error("Please provide all the required information.")

if __name__ == '__main__':
    main()
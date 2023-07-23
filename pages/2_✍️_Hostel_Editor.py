import streamlit as st
import pyrebase
import time

# Initialize Firebase configuration
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

def get_hostel_names():
    hostel_names = []
    for college in db.child("colleges").shallow().get().val():
        hostels = db.child("colleges").child(college).child("hostels").shallow().get().val()
        if hostels is not None:
            hostel_names.extend(list(hostels))
    return hostel_names

def get_college_name(hostel_name):
    college_name = []
    for college in db.child("colleges").shallow().get().val():
        for hostel in db.child("colleges").child(college).child("hostels").shallow().get().val():
            if hostel_name == hostel:
                return college
            
def update_email(hostel_name,college, new_email):
    db.child("colleges").child(college).child("hostels").child(hostel_name).child("email").set(new_email)

def delete_hostel_info(hostel_name, college):
    db.child("colleges").child(college).child("hostels").child(hostel_name).remove()


# Function to get hostel information based on the selected hostel name
def get_hostel_info(hostel_name):
    college = get_college_name(hostel_name)
    hostel_info = db.child("colleges").child(college).child("hostels").child(hostel_name).get().val()
    return hostel_info

# Function to update the price of the selected hostel
def update_price(hostel_name, room_type, new_price, college):
    db.child("colleges").child(college).child("hostels").child(hostel_name).child("rooms info").child(room_type).update({"price": new_price})

def update_price_capacity_avialability(hostel_name, room_type, new_price, new_capacity,available, college):
    db.child("colleges").child(college).child("hostels").child(hostel_name).child("rooms info").child(room_type).update({"price": new_price, "capacity": new_capacity,"availability":available})

# Streamlit app
def main():
    global block_access
    block_access = True
    
    st.markdown(
        "<h1 style='text-align: center; color: teal;'>Hostel Editor</h1>",
        unsafe_allow_html=True
    )

    # Get unique hostel names
    hostel_names = get_hostel_names()

    # Select a hostel
    selected_hostel = st.selectbox("Select a hostel:", [""] +hostel_names)
    hostel_info = get_hostel_info(selected_hostel)
    college = get_college_name(selected_hostel)
    if db.child("colleges").child(college).child("hostels").child(selected_hostel).child("registered_by").shallow().get().val() == st.session_state.username:
        block_access = False


    # Display hostel information
    if hostel_info is not None:
        st.subheader("Hostel Information:")
        location = hostel_info.get("location", "")
        st.info(f"Nearest College: {college}")
        st.info(f"Location: {location}")

        # Get rooms info
        rooms_info = hostel_info.get("rooms info", {})

        col1, col2 = st.columns([1, 1])

        with col2:
            # Update email
            st.subheader("Update Email")
            new_email = st.text_input("Enter new email:",value=db.child("colleges").child(college).child("hostels").child(selected_hostel).child("contact_email").shallow().get().val())
            if st.button("Update Email",disabled= block_access):
                update_email(selected_hostel,college, new_email)
                st.success("Email updated successfully!")
            
              
            # Delete Hostel
            st.subheader("Delete Hostel Info")
            if st.button("Delete Hostel",disabled= block_access):
                delete_hostel_info(selected_hostel, college)
                st.success(f"Hostel '{selected_hostel}' information deleted successfully!")
                # Clear the selected hostel after deletion
                selected_hostel = None
                st.info("Please wait while the page refreshes...")
                time.sleep(2)
                st.experimental_rerun()
        with col1:
            # Update price
            st.subheader("Update Room Info")
            room_type = st.selectbox("Select room type:", ["1_person", "2_sharing", "3_sharing"])
            current_price = rooms_info.get(room_type, {}).get("price", 0)
            new_price = st.number_input("Enter the new price:", step=500, value=current_price)
            current_capacity = rooms_info.get(room_type, {}).get("capacity", 0)
            new_capacity = st.number_input("Edit vaccant slot:", value=current_capacity)
            current_availability = rooms_info.get(room_type, {}).get("availability", 0)
            available = st.checkbox("Booking Availability", value=current_availability)
            
            
            if st.button("Update Price, Capacity and Availbilty", disabled=block_access):
                update_price_capacity_avialability(selected_hostel, room_type, new_price, new_capacity,available, college)
                st.success(f"Price, capacity and availability of {room_type} room updated successfully!")


        



    else:
        if selected_hostel is not "":
            st.warning("No hostel found with the selected name.")
        else:
            st.info("Please enter the available Hostel")


if __name__ == "__main__":
    main()







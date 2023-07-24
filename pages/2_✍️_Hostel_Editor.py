import streamlit as st
import pyrebase
import time
from firebase_handler.database_handler import (
    db,
    get_hostel_names,
    get_college_name,
    update_email,
    delete_hostel_info,
    get_hostel_info,
    update_price,
    update_price_capacity_avialability,
)



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
        st.markdown("<h3 style='text-align: center; color: aquamarine;'>Hostel Information:</h3>", unsafe_allow_html=True)
        location = hostel_info.get("location", "")
        st.info(f"Nearest College: {college}")
        st.info(f"Location: {location}")

        # Get rooms info
        rooms_info = hostel_info.get("rooms info", {})

        col1, col2 = st.columns([1, 1])

        with col2:
            # Update email
            st.markdown("<h3 style='text-align: center; color: aquamarine;'>Update Email</h3>", unsafe_allow_html=True)
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
            st.markdown("<h3 style='text-align: center; color: aquamarine;'>Update Room Details</h3>", unsafe_allow_html=True)
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






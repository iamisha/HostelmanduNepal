import streamlit as st
import pyrebase
import email, smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

# Firebase configuration
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

def send_email(room_type,hostel_name):
    subject = "HostelMandu: Room Booked"
    body = f"Hi,{st.session_state.username} this is to inform you that your room is booked at {hostel_name}, type: {room_type} "
    sender_email = "hoselmandu.com.np@gmail.com"
    password = 'mlvdyfofawxqbqrp'
    receiver_email = db.child("username").child(st.session_state.username).child("emails").shallow().get().val()
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    html = """\
        <html>
        <body>
            <h1 style="color: #2e6c80; text-align: center;">HostelMandu</h1>
            <h3 style="color: #5e9ca0;">Hello!</h3>
            <p>This is to confirm your booking</p> 
            <p>If you have any questions, please do not hesitate to contact us. phone no: +977 9807881556</p>
            <p>Best regards,</p>
            <p>HostelMandu</p>
            <p><a href="https://ibb.co/987qrWx"><img src="https://i.ibb.co/dWRQ5DN/Brown-Modern-Open-House-Flyer.jpg" alt="Brown-Modern-Open-House-Flyer" width="430" height="608" border="0" /></a></p>     
        </body>
        </html>
        """

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html, "html"))

    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email,text)


# Function to fetch unique college names from the database
def get_college_names():
    college_names = db.child("colleges").shallow().get().val()
    if college_names is not None:
        return list(college_names)
    else:
        return []
    
# Function to filter hostels based on user input and gender
def filter_hostels(college, room_type, min_price, max_price, gender):
    hostels = db.child("colleges").child(college).child("hostels").get().val()
    filtered_data = []

    if hostels is not None:
        for hostel_key, hostel in hostels.items():
            # Check if gender matches (or 'Any' gender is selected)
            hostel_gender = str(hostel.get('gender', '')).lower()
            if gender.lower() == 'any' or gender.lower() == hostel_gender:
                if room_type == '1_person' and '1_person' in hostel['rooms info']:
                    price = hostel['rooms info']['1_person']['price']
                    if min_price <= price <= max_price:
                        hostel_name = hostel.get('hostel_name', '')
                        hostel_location = hostel.get('location', '')
                        filtered_data.append((hostel_key, hostel_name, hostel_location, price, hostel_gender))

                elif room_type == '2_sharing' and '2_sharing' in hostel['rooms info']:
                    price = hostel['rooms info']['2_sharing']['price']
                    if min_price <= price <= max_price:
                        hostel_name = hostel.get('hostel_name', '')
                        hostel_location = hostel.get('location', '')
                        filtered_data.append((hostel_key, hostel_name, hostel_location, price, hostel_gender))

                elif room_type == '3_sharing' and '3_sharing' in hostel['rooms info']:
                    price = hostel['rooms info']['3_sharing']['price']
                    if min_price <= price <= max_price:
                        hostel_name = hostel.get('hostel_name', '')
                        hostel_location = hostel.get('location', '')
                        filtered_data.append((hostel_key, hostel_name, hostel_location, price, hostel_gender))

    return filtered_data

def book_room(hostel_name, college, room_type):
    # Get the current capacity and availability of the selected room type
    room_info = db.child("colleges").child(college).child("hostels").child(hostel_name).child("rooms info").child(room_type).get().val()
    current_capacity = room_info.get("capacity", 0)
    available = room_info.get("availability", 0)

    # Check if the room is available for booking
    if available and current_capacity > 0:
        # Update the availability and capacity after booking
        db.child("colleges").child(college).child("hostels").child(hostel_name).child("rooms info").child(room_type).update({
            "availability": current_capacity - 1 > 0,
            "capacity": current_capacity - 1
        })

        # Add booking information to the database
        booking_info = {
            "hostel_name": hostel_name,
            "room_type": room_type,
            "booked_by": st.session_state.username
        }
        db.child("bookings").push(booking_info)
        send_email(room_type,hostel_name)
        st.balloons()
        st.info(f"Room booked successfully! You have booked a {room_type} room in {hostel_name}.")
                    
    else:
        if not available:
            st.error("The selected room type is not available for booking. Please choose another room type.")
        else:
            st.error("No capacity left for the selected room type. Please choose another room type.")

# Streamlit app
def main():
    
    st.markdown("<h1 style='text-align: center; color: teal;'>Hostel Finder</h1>", unsafe_allow_html=True)
    
    # Get unique college names
    college_names = get_college_names()

    # Input fields
    college_name = st.selectbox("Select your college:", [""]+college_names)
    room_type = st.selectbox("Select room type:", ['1_person', '2_sharing', '3_sharing'])
    gender = st.selectbox("Select gender:", ['Any', 'Male', 'Female'])
    min_price, max_price = st.slider("Price range:", 5000, 25000, (5000, 25000), step=1000)
    

    # Filter hostels based on user input and gender
    if st.button("Find Hostels",disabled= not st.session_state.signout):
        filtered_hostels = filter_hostels(college_name, room_type, min_price, max_price, gender)

        # Sort the filtered hostels based on gender
        filtered_hostels = sorted(filtered_hostels, key=lambda x: x[1] if x[1] else "")

        # Display filtered hostels in a table
        if not filtered_hostels:
            st.warning("No hostels found matching your criteria.")
        else:
            st.success("Here are the matching hostels:")
            for _, hostel_name, hostel_location, price, hostel_gender in filtered_hostels:
                hostel_data = [{"Hostel Name": hostel_name, "Location": hostel_location, room_type +" Room Price": price, "Gender": hostel_gender} ]
                st.table(hostel_data)
                st.button("Book Hostel", key=f"{hostel_name}-{room_type}", on_click=book_room, args=(hostel_name, college_name, room_type))
                
if __name__ == "__main__":
    main()

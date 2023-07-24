import pyrebase

# Firebase configuration
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
# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Database handling code for the Hostel Registeration
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


# Database handling code for the Hostel Editor

    # Get unique hostel names
    hostel_names = get_hostel_names()

    # Select a hostel
    selected_hostel = st.selectbox("Select a hostel:", [""] +hostel_names)
    hostel_info = get_hostel_info(selected_hostel)
    college = get_college_name(selected_hostel)
    if db.child("colleges").child(college).child("hostels").child(selected_hostel).child("registered_by").shallow().get().val() == st.session_state.username:
        block_access = False


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




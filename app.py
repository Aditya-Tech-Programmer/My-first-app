
import streamlit as st
import csv
import os
import random
import re
from datetime import datetime, date
import pandas as pd


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="RailBook",
    page_icon="🚆",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background: white;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA LOCATION
# =========================================================

if os.path.exists("/content/drive/MyDrive"):
    DATA_DIR = "/content/drive/MyDrive/RailBookData"
else:
    DATA_DIR = "/content/railbook_data"

os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.csv")
TRAINS_FILE = os.path.join(DATA_DIR, "trains.csv")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.csv")
PASSENGERS_FILE = os.path.join(DATA_DIR, "passengers.csv")
TICKET_FOLDER = os.path.join(DATA_DIR, "tickets")

os.makedirs(TICKET_FOLDER, exist_ok=True)


# =========================================================
# CSV FIELDS
# =========================================================

USER_FIELDS = [
    "username",
    "password",
    "name",
    "mobile",
    "email"
]

TRAIN_FIELDS = [
    "train_no",
    "train_name",
    "source",
    "destination",
    "departure",
    "arrival",
    "duration",
    "classes",
    "sl_seats",
    "3a_seats",
    "2a_seats",
    "1a_seats",
    "sl_fare",
    "3a_fare",
    "2a_fare",
    "1a_fare"
]

BOOKING_FIELDS = [
    "pnr",
    "username",
    "train_no",
    "journey_date",
    "class_name",
    "passenger_count",
    "total_fare",
    "status",
    "booking_time"
]

PASSENGER_FIELDS = [
    "pnr",
    "passenger_no",
    "name",
    "age",
    "gender",
    "berth",
    "coach",
    "seat"
]


# =========================================================
# CSV FUNCTIONS
# =========================================================

def create_file(filename, fields):

    if not os.path.exists(filename):

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()


def initialize_files():

    create_file(USERS_FILE, USER_FIELDS)
    create_file(TRAINS_FILE, TRAIN_FIELDS)
    create_file(BOOKINGS_FILE, BOOKING_FIELDS)
    create_file(PASSENGERS_FILE, PASSENGER_FIELDS)


def read_csv(filename):

    if not os.path.exists(filename):
        return []

    with open(
        filename,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))


def write_csv(filename, fields, rows):

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()

        for row in rows:

            writer.writerow({
                field: row.get(field, "")
                for field in fields
            })


initialize_files()


# =========================================================
# SAMPLE TRAINS
# =========================================================

def add_sample_trains():

    trains = read_csv(TRAINS_FILE)

    if len(trains) > 0:
        return

    trains = [

        {
            "train_no": "12101",
            "train_name": "Deccan Express",
            "source": "Mumbai",
            "destination": "Pune",
            "departure": "07:10",
            "arrival": "10:25",
            "duration": "3h 15m",
            "classes": "SL,3A,2A",
            "sl_seats": "80",
            "3a_seats": "50",
            "2a_seats": "30",
            "1a_seats": "0",
            "sl_fare": "180",
            "3a_fare": "550",
            "2a_fare": "750",
            "1a_fare": "0"
        },

        {
            "train_no": "11010",
            "train_name": "Sinhagad Express",
            "source": "Mumbai",
            "destination": "Pune",
            "departure": "09:10",
            "arrival": "12:45",
            "duration": "3h 35m",
            "classes": "SL,3A,2A",
            "sl_seats": "100",
            "3a_seats": "60",
            "2a_seats": "30",
            "1a_seats": "0",
            "sl_fare": "200",
            "3a_fare": "600",
            "2a_fare": "800",
            "1a_fare": "0"
        },

        {
            "train_no": "12123",
            "train_name": "Deccan Queen",
            "source": "Mumbai",
            "destination": "Pune",
            "departure": "17:10",
            "arrival": "20:25",
            "duration": "3h 15m",
            "classes": "SL,3A,2A,1A",
            "sl_seats": "70",
            "3a_seats": "50",
            "2a_seats": "25",
            "1a_seats": "10",
            "sl_fare": "220",
            "3a_fare": "650",
            "2a_fare": "850",
            "1a_fare": "1200"
        }
    ]

    write_csv(
        TRAINS_FILE,
        TRAIN_FIELDS,
        trains
    )


add_sample_trains()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# =========================================================
# VALIDATION
# =========================================================

def valid_mobile(mobile):

    return bool(
        re.fullmatch(
            r"[6-9][0-9]{9}",
            mobile
        )
    )


def valid_email(email):

    return bool(
        re.fullmatch(
            r"[^@]+@[^@]+\.[^@]+",
            email
        )
    )


# =========================================================
# PNR
# =========================================================

def generate_pnr():

    existing = {
        row["pnr"]
        for row in read_csv(BOOKINGS_FILE)
    }

    while True:

        pnr = str(
            random.randint(
                1000000000,
                9999999999
            )
        )

        if pnr not in existing:
            return pnr


# =========================================================
# TRAIN FUNCTIONS
# =========================================================

def get_train(train_no):

    trains = read_csv(TRAINS_FILE)

    for train in trains:

        if train["train_no"] == train_no:
            return train

    return None


def search_trains(source, destination):

    source = source.strip().lower()
    destination = destination.strip().lower()

    results = []

    for train in read_csv(TRAINS_FILE):

        if (
            train["source"].lower() == source
            and
            train["destination"].lower() == destination
        ):

            results.append(train)

    return results


def seat_field(class_name):

    return {
        "SL": "sl_seats",
        "3A": "3a_seats",
        "2A": "2a_seats",
        "1A": "1a_seats"
    }[class_name]


def fare_field(class_name):

    return {
        "SL": "sl_fare",
        "3A": "3a_fare",
        "2A": "2a_fare",
        "1A": "1a_fare"
    }[class_name]


def available_classes(train):

    result = []

    mapping = {
        "SL": "sl_seats",
        "3A": "3a_seats",
        "2A": "2a_seats",
        "1A": "1a_seats"
    }

    for class_name, field in mapping.items():

        if int(train.get(field, 0)) > 0:
            result.append(class_name)

    return result


# =========================================================
# SEAT ALLOCATION
# =========================================================

def coach_list(class_name):

    if class_name == "SL":
        return [f"S{i}" for i in range(1, 11)]

    if class_name == "3A":
        return [f"B{i}" for i in range(1, 6)]

    if class_name == "2A":
        return [f"A{i}" for i in range(1, 4)]

    return ["H1"]


def used_seats(train_no, class_name, coach):

    bookings = read_csv(BOOKINGS_FILE)
    passengers = read_csv(PASSENGERS_FILE)

    valid_pnrs = {
        b["pnr"]
        for b in bookings
        if (
            b["status"] == "CONFIRMED"
            and
            b["train_no"] == train_no
            and
            b["class_name"] == class_name
        )
    }

    used = set()

    for passenger in passengers:

        if (
            passenger["pnr"] in valid_pnrs
            and
            passenger["coach"] == coach
        ):

            try:
                used.add(
                    int(passenger["seat"])
                )
            except:
                pass

    return used


def allocate_seat(train_no, class_name):

    for coach in coach_list(class_name):

        used = used_seats(
            train_no,
            class_name,
            coach
        )

        for seat in range(1, 73):

            if seat not in used:

                return coach, seat

    return None, None


# =========================================================
# TICKET
# =========================================================

def ticket_text(pnr):

    bookings = read_csv(BOOKINGS_FILE)
    passengers = read_csv(PASSENGERS_FILE)

    booking = None

    for b in bookings:

        if b["pnr"] == pnr:
            booking = b
            break

    if booking is None:
        return "Ticket not found."

    train = get_train(
        booking["train_no"]
    )

    text = []

    text.append("=" * 55)
    text.append("                 🚆 RAILBOOK")
    text.append("               RAILWAY TICKET")
    text.append("=" * 55)

    text.append(
        f"PNR          : {booking['pnr']}"
    )

    text.append(
        f"Train        : {train['train_no']} - {train['train_name']}"
    )

    text.append(
        f"Route        : {train['source']} → {train['destination']}"
    )

    text.append(
        f"Journey Date : {booking['journey_date']}"
    )

    text.append(
        f"Class        : {booking['class_name']}"
    )

    text.append(
        f"Fare         : ₹{booking['total_fare']}"
    )

    text.append(
        f"Status       : {booking['status']}"
    )

    text.append("-" * 55)
    text.append("PASSENGERS")
    text.append("-" * 55)

    for p in passengers:

        if p["pnr"] == pnr:

            text.append(
                f"{p['passenger_no']}. "
                f"{p['name']} | "
                f"Age: {p['age']} | "
                f"{p['gender']} | "
                f"{p['coach']}-{p['seat']} | "
                f"{p['berth']}"
            )

    text.append("-" * 55)

    text.append(
        f"Booking Time : {booking['booking_time']}"
    )

    text.append("=" * 55)
    text.append("Thank you for using RailBook! 🚆")
    text.append("=" * 55)

    return "\n".join(text)


# =========================================================
# HOME
# =========================================================

def home_page():

    st.markdown("""
    <div class="hero">

    <h1>🚆 RailBook</h1>

    <p>
    Smart Railway Reservation System
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="card">
        <h2>🔎 Search</h2>
        <p>Find trains between stations.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">
        <h2>🎫 Book</h2>
        <p>Book tickets with passenger details.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="card">
        <h2>📋 Manage</h2>
        <p>Check PNR and manage bookings.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("✨ Features")

    features = [
        "🔐 Registration & Login",
        "🚆 Train Search",
        "🎫 Ticket Booking",
        "💺 Seat Allocation",
        "🔍 PNR Status",
        "❌ Cancellation",
        "👤 Profile",
        "🛠️ Admin Panel",
        "💰 Revenue",
        "📥 Ticket Download"
    ]

    cols = st.columns(2)

    for i, feature in enumerate(features):

        with cols[i % 2]:
            st.info(feature)


# =========================================================
# LOGIN / REGISTER
# =========================================================

def authentication():

    st.header("🔐 Account")

    login_tab, register_tab, admin_tab = st.tabs(
        [
            "🔑 Login",
            "📝 Register",
            "🛠️ Admin Login"
        ]
    )

    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        with st.form("login_form"):

            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            submit_login = st.form_submit_button(
                "🔐 Login",
                use_container_width=True
            )

        if submit_login:

            username = username.strip()

            users = read_csv(
                USERS_FILE
            )

            found = None

            for user in users:

                if (
                    user.get("username", "") == username
                    and
                    user.get("password", "") == password
                ):

                    found = user
                    break

            if found:

                # IMPORTANT:
                # Save username in session.

                st.session_state.logged_in = True
                st.session_state.username = found["username"]
                st.session_state.user_name = found["name"]
                st.session_state.role = "user"

                st.success(
                    f"Welcome, {found['name']}! 👋"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        with st.form("register_form"):

            new_username = st.text_input(
                "Choose Username"
            )

            new_password = st.text_input(
                "Password",
                type="password"
            )

            new_name = st.text_input(
                "Full Name"
            )

            new_mobile = st.text_input(
                "Mobile Number"
            )

            new_email = st.text_input(
                "Email"
            )

            submit_register = st.form_submit_button(
                "📝 Create Account",
                use_container_width=True
            )

        if submit_register:

            new_username = new_username.strip()
            new_name = new_name.strip()
            new_mobile = new_mobile.strip()
            new_email = new_email.strip()

            if new_username == "":

                st.error(
                    "Username cannot be empty."
                )

            elif new_password == "":

                st.error(
                    "Password cannot be empty."
                )

            elif new_name == "":

                st.error(
                    "Name cannot be empty."
                )

            elif not valid_mobile(new_mobile):

                st.error(
                    "Enter a valid 10-digit mobile number."
                )

            elif not valid_email(new_email):

                st.error(
                    "Enter a valid email address."
                )

            else:

                users = read_csv(
                    USERS_FILE
                )

                exists = False

                for user in users:

                    if (
                        user.get("username", "").lower()
                        ==
                        new_username.lower()
                    ):

                        exists = True
                        break

                if exists:

                    st.error(
                        "❌ Username already exists."
                    )

                else:

                    new_user = {
                        "username": new_username,
                        "password": new_password,
                        "name": new_name,
                        "mobile": new_mobile,
                        "email": new_email
                    }

                    users.append(new_user)

                    write_csv(
                        USERS_FILE,
                        USER_FIELDS,
                        users
                    )

                    st.success(
                        "🎉 Account created successfully!"
                    )

                    st.info(
                        f"Your username is: {new_username}"
                    )

                    st.write(
                        "Now open the Login tab and login."
                    )

    # =====================================================
    # ADMIN
    # =====================================================

    with admin_tab:

        st.info(
            "Demo Admin: admin / admin123"
        )

        with st.form("admin_form"):

            admin_username = st.text_input(
                "Admin Username"
            )

            admin_password = st.text_input(
                "Admin Password",
                type="password"
            )

            submit_admin = st.form_submit_button(
                "🛠️ Login as Admin",
                use_container_width=True
            )

        if submit_admin:

            if (
                admin_username == "admin"
                and
                admin_password == "admin123"
            ):

                st.session_state.logged_in = True
                st.session_state.username = "admin"
                st.session_state.user_name = "Administrator"
                st.session_state.role = "admin"

                st.success(
                    "Admin login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid admin credentials."
                )


# =========================================================
# USER DASHBOARD
# =========================================================

def user_dashboard():

    username = st.session_state.username

    bookings = read_csv(
        BOOKINGS_FILE
    )

    my_bookings = [
        b for b in bookings
        if b["username"] == username
    ]

    confirmed = [
        b for b in my_bookings
        if b["status"] == "CONFIRMED"
    ]

    cancelled = [
        b for b in my_bookings
        if b["status"] == "CANCELLED"
    ]

    total = sum(
        float(b["total_fare"])
        for b in confirmed
    )

    st.markdown(
        f"""
        <div class="hero">

        <h1>🏠 Welcome, {st.session_state.user_name}!</h1>

        <p>
        Manage your railway bookings from here.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🎫 Bookings",
        len(my_bookings)
    )

    c2.metric(
        "✅ Confirmed",
        len(confirmed)
    )

    c3.metric(
        "❌ Cancelled",
        len(cancelled)
    )

    c4.metric(
        "💰 Spent",
        f"₹{total:.0f}"
    )

    st.subheader("📋 Recent Bookings")

    if my_bookings:

        df = pd.DataFrame(
            my_bookings
        )

        st.dataframe(
            df[
                [
                    "pnr",
                    "train_no",
                    "journey_date",
                    "class_name",
                    "total_fare",
                    "status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No bookings yet."
        )


# =========================================================
# SEARCH
# =========================================================

def search_page():

    st.header("🔎 Search Trains")

    c1, c2 = st.columns(2)

    with c1:

        source = st.text_input(
            "From",
            placeholder="Mumbai"
        )

    with c2:

        destination = st.text_input(
            "To",
            placeholder="Pune"
        )

    journey_date = st.date_input(
        "Journey Date",
        min_value=date.today()
    )

    if st.button(
        "🔎 Search",
        use_container_width=True
    ):

        if not source or not destination:

            st.error(
                "Enter source and destination."
            )

            return

        results = search_trains(
            source,
            destination
        )

        if not results:

            st.warning(
                "No trains found."
            )

            return

        st.success(
            f"{len(results)} train(s) found."
        )

        for train in results:

            with st.container(border=True):

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.subheader(
                        f"🚆 {train['train_name']}"
                    )

                    st.write(
                        f"Train No: {train['train_no']}"
                    )

                with c2:

                    st.write(
                        f"🕐 {train['departure']} → "
                        f"{train['arrival']}"
                    )

                    st.write(
                        f"⏱️ {train['duration']}"
                    )

                with c3:

                    st.metric(
                        "SL Seats",
                        train["sl_seats"]
                    )


# =========================================================
# BOOKING
# =========================================================

def booking_page():

    st.header("🎫 Book Ticket")

    c1, c2 = st.columns(2)

    with c1:

        source = st.text_input(
            "From",
            key="booking_source"
        )

    with c2:

        destination = st.text_input(
            "To",
            key="booking_destination"
        )

    journey_date = st.date_input(
        "Journey Date",
        min_value=date.today(),
        key="booking_date"
    )

    if not source or not destination:

        st.info(
            "Enter source and destination first."
        )

        return

    trains = search_trains(
        source,
        destination
    )

    if not trains:

        st.warning(
            "No trains found."
        )

        return

    train_options = {}

    for train in trains:

        label = (
            f"{train['train_no']} - "
            f"{train['train_name']} | "
            f"{train['departure']} → "
            f"{train['arrival']}"
        )

        train_options[label] = train["train_no"]

    selected_label = st.selectbox(
        "🚆 Select Train",
        list(train_options.keys())
    )

    train_no = train_options[
        selected_label
    ]

    train = get_train(train_no)

    classes = available_classes(train)

    if not classes:

        st.error(
            "No seats available."
        )

        return

    class_name = st.selectbox(
        "💺 Select Class",
        classes
    )

    sf = seat_field(class_name)
    ff = fare_field(class_name)

    seats = int(train[sf])
    fare = int(train[ff])

    st.info(
        f"Available seats: {seats} | "
        f"Fare per passenger: ₹{fare}"
    )

    count = st.number_input(
        "Number of Passengers",
        min_value=1,
        max_value=min(6, seats),
        value=1,
        step=1
    )

    st.divider()

    st.subheader("👥 Passenger Details")

    passengers = []

    with st.form("booking_form"):

        for i in range(int(count)):

            st.markdown(
                f"### Passenger {i + 1}"
            )

            c1, c2 = st.columns(2)

            with c1:

                name = st.text_input(
                    "Name",
                    key=f"pname_{i}"
                )

                age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=120,
                    value=18,
                    key=f"page_{i}"
                )

            with c2:

                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"],
                    key=f"pgender_{i}"
                )

                berth = st.selectbox(
                    "Berth",
                    [
                        "No Preference",
                        "Lower",
                        "Middle",
                        "Upper",
                        "Side Lower",
                        "Side Upper"
                    ],
                    key=f"pberth_{i}"
                )

            passengers.append({
                "name": name.strip(),
                "age": age,
                "gender": gender,
                "berth": berth
            })

        total_fare = fare * int(count)

        st.markdown(
            f"## 💰 Total: ₹{total_fare}"
        )

        submit = st.form_submit_button(
            "🎫 Confirm Booking",
            use_container_width=True
        )

    if submit:

        for p in passengers:

            if p["name"] == "":

                st.error(
                    "Passenger name cannot be empty."
                )

                return

        pnr = generate_pnr()

        booking = {
            "pnr": pnr,
            "username": st.session_state.username,
            "train_no": train_no,
            "journey_date": journey_date.strftime("%d-%m-%Y"),
            "class_name": class_name,
            "passenger_count": str(count),
            "total_fare": str(total_fare),
            "status": "CONFIRMED",
            "booking_time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }

        bookings = read_csv(
            BOOKINGS_FILE
        )

        bookings.append(
            booking
        )

        write_csv(
            BOOKINGS_FILE,
            BOOKING_FIELDS,
            bookings
        )

        passenger_rows = read_csv(
            PASSENGERS_FILE
        )

        for i, p in enumerate(
            passengers,
            start=1
        ):

            coach, seat = allocate_seat(
                train_no,
                class_name
            )

            if coach is None:

                st.error(
                    "Seat allocation failed."
                )

                return

            passenger_rows.append({
                "pnr": pnr,
                "passenger_no": str(i),
                "name": p["name"],
                "age": str(p["age"]),
                "gender": p["gender"],
                "berth": p["berth"],
                "coach": coach,
                "seat": str(seat)
            })

        write_csv(
            PASSENGERS_FILE,
            PASSENGER_FIELDS,
            passenger_rows
        )

        # Reduce available seats

        trains_data = read_csv(
            TRAINS_FILE
        )

        for t in trains_data:

            if t["train_no"] == train_no:

                t[sf] = str(
                    int(t[sf]) - int(count)
                )

                break

        write_csv(
            TRAINS_FILE,
            TRAIN_FIELDS,
            trains_data
        )

        ticket = ticket_text(
            pnr
        )

        ticket_file = os.path.join(
            TICKET_FOLDER,
            f"{pnr}.txt"
        )

        with open(
            ticket_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(ticket)

        st.success(
            "🎉 Ticket booked successfully!"
        )

        st.balloons()

        st.metric(
            "Your PNR",
            pnr
        )

        with st.expander(
            "🎫 View Ticket"
        ):

            st.code(ticket)

        st.download_button(
            "📥 Download Ticket",
            ticket,
            file_name=f"{pnr}.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# PNR STATUS
# =========================================================

def pnr_page():

    st.header("🔍 PNR Status")

    pnr = st.text_input(
        "Enter PNR"
    )

    if st.button(
        "🔎 Check PNR",
        use_container_width=True
    ):

        bookings = read_csv(
            BOOKINGS_FILE
        )

        booking = None

        for b in bookings:

            if b["pnr"] == pnr:

                booking = b
                break

        if booking is None:

            st.error(
                "PNR not found."
            )

            return

        if (
            st.session_state.role != "admin"
            and
            booking["username"]
            !=
            st.session_state.username
        ):

            st.error(
                "You can only view your own PNR."
            )

            return

        train = get_train(
            booking["train_no"]
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "PNR",
            booking["pnr"]
        )

        c2.metric(
            "Train",
            booking["train_no"]
        )

        c3.metric(
            "Status",
            booking["status"]
        )

        st.write(
            f"**Train:** {train['train_name']}"
        )

        st.write(
            f"**Route:** {train['source']} → "
            f"{train['destination']}"
        )

        st.write(
            f"**Date:** {booking['journey_date']}"
        )

        st.write(
            f"**Class:** {booking['class_name']}"
        )

        st.write(
            f"**Fare:** ₹{booking['total_fare']}"
        )

        passengers = [
            p for p in read_csv(PASSENGERS_FILE)
            if p["pnr"] == pnr
        ]

        if passengers:

            df = pd.DataFrame(
                passengers
            )

            st.subheader(
                "👥 Passengers"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        ticket = ticket_text(
            pnr
        )

        st.download_button(
            "📥 Download Ticket",
            ticket,
            file_name=f"{pnr}.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# MY BOOKINGS
# =========================================================

def bookings_page():

    st.header("📋 My Bookings")

    bookings = read_csv(
        BOOKINGS_FILE
    )

    mine = [
        b for b in bookings
        if b["username"]
        ==
        st.session_state.username
    ]

    if not mine:

        st.info(
            "No bookings found."
        )

        return

    df = pd.DataFrame(
        mine
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CANCEL
# =========================================================

def cancel_page():

    st.header("❌ Cancel Ticket")

    pnr = st.text_input(
        "Enter PNR"
    )

    if st.button(
        "❌ Cancel Ticket",
        use_container_width=True
    ):

        bookings = read_csv(
            BOOKINGS_FILE
        )

        found = None

        for b in bookings:

            if (
                b["pnr"] == pnr
                and
                b["username"]
                ==
                st.session_state.username
            ):

                found = b
                break

        if found is None:

            st.error(
                "Booking not found."
            )

            return

        if found["status"] == "CANCELLED":

            st.warning(
                "Ticket already cancelled."
            )

            return

        found["status"] = "CANCELLED"

        write_csv(
            BOOKINGS_FILE,
            BOOKING_FIELDS,
            bookings
        )

        # Restore seats

        trains = read_csv(
            TRAINS_FILE
        )

        sf = seat_field(
            found["class_name"]
        )

        for train in trains:

            if train["train_no"] == found["train_no"]:

                train[sf] = str(
                    int(train[sf])
                    +
                    int(found["passenger_count"])
                )

                break

        write_csv(
            TRAINS_FILE,
            TRAIN_FIELDS,
            trains
        )

        st.success(
            "🎉 Ticket cancelled successfully."
        )


# =========================================================
# PROFILE
# =========================================================

def profile_page():

    st.header("👤 My Profile")

    users = read_csv(
        USERS_FILE
    )

    user = None

    for u in users:

        if (
            u["username"]
            ==
            st.session_state.username
        ):

            user = u
            break

    if user is None:

        st.error(
            "Profile not found."
        )

        return

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            f"**Username:** {user['username']}"
        )

        st.info(
            f"**Name:** {user['name']}"
        )

    with c2:

        st.info(
            f"**Mobile:** {user['mobile']}"
        )

        st.info(
            f"**Email:** {user['email']}"
        )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard():

    st.header("🛠️ Admin Dashboard")

    users = read_csv(
        USERS_FILE
    )

    trains = read_csv(
        TRAINS_FILE
    )

    bookings = read_csv(
        BOOKINGS_FILE
    )

    confirmed = [
        b for b in bookings
        if b["status"] == "CONFIRMED"
    ]

    revenue = sum(
        float(b["total_fare"])
        for b in confirmed
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Users",
        len(users)
    )

    c2.metric(
        "🚆 Trains",
        len(trains)
    )

    c3.metric(
        "🎫 Bookings",
        len(bookings)
    )

    c4.metric(
        "💰 Revenue",
        f"₹{revenue:.0f}"
    )

    st.subheader(
        "📋 Recent Bookings"
    )

    if bookings:

        df = pd.DataFrame(
            bookings
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# ADMIN TRAINS
# =========================================================

def admin_trains():

    st.header("🚆 Manage Trains")

    trains = read_csv(
        TRAINS_FILE
    )

    st.subheader(
        "Existing Trains"
    )

    if trains:

        st.dataframe(
            pd.DataFrame(trains),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader(
        "➕ Add Train"
    )

    with st.form("add_train"):

        c1, c2 = st.columns(2)

        with c1:

            train_no = st.text_input(
                "Train Number"
            )

            train_name = st.text_input(
                "Train Name"
            )

            source = st.text_input(
                "Source"
            )

            destination = st.text_input(
                "Destination"
            )

        with c2:

            departure = st.text_input(
                "Departure"
            )

            arrival = st.text_input(
                "Arrival"
            )

            duration = st.text_input(
                "Duration"
            )

        st.subheader(
            "Seats & Fares"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            sl_seats = st.number_input(
                "SL Seats",
                min_value=0,
                value=50
            )

            sl_fare = st.number_input(
                "SL Fare",
                min_value=0,
                value=200
            )

        with c2:

            a3_seats = st.number_input(
                "3A Seats",
                min_value=0,
                value=30
            )

            a3_fare = st.number_input(
                "3A Fare",
                min_value=0,
                value=500
            )

        with c3:

            a2_seats = st.number_input(
                "2A Seats",
                min_value=0,
                value=20
            )

            a2_fare = st.number_input(
                "2A Fare",
                min_value=0,
                value=700
            )

        with c4:

            a1_seats = st.number_input(
                "1A Seats",
                min_value=0,
                value=0
            )

            a1_fare = st.number_input(
                "1A Fare",
                min_value=0,
                value=0
            )

        add = st.form_submit_button(
            "➕ Add Train",
            use_container_width=True
        )

    if add:

        if not train_no or not train_name:

            st.error(
                "Train number and name are required."
            )

        else:

            duplicate = any(
                t["train_no"] == train_no
                for t in trains
            )

            if duplicate:

                st.error(
                    "Train number already exists."
                )

            else:

                classes = []

                if sl_seats > 0:
                    classes.append("SL")

                if a3_seats > 0:
                    classes.append("3A")

                if a2_seats > 0:
                    classes.append("2A")

                if a1_seats > 0:
                    classes.append("1A")

                new_train = {

                    "train_no": train_no,
                    "train_name": train_name,
                    "source": source,
                    "destination": destination,
                    "departure": departure,
                    "arrival": arrival,
                    "duration": duration,
                    "classes": ",".join(classes),
                    "sl_seats": str(sl_seats),
                    "3a_seats": str(a3_seats),
                    "2a_seats": str(a2_seats),
                    "1a_seats": str(a1_seats),
                    "sl_fare": str(sl_fare),
                    "3a_fare": str(a3_fare),
                    "2a_fare": str(a2_fare),
                    "1a_fare": str(a1_fare)
                }

                trains.append(
                    new_train
                )

                write_csv(
                    TRAINS_FILE,
                    TRAIN_FIELDS,
                    trains
                )

                st.success(
                    "🚆 Train added successfully."
                )

                st.rerun()


# =========================================================
# ADMIN USERS
# =========================================================

def admin_users():

    st.header("👥 Users")

    users = read_csv(
        USERS_FILE
    )

    if users:

        st.dataframe(
            pd.DataFrame(users),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No users registered."
        )


# =========================================================
# ADMIN BOOKINGS
# =========================================================

def admin_bookings():

    st.header("🎫 All Bookings")

    bookings = read_csv(
        BOOKINGS_FILE
    )

    if bookings:

        st.dataframe(
            pd.DataFrame(bookings),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No bookings."
        )


# =========================================================
# ADMIN REVENUE
# =========================================================

def admin_revenue():

    st.header("💰 Revenue")

    bookings = read_csv(
        BOOKINGS_FILE
    )

    confirmed = [
        b for b in bookings
        if b["status"] == "CONFIRMED"
    ]

    total = sum(
        float(b["total_fare"])
        for b in confirmed
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "💰 Total Revenue",
        f"₹{total:.0f}"
    )

    c2.metric(
        "🎫 Confirmed Tickets",
        len(confirmed)
    )

    if confirmed:

        st.dataframe(
            pd.DataFrame(confirmed),
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# SIDEBAR
# =========================================================

if st.session_state.logged_in:

    with st.sidebar:

        st.title("🚆 RailBook")

        st.success(
            f"👤 {st.session_state.username}"
        )

        st.divider()

        if st.session_state.role == "user":

            menu = st.radio(
                "Navigation",
                [
                    "🏠 Dashboard",
                    "🔎 Search Trains",
                    "🎫 Book Ticket",
                    "🔍 PNR Status",
                    "📋 My Bookings",
                    "❌ Cancel Ticket",
                    "👤 Profile"
                ]
            )

        else:

            menu = st.radio(
                "Admin Navigation",
                [
                    "📊 Dashboard",
                    "🚆 Manage Trains",
                    "👥 Users",
                    "🎫 Bookings",
                    "💰 Revenue"
                ]
            )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_name = ""
            st.session_state.role = ""

            st.rerun()


# =========================================================
# MAIN APP
# =========================================================

if not st.session_state.logged_in:

    home_page()

    st.divider()

    authentication()

else:

    if st.session_state.role == "user":

        if menu == "🏠 Dashboard":
            user_dashboard()

        elif menu == "🔎 Search Trains":
            search_page()

        elif menu == "🎫 Book Ticket":
            booking_page()

        elif menu == "🔍 PNR Status":
            pnr_page()

        elif menu == "📋 My Bookings":
            bookings_page()

        elif menu == "❌ Cancel Ticket":
            cancel_page()

        elif menu == "👤 Profile":
            profile_page()

    else:

        if menu == "📊 Dashboard":
            admin_dashboard()

        elif menu == "🚆 Manage Trains":
            admin_trains()

        elif menu == "👥 Users":
            admin_users()

        elif menu == "🎫 Bookings":
            admin_bookings()

        elif menu == "💰 Revenue":
            admin_revenue()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🚆 RailBook | Python + Streamlit + CSV | Educational Project"
)

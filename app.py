import streamlit as st
import pandas as pd
import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pony Pursuits | Book Your Adventure",
    page_icon="🐎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PROMINENT BRANDING & SIDEBAR LOGO SETUP ---
with st.sidebar:
    st.markdown("""
        <div style="background-color: #FFFFFF; padding: 14px; border-radius: 14px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 12px; border: 1px solid #EAEFE5;">
            <p style="font-size: 0.85rem; font-weight: 700; color: #1A252C; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 1.5px;">Pony Pursuits</p>
            <p style="font-size: 0.7rem; color: #555; margin: 0;">5-Star Licensed Equestrian Centre</p>
        </div>
    """, unsafe_allow_html=True)
    try:
        st.image("logo.jpg", use_container_width=True)
    except Exception:
        st.info("🐎 Pony Pursuits Portal")
    st.divider()

# --- CUSTOM CSS FOR HIGH-END BOUTIQUE EQUINE UI ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        /* Global Font & Background Overhaul */
        .stApp { 
            background-color: #F7F8F5; 
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        [data-testid="stSidebar"] { 
            background-color: #FFFFFF; 
            border-right: 1px solid #EBEFE6; 
        }

        /* Editorial Headings */
        h1, h2, h3 { 
            font-family: 'Playfair Display', serif !important;
            color: #1A252C !important;
            letter-spacing: -0.5px;
        }

        /* High-End Metric Cards */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.03);
            border: 1px solid #EAEFE5;
        }
        [data-testid="stMetricValue"] { 
            font-family: 'Playfair Display', serif;
            font-size: 2rem !important; 
            color: #2C4A3E !important; 
        }

        /* Luxurious Activity Cards */
        .activity-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 12px 35px -10px rgba(0,0,0,0.04);
            margin-bottom: 20px;
            border: 1px solid #EAEFE5;
            border-left: 4px solid #2C4A3E;
            transition: transform 0.2s ease;
        }
        .activity-card:hover {
            transform: translateY(-2px);
        }

        /* Polished Buttons */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 500 !important;
            letter-spacing: 0.3px;
            border: 1px solid #D8E2D0 !important;
            transition: all 0.2s ease-in-out;
        }
        
        /* Form container polish */
        [data-testid="stForm"] {
            background-color: #FFFFFF;
            padding: 28px;
            border-radius: 20px;
            box-shadow: 0 15px 40px -10px rgba(0,0,0,0.03);
            border: 1px solid #EAEFE5;
        }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame([
        {"Location": "Huckleberry Farm (Heathfield, OX5)", "Date": "2026-04-02", "Time": "10:00 AM", "Activity": "Adult Private Flatwork", "Details": "Jubilee (Rider: Charlotte V.)", "Status": "Confirmed"},
        {"Location": "Huckleberry Farm (Heathfield, OX5)", "Date": "2026-04-02", "Time": "1:00 PM", "Activity": "Pony Therapy & Groundwork", "Details": "Teddy (Rider: Chloe S.)", "Status": "Confirmed"},
        {"Location": "Sandy Lane (Horspath, OX33)", "Date": "2026-04-03", "Time": "2:30 PM", "Activity": "Shotover Advanced Hack", "Details": "Spice (Rider: The Harrison Family)", "Status": "Confirmed"}
    ])

if "ponies" not in st.session_state:
    st.session_state.ponies = pd.DataFrame([
        {"Pony": "Crackerjack", "Breed": "Welsh Cross", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 60, "Status": "In Memory (🕊️)", "Notes": "Where Pony Pursuits started. A legendary versatile schoolmaster, deeply missed 🌟"},
        {"Pony": "Bo Bo", "Breed": "Miniature Shetland", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 25, "Status": "In Memory (🕊️)", "Notes": "Founding Pony Pursuits pony, grey roan character ❤️"},
        {"Pony": "Jubilee", "Breed": "Gypsy Cob", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 90, "Status": "Active (🟢)", "Notes": "Exceptional weight carrier for adult riders, calm & responsive 🌳"},
        {"Pony": "Teddy", "Breed": "Welsh Cross", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 55, "Status": "Active (🟢)", "Notes": "Cuddly companion pony, wonderful for therapy work 🤗"},
        {"Pony": "Spice", "Breed": "Gypsy Cob", "Current_Yard": "Sandy Lane", "Max_Weight_kg": 80, "Status": "Active (🟢)", "Notes": "Blue roan, ideal for confident woodland hacks 🌲"},
        {"Pony": "Prince", "Breed": "Mini Cob", "Current_Yard": "Sandy Lane", "Max_Weight_kg": 45, "Status": "Active (🟢)", "Notes": "Trained to ride & drive 🐎"},
        {"Pony": "Milkshake", "Breed": "Mini Cob", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 50, "Status": "Active (🟡)", "Notes": "Friendly riding pony (Sunny's brother) 🍦"},
        {"Pony": "Spirit", "Breed": "Mini Cob", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 50, "Status": "Active (🟢)", "Notes": "Blagdon pony, great for younger riders ✨"},
        {"Pony": "Sam", "Breed": "Shetland", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 25, "Status": "Retired (⚪)", "Notes": "Elder statesman in well-earned retirement 🥕"}
    ])

if "clients" not in st.session_state:
    st.session_state.clients = pd.DataFrame([
        {"Client": "The Harrison Family", "Riders": 3, "Credits_Remaining": 4, "Email": "harrison@example.com", "Medical_Notes": "None declared"},
        {"Client": "Charlotte Vance", "Riders": 1, "Credits_Remaining": 6, "Email": "charlotte@example.com", "Medical_Notes": "None declared"}
    ])

if "waitlist" not in st.session_state:
    st.session_state.waitlist = pd.DataFrame(columns=["Client_Name", "Date", "Time", "Activity", "Weight_kg", "Requested_At"])

if "provisions" not in st.session_state:
    st.session_state.provisions = pd.DataFrame([
        {"Student": "Leo M.", "School/Agency": "Oxfordshire Alternative Ed", "Program": "Work-Based Horse Care (Level 1)", "Hours_Logged": 12, "Target_Hours": 30},
        {"Student": "Chloe S.", "School/Agency": "Cherwell SEN Provision", "Program": "Pony Therapy & Groundwork", "Hours_Logged": 8, "Target_Hours": 15}
    ])

if "welfare_schedule" not in st.session_state:
    st.session_state.welfare_schedule = pd.DataFrame([
        {"Pony": "Jubilee", "Event": "Farrier (Full Set)", "Due_Date": "2026-04-10", "Status": "Scheduled"},
        {"Pony": "Teddy", "Event": "Equine Dentist Check", "Due_Date": "2026-04-15", "Status": "Pending"},
        {"Pony": "Spice", "Event": "Vaccination Booster", "Due_Date": "2026-05-01", "Status": "Booked"}
    ])

if "feedback_submissions" not in st.session_state:
    st.session_state.feedback_submissions = pd.DataFrame(columns=["Rider", "Pony", "Rating", "Comments", "Date"])

if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "All Bookings"

# --- HELPER FUNCTIONS ---
def is_pony_booked(pony_name, date_str, time_str):
    for _, row in st.session_state.bookings.iterrows():
        if row['Date'] == date_str and row['Time'] == time_str and row['Status'] == "Confirmed":
            if pony_name.lower() in str(row['Details']).lower():
                return True
    return False

def get_pony_image_path(pony_name):
    clean_name = pony_name.strip()
    for candidate in [f"{clean_name}.jpg", f"{clean_name.lower()}.jpg", f"{clean_name}.png", f"{clean_name.lower()}.png", f"{clean_name}.jpeg"]:
        if os.path.exists(candidate):
            return candidate
    return None

def get_yard_map_link(location_str):
    if "Sandy Lane" in location_str:
        return "https://maps.google.com/?q=Sandy+Lane+Horspath+Oxford+OX33"
    else:
        return "https://maps.google.com/?q=Huckleberry+Farm+Heathfield+Oxford+OX5"

# --- DEFINE ADMIN PAGES ---
def page_dashboard():
    st.title("Welcome back, Charlotte 🌟")
    st.caption("5-Star Licensed Centre Management • Click any metric card below to filter data instantly")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        huck_count = len(st.session_state.bookings[(st.session_state.bookings['Location'].str.contains('Huckleberry')) & (st.session_state.bookings['Status'] == 'Confirmed')])
        st.metric(label="Huckleberry Farm", value=f"{huck_count} Booked", delta="OX5 Yard")
        if st.button("🔍 Filter Huckleberry", use_container_width=True):
            st.session_state.dashboard_view = "Huckleberry"
            st.rerun()

    with col2:
        sandy_count = len(st.session_state.bookings[(st.session_state.bookings['Location'].str.contains('Sandy Lane')) & (st.session_state.bookings['Status'] == 'Confirmed')])
        st.metric(label="Sandy Lane / Shotover", value=f"{sandy_count} Booked", delta="OX33 Yard")
        if st.button("🔍 Filter Sandy Lane", use_container_width=True):
            st.session_state.dashboard_view = "Sandy Lane"
            st.rerun()

    with col3:
        wait_count = len(st.session_state.waitlist)
        st.metric(label="Waiting List", value=f"{wait_count} Riders", delta="Queue Active")
        if st.button("🔍 View Waitlist", use_container_width=True):
            st.session_state.dashboard_view = "Waitlist"
            st.rerun()

    with col4:
        working_ponies = len(st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Retired|Memory')])
        st.metric(label="Happy Herd", value=f"{working_ponies} Ready", delta="100% Fit")
        if st.button("🔍 View Herd Rota", use_container_width=True):
            st.session_state.dashboard_view = "Herd"
            st.rerun()

    st.markdown("---")
    
    if st.session_state.dashboard_view == "Huckleberry":
        col_head, col_btn = st.columns([4, 1])
        with col_head:
            st.subheader("📍 Filtered View: Huckleberry Farm Bookings")
        with col_btn:
            if st.button("🔄 Clear Filter"):
                st.session_state.dashboard_view = "All Bookings"
                st.rerun()
        huck_df = st.session_state.bookings[st.session_state.bookings['Location'].str.contains("Huckleberry")]
        st.dataframe(huck_df, use_container_width=True)

    elif st.session_state.dashboard_view == "Sandy Lane":
        col_head, col_btn = st.columns([4, 1])
        with col_head:
            st.subheader("📍 Filtered View: Sandy Lane / Shotover Bookings")
        with col_btn:
            if st.button("🔄 Clear Filter"):
                st.session_state.dashboard_view = "All Bookings"
                st.rerun()
        sandy_df = st.session_state.bookings[st.session_state.bookings['Location'].str.contains("Sandy Lane")]
        st.dataframe(sandy_df, use_container_width=True)

    elif st.session_state.dashboard_view == "Waitlist":
        col_head, col_btn = st.columns([4, 1])
        with col_head:
            st.subheader("⏳ Active Waiting List Queue")
        with col_btn:
            if st.button("🔄 Clear Filter"):
                st.session_state.dashboard_view = "All Bookings"
                st.rerun()
        if st.session_state.waitlist.empty:
            st.info("The waiting list is currently empty.")
        else:
            st.dataframe(st.session_state.waitlist, use_container_width=True)

    elif st.session_state.dashboard_view == "Herd":
        col_head, col_btn = st.columns([4, 1])
        with col_head:
            st.subheader("🗺️ Active Herd Rota & Status")
        with col_btn:
            if st.button("🔄 Clear Filter"):
                st.session_state.dashboard_view = "All Bookings"
                st.rerun()
        st.dataframe(st.session_state.ponies, use_container_width=True)

    else:
        st.subheader("📅 All Confirmed Bookings Overview")
        st.dataframe(st.session_state.bookings, use_container_width=True)

def page_schedule():
    st.subheader("📅 Master Events & Booking Schedule")
    location_filter = st.radio("Filter Yard Location:", ["All Locations", "Huckleberry Farm (Heathfield, OX5)", "Sandy Lane (Horspath, OX33)"], horizontal=True)
    st.markdown("---")
    df_b = st.session_state.bookings
    if location_filter != "All Locations":
        df_b = df_b[df_b['Location'] == location_filter]
    st.dataframe(df_b, use_container_width=True)

    with st.expander("➕ Create Admin Event / Override Booking"):
        with st.form("admin_event_form"):
            e_loc = st.selectbox("Location", ["Huckleberry Farm (Heathfield, OX5)", "Sandy Lane (Horspath, OX33)"])
            e_date = st.date_input("Event Date")
            e_time = st.selectbox("Time Slot", ["10:00 AM", "11:30 AM", "1:00 PM", "2:30 PM", "4:00 PM"])
            e_act = st.selectbox("Activity", ["Shotover Advanced Hack 🌲", "Adult Private Flatwork ⭐", "Ride & Groom Session 🐴", "Pony Therapy & Play 🐾"])
            
            active_ponies = st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Retired|Memory')]['Pony'].tolist()
            e_pony = st.selectbox("Assign Specific Pony", active_ponies)
            e_rider = st.text_input("Rider / Participant Name")
            
            submitted = st.form_submit_button("Publish Confirmed Booking")
            if submitted:
                date_str = e_date.strftime("%Y-%m-%d")
                if is_pony_booked(e_pony, date_str, e_time):
                    st.error(f"❌ Conflict: **{e_pony}** is already booked for this time slot.")
                else:
                    details_str = f"{e_pony} (Rider: {e_rider if e_rider else 'Admin Booking'})"
                    new_evt = pd.DataFrame([{"Location": e_loc, "Date": date_str, "Time": e_time, "Activity": e_act, "Details": details_str, "Status": "Confirmed"}])
                    st.session_state.bookings = pd.concat([st.session_state.bookings, new_evt], ignore_index=True)
                    st.success(f"✅ Booking added securely for **{e_pony}**.")
                    st.rerun()

    if not st.session_state.waitlist.empty:
        st.markdown("### 🕒 Active Waiting List Queue")
        st.dataframe(st.session_state.waitlist, use_container_width=True)

def page_ponies():
    st.subheader("🗺️ Meet the Herd & Stable Allocations")
    st.dataframe(st.session_state.ponies, use_container_width=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        with st.form("move_pony_form"):
            st.markdown("#### Move Pony Between Yards")
            p_name = st.selectbox("Select Pony", st.session_state.ponies['Pony'].tolist())
            target_yard = st.selectbox("New Yard Location", ["Huckleberry Farm", "Sandy Lane / Shotover"])
            if st.form_submit_button("Update Yard Allocation"):
                st.session_state.ponies.loc[st.session_state.ponies['Pony'] == p_name, 'Current_Yard'] = target_yard
                st.success(f"Moved {p_name} successfully!")
                st.rerun()
    with col_b:
        with st.form("add_pony_form"):
            st.markdown("#### Register New Pony")
            new_p_name = st.text_input("Pony Name")
            new_p_breed = st.text_input("Breed", "Cob Cross")
            new_p_weight = st.number_input("Max Weight Limit (kg)", value=70)
            new_p_yard = st.selectbox("Initial Yard", ["Huckleberry Farm", "Sandy Lane / Shotover"])
            if st.form_submit_button("Save to Herd Register"):
                if new_p_name:
                    new_row = pd.DataFrame([{
                        "Pony": new_p_name, "Breed": new_p_breed, "Current_Yard": new_p_yard, 
                        "Max_Weight_kg": new_p_weight, "Status": "Active (🟢)", "Notes": "Newly added licensed mount ⭐"
                    }])
                    st.session_state.ponies = pd.concat([st.session_state.ponies, new_row], ignore_index=True)
                    st.success(f"Registered {new_p_name}!")
                    st.rerun()

def page_provisions():
    st.subheader("🎒 Alternative Provision & Student Hours Tracker")
    st.dataframe(st.session_state.provisions, use_container_width=True)
    with st.expander("➕ Log Student Hours / Add Placement"):
        with st.form("provision_form"):
            s_name = st.text_input("Student Name")
            s_agency = st.text_input("School / Local Authority Agency")
            s_prog = st.selectbox("Program Type", ["Work-Based Horse Care (Level 1)", "Pony Therapy & Groundwork", "Wellbeing Hack Block"])
            s_hours = st.number_input("Hours to Add", min_value=1, max_value=10, value=2)
            if st.form_submit_button("Save & Update Hours"):
                existing = st.session_state.provisions[st.session_state.provisions['Student'] == s_name]
                if not existing.empty:
                    st.session_state.provisions.loc[st.session_state.provisions['Student'] == s_name, 'Hours_Logged'] += s_hours
                else:
                    new_p = pd.DataFrame([{"Student": s_name, "School/Agency": s_agency, "Program": s_prog, "Hours_Logged": s_hours, "Target_Hours": 20}])
                    st.session_state.provisions = pd.concat([st.session_state.provisions, new_p], ignore_index=True)
                st.success(f"Updated records for {s_name}!")
                st.rerun()

def page_welfare():
    st.subheader("🐎 Equine Welfare & Licensing Constraints")
    st.write("Cherwell District Council 5-star license compliance monitoring (License no: RID0010).")
    st.dataframe(st.session_state.ponies[['Pony', 'Breed', 'Max_Weight_kg', 'Status', 'Notes']], use_container_width=True)

def page_vet():
    st.subheader("🩺 Vet, Farrier & Routine Health Calendar")
    st.dataframe(st.session_state.welfare_schedule, use_container_width=True)
    with st.expander("➕ Schedule New Health Check / Farrier Visit"):
        with st.form("vet_form"):
            v_pony = st.selectbox("Select Pony", st.session_state.ponies['Pony'].tolist())
            v_event = st.selectbox("Care Event Type", ["Farrier (Full Set)", "Farrier (Trimming)", "Equine Dentist Check", "Vaccination Booster", "Vet Health Check"])
            v_date = st.date_input("Due Date")
            v_status = st.selectbox("Status", ["Scheduled", "Pending", "Booked"])
            if st.form_submit_button("Log Care Event"):
                new_v = pd.DataFrame([{"Pony": v_pony, "Event": v_event, "Due_Date": v_date.strftime("%Y-%m-%d"), "Status": v_status}])
                st.session_state.welfare_schedule = pd.concat([st.session_state.welfare_schedule, new_v], ignore_index=True)
                st.success(f"Added {v_event} for {v_pony} successfully!")
                st.rerun()

def page_clients():
    st.subheader("👥 Client & Token Pack Database")
    st.dataframe(st.session_state.clients, use_container_width=True)
    with st.expander("➕ Adjust Client Credit Packs / Tokens"):
        with st.form("token_form"):
            target_client = st.selectbox("Select Client", st.session_state.clients['Client'].tolist())
            token_change = st.number_input("Token Packs to Add (+) / Deduct (-)", min_value=-10, max_value=10, value=1)
            if st.form_submit_button("Update Token Ledger"):
                current_tokens = int(st.session_state.clients.loc[st.session_state.clients['Client'] == target_client, 'Credits_Remaining'].values[0])
                new_total = max(current_tokens + token_change, 0)
                st.session_state.clients.loc[st.session_state.clients['Client'] == target_client, 'Credits_Remaining'] = new_total
                st.success(f"Updated balance for {target_client}. New token pack total: {new_total}")
                st.rerun()

# --- CLIENT PORTAL ---
def page_client_portal():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #2C4A3E, #3D6B56); padding: 35px; border-radius: 18px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
            <h1 style="color: white !important; font-size: 2.4rem; margin-bottom: 8px;">Pony Pursuits</h1>
            <p style="font-size: 1.15rem; opacity: 0.95; max-weight: 400; margin: 0;">Boutique Equestrian Experiences & Woodland Hacks in Oxfordshire</p>
        </div>
    """, unsafe_allow_html=True)
    
    client_tab_book, client_tab_feedback, client_tab_herd, client_tab_waitlist, client_tab_profile = st.tabs([
        "✨ Book an Experience", 
        "🌟 Ride & Feedback",
        "🥕 Meet Our Herd", 
        "⏳ Waiting List", 
        "👤 My Token Balance"
    ])
    
    with client_tab_book:
        st.subheader("Select Your Experience")
        st.write("Tailored sessions for adult riders, families, and enthusiasts across our two distinct Oxfordshire yards.")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("""
                <div class="activity-card">
                    <h4>🌲 Shotover Advanced & Scenic Hacks</h4>
                    <p>Explore the stunning trails around Shotover Country Park from our Sandy Lane yard (OX33). Designed for enjoyable hacks through varied terrain.</p>
                </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
                <div class="activity-card">
                    <h4>⭐ Adult Private Flatwork & Groundwork</h4>
                    <p>Based at Huckleberry Farm (OX5). Refine your riding skills, build partnership, or enjoy restorative time with our seasoned cobs.</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        with st.form("fun_client_booking_form"):
            st.markdown("### 📝 Secure Booking Form")
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                c_name = st.text_input("Rider / Family Name")
                c_email = st.text_input("Account Email Address")
                c_weight = st.number_input("Rider Weight (kg) [For safe equine weight matching]", min_value=30, max_value=110, value=65)
            with f_col2:
                c_location = st.selectbox("Choose Yard Location", ["Huckleberry Farm (Heathfield, OX5)", "Sandy Lane (Horspath, OX33)"])
                c_activity = st.selectbox("Choose Activity", ["Shotover Advanced Hack 🌲", "Adult Private Flatwork ⭐", "Ride & Groom Session 🐴", "Pony Therapy & Play 🐾"])
                c_date = st.date_input("Select Date")
                c_time = st.selectbox("Select Time Slot", ["10:00 AM", "11:30 AM", "1:00 PM", "2:30 PM", "4:00 PM"])
            
            st.markdown("")
            submit_booking = st.form_submit_button("Confirm Booking & Allocate Mount", use_container_width=True)
            
            if submit_booking and c_name:
                date_str = c_date.strftime("%Y-%m-%d")
                
                client_row = st.session_state.clients[st.session_state.clients['Client'].str.contains(c_name, case=False, na=False)]
                if not client_row.empty:
                    tokens_left = int(client_row['Credits_Remaining'].values[0])
                    if tokens_left <= 0:
                        st.error("⚠️ You have 0 token pack credits remaining. Please top up your package to book.")
                        return
                
                active_herd = st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Retired|Memory')]
                weight_matched = active_herd[active_herd['Max_Weight_kg'] >= c_weight]
                
                available_ponies = []
                for _, p_row in weight_matched.iterrows():
                    if not is_pony_booked(p_row['Pony'], date_str, c_time):
                        available_ponies.append(p_row['Pony'])
                
                if weight_matched.empty:
                    st.error("❌ We could not locate an active mount matching this weight requirement safely. Please contact the yard directly.")
                elif not available_ponies:
                    st.warning("⚠️ All suitable weight-matched mounts are currently reserved for this slot. Would you like to join our waiting list?")
                    new_wait = pd.DataFrame([{"Client_Name": c_name, "Date": date_str, "Time": c_time, "Activity": c_activity, "Weight_kg": c_weight, "Requested_At": str(datetime.date.today())}])
                    st.session_state.waitlist = pd.concat([st.session_state.waitlist, new_wait], ignore_index=True)
                    st.info("📋 Added to the waiting list. We will notify you promptly if a space opens.")
                else:
                    assigned_pony = available_ponies[0]
                    new_booking = pd.DataFrame([{
                        "Location": c_location, "Date": date_str,
                        "Time": c_time, "Activity": c_activity, "Details": f"{assigned_pony} (Rider: {c_name})", "Status": "Confirmed"
                    }])
                    st.session_state.bookings = pd.concat([st.session_state.bookings, new_booking], ignore_index=True)
                    
                    if not client_row.empty:
                        idx = client_row.index[0]
                        st.session_state.clients.loc[idx, 'Credits_Remaining'] -= 1
                        
                    st.balloons()
                    st.success(f"✨ Booking confirmed! You have been successfully matched with: **{assigned_pony}**.")

    with client_tab_feedback:
        st.subheader("🌟 Your Matched Rides & Memory Log")
        st.write("Review your upcoming or past confirmed bookings, check yard details with Google Maps, and share your feedback!")
        
        confirmed_bookings = st.session_state.bookings[st.session_state.bookings['Status'] == "Confirmed"]
        
        if confirmed_bookings.empty:
            st.info("No confirmed bookings found to display.")
        else:
            for _, b_row in confirmed_bookings.iterrows():
                details = str(b_row['Details'])
                pony_matched = "Pony"
                for p_name in st.session_state.ponies['Pony'].tolist():
                    if p_name.lower() in details.lower():
                        pony_matched = p_name
                        break
                
                img_path = get_pony_image_path(pony_matched)
                map_url = get_yard_map_link(b_row['Location'])
                
                col_p_img, col_p_details = st.columns([1, 2.5])
                with col_p_img:
                    if img_path:
                        st.image(img_path, use_container_width=True)
                    else:
                        st.markdown("""
                            <div style="background-color: #E2E8F0; padding: 45px 10px; border-radius: 12px; text-align: center; color: #718096; font-size: 0.8rem; border: 1px dashed #CBD5E1;">
                                🐎 Matched Mount
                            </div>
                        """, unsafe_allow_html=True)
                        
                with col_p_details:
                    st.markdown(f"""
                        <div style="background: white; padding: 20px; border-radius: 14px; border: 1px solid #EAEFE5; box-shadow: 0 4px 15px rgba(0,0,0,0.02); margin-bottom: 15px;">
                            <h4 style="margin-top:0; font-family: 'Playfair Display', serif; color: #2C4A3E;">✨ Matched with: {pony_matched}</h4>
                            <p style="margin: 4px 0;"><b>Activity:</b> {b_row['Activity']}</p>
                            <p style="margin: 4px 0;"><b>Details:</b> {b_row['Details']}</p>
                            <p style="margin: 4px 0;"><b>Date & Time:</b> {b_row['Date']} at {b_row['Time']}</p>
                            <p style="margin: 4px 0;"><b>Location:</b> {b_row['Location']}</p>
                            <div style="margin-top: 10px;">
                                <a href="{map_url}" target="_blank" style="background-color: #2C4A3E; color: white; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-size: 0.85rem; font-weight: 500; display: inline-block;">📍 Open Yard in Google Maps</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### 💌 Leave Feedback on Your Session")
            with st.form("client_feedback_form"):
                fb_rider = st.text_input("Your Name / Rider Name")
                fb_pony = st.selectbox("Pony You Ridden", st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Memory')]['Pony'].tolist())
                fb_rating = st.select_slider("Experience Rating", options=["⭐⭐⭐⭐⭐ (Exceptional)", "⭐⭐⭐⭐ (Wonderful)", "⭐⭐⭐ (Good)", "⭐⭐ (Fair)", "⭐ (Needs Improvement)"], value="⭐⭐⭐⭐⭐ (Exceptional)")
                fb_comments = st.text_area("Share your experience or comments about your ride:")
                
                submitted_fb = st.form_submit_button("Submit Review & Memories")
                if submitted_fb and fb_rider:
                    new_fb = pd.DataFrame([{"Rider": fb_rider, "Pony": fb_pony, "Rating": fb_rating, "Comments": fb_comments, "Date": str(datetime.date.today())}])
                    st.session_state.feedback_submissions = pd.concat([st.session_state.feedback_submissions, new_fb], ignore_index=True)
                    st.success("✨ Thank you! Your feedback has been securely shared with Charlotte and the team.")

    with client_tab_herd:
        st.subheader("🥕 Meet Our Herd & Fond Memories")
        st.write("Professional, well-schooled companions alongside tributes to where it all began:")
        
        for _, p in st.session_state.ponies.iterrows():
            col_img, col_info = st.columns([1, 3])
            img_path = get_pony_image_path(p['Pony'])
            
            with col_img:
                if img_path:
                    st.image(img_path, use_container_width=True)
                else:
                    st.markdown("""
                        <div style="background-color: #E2E8F0; padding: 35px 10px; border-radius: 10px; text-align: center; color: #718096; font-size: 0.8rem; border: 1px dashed #CBD5E1;">
                            📷 Photo Pending
                        </div>
                    """, unsafe_allow_html=True)
                    
            with col_info:
                st.markdown(f"""
                    <div style="background: white; padding: 18px; border-radius: 14px; margin-bottom: 12px; border: 1px solid #EAEFE5; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                        <h4 style="margin-top: 0; font-family: 'Playfair Display', serif; color: #1A252C;">🐎 {p['Pony']} <span style="font-size: 0.9rem; font-weight: normal; color: #666;">({p['Breed']}) — Yard: {p['Current_Yard']}</span></h4>
                        <p style="margin: 4px 0; font-size: 0.9rem;"><b>Status:</b> {p['Status']} &nbsp;|&nbsp; <b>Weight Capacity:</b> Up to {p['Max_Weight_kg']} kg</p>
                        <p style="margin: 4px 0; font-size: 0.9rem; color: #555;"><i>{p['Notes']}</i></p>
                    </div>
                """, unsafe_allow_html=True)

    with client_tab_waitlist:
        st.subheader("⏳ Waiting List Status")
        st.write("Active queue for fully booked time slots.")
        if st.session_state.waitlist.empty:
            st.info("You do not have any active waiting list requests.")
        else:
            st.dataframe(st.session_state.waitlist, use_container_width=True)

    with client_tab_profile:
        st.subheader("👤 Client Profile & Token Ledger")
        lookup_email = st.text_input("Enter your registered account email to view token packs:")
        if lookup_email:
            match = st.session_state.clients[st.session_state.clients['Email'].str.contains(lookup_email, case=False, na=False)]
            if not match.empty:
                for _, row in match.iterrows():
                    st.success(f"Welcome back, {row['Client']} 👋")
                    st.metric(label="Remaining Token Pack Credits", value=f"{row['Credits_Remaining']} Tokens 🪙")
                    st.write(f"**Associated Riders:** {row['Riders']}")
                    st.write(f"**Medical / Dietary Notes:** {row['Medical_Notes']}")
            else:
                st.warning("No account found matching this email address. Please speak with us at the yard.")

# --- NAVIGATION ROUTING ---
admin_pages = [
    st.Page(page_dashboard, title="Dashboard & Metrics", icon="🏠"),
    st.Page(page_schedule, title="Master Schedule", icon="📅"),
    st.Page(page_ponies, title="Herd Rota & Profiles", icon="🗺️"),
    st.Page(page_provisions, title="Alternative Provisions", icon="🎒"),
    st.Page(page_welfare, title="Equine Welfare", icon="🐎"),
    st.Page(page_vet, title="Vet & Farrier Hub", icon="🩺"),
    st.Page(page_clients, title="Clients & Tokens", icon="👥")
]

client_pages = [
    st.Page(page_client_portal, title="Client Booking Portal", icon="🌟")
]

navigation_structure = {
    "🔒 Admin Portal": admin_pages,
    "🌟 Client Portal": client_pages
}

pg = st.navigation(navigation_structure)
pg.run()
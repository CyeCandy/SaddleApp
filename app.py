import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pony Pursuits | Book Your Adventure",
    page_icon="🐎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PROMINENT BRANDING & SIDEBAR LOGO SETUP ---
# We use a custom container in the sidebar to make the logo clean, crisp, and high-visibility
with st.sidebar:
    st.markdown("""
        <div style="background-color: #FFFFFF; padding: 12px; border-radius: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px;">
            <p style="font-size: 0.85rem; font-weight: bold; color: #2C3E50; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Pony Pursuits</p>
        </div>
    """, unsafe_allow_html=True)
    try:
        st.image("logo.jpg", use_container_width=True)
    except Exception:
        st.info("🐎 Pony Pursuits Portal")
    st.divider()

# --- CUSTOM CSS FOR WARM, INVITING UI ---
st.markdown("""
    <style>
        .stApp { background-color: #F4F6F0; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
        h1, h2, h3 { color: #2C3E50; font-family: 'Helvetica Neue', sans-serif; }
        [data-testid="stMetricValue"] { font-size: 2.2rem; color: #27AE60; }
        
        /* Custom card styling for activities */
        .activity-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            border-left: 5px solid #27AE60;
        }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame([
        {"Location": "Huckleberry Farm (Heathfield, OX5)", "Date": "2026-04-02", "Time": "10:00 AM", "Activity": "Ride & Groom Session", "Details": "Teddy (Rider: Leo M.)", "Status": "Confirmed"},
        {"Location": "Huckleberry Farm (Heathfield, OX5)", "Date": "2026-04-02", "Time": "1:00 PM", "Activity": "Pony Therapy & Play", "Details": "Jubilee (Rider: Chloe S.)", "Status": "Confirmed"},
        {"Location": "Sandy Lane (Horspath, OX33)", "Date": "2026-04-03", "Time": "2:30 PM", "Activity": "Shotover Woodland Hack", "Details": "Spice (Rider: The Harrison Family)", "Status": "Confirmed"}
    ])

if "ponies" not in st.session_state:
    st.session_state.ponies = pd.DataFrame([
        {"Pony": "Jubilee", "Breed": "Gypsy Cob", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 90, "Status": "Active (🟢)", "Notes": "Great weight carrier for adults, calm & kind 🌳"},
        {"Pony": "Teddy", "Breed": "Welsh Cross", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 55, "Status": "Active (🟢)", "Notes": "Cuddly painting pony, loves humans 🤗"},
        {"Pony": "Spice", "Breed": "Gypsy Cob", "Current_Yard": "Sandy Lane", "Max_Weight_kg": 80, "Status": "Active (🟢)", "Notes": "Blue roan, ideal for woodland hacks 🌲"},
        {"Pony": "Prince", "Breed": "Mini Cob", "Current_Yard": "Sandy Lane", "Max_Weight_kg": 45, "Status": "Active (🟢)", "Notes": "Trained to ride & drive 🐎"},
        {"Pony": "Milkshake", "Breed": "Mini Cob", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 50, "Status": "Active (🟡)", "Notes": "Friendly riding pony 🍦"},
        {"Pony": "Spirit", "Breed": "Mini Cob", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 50, "Status": "Active (🟢)", "Notes": "Blagdon pony, great for youngsters ✨"},
        {"Pony": "Sam", "Breed": "Shetland", "Current_Yard": "Huckleberry Farm", "Max_Weight_kg": 25, "Status": "Retired (⚪)", "Notes": "Elder statesman in well-earned retirement 🥕"}
    ])

if "clients" not in st.session_state:
    st.session_state.clients = pd.DataFrame([
        {"Client": "The Harrison Family", "Riders": 3, "Credits_Remaining": 4, "Email": "harrison@example.com", "Medical_Notes": "None declared"},
        {"Client": "Sarah Jenkins", "Riders": 1, "Credits_Remaining": 2, "Email": "sarah@example.com", "Medical_Notes": "Mild allergy to stable dust"}
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

# --- HELPER FUNCTIONS ---
def is_pony_booked(pony_name, date_str, time_str):
    for _, row in st.session_state.bookings.iterrows():
        if row['Date'] == date_str and row['Time'] == time_str and row['Status'] == "Confirmed":
            if pony_name.lower() in str(row['Details']).lower():
                return True
    return False

# --- DEFINE ADMIN PAGES ---
def page_dashboard():
    st.title("Welcome back, Charlotte! 🌟")
    st.caption("5-Star Licensed Centre Management • Huckleberry Farm & Sandy Lane")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        huck_count = len(st.session_state.bookings[(st.session_state.bookings['Location'].str.contains('Huckleberry')) & (st.session_state.bookings['Status'] == 'Confirmed')])
        st.metric(label="Huckleberry Farm", value=f"{huck_count} Booked", delta="OX5 Yard")
    with col2:
        sandy_count = len(st.session_state.bookings[(st.session_state.bookings['Location'].str.contains('Sandy Lane')) & (st.session_state.bookings['Status'] == 'Confirmed')])
        st.metric(label="Sandy Lane / Shotover", value=f"{sandy_count} Booked", delta="OX33 Yard")
    with col3:
        wait_count = len(st.session_state.waitlist)
        st.metric(label="Waiting List", value=f"{wait_count} Riders", delta="Queue Active")
    with col4:
        working_ponies = len(st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Retired')])
        st.metric(label="Happy Herd", value=f"{working_ponies} Ready", delta="100% Fit")

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
            e_act = st.selectbox("Activity", ["Shotover Woodland Hack 🌲", "Ride & Groom Session 🐴", "Pony Therapy & Play 🐾", "Private Lesson ⭐"])
            
            active_ponies = st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Retired')]['Pony'].tolist()
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
        <div style="background: linear-gradient(135deg, #27AE60, #2ECC71); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px;">
            <h1>🐎 Welcome to Pony Pursuits!</h1>
            <p style="font-size: 1.2rem; margin-top: 5px;">Inclusive, friendly riding & outdoor adventures in Oxfordshire. No elitism, just pure fun with horses! 🌳✨</p>
        </div>
    """, unsafe_allow_html=True)
    
    client_tab_book, client_tab_herd, client_tab_waitlist, client_tab_profile = st.tabs([
        "✨ Book an Adventure", 
        "🥕 Meet Our Ponies", 
        "⏳ Waiting List", 
        "👤 My Token Balance"
    ])
    
    with client_tab_book:
        st.subheader("Choose Your Experience & Ride!")
        st.write("Fill in your details below to find your perfect equine match and book your session instantly.")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("""
                <div class="activity-card">
                    <h4>🌲 Shotover Woodland Hacks</h4>
                    <p>Explore the stunning trails around Shotover Country Park from our Sandy Lane yard (OX33). Perfect for refreshing outdoor hacks!</p>
                </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
                <div class="activity-card">
                    <h4>🧸 Ride & Groom / Pony Therapy</h4>
                    <p>Based at Huckleberry Farm (OX5). Get hands-on with brushing, pampering, and bonding with our friendly, calm herd.</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        with st.form("fun_client_booking_form"):
            st.markdown("### 📝 Quick Booking Form")
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                c_name = st.text_input("Your Family / Rider Name")
                c_email = st.text_input("Your Email Address")
                c_weight = st.number_input("Rider Weight (kg) [For safe pony matching]", min_value=20, max_value=110, value=50)
            with f_col2:
                c_location = st.selectbox("Choose Your Location", ["Huckleberry Farm (Heathfield, OX5)", "Sandy Lane (Horspath, OX33)"])
                c_activity = st.selectbox("Choose Your Activity", ["Shotover Woodland Hack 🌲", "Ride & Groom Session 🐴", "Pony Therapy & Play 🐾", "Private Lesson ⭐"])
                c_date = st.date_input("Pick a Date")
                c_time = st.selectbox("Pick a Time Slot", ["10:00 AM", "11:30 AM", "1:00 PM", "2:30 PM", "4:00 PM"])
            
            st.markdown("")
            submit_booking = st.form_submit_button("🎉 Book My Pony Adventure Now!", use_container_width=True)
            
            if submit_booking and c_name:
                date_str = c_date.strftime("%Y-%m-%d")
                
                client_row = st.session_state.clients[st.session_state.clients['Client'].str.contains(c_name, case=False, na=False)]
                if not client_row.empty:
                    tokens_left = int(client_row['Credits_Remaining'].values[0])
                    if tokens_left <= 0:
                        st.error("⚠️ You have 0 token pack credits left. Please top up your account to book!")
                        return
                
                active_herd = st.session_state.ponies[~st.session_state.ponies['Status'].str.contains('Retired')]
                weight_matched = active_herd[active_herd['Max_Weight_kg'] >= c_weight]
                
                available_ponies = []
                for _, p_row in weight_matched.iterrows():
                    if not is_pony_booked(p_row['Pony'], date_str, c_time):
                        available_ponies.append(p_row['Pony'])
                
                if weight_matched.empty:
                    st.error("❌ Oops! We couldn't find a working pony that matches this weight requirement safely. Please reach out to us directly!")
                elif not available_ponies:
                    st.warning("⚠️ All suitable weight-matched ponies are already booked for this exact slot. Would you like to join our waiting list?")
                    new_wait = pd.DataFrame([{"Client_Name": c_name, "Date": date_str, "Time": c_time, "Activity": c_activity, "Weight_kg": c_weight, "Requested_At": str(datetime.date.today())}])
                    st.session_state.waitlist = pd.concat([st.session_state.waitlist, new_wait], ignore_index=True)
                    st.info("📋 Added to the waiting list! We'll notify you if a space opens up.")
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
                    st.success(f"🥳 Hooray {c_name}! Your booking is confirmed. You've been magically matched with our wonderful pony: **{assigned_pony}**!")

    with client_tab_herd:
        st.subheader("🥕 Meet the Wonderful Pony Pursuits Family!")
        st.write("Get to know the lovely characters you or your children will meet at our yards:")
        
        for _, p in st.session_state.ponies.iterrows():
            st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3498DB;">
                    <h4>🐎 {p['Pony']} ({p['Breed']}) — <span style="font-size: 0.9rem; color: #555;">Based at {p['Current_Yard']}</span></h4>
                    <p style="margin: 2px 0;"><b>Status:</b> {p['Status']} | <b>Weight Limit:</b> Up to {p['Max_Weight_kg']} kg</p>
                    <p style="margin: 2px 0; color: #666;"><i>{p['Notes']}</i></p>
                </div>
            """, unsafe_allow_html=True)

    with client_tab_waitlist:
        st.subheader("⏳ Your Waiting List Queue")
        st.write("Checking for openings when sessions are fully booked.")
        if st.session_state.waitlist.empty:
            st.info("You don't have any active waiting list requests right now.")
        else:
            st.dataframe(st.session_state.waitlist, use_container_width=True)

    with client_tab_profile:
        st.subheader("👤 My Rider Profile & Token Credits")
        lookup_email = st.text_input("Enter your account email to view your tokens:")
        if lookup_email:
            match = st.session_state.clients[st.session_state.clients['Email'].str.contains(lookup_email, case=False, na=False)]
            if not match.empty:
                for _, row in match.iterrows():
                    st.success(f"Welcome back, {row['Client']}! 👋")
                    st.metric(label="Your Remaining Token Pack Credits", value=f"{row['Credits_Remaining']} Tokens 🪙")
                    st.write(f"**Registered Riders on Account:** {row['Riders']}")
                    st.write(f"**Medical / Care Notes:** {row['Medical_Notes']}")
            else:
                st.warning("We couldn't find an account matching that email address. Let us know at the yard and we'll get you set up!")

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
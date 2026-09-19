import streamlit as st

# Page Configuration
st.set_page_config(page_title="SaddleApp- Pony Pursuits Portal", layout="centered")

# App Header tailored to Charlotte Marshall's business
st.markdown("### 🐎 Pony Pursuits | Admin Portal")
st.title("Welcome back, Charlotte!")
st.caption("5-Star Licensed Centre Management • Powered by Saddle")

st.divider()

# Multi-location & Yard Status Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Huckleberry Farm (OX5)", value="8 Sessions", delta="Today")
with col2:
    st.metric(label="Sandy Lane / Shotover", value="5 Hacks", delta="Today")
with col3:
    st.metric(label="Active Ponies", value="12 / 12", delta="100% Health")

st.info("📍 **Active View:** Managing schedules across both Oxfordshire locations seamlessly.")

# Core Management Tabs replacing EC Pro clutter
tab_schedule, tab_services, tab_welfare, tab_clients = st.tabs([
    "📅 Multi-Site Schedule", "✨ Specialized Activities", "🐎 Equine Welfare & Limits", "👥 Client Accounts"
])

with tab_schedule:
    st.subheader("Today's Live Bookings")
    
    location_filter = st.radio("Select Yard Location:", ["All Locations", "Huckleberry Farm (Heathfield)", "Sandy Lane (Horspath)"], horizontal=True)
    
    st.markdown("---")
    if location_filter != "Sandy Lane (Horspath)":
        st.markdown("🏡 **[Huckleberry Farm] 10:00 AM** - Ride & Groom Session (Pony: Button)")
        st.markdown("🏡 **[Huckleberry Farm] 1:00 PM** - Pony Therapy Provision (Pony: Thunder)")
        
    if location_filter != "Huckleberry Farm (Heathfield)":
        st.markdown("🌳 **[Sandy Lane] 2:30 PM** - Shotover Woodland Hack (4 Riders Booked)")

with tab_services:
    st.subheader("Manage Bookings & Specialized Offerings")
    st.write("Unlike rigid school software, easily configure bespoke sessions:")
    
    service_type = st.selectbox("Activity Category", [
        "Woodland Hacks", 
        "Ride & Groom Sessions", 
        "Pony Therapy", 
        "Birthday Parties / Events",
        "Alternative Provision / Work-Based Care"
    ])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("Custom Session Name", value=f"Custom {service_type}")
    with col_b:
        st.number_input("Max Participant Capacity", min_value=1, max_value=20, value=5)
        
    if st.button("Update Activity Settings", type="primary"):
        st.success(f"Successfully updated rules for {service_type}!")

with tab_welfare:
    st.subheader("Pony Workload & Weight Constraints")
    st.write("Ensure compliance with Cherwell District Council 5-star licensing rules.")
    
    st.markdown("- **Thunder**: Max Rider Weight: 85kg | *Status:* Rested for afternoon therapy session (🟢)")
    st.markdown("- **Button**: Max Rider Weight: 50kg | *Status:* Completed morning groom block (🟡)")
    
    if st.button("Log Rest Period / Override Weight Limit"):
        st.toast("Welfare log updated.")

with tab_clients:
    st.subheader("Client & Rider Database")
    search_client = st.text_input("🔍 Search by rider name, parent, or email...")
    st.markdown("👤 **The Harrison Family** (3 Riders | Active Credit Pack: 4 Sessions remaining)")
    st.markdown("👤 **Local Authority Provision Group** (Weekly Alternative Care Bookings)")
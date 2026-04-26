"""
Main Application File
Crime Record Management & Analysis System
Streamlit UI with Sidebar Navigation
"""

import streamlit as st
from datetime import datetime
from modules.db_operations import DatabaseManager
from modules.police_module import PoliceOfficer
from modules.dashboard import Dashboard

try:
    from streamlit_option_menu import option_menu
except ImportError:
    option_menu = None


# ==================== HELPER FUNCTIONS ====================

def searchable_dropdown(label, options, key_prefix):
    """
    Create a searchable dropdown that allows typing custom values
    Returns either selected option or custom typed value
    """
    col1, col2 = st.columns([4, 1])
    
    with col1:
        selected = st.selectbox(label, options, key=f"{key_prefix}_select")
    
    with col2:
        add_custom = st.checkbox("🔧", key=f"{key_prefix}_custom", help="Add custom value")
    
    if add_custom:
        custom_value = st.text_input(f"Enter custom {label.lower()}", key=f"{key_prefix}_input", placeholder="Type here...")
        return custom_value if custom_value else selected
    
    return selected


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Crime Record Management System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INITIALIZATION ====================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.officer_id = None
    st.session_state.officer_name = None
    st.session_state.badge_number = None

if 'viewing_public_dashboard' not in st.session_state:
    st.session_state.viewing_public_dashboard = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False


# ==================== AUTHENTICATION PAGES ====================

def show_auth_page():
    """Show login/register page or public dashboard option"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        st.title("🚨 Crime Management System")
        st.markdown("<h3 style='text-align: center;'>Police Officers Portal</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Choice between public dashboard and login
        st.subheader("Select an Option")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📊 View Public Dashboard", use_container_width=True, key="public_dash_btn"):
                st.session_state.viewing_public_dashboard = True
                st.rerun()
        
        with col_b:
            if st.button("🔐 Officer Login", use_container_width=True, key="officer_login_btn"):
                st.session_state.show_login = True
                st.rerun()
        
        st.markdown("---")
        
        # Show login/register only if officer_login button is clicked
        if not st.session_state.get('show_login', False):
            st.info("👉 Choose an option above to continue")
            return
        
        # Tab for login and register
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        # ==================== LOGIN TAB ====================
        with tab1:
            st.subheader("Officer Login")
            
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
            
            if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                if username and password:
                    police = PoliceOfficer()
                    success, officer_data, message = police.login_officer(username, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.officer_id = officer_data[0]
                        st.session_state.officer_name = officer_data[1]
                        st.session_state.badge_number = officer_data[2]
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter username and password")
            
            st.markdown("---")
            st.info("ℹ️ Don't have an account? Go to the Register tab to create one.")
        
        # ==================== REGISTER TAB ====================
        with tab2:
            st.subheader("Create New Account")
            
            with st.form("registration_form"):
                name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email", placeholder="Enter your email")
                badge_number = st.text_input("Badge Number", placeholder="Enter your police badge number")
                username = st.text_input("Username", placeholder="Choose a username (min 4 chars)")
                password = st.text_input("Password", type="password", placeholder="Enter password (min 6 chars)")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
                submit_btn = st.form_submit_button("📝 Register", use_container_width=True)
                
                if submit_btn:
                    police = PoliceOfficer()
                    success, message = police.register_officer(
                        username, password, confirm_password, name, badge_number, email
                    )
                    
                    if success:
                        st.success(message)
                        st.info("✅ Registration successful! Please login with your credentials.")
                    else:
                        st.error(message)


# ==================== POLICE OFFICER PANEL ====================

def show_police_panel():
    """Show police officer panel with CRUD operations"""
    
    st.title("👮 Police Officer Control Panel")
    
    # Display officer info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"👤 Officer: {st.session_state.officer_name}")
    with col2:
        st.info(f"🎖️ Badge: {st.session_state.badge_number}")
    with col3:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.officer_id = None
            st.session_state.officer_name = None
            st.session_state.badge_number = None
            st.rerun()
    
    st.markdown("---")
    
    # Police operations menu
    police_menu = st.radio(
        "Select Operation:",
        ["➕ Add Crime Record", "✏️ Update Record", "🗑️ Delete Record", "📋 View All Records"],
        horizontal=True
    )
    
    police = PoliceOfficer()
    officer_id = st.session_state.officer_id
    
    # ==================== ADD CRIME RECORD ====================
    if police_menu == "➕ Add Crime Record":
        st.subheader("Add New Crime Record")
        
        with st.form("add_crime_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                crime_type = searchable_dropdown("Crime Type", police.get_crime_types(), "add_crime")
                city = searchable_dropdown("City/Location", police.get_indian_cities(), "add_city")
                date = st.date_input("Crime Date")
            
            with col2:
                time_val = st.time_input("Crime Time")
                gender = st.selectbox("Victim Gender", ["Select"] + police.get_genders())
                weapon = searchable_dropdown("Weapon Used", police.get_weapons(), "add_weapon")
            
            submit = st.form_submit_button("✅ Add Record", use_container_width=True)
            
            if submit:
                success, message = police.add_crime_record(
                    crime_type, city, date, time_val, gender, weapon, officer_id, st.session_state.officer_name
                )
                
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)
    
    # ==================== UPDATE CRIME RECORD ====================
    elif police_menu == "✏️ Update Record":
        st.subheader("Update Crime Record")
        
        columns, results = police.get_all_records()
        
        if results is None or len(results) == 0:
            st.warning("No records found")
        else:
            # Create options display
            record_options = [f"ID: {row[0]} - {row[1]} - {row[2]}" for row in results]
            selected_idx = st.selectbox("Select Record to Update", range(len(results)), format_func=lambda x: record_options[x])
            
            selected_record = results[selected_idx]
            record_id = selected_record[0]
            
            with st.form("update_crime_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    crime_type = searchable_dropdown("Crime Type", police.get_crime_types(), "upd_crime")
                    city = searchable_dropdown("City/Location", police.get_indian_cities(), "upd_city")
                    date = st.date_input("Crime Date", key="update_date")
                
                with col2:
                    time_val = st.time_input("Crime Time", key="update_time")
                    gender = st.selectbox("Victim Gender", ["Select"] + police.get_genders(), key="update_gender")
                    weapon = searchable_dropdown("Weapon Used", police.get_weapons(), "upd_weapon")
                
                submit = st.form_submit_button("✅ Update Record", use_container_width=True)
                
                if submit:
                    success, message = police.update_crime_record(
                        record_id, crime_type, city, date, time_val, gender, weapon, officer_id, st.session_state.officer_name
                    )
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    # ==================== DELETE CRIME RECORD ====================
    elif police_menu == "🗑️ Delete Record":
        st.subheader("Delete Crime Record")
        
        columns, results = police.get_all_records()
        
        if results is None or len(results) == 0:
            st.warning("No records found")
        else:
            record_options = [f"ID: {row[0]} - {row[1]} - {row[2]}" for row in results]
            selected_idx = st.selectbox("Select Record to Delete", range(len(results)), format_func=lambda x: record_options[x])
            
            selected_record = results[selected_idx]
            record_id = selected_record[0]
            
            st.warning("⚠️ This action cannot be undone!")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Delete", use_container_width=True, key="delete_btn"):
                    success, message = police.delete_crime_record(record_id, officer_id, st.session_state.officer_name, selected_record[1], selected_record[2])
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            with col2:
                st.button("❌ Cancel", use_container_width=True, disabled=True)
    
    # ==================== VIEW ALL RECORDS ====================
    elif police_menu == "📋 View All Records":
        st.subheader("All Crime Records")
        
        columns, results = police.get_all_records()
        
        if results is None or len(results) == 0:
            st.info("No records found")
        else:
            import pandas as pd
            df = pd.DataFrame(results, columns=columns)
            st.dataframe(df, use_container_width=True, height=500)
            st.success(f"Total Records: {len(df)}")


# ==================== CRIME ANALYSIS DASHBOARD ====================

def show_dashboard():
    """Show crime analysis dashboard"""
    
    dashboard = Dashboard()
    dashboard.load_data()
    
    # Render header
    dashboard.render_header()
    
    # Render filters
    city, crime_type, gender = dashboard.render_filters()
    
    # Apply filters
    filtered_data = dashboard.apply_filters(city, crime_type, gender)
    
    # Render summary cards
    dashboard.render_summary_cards(filtered_data)
    
    # Render safety status
    dashboard.render_safety_status(filtered_data)
    
    # Render analysis section
    dashboard.render_analysis_section(filtered_data)
    
    # Render data table
    dashboard.render_data_table(filtered_data)
    
    # Render emergency contacts
    dashboard.render_emergency_contacts()
    
    # Render footer
    dashboard.render_footer()


# ==================== ACTIVITY LOG ====================

def show_activity_log():
    """Show activity log page with officer operations"""
    
    st.title("📋 Activity Log")
    st.markdown("Track all crime record operations (add, update, delete)")
    st.markdown("---")
    
    db = DatabaseManager()
    
    # Filter options
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        filter_type = st.radio("Filter by:", ["All Operations", "Officer Operations"], horizontal=True)
    
    if filter_type == "Officer Operations":
        with col2:
            officer_name = st.text_input("Filter by Officer Name", value=st.session_state.officer_name)
    else:
        officer_name = None
    
    with col3:
        num_records = st.selectbox("Show last N records:", [10, 20, 50, 100], index=1)
    
    st.markdown("---")
    
    # Fetch operations
    if filter_type == "Officer Operations" and officer_name:
        columns, operations = db.get_officer_operations(officer_name, num_records)
        title_text = f"Operations by {officer_name}"
    else:
        columns, operations = db.get_recent_operations(num_records)
        title_text = "All Recent Operations"
    
    if operations is None or len(operations) == 0:
        st.info(f"ℹ️ No operations found for {title_text.lower()}")
    else:
        st.subheader(f"📊 {title_text} (Latest {len(operations)})")
        
        # Create a detailed table
        import pandas as pd
        df_data = []
        
        for op in operations:
            officer_name_op, operation, record_id, crime_type, city, timestamp = op
            
            # Add emoji based on operation
            if operation == "ADD":
                op_emoji = "➕"
                op_color = "green"
            elif operation == "UPDATE":
                op_emoji = "✏️"
                op_color = "blue"
            elif operation == "DELETE":
                op_emoji = "🗑️"
                op_color = "red"
            else:
                op_emoji = "❓"
                op_color = "gray"
            
            df_data.append({
                "Officer": f"👮 {officer_name_op}",
                "Operation": f"{op_emoji} {operation}",
                "Record ID": f"#{record_id}" if record_id else "N/A",
                "Crime Type": crime_type or "N/A",
                "City": city or "N/A",
                "Timestamp": timestamp
            })
        
        df = pd.DataFrame(df_data)
        
        # Display as table with custom styling
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Summary stats
        st.markdown("---")
        st.subheader("📈 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            add_count = sum(1 for op in operations if op[1] == "ADD")
            st.metric("➕ Added", add_count)
        
        with col2:
            update_count = sum(1 for op in operations if op[1] == "UPDATE")
            st.metric("✏️ Updated", update_count)
        
        with col3:
            delete_count = sum(1 for op in operations if op[1] == "DELETE")
            st.metric("🗑️ Deleted", delete_count)
        
        with col4:
            total_operations = len(operations)
            st.metric("📊 Total", total_operations)


# ==================== ADMIN SETUP ====================

def show_admin_setup():
    """Show admin setup page"""
    
    st.title("⚙️ Admin Setup")
    st.markdown("---")
    
    st.warning("⚠️ This section is for initial database setup only")
    
    if st.button("🗄️ Create Database Tables", use_container_width=True):
        db = DatabaseManager()
        if db.create_tables():
            st.success("✅ Database tables created successfully!")
        else:
            st.error("❌ Failed to create tables")


# ==================== MAIN APP LOGIC ====================

def main():
    """Main application"""
    
    # Show public dashboard if selected
    if st.session_state.viewing_public_dashboard:
        with st.sidebar:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.title("🚨 Crime Management System")
            with col2:
                if st.button("🚪 Exit", key="exit_public_dash"):
                    st.session_state.viewing_public_dashboard = False
                    st.rerun()
        
        show_dashboard()
        return
    
    # Show auth page if not logged in
    if not st.session_state.logged_in:
        show_auth_page()
    else:
        # Create sidebar navigation
        with st.sidebar:
            st.markdown("---")
            if option_menu:
                selected = option_menu(
                    menu_title="🔷 Navigation",
                    options=["👮 Police Panel", "📊 Dashboard", "📋 Activity Log", "⚙️ Setup"],
                    icons=["person-check", "bar-chart-line", "list-check", "gear"],
                    menu_icon="cast",
                    default_index=0,
                )
            else:
                # Fallback if streamlit_option_menu not available
                selected = st.radio(
                    "Navigation",
                    ["👮 Police Panel", "📊 Dashboard", "📋 Activity Log", "⚙️ Setup"],
                    label_visibility="collapsed"
                )
            st.markdown("---")
        
        # Show selected page
        if selected == "👮 Police Panel":
            show_police_panel()
        elif selected == "📊 Dashboard":
            show_dashboard()
        elif selected == "📋 Activity Log":
            show_activity_log()
        elif selected == "⚙️ Setup":
            show_admin_setup()


if __name__ == "__main__":
    main()

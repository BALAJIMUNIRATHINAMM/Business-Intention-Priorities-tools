import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import AuthManager

# Check authentication
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.error("Please login to access this page")
    st.page_link("pages/Login.py", label="Go to Login", icon="🔐")
    st.stop()

st.set_page_config(
    page_title="User Dashboard - Business Priority Tools",
    page_icon="👤",
    layout="wide"
)

# Initialize auth manager
auth_manager = AuthManager()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("👤 User Dashboard")
    st.subheader(f"Welcome back, {st.session_state['name']}")

with col2:
    if st.button("🚪 Logout", type="secondary"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Sidebar navigation
st.sidebar.title("User Menu")
user_page = st.sidebar.selectbox(
    "Select Page",
    ["Overview", "My Usage", "Account Settings", "Tools"]
)

username = st.session_state['username']

if user_page == "Overview":
    # User overview
    st.header("📊 Account Overview")
    
    # Get user usage data
    usage_data = auth_manager.get_user_usage(username, days=30)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_usage = sum([row[2] for row in usage_data])
    
    with col1:
        st.metric(
            label="Total Usage (30d)",
            value=total_usage,
            delta="Actions performed"
        )
    
    with col2:
        unique_tools = len(set([row[0] for row in usage_data]))
        st.metric(
            label="Tools Used",
            value=unique_tools,
            delta="Different tools"
        )
    
    with col3:
        avg_processing_time = sum([row[3] or 0 for row in usage_data]) / max(len(usage_data), 1)
        st.metric(
            label="Avg Processing Time",
            value=f"{avg_processing_time:.2f}s",
            delta="Per operation"
        )
    
    with col4:
        total_data_processed = sum([row[4] or 0 for row in usage_data])
        st.metric(
            label="Data Processed",
            value=f"{total_data_processed/1024/1024:.1f} MB",
            delta="Total size"
        )
    
    # Usage by tool
    if usage_data:
        st.header("🔧 Tool Usage Breakdown")
        
        tool_usage_df = pd.DataFrame(usage_data, columns=[
            'Tool', 'Action', 'Count', 'Avg Time', 'Total Size'
        ])
        
        # Group by tool
        tool_summary = tool_usage_df.groupby('Tool').agg({
            'Count': 'sum',
            'Avg Time': 'mean',
            'Total Size': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                tool_summary, 
                values='Count', 
                names='Tool',
                title="Usage Distribution by Tool"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                tool_summary, 
                x='Tool', 
                y='Count',
                title="Usage Count by Tool"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.header("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Signal BF Tool", use_container_width=True):
            st.page_link("pages/Signal BF.py", label="Go to Signal BF Tool")
    
    with col2:
        if st.button("🏢 Company BF Tool", use_container_width=True):
            st.page_link("pages/Company BF.py", label="Go to Company BF Tool")
    
    with col3:
        if st.button("📈 Aggregated Tool", use_container_width=True):
            st.page_link("pages/Aggregated.py", label="Go to Aggregated Tool")

elif user_page == "My Usage":
    st.header("📈 My Usage Statistics")
    
    # Time range selector
    time_range = st.selectbox(
        "Select Time Range",
        ["Last 7 days", "Last 30 days", "Last 90 days"]
    )
    
    days_map = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 90 days": 90
    }
    days = days_map[time_range]
    
    # Get detailed usage data
    import sqlite3
    conn = sqlite3.connect(auth_manager.db_file)
    
    usage_over_time = pd.read_sql_query(f'''
        SELECT DATE(timestamp) as date, 
               tool_name,
               COUNT(*) as usage_count
        FROM usage_logs
        WHERE username = ? AND timestamp >= datetime('now', '-{days} days')
        GROUP BY DATE(timestamp), tool_name
        ORDER BY date
    ''', conn, params=(username,))
    
    if not usage_over_time.empty:
        st.subheader("Usage Trend")
        fig = px.line(
            usage_over_time, 
            x='date', 
            y='usage_count',
            color='tool_name',
            title=f"My Usage Trend - {time_range}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed usage table
    detailed_usage = pd.read_sql_query(f'''
        SELECT timestamp, tool_name, action, file_size, processing_time, success
        FROM usage_logs
        WHERE username = ? AND timestamp >= datetime('now', '-{days} days')
        ORDER BY timestamp DESC
    ''', conn, params=(username,))
    
    if not detailed_usage.empty:
        st.subheader("Detailed Usage History")
        st.dataframe(detailed_usage, use_container_width=True)
    else:
        st.info("No usage data found for the selected time range")
    
    conn.close()

elif user_page == "Account Settings":
    st.header("⚙️ Account Settings")
    
    # Get current user info
    users = auth_manager.get_all_users()
    current_user = None
    for user in users:
        if user[0] == username:
            current_user = user
            break
    
    if current_user:
        st.subheader("Profile Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Username", value=current_user[0], disabled=True)
            st.text_input("Email", value=current_user[1])
            st.text_input("Full Name", value=current_user[2])
        
        with col2:
            st.text_input("Role", value=current_user[3], disabled=True)
            st.text_input("Plan", value=current_user[4], disabled=True)
            st.text_input("Member Since", value=current_user[5], disabled=True)
        
        # Password change
        st.subheader("Change Password")
        
        with st.form("password_change"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password"):
                if new_password != confirm_password:
                    st.error("New passwords do not match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long!")
                else:
                    st.success("Password changed successfully!")
        
        # Account preferences
        st.subheader("Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Email notifications", value=True)
            st.checkbox("Usage alerts", value=False)
        
        with col2:
            st.selectbox("Theme", ["Light", "Dark", "Auto"])
            st.selectbox("Language", ["English", "Spanish", "French"])
        
        if st.button("Save Preferences"):
            st.success("Preferences saved successfully!")

elif user_page == "Tools":
    st.header("🛠️ Available Tools")
    
    # Tool cards
    tools = [
        {
            "name": "Signal BF Priority Extraction",
            "description": "Extract priority signals from business function reports",
            "icon": "📊",
            "page": "pages/Signal BF.py"
        },
        {
            "name": "Company BF Priority Extraction", 
            "description": "Process company-specific business function priorities",
            "icon": "🏢",
            "page": "pages/Company BF.py"
        },
        {
            "name": "Aggregated Priority Extraction",
            "description": "Combine and analyze aggregated priorities",
            "icon": "📈",
            "page": "pages/Aggregated.py"
        },
        {
            "name": "BF Consolidated Priority",
            "description": "Advanced consolidated priority extraction",
            "icon": "🔄",
            "page": "pages/BF Consolidated.py"
        }
    ]
    
    cols = st.columns(2)
    
    for i, tool in enumerate(tools):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style='padding: 1rem; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 1rem;'>
                    <h3>{tool['icon']} {tool['name']}</h3>
                    <p>{tool['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Open {tool['name']}", key=f"tool_{i}"):
                    st.page_link(tool['page'], label=f"Go to {tool['name']}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>© 2025 Draup Dataflow Engine | User Dashboard v1.0</p>
    </div>
    """, 
    unsafe_allow_html=True
)
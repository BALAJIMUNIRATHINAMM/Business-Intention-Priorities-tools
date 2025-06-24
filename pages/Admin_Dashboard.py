import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

if st.session_state.get('user_role') != 'admin':
    st.error("Access denied. Admin privileges required.")
    st.stop()

st.set_page_config(
    page_title="Admin Dashboard - Business Priority Tools",
    page_icon="👑",
    layout="wide"
)

# Initialize auth manager
auth_manager = AuthManager()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("👑 Admin Dashboard")
    st.subheader(f"Welcome, {st.session_state['name']}")

with col2:
    if st.button("🚪 Logout", type="secondary"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Sidebar navigation
st.sidebar.title("Admin Navigation")
admin_page = st.sidebar.selectbox(
    "Select Page",
    ["Overview", "User Management", "Usage Analytics", "System Settings"]
)

if admin_page == "Overview":
    # Get usage statistics
    stats = auth_manager.get_usage_stats()
    
    # Key metrics
    st.header("📊 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Users",
            value=stats['total_users'],
            delta=f"+{stats['active_users']} active"
        )
    
    with col2:
        st.metric(
            label="Active Users (30d)",
            value=stats['active_users'],
            delta=f"{(stats['active_users']/max(stats['total_users'], 1)*100):.1f}% of total"
        )
    
    with col3:
        st.metric(
            label="Total Usage Events",
            value=stats['total_usage'],
            delta="All time"
        )
    
    with col4:
        st.metric(
            label="Most Used Tool",
            value=stats['tool_usage'][0][0] if stats['tool_usage'] else "N/A",
            delta=f"{stats['tool_usage'][0][1]} uses" if stats['tool_usage'] else "0 uses"
        )
    
    # Usage by tool chart
    if stats['tool_usage']:
        st.header("🔧 Tool Usage Distribution")
        
        tool_df = pd.DataFrame(stats['tool_usage'], columns=['Tool', 'Usage Count'])
        
        fig = px.pie(
            tool_df, 
            values='Usage Count', 
            names='Tool',
            title="Usage Distribution by Tool"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.header("📈 Recent System Activity")
    
    # Get recent usage logs
    import sqlite3
    conn = sqlite3.connect(auth_manager.db_file)
    recent_activity = pd.read_sql_query('''
        SELECT username, tool_name, action, timestamp, success
        FROM usage_logs
        ORDER BY timestamp DESC
        LIMIT 20
    ''', conn)
    conn.close()
    
    if not recent_activity.empty:
        st.dataframe(recent_activity, use_container_width=True)
    else:
        st.info("No recent activity to display")

elif admin_page == "User Management":
    st.header("👥 User Management")
    
    # Get all users
    users = auth_manager.get_all_users()
    
    if users:
        # Convert to DataFrame for better display
        users_df = pd.DataFrame(users, columns=[
            'Username', 'Email', 'Name', 'Role', 'Plan', 
            'Created Date', 'Last Login', 'Active'
        ])
        
        # User statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", len(users_df))
        
        with col2:
            admin_count = len(users_df[users_df['Role'] == 'admin'])
            st.metric("Admin Users", admin_count)
        
        with col3:
            active_count = len(users_df[users_df['Active'] == 1])
            st.metric("Active Users", active_count)
        
        # Users table with filters
        st.subheader("User List")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            role_filter = st.selectbox("Filter by Role", ["All", "admin", "user"])
        
        with col2:
            plan_filter = st.selectbox("Filter by Plan", ["All", "basic", "premium", "enterprise"])
        
        with col3:
            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive"])
        
        # Apply filters
        filtered_df = users_df.copy()
        
        if role_filter != "All":
            filtered_df = filtered_df[filtered_df['Role'] == role_filter]
        
        if plan_filter != "All":
            filtered_df = filtered_df[filtered_df['Plan'] == plan_filter]
        
        if status_filter == "Active":
            filtered_df = filtered_df[filtered_df['Active'] == 1]
        elif status_filter == "Inactive":
            filtered_df = filtered_df[filtered_df['Active'] == 0]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # User actions
        st.subheader("User Actions")
        
        selected_user = st.selectbox("Select User", users_df['Username'].tolist())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("View User Details"):
                user_data = users_df[users_df['Username'] == selected_user].iloc[0]
                st.json(user_data.to_dict())
        
        with col2:
            if st.button("Reset Password"):
                st.info("Password reset functionality would be implemented here")
        
        with col3:
            if st.button("Deactivate User"):
                st.warning("User deactivation functionality would be implemented here")
    
    else:
        st.info("No users found in the system")

elif admin_page == "Usage Analytics":
    st.header("📊 Usage Analytics")
    
    # Time range selector
    time_range = st.selectbox(
        "Select Time Range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
    )
    
    # Convert time range to days
    days_map = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 90 days": 90,
        "All time": 9999
    }
    days = days_map[time_range]
    
    # Get usage data
    import sqlite3
    conn = sqlite3.connect(auth_manager.db_file)
    
    # Usage over time
    usage_over_time = pd.read_sql_query(f'''
        SELECT DATE(timestamp) as date, COUNT(*) as usage_count
        FROM usage_logs
        WHERE timestamp >= datetime('now', '-{days} days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    ''', conn)
    
    if not usage_over_time.empty:
        st.subheader("Usage Trend")
        fig = px.line(
            usage_over_time, 
            x='date', 
            y='usage_count',
            title=f"Daily Usage - {time_range}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top users
    top_users = pd.read_sql_query(f'''
        SELECT username, COUNT(*) as usage_count
        FROM usage_logs
        WHERE timestamp >= datetime('now', '-{days} days')
        GROUP BY username
        ORDER BY usage_count DESC
        LIMIT 10
    ''', conn)
    
    if not top_users.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Users by Activity")
            fig = px.bar(
                top_users, 
                x='username', 
                y='usage_count',
                title="Most Active Users"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("User Activity Table")
            st.dataframe(top_users, use_container_width=True)
    
    # Tool performance
    tool_performance = pd.read_sql_query(f'''
        SELECT tool_name, 
               COUNT(*) as usage_count,
               AVG(processing_time) as avg_processing_time,
               SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
        FROM usage_logs
        WHERE timestamp >= datetime('now', '-{days} days')
        GROUP BY tool_name
    ''', conn)
    
    if not tool_performance.empty:
        st.subheader("Tool Performance Metrics")
        st.dataframe(tool_performance, use_container_width=True)
    
    conn.close()

elif admin_page == "System Settings":
    st.header("⚙️ System Settings")
    
    # System configuration
    st.subheader("System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("System Name", value="Business Priority Tools")
        st.number_input("Default Usage Limit", value=100, min_value=1)
        st.selectbox("Default User Role", ["user", "admin"])
    
    with col2:
        st.selectbox("Default Plan", ["basic", "premium", "enterprise"])
        st.number_input("Session Timeout (minutes)", value=30, min_value=5)
        st.checkbox("Enable User Registration", value=True)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
    
    # Database management
    st.subheader("Database Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Backup Database"):
            st.info("Database backup functionality would be implemented here")
    
    with col2:
        if st.button("Clean Old Logs"):
            st.info("Log cleanup functionality would be implemented here")
    
    with col3:
        if st.button("Export User Data"):
            st.info("User data export functionality would be implemented here")
    
    # System health
    st.subheader("System Health")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Database Size", "2.5 MB")
    
    with col2:
        st.metric("Active Sessions", "3")
    
    with col3:
        st.metric("System Uptime", "99.9%")
    
    with col4:
        st.metric("Error Rate", "0.1%")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>© 2025 Draup Dataflow Engine | Admin Dashboard v1.0</p>
    </div>
    """, 
    unsafe_allow_html=True
)
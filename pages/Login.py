import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import AuthManager

st.set_page_config(
    page_title="Login - Business Priority Tools",
    page_icon="🔐",
    layout="centered"
)

# Initialize auth manager
auth_manager = AuthManager()

# Custom CSS for login page
st.markdown("""
<style>
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.demo-credentials {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Main login interface
st.markdown('<div class="login-container">', unsafe_allow_html=True)

st.markdown('<div class="login-header">', unsafe_allow_html=True)
st.title("🍳 Business Priority Tools")
st.subheader("Secure Login")
st.markdown('</div>', unsafe_allow_html=True)

# Get authenticator
authenticator = auth_manager.get_authenticator()

if authenticator:
    # Login widget
    name, authentication_status, username = authenticator.login('Login', 'main')
    
    if authentication_status == False:
        st.error('Username/password is incorrect')
        
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        
        # Demo credentials info
        with st.expander("🔍 Demo Credentials"):
            st.info("""
            **Admin Account:**
            - Username: admin
            - Password: admin123
            
            **Demo User Account:**
            - Username: demo_user  
            - Password: demo123
            """)
            
    elif authentication_status:
        # Update last login
        auth_manager.update_last_login(username)
        
        # Store user info in session state
        st.session_state['name'] = name
        st.session_state['username'] = username
        st.session_state['authentication_status'] = authentication_status
        
        # Get user role from database
        users = auth_manager.get_all_users()
        user_role = None
        for user in users:
            if user[0] == username:  # username is first column
                user_role = user[3]  # role is fourth column
                break
                
        st.session_state['user_role'] = user_role
        
        st.success(f'Welcome *{name}*!')
        st.info('Redirecting to dashboard...')
        
        # Redirect based on role
        if user_role == 'admin':
            st.page_link("pages/Admin_Dashboard.py", label="Go to Admin Dashboard", icon="👑")
        else:
            st.page_link("main.py", label="Go to Tools Dashboard", icon="🍳")

st.markdown('</div>', unsafe_allow_html=True)

# Registration section
st.markdown("---")
st.subheader("New User Registration")

with st.expander("Register New Account"):
    with st.form("registration_form"):
        reg_username = st.text_input("Username")
        reg_email = st.text_input("Email")
        reg_name = st.text_input("Full Name")
        reg_password = st.text_input("Password", type="password")
        reg_confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if reg_password != reg_confirm_password:
                st.error("Passwords do not match!")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif not reg_username or not reg_email or not reg_name:
                st.error("All fields are required!")
            else:
                success = auth_manager.register_user(
                    reg_username, reg_email, reg_name, reg_password
                )
                if success:
                    st.success("Registration successful! Please login with your credentials.")
                else:
                    st.error("Registration failed. Username or email already exists.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>© 2025 Draup Dataflow Engine | Secure Business Priority Extraction Platform</p>
    </div>
    """, 
    unsafe_allow_html=True
)
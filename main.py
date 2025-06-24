import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="Business Intention Priority Extraction Tools",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Business Intention Priority Extraction Tools is a data request application that streamlines data requests, enhances collaboration among stakeholders, and improves operational efficiency.",
        "Get help": "https://github.com/your-repo/issues",
        "Report a bug": "https://github.com/your-repo/issues"
    }
)

# Header with styling
st.header('🍳Business Intention Priorities Tools', divider='rainbow')

# Layout with uniform column spacing
col1, col2, col3 = st.columns(3)

# Reusable function for creating tool cards
def tool_card(title, description, button_label, page_link):
    st.markdown(f"<h3 style='text-align: center; color: #333;'>{title}</h3>", unsafe_allow_html=True)
    st.info(description, icon="ℹ️")
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    # Centered Button
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        if st.button(f"🔍 {button_label}", use_container_width=True):
            st.page_link(page_link, label=f"Go to {title}", icon="🍳")

# Creating tool sections
with col1:
    tool_card(
        title="Signal BF Priority Extraction Tool",
        description="📌 **How it works:** Upload a CSV or Excel file, process the data, and extract priority signals effortlessly.",
        button_label="Extract Priority Signals",
        page_link="pages/Signal BF.py"
    )

with col2:
    tool_card(
        title="Company BF Priority Extraction Tool",
        description="📌 **How it works:** Upload a CSV or Excel file, process the data, and extract priority companies effortlessly.",
        button_label="Extract Priority Company",
        page_link="pages/Company BF.py"
    )

with col3:
    tool_card(
        title="Aggregated Priority Extraction Tool",
        description="📌 **How it works:** Upload a CSV or Excel file, process the data, and extract aggregated priorities effortlessly.",
        button_label="Extract Aggregated Priorities",
        page_link="pages/Aggregated.py"
    )

# Additional Information Section
st.markdown("---")
st.header("📋 Additional Tools & Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 Advanced Tools")
    if st.button("🔄 BF Consolidated Priority Tool", use_container_width=True):
        st.page_link("pages/BF Consolidated.py", label="Go to Consolidated Tool", icon="🔄")
    
    if st.button("📊 Consolidated All Priorities", use_container_width=True):
        st.page_link("pages/Consolidated All.py", label="Go to All Priorities", icon="📊")

with col2:
    st.subheader("ℹ️ Information & Support")
    if st.button("📖 About & Attributions", use_container_width=True):
        st.page_link("pages/About.py", label="About This Application", icon="📖")
    
    st.info("Built with open-source technologies. See About page for full attributions.", icon="🙏")

# Open Source Notice
st.markdown("---")
st.markdown(
    """
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin: 20px 0;'>
        <h4 style='margin: 0; color: #333;'>🙏 Open Source Acknowledgment</h4>
        <p style='margin: 10px 0 0 0; color: #666;'>
            This application is built using excellent open-source libraries including Streamlit, Pandas, OpenPyXL, and XlsxWriter. 
            We thank the open-source community for making these tools available.
            <a href='pages/About.py' style='color: #1f77b4;'>View full attributions →</a>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Footer with enhanced attribution
st.markdown(
    """
    <style>
    .footer {
        position: fixed; 
        left: 0; 
        bottom: -17px; 
        width: 100%; 
        background-color: #b1b1b5; 
        color: black; 
        text-align: center;
        padding: 10px 0;
    }
    </style>
    <div class="footer">
        <p>© 2025 Draup Dataflow Engine | Built with open-source technologies | 
        <a href='pages/About.py' style='color: #333; text-decoration: none;'>View Attributions</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)
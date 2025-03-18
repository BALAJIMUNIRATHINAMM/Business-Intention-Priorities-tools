import streamlit as st
import os
print(os.listdir("/"))

# Set page configuration
st.set_page_config(
    page_title="Business Intention Priority Extraction Tools",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Business Intention Priority Extraction Tools is a data request application that streamlines data requests, enhances collaboration among stakeholders, and improves operational efficiency."
    }
)

# Header with styling
st.header('🍳Business Intention Priorities Tools',divider='rainbow')

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

# Footer
st.markdown(
    """
    <hr>
    <p style="text-align: center; color: #555;">Created by Balaji M</p>
    """,
    unsafe_allow_html=True
)

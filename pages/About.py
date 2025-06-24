import streamlit as st

st.set_page_config(
    page_title="About - Business Intention Priority Extraction Tools",
    page_icon="🍳",
    layout="wide"
)

st.title("🍳 About Business Intention Priority Extraction Tools")

# Application Information
st.header("Application Overview")
st.info("""
Business Intention Priority Extraction Tools is a comprehensive data processing application 
that streamlines data requests, enhances collaboration among stakeholders, and improves 
operational efficiency through automated priority extraction from business documents.
""")

# Features Section
st.header("Key Features")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Signal BF Priority Extraction")
    st.write("Extract priority signals from business function reports with advanced data processing capabilities.")
    
    st.subheader("🏢 Company BF Priority Extraction")
    st.write("Process company-specific business function priorities from structured datasets.")

with col2:
    st.subheader("📊 Aggregated Priority Extraction")
    st.write("Combine and analyze aggregated priorities across multiple data sources.")
    
    st.subheader("🔄 Consolidated Processing")
    st.write("Advanced consolidated priority extraction with comprehensive data analysis.")

# Technical Stack
st.header("Technical Stack")
st.write("This application is built using modern, open-source technologies:")

tech_stack = {
    "Frontend Framework": "Streamlit - Apache License 2.0",
    "Data Processing": "Pandas - BSD 3-Clause License", 
    "Excel Processing": "OpenPyXL (MIT) & XlsxWriter (BSD 2-Clause)",
    "Programming Language": "Python - PSF License",
    "Data Formats": "CSV, Excel, JSON support"
}

for tech, license_info in tech_stack.items():
    st.write(f"**{tech}**: {license_info}")

# Open Source Acknowledgments
st.header("Open Source Acknowledgments")
st.write("""
This application is built on the foundation of excellent open-source software. 
We acknowledge and thank the contributors to these projects:
""")

acknowledgments = [
    "**Streamlit Team** - For creating an exceptional framework for data applications",
    "**Pandas Development Team** - For the powerful data manipulation library",
    "**OpenPyXL Contributors** - For Excel file processing capabilities", 
    "**XlsxWriter Author (John McNamara)** - For Excel creation and formatting tools",
    "**Python Software Foundation** - For the Python programming language"
]

for ack in acknowledgments:
    st.write(f"• {ack}")

# Licensing Information
st.header("Licensing & Compliance")
st.write("""
This application complies with all applicable open-source licenses. 
For detailed attribution information, please see our [ATTRIBUTIONS.md](https://github.com/your-repo/attributions) file.
""")

# Contact Information
st.header("Contact & Support")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Development Team")
    st.write("© 2025 Draup Dataflow Engine")
    st.write("Built with ❤️ using open-source technologies")

with col2:
    st.subheader("License Inquiries")
    st.write("For questions regarding licensing or attributions:")
    st.write("📧 Contact: [your-email@company.com]")

# Version Information
st.header("Version Information")
st.write("**Current Version**: 1.0.0")
st.write("**Last Updated**: January 2025")
st.write("**License Compliance**: All dependencies properly attributed")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>This application respects and complies with all open-source licenses.</p>
        <p>Thank you to the open-source community for making this possible.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
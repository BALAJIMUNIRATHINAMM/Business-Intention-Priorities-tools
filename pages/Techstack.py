import streamlit as st
import pandas as pd
from worksheet.draup import DashboardFormatter  # Ensure this module is correctly implemented
from io import BytesIO

# Set the page configuration
st.set_page_config(
    page_title="Techstack",
    #page_icon="./Asset/bd.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': 'Techstack Tools'
    }
)

# Title Logo
#st.image('./Asset/bd.png', width=100)

# Add a header with a divider
st.header('Braindesk Data Project Optimization Pullouts', divider='rainbow')

# Step 3: UI/UX Design with Centered Layout for File Uploads
# Title and description
st.markdown("<center><h2 class='header'>Digital Product Mapping and Formatting Tool</h2></center>", unsafe_allow_html=True)
st.write("Upload the required files to map digital products to their makers and download a formatted output.")

# 2x2 column pattern for file uploads in the center
col1, col2 = st.columns(2)
# Upload files
with col1:
    stack_file = st.file_uploader("Upload Company Tech Stack Mapping Schema (Excel file)", type=["xlsx", "csv"])
with col2:
    maker_file = st.file_uploader("Upload Digital Applications and Platform Schema (CSV file)", type=["csv"])

@st.cache_data
def load_and_process_files(stack_file, maker_file):
    """Load the input files and process the mapping."""
    # Load files
    stack = pd.read_excel(stack_file) if stack_file.name.endswith('.xlsx') else pd.read_csv(stack_file)
    maker = pd.read_csv(maker_file)
    
    # Group and map 'Maker' by 'Digital Products'
    product_maker = maker.groupby('Digital Product')['Maker'].first()
    stack['product_maker'] = stack['digital_product'].map(product_maker).fillna('-')
    
    # Prepare the final output
    output = stack[['S.No.', 'Company', 'digital_product', 'product_maker', 'Digital Area', 'G2 Sub Sub Category','Max Date Posted','Min Date Posted','Confidence Score','Usage Index','MSA','Country']].fillna('-')
    return output

# Process the data if both files are uploaded
if stack_file and maker_file:
    output_data = load_and_process_files(stack_file, maker_file)
    
    # Display the processed data
    st.write("Mapped Data Preview:")
    st.dataframe(output_data)
    
    # Custom title input
    custom_title = st.text_input("Enter Custom Title for Formatted File", "Requested Accounts")
    
    # Formatter file upload
    formatter_file = st.file_uploader("Upload Formatter File (if required)", type=["xlsx"])
    
    # Convert DataFrame to CSV for download
    @st.cache_data
    def convert_csv(df):
        return df.to_csv(index=False)

    # Convert DataFrame to Excel
    def convert_excel(df):
        # Create a BytesIO buffer
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        return output.getvalue()

    # Convert both formats
    csv = convert_csv(output_data)
    excel = convert_excel(output_data)

    # Layout for download buttons with professional icons and hover effects
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download CSV 📄", 
            data=csv, 
            file_name="output.csv", 
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="Download Excel 📊", 
            data=excel, 
            file_name="output.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    # File download section
    st.subheader("📥 Download Formatted File")
    if formatter_file:
        formatter = DashboardFormatter(formatter_file, title=custom_title)
        
        # Generate formatted output
        output_name = "techstack_formatted_initiatives.xlsx"
        formatter.format_techstack(output_data)
        formatter.save(output_name)
        
        # Provide download button
        with open(output_name, "rb") as file:
            st.download_button(
                label="Download Formatted File 💾",
                data=file,
                file_name=output_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ Please upload the Formatter file to proceed with formatted download.")
else:
    st.warning("⚠️ Please upload both the required files to process the data.")

# Footer bar
footer="""<style>
.footer {position: fixed; left: 0; bottom: -17px; width: 100%; background-color: #b1b1b5; color: black; text-align: center; }</style>
<div class="footer"><p>© 2025 BDDRDP | Powered by Draup | All Rights Reserved</p></div>
"""
st.markdown(footer, unsafe_allow_html=True)

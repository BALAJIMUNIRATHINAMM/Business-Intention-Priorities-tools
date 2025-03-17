import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io

# Function to extract priorities
@st.cache_data
def extract_priorities(df):
    extracted_data = []
    
    required_columns = ['Company', 'Year', 'Report Name', 'Quarter', 'Report Type', 'Refreshed Date', 'Formatted Priorities']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ Missing columns in the uploaded file: {', '.join(missing_columns)}")
        return pd.DataFrame()
    
    for _, row in df.iterrows():
        company = row.get('Company', 'Unknown')
        year = row.get('Year', 'N/A')
        report_name = row.get('Report Name', 'N/A')
        quarter = row.get('Quarter', 'N/A')
        report_type = row.get('Report Type', 'N/A')
        refreshed_date = row.get('Refreshed Date', 'N/A')
        
        try:
            priorities = json.loads(str(row.get('Formatted Priorities', '{}')))
        except json.JSONDecodeError:
            st.warning(f"⚠️ Invalid JSON format for Company: {company}")
            continue
        
        for category, priority_list in priorities.items():
            for priority_item in priority_list:
                extracted_data.append({
                    'Company': company,
                    'Year': year,
                    'Report Name': report_name,
                    'Quarter': quarter,
                    'Report Type': report_type,
                    'Refreshed Date': refreshed_date,
                    'Priority': priority_item.get('priority', 'N/A'),
                    'Description': priority_item.get('description', 'N/A')
                })
    
    return pd.DataFrame(extracted_data)

# Streamlit App UI
st.set_page_config(page_title="Company BF Priority Extraction Tool", page_icon="🍳", layout="wide")
st.title("🍳 Company BF Priority Extraction Tool")   
st.info("This tool helps extract and download priority company business function from structured datasets. Upload a CSV or Excel file, process the data, and download the extracted priorities in a user-friendly format.")

# Session state for storing extracted data
if 'extracted_df' not in st.session_state:
    st.session_state['extracted_df'] = pd.DataFrame()

# File Upload
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    
    try:
        df = pd.read_csv(uploaded_file) if file_extension == "csv" else pd.read_excel(uploaded_file)
        st.success("✅ File Uploaded Successfully!")
        
        # Process and Extract Data
        extracted_df = extract_priorities(df)
        
        if not extracted_df.empty:
            extracted_df['Description'] = extracted_df['Description'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
            st.session_state['extracted_df'] = extracted_df
            
            # Display results
            st.subheader("📌 Extracted Priorities Preview")
            st.dataframe(extracted_df, use_container_width=True)
            
            # Generate dynamic filename
            date_str = datetime.today().strftime("%Y_%m_%d_%H_%M")
            output_filename_csv = f"company_extracted_priorities_{date_str}.csv"
            output_filename_excel = f"company_extracted_priorities_{date_str}.xlsx"
            
            # Convert DataFrame to CSV for download
            csv_data = extracted_df.to_csv(index=False).encode('utf-8')
            
            # Convert DataFrame to Excel for download
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
                extracted_df.to_excel(writer, index=False, sheet_name='Extracted Priorities')
            output_excel.seek(0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_data,
                    file_name=output_filename_csv,
                    mime="text/csv"
                )
            with col2:
                st.download_button(
                    label="📥 Download as Excel",
                    data=output_excel,
                    file_name=output_filename_excel,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            st.success("✅ Processed file successfully!")        
        else:
            st.warning("⚠️ No priorities extracted. Please check your file format.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.warning("Please upload a file to begin processing.")
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io

# Function to extract priorities
@st.cache_data
def extract_priorities(df):
    extracted_data = []
    
    required_columns = ['Company', 'Publication Month', 'Months Considered', 'Highlights Month', 'Priority Type', 'Formatted Priorities']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ Missing columns in the uploaded file: {', '.join(missing_columns)}")
        return pd.DataFrame()
    
    for _, row in df.iterrows():
        company = row.get('Company', 'Unknown')
        publication_month = row.get('Publication Month', 'N/A')
        months_considered = row.get('Months Considered', 'N/A')
        highlights_month = row.get('Highlights Month', 'N/A')
        priority_type = row.get('Priority Type', 'N/A')
        
        try:
            priorities = json.loads(str(row.get('Formatted Priorities', '{}')))
        except json.JSONDecodeError:
            st.warning(f"⚠️ Invalid JSON format for Company: {company}")
            continue
        
        for category, priority_list in priorities.items():
            for priority in priority_list:
                extracted_data.append({
                    'Company': company,
                    'Publication Month': publication_month,
                    'Months Considered': months_considered,
                    'Highlights Month': highlights_month,
                    'Priority Type': priority_type,
                    'BF': category,
                    'Priority': priority.get('priority', '-'),
                    'Description': priority.get('description', '-'),
                    'Recent Year Month': priority.get('recent_year_month', '-'),
                })
    
    return pd.DataFrame(extracted_data)

# Streamlit App UI
st.set_page_config(page_title="Signal BF Priority Extraction Tool", page_icon="🍳", layout="wide")
st.title("🍳 Signal BF Priority Extraction Tool")   
st.info("This tool helps extract and download priority signals business function from structured datasets. Upload a CSV or Excel file, process the data, and download the extracted priorities in a user-friendly format.")

# Session state for storing extracted data
if 'extracted_df' not in st.session_state:
    st.session_state['extracted_df'] = pd.DataFrame()

# File Upload
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
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
        output_filename_csv = f"signal_extracted_priorities_{date_str}.csv"
        output_filename_excel = f"signal_extracted_priorities_{date_str}.xlsx"
        
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
else:
    st.warning("Please upload a file to begin processing.")
import streamlit as st
import pandas as pd
import json
from itertools import islice
from datetime import datetime

@st.cache_data
def convert_binary_to_text(input_text):
    """Converts binary or escaped string data into a clean text format."""
    if isinstance(input_text, bytes):
        decoded_string = input_text.decode('utf-8')
        return decoded_string.replace("\\", "").replace("b'", '').replace("b\"", '').strip("\\'\"")
    return input_text

@st.cache_data
def sort_dict(input_dict):
    """Sorts dictionary values in descending order and returns top 3 keys as a string."""
    try:
        if isinstance(input_dict, str):
            input_dict = json.loads(input_dict.replace("'", "\""))  # Convert single to double quotes for valid JSON
        elif not isinstance(input_dict, dict):
            return ""
        
        sorted_values = sorted(input_dict.values(), reverse=True)
        dict_data = {key: input_dict[key] for key in sorted(input_dict, key=input_dict.get, reverse=True)}
        dict_data = dict(islice(dict_data.items(), 3))  # Take top 3 values
        return '; '.join(dict_data.keys())
    except Exception:
        return ""

# Streamlit App UI
st.set_page_config(page_title="Aggregated Priority Extraction Tool", page_icon="🍳", layout="wide")
st.title("\U0001F373 Aggregated Priority Extraction Tool")  
st.info("This tool helps extract and download Aggregated Priority from structured datasets. Upload a CSV or Excel file, process the data, and download the extracted priorities in a user-friendly format.")

uploaded_file = st.file_uploader("📂Upload Aggregated Priority Reports Mapping Schema", type=["csv", "xlsx"])
master_file = st.file_uploader("📂Upload Master Company Schema (Optional)", type=["csv", "xlsx"])

@st.cache_data
def read_file(file):
    """Reads the uploaded file and returns a pandas DataFrame."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    return None

if uploaded_file is not None:
    try:
        df = read_file(uploaded_file)
        
        required_columns = ['Priority Description', 'Usecase', 'Functional Workload', 'Company']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns in uploaded file: {', '.join(missing_columns)}")
        else:
            df['Description'] = df['Priority Description'].apply(lambda x: convert_binary_to_text(x.encode('utf-8') if isinstance(x, str) else x))
            df['Usecases'] = df['Usecase'].apply(sort_dict)
            df['Workload'] = df['Functional Workload'].apply(sort_dict)
            
            df_output = df[['S.No.', 'Company', 'Business Function', 'Priority Name', 'Description', 'Usecases', 'Workload',
                            'Recent Year Month', 'Recent Year Quarter', 'Months Considered', 'Quarter Considered', 'Primary Vertical']]
            
            if master_file is not None:
                cmp = read_file(master_file)
                if 'Company Name' in cmp.columns:
                    cmp.rename(columns={'Company Name': 'Company'}, inplace=True)
                    df_output = df_output.merge(cmp[['Company', 'Draup Verticals']], on='Company', how='left')
            
            st.subheader("📌Processed Data Preview:")
            st.dataframe(df_output, use_container_width=True)
            
            # Generate dynamic filename
            date_str = datetime.today().strftime("%Y_%m_%d_%H_%M")
            output_filename_csv = f"aggregated_extracted_priorities_{date_str}.csv"
            output_filename_excel = f"aggregated_extracted_priorities_{date_str}.xlsx"
            
            csv_data = df_output.to_csv(index=False).encode('utf-8')
            excel_writer = pd.ExcelWriter(output_filename_excel, engine='xlsxwriter')
            df_output.to_excel(excel_writer, index=False, sheet_name='Processed Data')
            excel_writer.close()
            output_excel = open(output_filename_excel, "rb").read()
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="\U0001F4E5 Download as CSV",
                    data=csv_data,
                    file_name=output_filename_csv,
                    mime="text/csv"
                )
            with col2:
                st.download_button(
                    label="\U0001F4E5 Download as Excel",
                    data=output_excel,
                    file_name=output_filename_excel,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        st.success("✅ Processed file successfully!")
            
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to begin processing.")


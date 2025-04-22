import streamlit as st
import pandas as pd
import json
import ast
from datetime import datetime
import io

# Streamlit App Configuration
st.set_page_config(page_title="BF Consolidated Priority Extraction Tool", page_icon="🍳", layout="wide")
st.title("🍳 BF Consolidated Priority Extraction Tool")   
st.info("This tool extracts and downloads company business function priorities from structured datasets. Upload a CSV or Excel file, process the data, and download the extracted priorities.")

# Function to extract priorities
@st.cache_data
def extract_priorities(df):
    extracted_data = []
    required_columns = ['Company Name', 'Consolidated AI Response']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"❌ Missing columns in the uploaded file: {', '.join(missing_columns)}")
        return pd.DataFrame()

    for _, row in df.iterrows():
        company = row.get('Company Name', 'Unknown')
        content = row.get('Consolidated AI Response', '{}')

        try:
            if pd.isna(content) or content in ["", "nan", "None"]:
                raise ValueError("Empty or invalid JSON field")

            content_str = str(content)
            try:
                priorities = json.loads(content_str)
            except json.JSONDecodeError:
                priorities = ast.literal_eval(content_str)

        except Exception:
            st.warning(f"⚠️ Invalid JSON format for Company: {company}")
            continue

        for category, priority_list in priorities.items():
            for priority_item in priority_list:
                extracted_data.append({
                    'Company': company,
                    'BF': category,
                    'Priority': priority_item.get('priority', '-'),
                    'Description': priority_item.get('description', '-'),
                    'source': priority_item.get('source', '-'),
                    'recent_year_month': priority_item.get('recent_year_month', '-'),
                    'recent_year_quarter': priority_item.get('recent_year_quarter', '-'),
                    'Upload_Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

    return pd.DataFrame(extracted_data)

# Session state for extracted data
if 'extracted_df' not in st.session_state:
    st.session_state['extracted_df'] = pd.DataFrame()

# File Upload
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=['csv', 'xlsx'])

# Expander for guidance
with st.expander("💡 Sample Format & Troubleshooting Tips"):
    st.markdown("""
    ✅ Ensure your file has the following columns:
    - `Company Name`
    - `Consolidated AI Response` (JSON format with keys like `priority`, `description`, `source`, etc.)

    ⚠️ Make sure JSON fields are not empty or incorrectly formatted.
    """)

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    try:
        df = pd.read_csv(uploaded_file) if file_extension == "csv" else pd.read_excel(uploaded_file)
        st.success("✅ File Uploaded Successfully!")

        extracted_df = extract_priorities(df)

        if not extracted_df.empty:
            extracted_df['Description'] = extracted_df['Description'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
            st.session_state['extracted_df'] = extracted_df

            # Filter and Search Section
            st.subheader("🔍 Search & Display Options")
            search_term = st.text_input("Search by Company, Priority, or Description")
            display_df = extracted_df.copy()

            if search_term:
                display_df = display_df[display_df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]

            selected_columns = st.multiselect("🧾 Select columns to display & download", display_df.columns.tolist(), default=display_df.columns.tolist())
            final_display_df = display_df[selected_columns]

            # Display DataFrame
            st.subheader("📌 Extracted Priorities Preview")
            st.dataframe(final_display_df, use_container_width=True)

            # Generate dynamic filenames
            date_str = datetime.today().strftime("%Y_%m_%d_%H_%M")
            output_filename_csv = f"Consolidated_extracted_priorities_{date_str}.csv"
            output_filename_excel = f"Consolidated_extracted_priorities_{date_str}.xlsx"

            # Download buttons
            csv_data = final_display_df.to_csv(index=False).encode('utf-8')
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
                final_display_df.to_excel(writer, index=False, sheet_name='Extracted Priorities')
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

            st.success("✅ Processed and ready for download!")  
        else:
            st.warning("⚠️ No priorities extracted. Please check the file format and data content.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.warning("📂 Please upload a file to begin processing.")

# Footer
st.markdown(
    """
    <style>
    .footer {position: fixed; left: 0; bottom: -17px; width: 100%; background-color: #b1b1b5; color: black; text-align: center;}
    </style>
    <div class="footer"><p>© 2025 Draup Dataflow Engine</p></div>
    """,
    unsafe_allow_html=True
)

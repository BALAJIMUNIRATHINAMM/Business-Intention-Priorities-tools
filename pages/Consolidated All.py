import streamlit as st
import pandas as pd
import json
import ast
from datetime import datetime
import io

# ------------------------ Streamlit Page Config ------------------------
st.set_page_config(page_title="BF Consolidated Priority All Extraction Tool", page_icon="🍳", layout="wide")
st.title("🍳 BF Consolidated All Priority Extraction Tool")
st.info("This tool extracts and downloads company business function priorities from structured datasets. Upload a CSV or Excel file, process the data, and download the extracted priorities.")

# ------------------------ Priority Extraction Function ------------------------
@st.cache_data
def extract_priorities(df):
    extracted_data = []

    required_columns = [
        'Company Name', 'Generated On', 'Is Outdated',
        'Input Output Ratio', 'Transcript AI Response',
        'Signal AI Response', 'Consolidated AI Response'
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    priority_columns = ['Transcript AI Response', 'Signal AI Response', 'Consolidated AI Response']

    for _, row in df.iterrows():
        company = row['Company Name']
        generated = row['Generated On']
        is_outdated = row['Is Outdated']
        input_output_ratio = row['Input Output Ratio']

        for col in priority_columns:
            content = row.get(col, '{}')
            if pd.isna(content) or str(content).strip() in ["", "nan", "None"]:
                continue

            try:
                content_str = str(content)
                try:
                    priorities = json.loads(content_str)
                except json.JSONDecodeError:
                    priorities = ast.literal_eval(content_str)

                if not isinstance(priorities, dict):
                    raise ValueError("Parsed content is not a dictionary")

                for category, priority_list in priorities.items():
                    for priority in priority_list:
                        description = priority.get('description', '-')
                        if isinstance(description, list):
                            description = ' '.join(description)

                        extracted_data.append({
                            'Company': company,
                            'BF': category,
                            'Priority': priority.get('priority', '-'),
                            'Description': description,
                            'source': priority.get('source', '-'),
                            'recent_year_month': priority.get('recent_year_month', '-'),
                            'recent_year_quarter': priority.get('recent_year_quarter', '-'),
                            'AI Column Source': col,
                            'Generated On': generated,
                            'Is Outdated': is_outdated,
                            'Input Output Ratio': input_output_ratio
                        })

            except Exception as e:
                print(f"⚠️ Error processing {col} for {company}: {e}")
                continue

    return pd.DataFrame(extracted_data)

# ------------------------ Session State Initialization ------------------------
if 'extracted_df' not in st.session_state:
    st.session_state['extracted_df'] = pd.DataFrame()

# ------------------------ File Upload Section ------------------------
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=['csv', 'xlsx'])

with st.expander("💡 Sample Format & Troubleshooting Tips"):
    st.markdown("""
    ✅ Ensure your file has the following columns:
    - `Company Name`
    - `Consolidated AI Response` (in valid JSON format with keys like `priority`, `description`, `source`, etc.)

    ⚠️ Avoid empty or invalid JSON formats in AI response columns.
    """)

# ------------------------ File Processing ------------------------
if uploaded_file:
    try:
        ext = uploaded_file.name.split('.')[-1].lower()
        df = pd.read_csv(uploaded_file) if ext == 'csv' else pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        extracted_df = extract_priorities(df)

        if not extracted_df.empty:
            st.session_state['extracted_df'] = extracted_df.copy()

            # ------------------------ Filter/Search Section ------------------------
            st.subheader("🔍 Search & Display Options")
            search_term = st.text_input("Search by Company, Priority, or Description")

            display_df = extracted_df.copy()
            if search_term:
                display_df = display_df[display_df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]

            selected_columns = st.multiselect(
                "🧾 Select columns to display & download",
                options=display_df.columns.tolist(),
                default=display_df.columns.tolist()
            )

            final_display_df = display_df[selected_columns]

            # ------------------------ Display Table ------------------------
            st.subheader("📌 Extracted Priorities Preview")
            st.dataframe(final_display_df, use_container_width=True)

            # ------------------------ Download Section ------------------------
            date_str = datetime.now().strftime("%Y_%m_%d_%H_%M")
            filename_csv = f"Consolidated_extracted_priorities_{date_str}.csv"
            filename_excel = f"Consolidated_extracted_priorities_{date_str}.xlsx"

            csv_data = final_display_df.to_csv(index=False).encode('utf-8')
            excel_io = io.BytesIO()
            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                final_display_df.to_excel(writer, sheet_name='Extracted Priorities', index=False)
            excel_io.seek(0)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 Download as CSV", data=csv_data, file_name=filename_csv, mime="text/csv")
            with col2:
                st.download_button("📥 Download as Excel", data=excel_io, file_name=filename_excel,
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            st.success("✅ Processed and ready for download!")

        else:
            st.warning("⚠️ No priorities were extracted. Please check the input data format.")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.warning("📂 Please upload a file to begin processing.")

# ------------------------ Footer ------------------------
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: -17px;
    width: 100%;
    background-color: #b1b1b5;
    color: black;
    text-align: center;
}
</style>
<div class="footer"><p>© 2025 Draup Dataflow Engine</p></div>
""", unsafe_allow_html=True)

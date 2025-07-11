import streamlit as st
import pandas as pd
import ast
from datetime import datetime
from itertools import islice

# -------------------------- Streamlit Config -------------------------- #
st.set_page_config(page_title="Aggregated Priority Extraction Tool", page_icon="📊", layout="wide")
st.title("📊 Aggregated Priority Extraction Tool")
st.info("Upload a priority mapping file (CSV or Excel) to extract and format top priorities, usecases, and workloads.")

# -------------------------- Utility Functions -------------------------- #

@st.cache_data
def convert_binary_to_text(input_data):
    """Cleans binary or escaped string input."""
    if isinstance(input_data, bytes):
        decoded = input_data.decode("utf-8", errors="ignore")
        return decoded.replace("\\", "").replace("b'", "").replace("b\"", "").strip("\\'\"")
    return input_data

@st.cache_data
def parse_usecases(input_data):
    """Parses dict or list of dicts with 'name' and 'score' from malformed strings (using ast)."""
    try:
        if isinstance(input_data, str):
            cleaned = input_data.strip()
            if cleaned.startswith("//"): cleaned = cleaned[2:]
            if cleaned.endswith("//"): cleaned = cleaned[:-2]
            input_data = ast.literal_eval(cleaned)

        if isinstance(input_data, dict):
            input_data = [{'name': k, 'score': v} for k, v in input_data.items()]

        if isinstance(input_data, list) and all(isinstance(d, dict) and 'name' in d and 'score' in d for d in input_data):
            sorted_items = sorted(input_data, key=lambda x: x['score'], reverse=True)
            return "; ".join(item['name'] for item in islice(sorted_items, 3))
    except Exception:
        pass
    return ""

@st.cache_data
def read_file(uploaded_file):
    """Reads CSV or Excel into DataFrame."""
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    return pd.DataFrame()

def generate_filenames():
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    return (
        f"aggregated_priorities_{timestamp}.csv",
        f"aggregated_priorities_{timestamp}.xlsx"
    )

# -------------------------- File Upload -------------------------- #

uploaded_file = st.file_uploader("📁 Upload Aggregated Priority Mapping File", type=["csv", "xlsx"])
master_file = st.file_uploader("📁 Upload Master Company Schema (Optional)", type=["csv", "xlsx"])

# -------------------------- Processing Logic -------------------------- #

if uploaded_file:
    try:
        df = read_file(uploaded_file)
        required_columns = ['Priority Description', 'Usecase', 'Functional Workload', 'Company']
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"Missing required columns: {', '.join(missing)}")
        else:
            # Step 1: Convert and clean text
            df['Description'] = df['Priority Description'].apply(
                lambda x: convert_binary_to_text(x.encode('utf-8') if isinstance(x, str) else x)
            )
            # Step 2: Parse usecases and workloads
            df['Usecases'] = df['Usecase'].apply(parse_usecases)
            df['Workload'] = df['Functional Workload'].apply(parse_usecases)

            # Step 3: Define final columns
            output_cols = [
                'S.No.', 'Company', 'Business Function', 'Priority Name', 'Description',
                'Usecases', 'Workload', 'Recent Year Month', 'Recent Year Quarter',
                'Months Considered', 'Quarter Considered', 'Primary Vertical'
            ]
            for col in output_cols:
                if col not in df.columns:
                    df[col] = '-'

            df_output = df[output_cols].fillna('-')

            # Step 4: Merge master company schema if provided
            if master_file:
                master_df = read_file(master_file)
                if 'Company Name' in master_df.columns:
                    master_df = master_df.rename(columns={'Company Name': 'Company'})
                    df_output = df_output.merge(
                        master_df[['Company', 'Draup Verticals']],
                        on='Company',
                        how='left'
                    )

            # Step 5: Show and download output
            st.subheader("📌 Processed Data Preview")
            st.dataframe(df_output, use_container_width=True)

            filename_csv, filename_excel = generate_filenames()
            csv_data = df_output.to_csv(index=False).encode("utf-8")
            df_output.to_excel(filename_excel, index=False, sheet_name="Priorities")

            with open(filename_excel, "rb") as f:
                excel_data = f.read()

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("⬇️ Download CSV", data=csv_data, file_name=filename_csv, mime="text/csv")
            with col2:
                st.download_button("⬇️ Download Excel", data=excel_data, file_name=filename_excel,
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            st.success("✅ File processed and ready!")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.warning("Upload a file to begin processing.")

# -------------------------- Footer -------------------------- #
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    font-size: 14px;
    background-color: #f1f3f5;
    padding: 8px;
    color: #333;
}
</style>
<div class="footer">© 2025 Draup Dataflow Engine</div>
""", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Data Cleaning App",
    page_icon="🧹",
    layout="wide"
)

st.title("🧑🏼‍🔧 Data Cleaning Application 👩🏼‍🔧")

# ===============================
# FILE UPLOAD
# ===============================
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()

        if file_ext == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Store original data only once
        if "data" not in st.session_state:
            st.session_state.data = df.copy()

    except Exception as e:
        st.error("‼️ Error reading file")
        st.stop()

    data = st.session_state.data

    # ===============================
    # DATA OVERVIEW
    # ===============================
    st.subheader("📈 Data Overview")
    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", data.shape[0])
    col2.metric("Columns", data.shape[1])
    col3.metric("Duplicate Rows", data.duplicated().sum())

    st.write("### Missing Values per Column")
    st.dataframe(data.isnull().sum())

    st.write("### Preview of Data")
    st.dataframe(data.head())

    # ===============================
    # CLEANING ACTIONS
    # ===============================
    st.subheader("🛠 Data Cleaning Actions")

    col1, col2, col3 = st.columns(3)

    # A) REMOVE MISSING VALUES
    with col1:
        if st.button("⛓️‍💥 Remove Missing Values"):
            st.session_state.data = data.dropna()
            st.success("✅ Missing values removed")

    # B) HANDLE MISSING VALUES
    with col2:
        fill_method = st.selectbox(
            "🔖 Fill Missing Values Using",
            ["Mean (numeric)", "Median (numeric)", "Mode"]
        )

        if st.button("⚙️ Handle Missing Values"):
            df_filled = data.copy()

            if fill_method == "Mean (numeric)":
                for col in df_filled.select_dtypes(include="number"):
                    df_filled[col].fillna(df_filled[col].mean(), inplace=True)

            elif fill_method == "Median (numeric)":
                for col in df_filled.select_dtypes(include="number"):
                    df_filled[col].fillna(df_filled[col].median(), inplace=True)

            else:  # Mode
                for col in df_filled.columns:
                    df_filled[col].fillna(df_filled[col].mode()[0], inplace=True)

            st.session_state.data = df_filled
            st.success("✅ Missing values handled")

    # C) REMOVE DUPLICATES
    with col3:
        if st.button("🔩 Remove Duplicate Records"):
            st.session_state.data = data.drop_duplicates()
            st.success("✅ Duplicate records removed")

    # ===============================
    # UPDATED DATA
    # ===============================
    st.subheader("🚮 Cleaned Data Preview")
    st.dataframe(st.session_state.data.head())

    # ===============================
    # DOWNLOAD CLEANED FILE
    # ===============================
    st.subheader("📥 Download Cleaned File")

    buffer = io.StringIO()
    st.session_state.data.to_csv(buffer, index=False)

    st.download_button(
        label="Download Cleaned CSV",
        data=buffer.getvalue(),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:

    st.info(" Please upload a CSV or Excel file to begin")

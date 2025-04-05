import streamlit as st
import pandas as pd

st.set_page_config(page_title="chethViz - Data Visualization Platform", layout="wide")

# --- Sidebars ---
with st.sidebar:
    st.title("🛠️ Filters")

    st.markdown("### 📂 Upload CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    st.markdown("### 🧩 Display Options")
    show_preview = st.checkbox("🔍 Show Dataset Preview", value=True)
    show_columns = st.checkbox("📑 Show Column Information", value=False)
    show_stats = st.checkbox("📊 Show Basic Stats", value=False)

    st.markdown("---")
    st.caption("🚀 Dark theme active by default")


# --- Main Area ---
st.title("📊 chethViz - Data Visualization Platform")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df  # Store for next steps

        if show_preview:
            st.subheader("🔍 Dataset Preview")
            st.dataframe(df.head(), use_container_width=True)

        if show_columns:
            st.subheader("📑 Column Information")
            st.write(df.dtypes)

        if show_stats:
            st.subheader("📊 Basic Stats")
            st.write(df.describe(include='all'))

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
else:
    st.info("👈 Upload a CSV from the sidebar to get started!")
    

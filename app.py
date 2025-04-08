import base64
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pygwalker.api.streamlit import StreamlitRenderer
import tempfile
import requests

st.set_page_config(page_title="chethViz - Data Visualization Platform", page_icon='assets/logo.png', layout="wide")

# Font style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code&display=swap');
    html, body, [class*="css"] {
        font-family: 'Fira Code';
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        margin-top: -50px;
        margin-bottom: 20px;
     
    }
    .tagline {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        margin-top: -10px;
        margin-bottom: 10px;
        font-family: 'Fira Code';
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        color: white;
        text-align: right;
        padding: 5px;
        font-size: 14px;
        font-weight: bold;
        font-family: 'Fira Code';
    }
    .footer a {
        color: white;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="title">chethViz</div>
    <div class="tagline"> Data visualization platform that allows you to easily upload, explore, and visualize your datasets. </div>
    <div class="footer"><a href="https://www.linkedin.com/in/chethanpatelpn" target="_blank"> Developed by Chethan Patel  </a></div>
""", unsafe_allow_html=True)

# Horizontal Menu
key_feature = option_menu(
    None, ["Home", "Try Iris dataset", "Try Titanic dataset"],
    icons=['house', 'bar-chart', 'bar-chart'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#0b0b0c"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {"font-family": 'Fira Code',"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#0b0b0c"},
        "nav-link-selected": {"background-color": "#3399ff"}
    }
)

# Customize Sidebar
with st.sidebar:
    st.title("🛠️ Customize")
    st.markdown("### 📂 Load Data")

    data_source = st.radio("Select Data Source:", ["Upload CSV", "From URL"])

    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file , on_bad_lines='skip', encoding_errors='ignore')
            st.session_state["df"] = df
            st.toast("File uploaded successfully!")
    else:
        url_input = st.text_input("Enter CSV URL:")
        submit = st.button("📥 Load from URL")
        if submit and url_input:
            try:
                df = pd.read_csv(url_input, on_bad_lines='skip', encoding_errors='ignore')
                st.session_state["df"] = df
                st.toast("CSV loaded successfully from URL!", icon='😍')
            except Exception as e:
                st.error(f"Failed to load CSV from URL: {e}")

    st.markdown("---")
    st.caption("🚀 Dark theme active by default")

# Home Page with GIF
if key_feature == "Home" and "df" not in st.session_state:
    @st.cache_data
    def get_gif_base64(gif_path):
        with open(gif_path, "rb") as gif_file:
            gif_bytes = gif_file.read()
            encoded_gif = base64.b64encode(gif_bytes).decode("utf-8")
        return encoded_gif

    gif_path = "assets/banner_cheth.gif"
    encoded_gif = get_gif_base64(gif_path)

    html_code = f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
        <img src="data:image/gif;base64,{encoded_gif}" 
            style="max-width: 1800px; height: 150%; border-radius: 20px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);" />
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

if key_feature == "Try Iris dataset":
    
    iris_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        response = requests.get(iris_url)
        tmp_file.write(response.content)
        tmp_file_path = tmp_file.name

    # Read the CSV into a DataFrame
    df = pd.read_csv(tmp_file_path)
    st.session_state["df"] = df
    st.toast("Iris dataset loaded successfully!", icon='🌸')


if key_feature == "Try Titanic dataset":
    
    # Convert Google Drive shareable link to direct download link
    file_id = "1shQR97rldKWEH5SyJlLlqCmvNlOoL_7Z"
    download_url = f"https://drive.google.com/uc?id={file_id}&export=download"

    # Create a temporary file and download the dataset into it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        response = requests.get(download_url)
        tmp_file.write(response.content)
        tmp_file_path = tmp_file.name

    # Load CSV into DataFrame
    df = pd.read_csv(tmp_file_path, on_bad_lines='skip', encoding_errors='ignore')
    st.session_state["df"] = df
    st.toast("Titanic dataset loaded successfully!", icon='😍')


@st.cache_resource
def get_pyg_renderer(dataframe) -> "StreamlitRenderer":
    return StreamlitRenderer(dataframe, spec_io_mode="rw", appearance='dark', kernel_computation=True)

df = st.session_state.get("df", None)
if df is not None:
    try:
        renderer = get_pyg_renderer(df)
        renderer.explorer()
    except Exception as e:
        st.error(f"❌ Error loading renderer: {e}")

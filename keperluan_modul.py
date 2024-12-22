import streamlit as st
import time
import pemanis
import pandas as pd
from datetime import datetime
from PIL import Image
import os
from streamlit_option_menu import option_menu
import base64
import altair as alt
import matriks

def gambar(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def bg():
    img1 = gambar("Documents/image/bg.png")    

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
    background-image: url(data:image/jpeg;base64,{img1});
    background-size: cover;
    width:100%;
    background-position: center;
    }}    

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
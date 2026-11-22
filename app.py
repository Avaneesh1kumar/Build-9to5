import os
import re
import streamlit as st
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="KisanMandi & Krishi Mitra",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<style>
    /* Upar wala black header bar aur Deploy button hide karein */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu {
        display: none !important;
    }

    /* Left Sidebar aur uska arrow button poori tarah hide karein */
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    /* Upar se extra khali jagah kam karein */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Light Sky Blue Main Background */
    .stApp {
        background: linear-gradient(180deg, #D6F0FF 0%, #EAF7FF 50%, #F5FBFF 100%);
        color: #0B2545;
    }

    /* Readable Dark Text for Headings & Labels */
    h1, h2, h3, p, label, .stMarkdown {
        color: #0B2545 !important;
    }

    /* Clean White Input Boxes */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0B2545 !important;
        border: 2px solid #64B5F6 !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
    }

    /* Green Farmer-Friendly Action Button */
    .stButton > button {
        background-color: #1B7F3A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        background-color: #14632D !important;
    }

    /* Top Metric Cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1.5px solid #90CAF9;
        border-top: 5px solid #0288D1;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(2, 136, 209, 0.08);
    }
    [data-testid="stMetricLabel"] {
        color: #37474F !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0B2545 !important;
        font-weight: 800 !important;
    }

    /* Data Cards */
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #B3E5FC;
        border-left: 6px solid #1B7F3A;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
    }
    .card-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #0D47A1;
        margin-bottom: 6px;
    }
    .card-body {
        font-size: 0.96rem;
        color: #1E293B;
        line-height: 1.55;
    }
    .card-meta {
        font-size: 0.84rem;
        font-weight: 600;
        color: #2E7D32;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

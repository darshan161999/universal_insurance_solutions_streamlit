import streamlit as st
import pandas as pd
from datetime import datetime
import re
import gspread
from google.oauth2.service_account import Credentials
import json

# Page configuration
st.set_page_config(
    page_title="Universal Insurance Solutions - Free Coverage Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force light theme in page config
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    /* Additional theme overrides for Streamlit Cloud */
    .stApp {
        background: #FFFFFF !important;
    }
    
    /* Override any dark theme that might be applied by Streamlit Cloud */
    [data-testid="stAppViewContainer"] {
        background: #FFFFFF !important;
    }
    
    /* Ensure all text is dark on light background */
    .stApp * {
        color: #1F2937 !important;
    }
    
    /* Override specific Streamlit components */
    .stApp .stMarkdown {
        color: #1F2937 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Modern Professional CSS with Responsive Design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Montserrat:wght@400;500;600;700&display=swap');
    
    /* Force Light Theme - Override Streamlit's default dark theme */
    .stApp {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }
    
    .stApp > header {
        background-color: #FFFFFF !important;
    }
    
    .stApp > div {
        background-color: #FFFFFF !important;
    }
    
    /* Override Streamlit's dark theme variables */
    :root {
        --primary-color: #3B82F6 !important;
        --background-color: #FFFFFF !important;
        --secondary-background-color: #F8FAFC !important;
        --text-color: #1F2937 !important;
        --font: 'Montserrat', sans-serif !important;
    }
    
    /* Force light theme on all Streamlit components */
    .stApp > div > div > div > div {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }
    
    /* Global Styles */
    * {
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        padding: 0;
        max-width: 1400px;
        margin: 0 auto;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 50%, #E2E8F0 100%);
        min-height: 100vh;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23CBD5E1' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }
    
    /* Modern Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%);
        color: white;
        border: none;
        padding: 14px 28px;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(29, 78, 216, 0.15), 0 2px 4px -1px rgba(29, 78, 216, 0.1);
        width: 100%;
        letter-spacing: 0.025em;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(29, 78, 216, 0.2), 0 10px 10px -5px rgba(29, 78, 216, 0.1);
        background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #60A5FA 100%);
        padding: 30px 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px -10px rgba(30, 58, 138, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
        border: none;
        backdrop-filter: blur(10px);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 40%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.1;
    }
    
    .hero-title {
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: clamp(24px, 4vw, 32px);
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .hero-subtitle {
        color: #E2E8F0;
        font-family: 'Poppins', sans-serif;
        font-size: clamp(14px, 2vw, 18px);
        margin-top: 8px;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .hero-badges {
        display: flex;
        gap: 6px;
        margin-top: 12px;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
        justify-content: center;
    }
    
    .badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 10px;
        border-radius: 16px;
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .badge:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }
    
    .hero-benefits {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 20px;
        justify-content: center;
    }
    
    .hero-benefit-item {
        background: rgba(255, 255, 255, 0.9);
        padding: 10px 16px;
        border-radius: 20px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        min-width: 140px;
        text-align: center;
    }
    
    .hero-benefit-item:hover {
        background: rgba(255, 255, 255, 1);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .hero-benefit-item strong {
        color: #1E3A8A;
        font-family: 'Poppins', sans-serif;
        font-size: 13px;
        font-weight: 600;
        display: block;
        margin-bottom: 4px;
    }
    
    .hero-benefit-item span {
        color: #6B7280;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 500;
        display: block;
    }
    
    /* Card Styling */
    .expertise-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .expertise-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        transition: width 0.3s ease;
    }
    
    .expertise-card:hover {
        transform: translateX(6px) translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(29, 78, 216, 0.15), 0 10px 10px -5px rgba(29, 78, 216, 0.1);
        border-color: #3B82F6;
        background: rgba(255, 255, 255, 0.95);
    }
    
    .expertise-card:hover::before {
        width: 5px;
    }
    
    .expertise-title {
        color: #1F2937;
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        font-weight: 600;
        margin: 0 0 4px 0;
        display: flex;
        align-items: center;
        gap: 8px;
        line-height: 1.3;
        letter-spacing: 0.025em;
        position: relative;
        z-index: 1;
    }
    
    .expertise-description {
        color: #4B5563;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        margin: 0;
        line-height: 1.4;
        font-weight: 500;
        letter-spacing: 0.01em;
        position: relative;
        z-index: 1;
    }
    
    /* Form Section */
    .form-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        position: relative;
        z-index: 1;
    }
    
    .form-header {
        color: #1F2937;
        font-family: 'Poppins', sans-serif;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .form-subheader {
        color: #4B5563;
        font-family: 'Montserrat', sans-serif;
        font-size: 15px;
        margin-bottom: 16px;
        font-weight: 400;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 2px solid #E5E7EB !important;
        padding: 16px 20px !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: rgba(255, 255, 255, 0.9) !important;
        color: #1F2937 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        outline: none !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Dropdown Arrow Styling - Hide custom arrow and style default */
    .stSelectbox>div>div>div::after {
        display: none !important;
    }
    
    /* Style the default Streamlit dropdown arrow */
    .stSelectbox>div>div>div[role="combobox"]::after,
    .stSelectbox>div>div>div[role="combobox"]:after,
    .stSelectbox>div>div>div::after {
        color: #374151 !important;
        font-size: 12px !important;
    }
    
    .stSelectbox>div>div>div[role="combobox"]:hover::after,
    .stSelectbox>div>div>div:hover::after {
        color: #1F2937 !important;
    }
    
    .stSelectbox>div>div>div[role="combobox"]:focus::after,
    .stSelectbox>div>div>div:focus::after {
        color: #3B82F6 !important;
    }
    
    /* Target the specific Streamlit dropdown arrow element */
    .stSelectbox div[data-baseweb="select"] div[role="combobox"]::after,
    .stSelectbox div[data-baseweb="select"] div[role="combobox"]:after {
        color: #374151 !important;
        font-size: 12px !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div[role="combobox"]:hover::after {
        color: #1F2937 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div[role="combobox"]:focus::after {
        color: #3B82F6 !important;
    }
    
    /* Target SVG arrows specifically */
    .stSelectbox svg {
        color: #1F2937 !important;
        fill: #1F2937 !important;
        stroke: #1F2937 !important;
    }
    
    .stSelectbox svg:hover {
        color: #111827 !important;
        fill: #111827 !important;
        stroke: #111827 !important;
    }
    
    .stSelectbox svg:focus {
        color: #3B82F6 !important;
        fill: #3B82F6 !important;
        stroke: #3B82F6 !important;
    }
    
    /* Target all possible arrow elements */
    .stSelectbox [data-baseweb="select"] svg,
    .stSelectbox [role="combobox"] svg,
    .stSelectbox div[role="combobox"] svg {
        color: #1F2937 !important;
        fill: #1F2937 !important;
        stroke: #1F2937 !important;
    }
    
    .stTextInput>div>div>input:hover,
    .stSelectbox>div>div>div:hover,
    .stTextArea>div>div>textarea:hover {
        border-color: #9CA3AF !important;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>div:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        background: rgba(255, 255, 255, 1) !important;
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif !important;
        transform: translateY(-2px) !important;
    }
    
    /* Dropdown Options Styling */
    .stSelectbox>div>div>div[role="combobox"] {
        cursor: pointer !important;
    }
    
    .stSelectbox>div>div>div[role="combobox"]:hover {
        border-color: #9CA3AF !important;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Dropdown Menu Styling */
    .stSelectbox>div>div>div[role="listbox"] {
        background: white !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        z-index: 1000 !important;
    }
    
    .stSelectbox>div>div>div[role="option"] {
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
        background: white !important;
    }
    
    .stSelectbox>div>div>div[role="option"]:hover {
        background: #F3F4F6 !important;
        color: #1F2937 !important;
    }
    
    .stSelectbox>div>div>div[role="option"][aria-selected="true"] {
        background: #3B82F6 !important;
        color: white !important;
    }
    
    /* Labels */
    .stTextInput>label,
    .stSelectbox>label,
    .stTextArea>label {
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.025em !important;
    }
    
    /* Why Choose Us Section */
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
        margin-top: 8px;
    }
    
    .benefit-item {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        padding: 6px;
        border-radius: 6px;
        border-left: 2px solid #3B82F6;
        transition: all 0.3s;
    }
    
    .benefit-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Success Message */
    .success-animation {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 600;
        box-shadow: 0 25px 50px -12px rgba(16, 185, 129, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
        animation: slideInBounce 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    
    .success-animation::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes slideInBounce {
        0% {
            transform: translateY(-30px) scale(0.8);
            opacity: 0;
        }
        50% {
            transform: translateY(10px) scale(1.05);
            opacity: 0.8;
        }
        100% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
    }
    
    @keyframes shimmer {
        0% {
            left: -100%;
        }
        100% {
            left: 100%;
        }
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        padding: 20px;
        border-radius: 16px;
        margin-top: 20px;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
    
    .footer-title {
        color: #1F2937;
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .footer-contact {
        color: #4B5563;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        margin-bottom: 6px;
        font-weight: 400;
    }
    
    .footer-link {
        color: #3B82F6;
        font-weight: 600;
        text-decoration: none;
    }
    
    /* Mobile Responsive Design */
    @media (max-width: 768px) {
        /* Main container adjustments */
        .main {
            padding: 0 10px !important;
            margin: 0 !important;
        }
        
        /* Hero section mobile optimization */
        .hero-section {
            padding: 20px 15px !important;
            margin: 10px 0 !important;
            border-radius: 12px !important;
        }
        
        .hero-title {
            font-size: clamp(24px, 6vw, 32px) !important;
            line-height: 1.2 !important;
            margin-bottom: 8px !important;
        }
        
        .hero-subtitle {
            font-size: clamp(14px, 4vw, 18px) !important;
            line-height: 1.3 !important;
            margin-bottom: 15px !important;
        }
        
        .hero-badges {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 6px !important;
            justify-content: center !important;
            margin-top: 15px !important;
        }
        
        .badge {
            padding: 6px 12px !important;
            font-size: 11px !important;
            border-radius: 20px !important;
            white-space: nowrap !important;
        }
        
        /* Column layout for mobile */
        div[data-testid="column"] {
            padding: 0 5px !important;
            margin-bottom: 15px !important;
        }
        
        /* Expertise section mobile */
        .expertise-container {
            margin-bottom: 20px !important;
        }
        
        .expertise-card {
            padding: 12px !important;
            margin-bottom: 8px !important;
            border-radius: 8px !important;
        }
        
        .expertise-title {
            font-size: 14px !important;
            margin-bottom: 6px !important;
        }
        
        .expertise-description {
            font-size: 12px !important;
            line-height: 1.4 !important;
        }
        
        /* Form container mobile */
        .form-container {
            padding: 20px 15px !important;
            margin: 10px 0 !important;
            border-radius: 12px !important;
        }
        
        .form-header {
            font-size: 20px !important;
            margin-bottom: 8px !important;
        }
        
        .form-subheader {
            font-size: 14px !important;
            margin-bottom: 20px !important;
        }
        
        /* Input fields mobile */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div,
        .stTextArea>div>div>textarea {
            padding: 14px 16px !important;
            font-size: 16px !important;
            border-radius: 8px !important;
        }
        
        .stTextInput>label,
        .stSelectbox>label,
        .stTextArea>label {
            font-size: 14px !important;
            margin-bottom: 6px !important;
        }
        
        /* Button mobile */
        .stButton>button {
            font-size: 16px !important;
            padding: 14px 24px !important;
            width: 100% !important;
            border-radius: 8px !important;
        }
        
        /* Benefits grid mobile */
        .benefits-grid {
            grid-template-columns: 1fr !important;
            gap: 8px !important;
            margin-top: 15px !important;
        }
        
        .benefit-item {
            padding: 12px !important;
            border-radius: 8px !important;
        }
        
        /* Contact information mobile */
        .contact-info {
            margin-top: 20px !important;
            padding: 15px !important;
            border-radius: 10px !important;
        }
        
        /* Success animation mobile */
        .success-animation {
            padding: 20px !important;
            font-size: 16px !important;
            border-radius: 12px !important;
        }
        
        /* Hide Streamlit sidebar on mobile */
        .stApp > div[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Force single column layout */
        .stApp > div[data-testid="stAppViewContainer"] > div {
            padding: 0 !important;
        }
    }
    
    /* Extra small mobile devices */
    @media (max-width: 480px) {
        .main {
            padding: 0 5px !important;
        }
        
        .hero-section {
            padding: 15px 10px !important;
        }
        
        .hero-title {
            font-size: clamp(20px, 7vw, 28px) !important;
        }
        
        .hero-subtitle {
            font-size: clamp(12px, 4vw, 16px) !important;
        }
        
        .badge {
            padding: 4px 8px !important;
            font-size: 10px !important;
        }
        
        .form-container {
            padding: 15px 10px !important;
        }
        
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div,
        .stTextArea>div>div>textarea {
            padding: 12px 14px !important;
            font-size: 16px !important;
        }
        
        .stButton>button {
            padding: 12px 20px !important;
            font-size: 15px !important;
        }
    }
    
    /* Landscape mobile orientation */
    @media (max-width: 768px) and (orientation: landscape) {
        .hero-section {
            padding: 15px 20px !important;
        }
        
        .hero-badges {
            flex-wrap: wrap !important;
            gap: 4px !important;
        }
        
        .badge {
            padding: 4px 8px !important;
            font-size: 10px !important;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        /* iPad Specific */
        .main {
            padding: 0 15px;
        }
        
        .hero-section {
            padding: 20px 18px;
        }
        
        .hero-title {
            font-size: clamp(22px, 4vw, 30px);
        }
        
        .hero-subtitle {
            font-size: clamp(13px, 2vw, 17px);
        }
        
        .expertise-card {
            padding: 7px;
            margin-bottom: 5px;
        }
        
        .expertise-title {
            font-size: 12px;
        }
        
        .expertise-description {
            font-size: 10px;
        }
        
        .benefits-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Checkbox Styling */
    .stCheckbox {
        margin-top: 12px;
    }
    
    .stCheckbox>label {
        font-size: 14px !important;
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
    }
    
    .stCheckbox>div>div {
        background: white !important;
        border: 2px solid #D1D5DB !important;
        border-radius: 4px !important;
        width: 18px !important;
        height: 18px !important;
    }
    
    .stCheckbox>div>div:hover {
        border-color: #3B82F6 !important;
        background: #F8FAFC !important;
    }
    
    .stCheckbox>div>div[data-checked="true"] {
        background: #3B82F6 !important;
        border-color: #3B82F6 !important;
    }
    
    .stCheckbox>div>div[data-checked="true"]:after {
        color: white !important;
    }
    
    /* Additional checkbox styling for better compatibility */
    .stCheckbox input[type="checkbox"] {
        accent-color: #3B82F6 !important;
    }
    
    .stCheckbox .stCheckbox label {
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        margin-left: 8px !important;
    }
    
    /* Fix for Streamlit checkbox styling */
    .stCheckbox > div > label {
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
    }
    
    /* Error state styling for input fields */
    .stTextInput>div>div>input[data-error="true"],
    .stSelectbox>div>div>div[data-error="true"],
    .stTextArea>div>div>textarea[data-error="true"] {
        border-color: #EF4444 !important;
        background: #FEF2F2 !important;
        color: #DC2626 !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    .stTextInput>div>div>input[data-error="true"]::placeholder,
    .stTextArea>div>div>textarea[data-error="true"]::placeholder {
        color: #F87171 !important;
    }
    
    /* Error labels */
    .stTextInput>label[data-error="true"],
    .stSelectbox>label[data-error="true"],
    .stTextArea>label[data-error="true"] {
        color: #DC2626 !important;
    }
    
    /* Error state for checkboxes */
    .stCheckbox[data-error="true"] > label {
        color: #DC2626 !important;
    }
    
    .stCheckbox[data-error="true"] > div > div {
        border-color: #EF4444 !important;
        background: #FEF2F2 !important;
    }
    
    /* Warning text styling for placeholders */
    .stTextInput>div>div>input::placeholder,
    .stSelectbox>div>div>div::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #6B7280 !important;
    }
    
    /* Red warning text in placeholders */
    .stTextInput>div>div>input[placeholder*="⚠️"]::placeholder,
    .stSelectbox>div>div>div[placeholder*="⚠️"]::placeholder,
    .stTextArea>div>div>textarea[placeholder*="⚠️"]::placeholder {
        color: #EF4444 !important;
        font-weight: 500 !important;
    }
    
    /* Red warning text in selectbox options */
    .stSelectbox>div>div>div[role="option"] {
        color: #1F2937 !important;
    }
    
    .stSelectbox>div>div>div[role="option"]:contains("⚠️") {
        color: #EF4444 !important;
        font-weight: 500 !important;
    }
    
    /* Force red color for warning text in all form elements */
    .stTextInput>div>div>input[placeholder*="⚠️"],
    .stSelectbox>div>div>div[data-value*="⚠️"],
    .stTextArea>div>div>textarea[placeholder*="⚠️"] {
        color: #EF4444 !important;
    }
    
    /* Red warning text in selectbox dropdown */
    .stSelectbox div[role="listbox"] div[role="option"]:first-child {
        color: #EF4444 !important;
        font-weight: 500 !important;
    }
    
    /* Section Headers */
    h3 {
        color: #1F2937 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-top: 16px !important;
        margin-bottom: 8px !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #F9FAFB !important;
        border-radius: 12px !important;
        border: 1px solid #E5E7EB !important;
    }
    
    /* Force light theme on all text elements */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #1F2937 !important;
    }
    
    .stApp p, .stApp span, .stApp div {
        color: #1F2937 !important;
    }
    
    /* Override Streamlit's default text colors */
    .stApp .stMarkdown {
        color: #1F2937 !important;
    }
    
    .stApp .stMarkdown p {
        color: #1F2937 !important;
    }
    
    .stApp .stMarkdown h1, .stApp .stMarkdown h2, .stApp .stMarkdown h3 {
        color: #1F2937 !important;
    }
    
    /* Force light theme on form elements */
    .stApp .stTextInput label, .stApp .stSelectbox label, .stApp .stTextArea label {
        color: #1F2937 !important;
    }
    
    .stApp .stTextInput input, .stApp .stSelectbox select, .stApp .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        border-color: #D1D5DB !important;
    }
    
    /* Fix dropdown selected text color */
    .stSelectbox > div > div > div {
        color: #1F2937 !important;
        background-color: #FFFFFF !important;
    }
    
    .stSelectbox > div > div > div[role="combobox"] {
        color: #1F2937 !important;
        background-color: #FFFFFF !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"] {
        color: #1F2937 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Fix placeholder and selected value text color */
    .stSelectbox input {
        color: #1F2937 !important;
        background-color: #FFFFFF !important;
    }
    
    .stSelectbox input::placeholder {
        color: #6B7280 !important;
    }
    
    .stSelectbox input[value] {
        color: #1F2937 !important;
    }
    
    /* Force text color on all selectbox text elements */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #1F2937 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div > div {
        color: #1F2937 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div > div > div {
        color: #1F2937 !important;
    }
    
    /* Fix dropdown options text color */
    .stSelectbox div[role="listbox"] div[role="option"] {
        color: #1F2937 !important;
        background-color: #FFFFFF !important;
    }
    
    .stSelectbox div[role="listbox"] div[role="option"]:hover {
        color: #1F2937 !important;
        background-color: #F3F4F6 !important;
    }
    
    .stSelectbox div[role="listbox"] div[role="option"][aria-selected="true"] {
        color: #1F2937 !important;
        background-color: #EFF6FF !important;
    }
    
    /* Force text color on all selectbox elements */
    .stSelectbox * {
        color: #1F2937 !important;
    }
    
    /* Override any Streamlit default text colors */
    .stSelectbox .stSelectbox > div > div > div > div {
        color: #1F2937 !important;
    }
    
    /* Override any dark theme classes */
    .stApp [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    .stApp [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }
    
    .stApp [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <script>
    // Function to apply error styling to form fields
    function applyErrorStyling() {
        // Check if there are error placeholders in form fields
        const textInputs = document.querySelectorAll('.stTextInput>div>div>input');
        const selectBoxes = document.querySelectorAll('.stSelectbox>div>div>div');
        const checkboxes = document.querySelectorAll('.stCheckbox');
        
        // Apply error styling to text inputs with error placeholders
        textInputs.forEach(input => {
            if (input.placeholder && input.placeholder.includes('⚠️')) {
                input.style.borderColor = '#EF4444';
                input.style.background = '#FEF2F2';
                input.style.color = '#DC2626';
                input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
                // Make placeholder text red
                input.style.setProperty('--placeholder-color', '#EF4444');
            }
        });
        
        // Apply error styling to select boxes with error options
        selectBoxes.forEach(select => {
            if (select.textContent && select.textContent.includes('⚠️')) {
                select.style.borderColor = '#EF4444';
                select.style.background = '#FEF2F2';
                select.style.color = '#DC2626';
                select.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
                // Make warning text red
                select.style.setProperty('--placeholder-color', '#EF4444');
            }
        });
        
        // Apply error styling to checkboxes with error text
        checkboxes.forEach(checkbox => {
            const label = checkbox.querySelector('label');
            if (label && label.textContent && label.textContent.includes('⚠️')) {
                const checkboxDiv = checkbox.querySelector('div>div');
                if (checkboxDiv) {
                    checkboxDiv.style.borderColor = '#EF4444';
                    checkboxDiv.style.background = '#FEF2F2';
                }
                label.style.color = '#DC2626';
            }
        });
        
        // Force red color for warning text in all form elements
        const allInputs = document.querySelectorAll('input, select, textarea');
        allInputs.forEach(input => {
            if (input.placeholder && input.placeholder.includes('⚠️')) {
                input.style.color = '#EF4444';
            }
            if (input.textContent && input.textContent.includes('⚠️')) {
                input.style.color = '#EF4444';
            }
        });
        
        // Target selectbox options specifically
        const selectOptions = document.querySelectorAll('.stSelectbox div[role="option"]');
        selectOptions.forEach(option => {
            if (option.textContent && option.textContent.includes('⚠️')) {
                option.style.color = '#EF4444';
                option.style.fontWeight = '500';
            }
        });
    }
    
    // Function to fix dropdown arrows
    function fixDropdownArrows() {
        // Find all dropdown arrows and make them darker
        const arrows = document.querySelectorAll('.stSelectbox [data-baseweb="select"] [role="combobox"]::after, .stSelectbox [data-baseweb="select"] [role="combobox"]:after');
        arrows.forEach(arrow => {
            arrow.style.color = '#1F2937';
        });
        
        // Target SVG arrows specifically and make them darker
        const svgArrows = document.querySelectorAll('.stSelectbox svg');
        svgArrows.forEach(svg => {
            svg.style.color = '#1F2937';
            svg.style.fill = '#1F2937';
            svg.style.stroke = '#1F2937';
            
            // Also target any path elements inside the SVG
            const paths = svg.querySelectorAll('path');
            paths.forEach(path => {
                path.style.fill = '#1F2937';
                path.style.stroke = '#1F2937';
                path.setAttribute('fill', '#1F2937');
                path.setAttribute('stroke', '#1F2937');
            });
            
            // Target any polygon elements inside the SVG
            const polygons = svg.querySelectorAll('polygon');
            polygons.forEach(polygon => {
                polygon.style.fill = '#1F2937';
                polygon.style.stroke = '#1F2937';
                polygon.setAttribute('fill', '#1F2937');
                polygon.setAttribute('stroke', '#1F2937');
            });
        });
        
        // Target any pseudo-elements
        const selectBoxes = document.querySelectorAll('.stSelectbox [role="combobox"]');
        selectBoxes.forEach(box => {
            const style = window.getComputedStyle(box, '::after');
            if (style.content && style.content !== 'none') {
                box.style.setProperty('--arrow-color', '#1F2937');
            }
        });
        
        // Force update any existing SVG elements
        const allSvgs = document.querySelectorAll('svg');
        allSvgs.forEach(svg => {
            if (svg.closest('.stSelectbox')) {
                svg.style.color = '#1F2937';
                svg.style.fill = '#1F2937';
                svg.style.stroke = '#1F2937';
            }
        });
    }
    
    // Function to fix dropdown text colors
    function fixDropdownTextColors() {
        // Fix selected text color in dropdowns
        const selectBoxes = document.querySelectorAll('.stSelectbox > div > div > div');
        selectBoxes.forEach(select => {
            select.style.color = '#1F2937';
            select.style.backgroundColor = '#FFFFFF';
        });
        
        // Fix input elements within selectboxes
        const inputs = document.querySelectorAll('.stSelectbox input');
        inputs.forEach(input => {
            input.style.color = '#1F2937';
            input.style.backgroundColor = '#FFFFFF';
        });
        
        // Fix placeholder text color
        const placeholders = document.querySelectorAll('.stSelectbox input::placeholder');
        placeholders.forEach(placeholder => {
            placeholder.style.color = '#6B7280';
        });
        
        // Fix dropdown options text color
        const options = document.querySelectorAll('.stSelectbox div[role="option"]');
        options.forEach(option => {
            option.style.color = '#1F2937';
            option.style.backgroundColor = '#FFFFFF';
        });
        
        // Fix all text elements in selectboxes
        const textElements = document.querySelectorAll('.stSelectbox div[data-baseweb="select"] *');
        textElements.forEach(element => {
            if (element.tagName !== 'SVG' && element.tagName !== 'PATH' && element.tagName !== 'POLYGON') {
                element.style.color = '#1F2937';
            }
        });
        
        // Force text color on all selectbox children
        const allSelectElements = document.querySelectorAll('.stSelectbox *');
        allSelectElements.forEach(element => {
            if (element.tagName !== 'SVG' && element.tagName !== 'PATH' && element.tagName !== 'POLYGON') {
                element.style.color = '#1F2937';
            }
        });
        
        // Additional fix for BaseWeb select components
        const baseWebSelects = document.querySelectorAll('[data-baseweb="select"]');
        baseWebSelects.forEach(select => {
            const textElements = select.querySelectorAll('*');
            textElements.forEach(element => {
                if (element.tagName !== 'SVG' && element.tagName !== 'PATH' && element.tagName !== 'POLYGON') {
                    element.style.color = '#1F2937';
                }
            });
        });
    }
    
    // Apply error styling when page loads
    document.addEventListener('DOMContentLoaded', function() {
        applyErrorStyling();
        fixDropdownArrows();
        fixDropdownTextColors();
    });
    
    // Apply error styling after form submission
    setTimeout(function() {
        applyErrorStyling();
        fixDropdownArrows();
        fixDropdownTextColors();
    }, 100);
    
    // Apply error styling when form fields are updated
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0 || mutation.type === 'attributes') {
                setTimeout(function() {
                    applyErrorStyling();
                    fixDropdownArrows();
                    fixDropdownTextColors();
                }, 50);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['placeholder', 'textContent']
    });
    
    // Additional interval check to ensure arrows and text colors are styled
    setInterval(function() {
        fixDropdownArrows();
        fixDropdownTextColors();
    }, 500);
    </script>
""", unsafe_allow_html=True)

# Initialize session state
if 'submissions_count' not in st.session_state:
    st.session_state.submissions_count = 0
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_timer' not in st.session_state:
    st.session_state.success_timer = 0
if 'submitted_data' not in st.session_state:
    st.session_state.submitted_data = {}

# Insurance expertise areas
INSURANCE_TYPES = {
    "Medicare": {"icon": "🏥", "description": "Medicare Advantage, Supplement & Prescription Plans"},
    "Health Insurance": {"icon": "💊", "description": "Federal & State Marketplace Plans"},
    "Life Insurance": {"icon": "🛡️", "description": "Term, Permanent & Hybrid Long-Term Care"},
    "Annuities": {"icon": "💰", "description": "Income Strategies with Living Benefits"},
    "Home, Auto & Business": {"icon": "🏠", "description": "Complete Property & Casualty Coverage"},
    "Long-Term Care": {"icon": "🤝", "description": "Traditional & Hybrid LTC Solutions"},
    "Travel Medical": {"icon": "✈️", "description": "International Coverage & Pre-existing Conditions"},
    "Disability": {"icon": "⚕️", "description": "Industry-Specific Income Protection"}
}

# States where licensed
LICENSED_STATES = [
    "Massachusetts", "New Hampshire", "Connecticut", "Rhode Island",
    "Maine", "Vermont", "New York", "New Jersey", "Pennsylvania",
    "Florida", "California", "Texas", "Illinois", "Ohio"
]

# Google Sheets Configuration
SHEET_NAME = "Insurance Leads"
WORKSHEET_NAME = "Sheet1"

@st.cache_resource
def init_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        creds_dict = st.secrets["gcp_service_account"]
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        if not worksheet.get_all_values():
            headers = ['Timestamp', 'Name', 'Email', 'Phone', 'State', 'Insurance_Type', 'Notes', 'Status', 'Source']
            worksheet.append_row(headers)
        
        return worksheet
    except Exception as e:
        return None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) == 10

def save_to_google_sheets(worksheet, data):
    try:
        row = [
            data['Timestamp'],
            data['Name'],
            data['Email'],
            data['Phone'],
            data['State'],
            data['Insurance_Type'],
            data['Notes'],
            data['Status'],
            data['Source']
        ]
        worksheet.append_row(row)
        return True
    except Exception as e:
        return save_to_local_csv(data)

def save_to_local_csv(data):
    """Fallback to local CSV if Google Sheets fails"""
    import os
    csv_file = 'insurance_leads_backup.csv'
    try:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            df = pd.DataFrame([data])
        df.to_csv(csv_file, index=False)
        return True
    except:
        return False

# Initialize Google Sheets
worksheet = init_google_sheets()

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Universal Insurance Solutions</h1>
    <p class="hero-subtitle">Your Trusted Insurance Partner in Shrewsbury, MA</p>
    <div class="hero-badges">
        <span class="badge">✓ Licensed in 14 States</span>
        <span class="badge">✓ 40+ Major Carriers</span>
        <span class="badge">✓ Free Coverage Analysis</span>
        <span class="badge">✓ 24-48 Hour Response</span>
        <span class="badge">✓ Expert Guidance</span>
        <span class="badge">✓ Personalized Service</span>
        <span class="badge">✓ No Hidden Fees</span>
        <span class="badge">✓ Multiple Carriers</span>
    </div>
    
</div>
""", unsafe_allow_html=True)

# Handle success message display and auto-cleanup
if st.session_state.show_success:
    st.session_state.success_timer += 1
    
    # Show success message
    st.markdown("""
    <div class="success-animation">
        ✅ Success! Your Free Coverage Analysis Request Has Been Received!
        <br>
        <span style="font-size: 16px; font-weight: 400;">
            One of our licensed professionals will contact you within 24-48 hours.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
    
    # Show confirmation with submitted data
    if st.session_state.submitted_data:
        with st.expander("📋 View Submission Details"):
            details_col1, details_col2 = st.columns(2)
            with details_col1:
                st.write(f"**Name:** {st.session_state.submitted_data.get('Name', 'N/A')}")
                st.write(f"**Email:** {st.session_state.submitted_data.get('Email', 'N/A')}")
                st.write(f"**Phone:** {st.session_state.submitted_data.get('Phone', 'N/A')}")
            with details_col2:
                st.write(f"**State:** {st.session_state.submitted_data.get('State', 'N/A')}")
                st.write(f"**Insurance Type:** {st.session_state.submitted_data.get('Insurance_Type', 'N/A')}")
    
    # Show countdown and auto-cleanup after 20 seconds (15s display + 5s delay)
    remaining = 20 - st.session_state.success_timer
    
    # Different messages based on timer phase
    if st.session_state.success_timer <= 15:
        message = f"✅ Success! Your request has been received. Form will reset in {remaining} seconds..."
        bg_color = "#F0FDF4"
        border_color = "#10B981"
        text_color = "#047857"
    else:
        message = f"🔄 Preparing to reset form... {remaining} seconds remaining..."
        bg_color = "#FEF3C7"
        border_color = "#F59E0B"
        text_color = "#92400E"
    
    st.markdown(f"""
    <div style="margin-top: 20px; padding: 16px; background: {bg_color}; border-radius: 12px; border-left: 4px solid {border_color};">
        <p style="color: {text_color}; margin: 0; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;">
            {message}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-cleanup after 20 seconds (15s display + 5s delay)
    if st.session_state.success_timer >= 20:
        # Clear success state and reset form
        st.session_state.show_success = False
        st.session_state.success_timer = 0
        st.session_state.submitted_data = {}
        # Clear any error states
        if 'show_errors' in st.session_state:
            del st.session_state.show_errors
        # Clear form data to reset fields
        for key in ['first_name', 'last_name', 'email', 'phone', 'state', 'insurance_type']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    else:
        # Increment timer and rerun
        st.rerun()

# Create responsive columns
col1, col2 = st.columns([1, 1.2], gap="large")

# Left Column - Areas of Expertise
with col1:
    st.markdown("### Our Areas of Expertise")
    
    for insurance_type, details in INSURANCE_TYPES.items():
        st.markdown(f"""
        <div class="expertise-card">
            <h4 class="expertise-title">
                <span style="font-size: 18px;">{details['icon']}</span>
                {insurance_type}
            </h4>
            <p class="expertise-description">{details['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    

# Right Column - Form
with col2:
    st.markdown("""
    <div class="form-container">
        <h2 class="form-header">Get Your Free Coverage Analysis</h2>
        <p class="form-subheader">Complete this form and our licensed professionals will contact you within 24-48 hours</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        with st.form("insurance_form", clear_on_submit=True):
            # Check for errors to determine placeholders
            show_errors = st.session_state.get('show_errors', False)
            
            # Name fields in two columns
            name_col1, name_col2 = st.columns(2)
            with name_col1:
                first_name = st.text_input(
                    "First Name *",
                    placeholder="⚠️ Please enter your first name" if show_errors else "John",
                    key="first_name"
                )
            with name_col2:
                last_name = st.text_input(
                    "Last Name *",
                    placeholder="⚠️ Please enter your last name" if show_errors else "Doe",
                    key="last_name"
                )
            
            # Contact fields
            email = st.text_input(
                "Email Address *",
                placeholder="⚠️ Please enter a valid email address" if show_errors else "john.doe@example.com",
                key="email"
            )
            
            # Phone and State in two columns
            contact_col1, contact_col2 = st.columns(2)
            with contact_col1:
                phone = st.text_input(
                    "Phone Number *",
                    placeholder="⚠️ Please enter a valid 10-digit phone number" if show_errors else "(555) 123-4567",
                    key="phone"
                )
            with contact_col2:
                state = st.selectbox(
                    "State *",
                    options=["⚠️ Please select your state"] + LICENSED_STATES if show_errors else ["Select your state..."] + LICENSED_STATES,
                    key="state"
                )
            
            # Insurance interest
            insurance_interest = st.selectbox(
                "Insurance Type *",
                options=["⚠️ Please select an insurance type"] + list(INSURANCE_TYPES.keys()) if show_errors else ["Select insurance type..."] + list(INSURANCE_TYPES.keys()),
                key="insurance_type"
            )
            
            
            # Submit button
            submitted = st.form_submit_button(
                "🚀 Get My Free Analysis",
                type="primary",
                use_container_width=True
            )
            
            # Contact Information
            st.markdown("""
            <div style="margin-top: 25px; padding: 20px; background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.9) 100%); border-radius: 16px; border-left: 5px solid #3B82F6; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); backdrop-filter: blur(10px); position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 100px; height: 100px; background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%); border-radius: 50%; transform: translate(30px, -30px);"></div>
                <h4 style="color: #1F2937; margin: 0 0 16px 0; font-family: 'Poppins', sans-serif; font-size: 18px; font-weight: 700; position: relative; z-index: 1;">📞 Need Immediate Assistance?</h4>
                <div style="position: relative; z-index: 1;">
                    <p style="color: #4B5563; margin: 6px 0; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;">
                        <strong style="color: #1F2937;">Phone:</strong> <a href="tel:508-579-4251" style="color: #3B82F6; text-decoration: none; font-weight: 600; transition: color 0.3s ease;">(508) 579-4251</a>
                    </p>
                    <p style="color: #4B5563; margin: 6px 0; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;">
                        <strong style="color: #1F2937;">Email:</strong> <a href="mailto:ravi@universalinsurancesolutions.com" style="color: #3B82F6; text-decoration: none; font-weight: 600; transition: color 0.3s ease;">ravi@universalinsurancesolutions.com</a>
                    </p>
                    <p style="color: #4B5563; margin: 6px 0; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;">
                        <strong style="color: #1F2937;">Email:</strong> <a href="mailto:Dev@uisolutionsinc.com" style="color: #3B82F6; text-decoration: none; font-weight: 600; transition: color 0.3s ease;">Dev@uisolutionsinc.com</a>
                    </p>
                    <p style="color: #4B5563; margin: 6px 0; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;">
                        <strong style="color: #1F2937;">Address:</strong> 67 Boylston Cir, Shrewsbury, MA 01545
                    </p>
                    <p style="color: #4B5563; margin: 6px 0; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;">
                        <strong style="color: #1F2937;">Hours:</strong> Mon - Fri: 8am-5pm | Weekend by appointment
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if submitted:
                errors = []
                
                if not first_name or len(first_name.strip()) < 2:
                    errors.append("Please enter your first name")
                
                if not last_name or len(last_name.strip()) < 2:
                    errors.append("Please enter your last name")
                
                if not email or not validate_email(email):
                    errors.append("Please enter a valid email address")
                
                if not phone or not validate_phone(phone):
                    errors.append("Please enter a valid 10-digit phone number")
                
                if state == "Select your state...":
                    errors.append("Please select your state")
                
                if insurance_interest == "Select insurance type...":
                    errors.append("Please select an insurance type")
                
                
                if errors:
                    # Set session state to show field errors
                    st.session_state.show_errors = True
                else:
                    # Clear error state on successful validation
                    if 'show_errors' in st.session_state:
                        del st.session_state.show_errors
                    
                    # Prepare data
                    data = {
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Name': f"{first_name.strip()} {last_name.strip()}",
                        'Email': email.strip().lower(),
                        'Phone': re.sub(r'\D', '', phone),
                        'State': state,
                        'Insurance_Type': insurance_interest,
                        'Notes': '',
                        'Status': 'New',
                        'Source': 'Web Form'
                    }
                    
                    # Save data
                    if worksheet:
                        success = save_to_google_sheets(worksheet, data)
                    else:
                        success = save_to_local_csv(data)
                    
                    if success:
                        st.session_state.submissions_count += 1
                        st.session_state.show_success = True
                        st.session_state.success_timer = 0
                        
                        # Store submitted data for display
                        st.session_state.submitted_data = {
                            'Name': data['Name'],
                            'Email': data['Email'],
                            'Phone': phone,
                            'State': data['State'],
                            'Insurance_Type': data['Insurance_Type']
                        }
                        
                        # Force rerun to show success message
                        st.rerun()
                    else:
                        st.error("❌ System error. Please try again or call us directly.")

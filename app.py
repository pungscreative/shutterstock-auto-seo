import streamlit as st
import pandas as pd
from PIL import Image
from google import genai
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Shutterstock Pro Studio", layout="wide")

st.title("✨ Shutterstock Pro Studio (AQ-Key Ready)")

api_key = st.text_input("Masukkan API Key (AQ...):", type="password")
uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    if st.button("Generate SEO Metadata"):
        with st.spinner("✨ Menghubungkan via Interactions API..."):
            try:
                # Inisialisasi client baru yang mendukung format AQ.
                client = genai.Client(api_key=api_key)
                
                # Menggunakan model standar yang didukung Interactions API
                model_name = "gemini-1.5-flash" 
                
                img = Image.open(uploaded_file)
                prompt = "Act as a professional Shutterstock contributor. Provide TITLE, KEYWORDS (50 total), CATEGORY, and DESCRIPTION in English."
                
                # Pemanggilan menggunakan client SDK baru
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, img]
                )
                
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Gagal terhubung dengan kunci AQ.: {e}")
                st.info("Pastikan Anda menggunakan pustaka 'google-genai' terbaru (bukan 'google-generativeai').")

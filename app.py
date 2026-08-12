import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Shutterstock Pro Studio", page_icon="✨", layout="wide")

# CSS Estetik
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at 10% 20%, rgba(120, 119, 198, 0.25) 0%, transparent 40%), linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%); color: #f8fafc; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 30px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

st.title("✨ Shutterstock Pro Studio")

col1, col2 = st.columns(2)

with col1:
    api_key = st.text_input("Gemini API Key:", type="password")
    uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

with col2:
    if uploaded_file and api_key:
        if st.button("Generate CSV"):
            with st.spinner("Gemini 3.5 Flash sedang bekerja..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash') # Menggunakan versi stabil flash
                
                img = Image.open(uploaded_file)
                prompt = """
                Act as a Shutterstock expert. Analyze the image and provide:
                TITLE: [Concise Title]
                KEYWORDS: [50 comma-separated keywords]
                CATEGORY: [Category e.g. Animals/Wildlife]
                DESCRIPTION: [Commercial Description]
                Return in English only.
                """
                response = model.generate_content([prompt, img])
                
                # Parsing
                data_dict = {}
                for line in response.text.split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        data_dict[k.strip()] = v.strip()
                
                # Pembuatan DataFrame dengan struktur yang benar
                df = pd.DataFrame({
                    "Filename": [uploaded_file.name],
                    "Description": [f"{data_dict.get('TITLE', '')} {data_dict.get('DESCRIPTION', '')}"],
                    "Keywords": [data_dict.get('KEYWORDS', '')],
                    "Categories": [data_dict.get('CATEGORY', 'Animals/Wildlife')],
                    "Editorial": [0],
                    "Date Created": [datetime.now().strftime("%Y-%m-%d")],
                    "Location": ["Mataram"]
                })
                
                st.dataframe(df)
                st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="shutterstock.csv", mime="text/csv")

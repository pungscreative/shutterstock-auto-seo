import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Shutterstock Pro Studio", page_icon="✨", layout="wide")

# CSS Estetik Glassmorphism
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at 10% 20%, rgba(120, 119, 198, 0.25) 0%, transparent 40%), linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%); color: #f8fafc; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 30px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

st.title("✨ Shutterstock Pro Studio")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key:", type="password")
    uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if uploaded_file and api_key:
        if st.button("Generate SEO Metadata & CSV"):
            with st.spinner("✨ Gemini sedang meracik metadata..."):
                try:
                    genai.configure(api_key=api_key)
                    # Menggunakan model 1.5-flash yang tersedia secara resmi di API
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    img = Image.open(uploaded_file)
                    prompt = "Analyze this image for Shutterstock. Provide TITLE, KEYWORDS (50 total, comma-separated), CATEGORY, and DESCRIPTION in English."
                    response = model.generate_content([prompt, img])
                    
                    # Parsing hasil
                    data_dict = {}
                    for line in response.text.split('\n'):
                        if ':' in line:
                            k, v = line.split(':', 1)
                            data_dict[k.strip()] = v.strip()
                    
                    df = pd.DataFrame({
                        "Filename": [uploaded_file.name],
                        "Description": [f"{data_dict.get('TITLE', 'Image')} {data_dict.get('DESCRIPTION', '')}"],
                        "Keywords": [data_dict.get('KEYWORDS', '')],
                        "Categories": [data_dict.get('CATEGORY', 'Nature')],
                        "Editorial": [0],
                        "Date Created": [datetime.now().strftime("%Y-%m-%d")],
                        "Location": ["Mataram"]
                    })
                    
                    st.success("✅ Metadata berhasil dibuat!")
                    st.dataframe(df)
                    st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="shutterstock_upload.csv", mime="text/csv")
                
                except Exception as e:
                    st.error(f"Error API: {e}. Pastikan API Key valid dan model 'gemini-1.5-flash' diizinkan.")
    st.markdown('</div>', unsafe_allow_html=True)

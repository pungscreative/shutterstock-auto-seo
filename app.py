import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
import io

# Konfigurasi Halaman & Tema Estetik
st.set_page_config(
    page_title="Shutterstock Pro Studio", 
    page_icon="✨", 
    layout="wide"
)

# Custom CSS untuk Tampilan Estetik, Bersih, & Profesional (Gaya Neumorphism / Glassmorphism)
st.markdown("""
<style>
    /* Background & Global Font */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .hero-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        padding: 30px 40px;
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.04);
        margin-bottom: 30px;
    }
    
    /* Card Container */
    .custom-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
        border: 1px solid #f1f5f9;
        margin-bottom: 20px;
    }

    /* Custom Button Style */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(79, 70, 229, 0.35);
    }
    
    /* Text Input & Uploader Customization */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        padding: 10px 15px;
        background: rgba(255, 255, 255, 0.8);
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="hero-container">
        <h1 style="margin:0; font-size: 2.2rem; background: linear-gradient(90deg, #4f46e5, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ✨ Shutterstock Pro Studio
        </h1>
        <p style="color: #64748b; margin-top: 8px; font-size: 1.05rem;">
            Powered by <b>Gemini 3.5 Flash</b> — AI-Powered Microstock Metadata & CSV Automation Studio.
        </p>
    </div>
""", unsafe_allow_html=True)

# Layout Utama Dibagi Menjadi 2 Kolom
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("🔑 Konfigurasi & Upload")
    
    api_key = st.text_input("Google Gemini API Key:", type="password", placeholder="Masukkan API Key (AIzaSy...)")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Pilih File Foto (JPG/PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview Aset Visual", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("🚀 Hasil Analisis & CSV")
    
    if uploaded_file is not None:
        if st.button("Mulai Automasi SEO & CSV"):
            if not api_key:
                st.error("⚠️ Silakan masukkan Google Gemini API Key terlebih dahulu!")
            else:
                with st.spinner("🤖 Gemini 3.5 Flash sedang menganalisis foto dan meracik SEO terbaik..."):
                    try:
                        genai.configure(api_key=api_key)
                        
                        # Menggunakan model gemini-3.5-flash sesuai titah
                        model = genai.GenerativeModel('gemini-3.5-flash')
                        
                        prompt = """
                        Act as an elite Shutterstock Microstock Expert. Analyze this image thoroughly to maximize downloads.
                        Return ONLY this exact structured format with labels:
                        TITLE: [A concise, commercial search-friendly title]
                        KEYWORDS: [Exactly 50 relevant commercial keywords separated by commas, sorted from specific subject to abstract concept]
                        CATEGORY: [Choose 1 best matching Shutterstock category from standard list e.g. Business, Technology, Nature, Backgrounds, People]
                        DESCRIPTION: [A clear, highly descriptive commercial description]
                        """
                        
                        response = model.generate_content([prompt, image])
                        text = response.text
                        
                        # Parsing data dari AI
                        data_dict = {}
                        for line in text.split('\n'):
                            if ':' in line:
                                k, v = line.split(':', 1)
                                data_dict[k.strip()] = v.strip()
                        
                        # Format Data CSV Shutterstock
                        csv_data = {
                            "Filename": [uploaded_file.name],
                            "Description": [f"{data_dict.get('TITLE', '')} {data_dict.get('DESCRIPTION', '')}"],
                            "Keywords": [data_dict.get('KEYWORDS', '')],
                            "Categories": [data_dict.get('CATEGORY', 'Backgrounds/Textures')]
                        }
                        df = pd.DataFrame(csv_data)
                        
                        st.success("✅ Metadata & CSV Berhasil Digenerate dengan Gemini 3.5 Flash!")
                        
                        # Preview Hasil dalam bentuk tabel yang bersih
                        st.dataframe(df, use_container_width=True)
                        
                        # Tombol Download CSV
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download File CSV Shutterstock",
                            data=csv,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_shutterstock.csv",
                            mime="text/csv"
                        )
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
    else:
        st.info("👈 Silakan upload foto di sebelah kiri untuk melihat hasil analisis AI dan mengunduh file CSV.")
        
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
import io

# Konfigurasi Halaman & Tema Estetik
st.set_page_config(
    page_title="Shutterstock Pro Studio | AI Automation", 
    page_icon="✨", 
    layout="wide"
)

# Custom CSS: Gaya 3D Glassmorphism & Kosmik
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(120, 119, 198, 0.25) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(79, 70, 229, 0.2) 0%, transparent 40%),
                    linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }

    header, footer {visibility: hidden;}

    .hero-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 30px;
        padding: 40px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        margin-bottom: 30px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }

    .gradient-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #a78bfa 70%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 10px;
    }

    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 500;
    }

    .stTextInput>div>div>input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #fff !important;
        border-radius: 14px !important;
        padding: 12px 18px !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white;
        border-radius: 14px;
        padding: 14px 28px;
        font-weight: 700;
        border: none;
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.50px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(168, 85, 247, 0.6);
    }

    label, .stFileUploader label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-card">
        <div class="gradient-title">Shutterstock Pro Studio</div>
        <div class="sub-title">
            Next-Gen Microstock Metadata & CSV Automation Studio • Powered by <b>Gemini 3.5 Flash</b>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔑 Konfigurasi & Upload Aset")
    
    api_key = st.text_input("Google Gemini API Key:", type="password", placeholder="Masukkan API Key (AIzaSy...)")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Pilih File Foto (JPG/PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview Aset Visual", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🚀 Hasil Analisis & Export CSV")
    
    if uploaded_file is not None:
        if st.button("Mulai Automasi SEO & CSV"):
            if not api_key:
                st.error("⚠️ Silakan masukkan Google Gemini API Key terlebih dahulu!")
            else:
                with st.spinner("✨ Gemini 3.5 Flash sedang meracik SEO dan Metadata terbaik..."):
                    try:
                        genai.configure(api_key=api_key)
                        
                        # Menggunakan model gemini-3.5-flash
                        model = genai.GenerativeModel('gemini-3.5-flash')
                        
                        prompt = """
                        Act as an elite Shutterstock Microstock Expert. Analyze this image thoroughly to maximize global sales.
                        CRITICAL REQUIREMENT: The output MUST be entirely in ENGLISH because Shutterstock global marketplace requires English metadata.
                        Return ONLY this exact structured format with labels:
                        TITLE: [A concise, commercial search-friendly title in English]
                        KEYWORDS: [Exactly 50 relevant commercial keywords in English separated by commas, sorted from specific subject to abstract concept]
                        CATEGORY: [Choose 1 best matching Shutterstock category from standard list e.g. Animals/Wildlife, Nature, Backgrounds, People]
                        DESCRIPTION: [A clear, highly descriptive commercial description in English]
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
                            "Categories": [data_dict.get('CATEGORY', 'Animals/Wildlife')]
                        }
                        df = pd.DataFrame(csv_data)
                        
                        st.success("✅ SEO & CSV Berhasil Digenerate oleh Gemini 3.5 Flash (Standar Internasional Shutterstock)!")
                        
                        # Preview Hasil Tabel
                        st.dataframe(df, use_container_width=True)
                        
                        # Tombol Download CSV Estetik
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
        st.info("👈 Silakan upload foto di sebelah kiri untuk mengaktifkan mesin automasi AI.")
        
    st.markdown('</div>', unsafe_allow_html=True)

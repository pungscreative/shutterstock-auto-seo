import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy Pro | AI SEO Metadata", page_icon="✨", layout="wide")

# CSS Styling - Tata Letak Kartu Kaca & Inner Box yang Presisi Sesuai Permintaan
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #c7d2fe 0%, #e9d5ff 35%, #fbcfe8 70%, #fed7aa 100%);
        background-attachment: fixed;
    }
    
    /* Header Utama dengan Efek Kaca */
    .hero-container {
        text-align: center;
        padding: 25px;
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    .badge-text {
        font-size: 0.75rem;
        font-weight: 700;
        color: #7e22ce;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .gradient-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 2.3rem;
        background: linear-gradient(135deg, #4338ca 0%, #7e22ce 50%, #be185d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* Kolom Utama sebagai Kartu Kaca Transparan Besar */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.7) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
    }

    /* Judul Kolom */
    .card-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        color: #1e1b4b;
        margin-bottom: 15px;
    }

    /* Kotak Inner Box untuk File Uploader & Area Hasil AI */
    [data-testid="stFileUploader"], .inner-result-box {
        background: rgba(255, 255, 255, 0.55) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }

    .stFileUploader label p {
        color: #1e1b4b !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Utama dengan Badge
st.markdown("""
<div class="hero-container">
    <div class="badge-text">✨ AI-POWERED PUNGS CREATIVE</div>
    <h1 class="gradient-title">Nyetok.Kuy Pro</h1>
    <p style="color: #475569; font-weight: 500; font-size: 0.95rem;">Sistem Otomatisasi Metadata Stok Foto Profesional & SEO Optimal</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card-title">⚙️ Konfigurasi & Upload</div>', unsafe_allow_html=True)
    
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    if not api_key:
        api_key = st.text_input("🔑 Masukkan Gemini API Key", type="password")
    
    uploaded_file = st.file_uploader("📁 Drag & Drop atau Klik untuk Upload Foto Produk (Max 200MB)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Pratinjau Foto", use_container_width=True)

with col2:
    st.markdown('<div class="card-title">📊 Hasil Pemrosesan AI</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="inner-result-box">', unsafe_allow_html=True)
    if uploaded_file and api_key:
        if st.button("🚀 Generate Metadata SEO", type="primary", use_container_width=True):
            with st.spinner("✨ AI sedang meracik metadata terbaik..."):
                try:
                    client = genai.Client(api_key=api_key.strip())
                    img = Image.open(uploaded_file)
                    
                    prompt = """
                    Act as a professional Shutterstock contributor. 
                    Analyze the image and provide metadata in English format:
                    TITLE: [A concise, commercial search-friendly title]
                    KEYWORDS: [Provide EXACTLY 45 relevant comma-separated keywords.]
                    CATEGORY: [Pick one: Animals/Wildlife, Nature, Backgrounds, People, Technology, Food/Drink]
                    DESCRIPTION: [A detailed commercial description]
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[prompt, img]
                    )
                    
                    st.success("🎉 Metadata berhasil disusun!")
                    st.text_area("Hasil Lengkap AI:", response.text, height=200)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada sistem AI: {e}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <p style="color: #475569; font-size: 0.9rem; margin-bottom: 15px;">⚡ Silakan unggah foto terlebih dahulu di kolom sebelah kiri untuk mengaktifkan mesin AI.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("🚀 Generate Metadata SEO", disabled=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.85rem;'>© 2026 Nyetok.Kuy - All Rights Reserved | powered by Pungs Creative</p>", unsafe_allow_html=True)

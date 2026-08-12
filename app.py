import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy Pro | AI SEO Metadata", page_icon="✨", layout="wide")

# CSS Styling - Menggunakan Wadah Kustom Aman (Tanpa Merusak Selector Kolom Streamlit)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Background Fluid Bergradasi Pastel */
    .stApp {
        background: linear-gradient(135deg, #c7d2fe 0%, #e9d5ff 35%, #fbcfe8 70%, #fed7aa 100%);
        background-attachment: fixed;
        position: relative;
        overflow-x: hidden;
        color: #1e1b4b;
    }
    
    /* Elemen Fluid & Liquid Gradient Blobs Organik */
    .stApp::before {
        content: '';
        position: absolute;
        top: -80px;
        left: -80px;
        width: 500px;
        height: 500px;
        background: linear-gradient(135deg, #9333ea, #3b82f6, #ec4899);
        border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
        filter: blur(80px);
        opacity: 0.55;
        z-index: 0;
        pointer-events: none;
    }
    .stApp::after {
        content: '';
        position: absolute;
        bottom: -100px;
        right: -100px;
        width: 550px;
        height: 550px;
        background: linear-gradient(135deg, #f43f5e, #8b5cf6, #06b6d4);
        border-radius: 60% 40% 30% 70% / 50% 30% 70% 50%;
        filter: blur(85px);
        opacity: 0.55;
        z-index: 0;
        pointer-events: none;
    }
    
    /* Hero Header dengan Efek Kaca Transparan */
    .hero-container {
        text-align: center;
        padding: 35px 20px;
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.7);
        position: relative;
        z-index: 1;
    }
    
    /* Font Tebal Gemuk dengan Gradasi Fluid yang Kontras */
    .gradient-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 2.8rem;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #4338ca 0%, #7e22ce 50%, #be185d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.08));
        margin-bottom: 8px;
    }
    
    .hero-subtitle {
        color: #475569;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Kotak Kaca Transparan Penuh (Liquid Glass UI Kit) yang Aman */
    .glass-box {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.7);
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
        height: 100%;
    }
    .glass-box:hover {
        border-color: rgba(255, 255, 255, 0.8);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    /* Heading dalam Kotak */
    h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        color: #1e1b4b !important;
        margin-bottom: 20px !important;
        font-size: 1.25rem !important;
    }
    
    /* Tombol & Aksi Mengkilap Transparan */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.2)) !important;
        backdrop-filter: blur(10px);
        color: #1e1b4b !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        padding: 13px 20px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.9);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.4)) !important;
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.1);
        border-color: #ffffff !important;
        color: #0f172a !important;
    }
    
    /* File Uploader Kaca Transparan */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.2);
        border: 2px dashed rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        padding: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.85rem;
        margin-top: 50px;
        padding-top: 25px;
        border-top: 1px solid rgba(255, 255, 255, 0.4);
        position: relative;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# Layout Header Hero
st.markdown("""
<div class="hero-container">
    <div style="display: inline-block; background: rgba(255, 255, 255, 0.5); color: #6b21a8; padding: 4px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.8);">✨ AI-POWERED PUNGS CREATIVE</div>
    <h1 class="gradient-title">Nyetok.Kuy Pro</h1>
    <p class="hero-subtitle">Sistem Otomatisasi Metadata Stok Foto Profesional & SEO Optimal</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("⚙️ Konfigurasi & Upload")
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None
        st.error("⚠️ API Key tidak terkonfigurasi di secrets.toml.")
    
    uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "jpeg", "png"], help="Maksimal ukuran file 200MB")
    
    if uploaded_file:
        st.image(uploaded_file, width='stretch', caption="Pratinjau Foto")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("📊 Hasil Pemrosesan AI")
    
    if uploaded_file and api_key:
        if st.button("🚀 Generate Metadata SEO"):
            with st.spinner("✨ AI sedang meracik metadata terbaik untuk Baginda..."):
                try:
                    client = genai.Client(api_key=api_key.strip())
                    img = Image.open(uploaded_file)
                    
                    prompt = """
                    Act as a professional Shutterstock contributor. 
                    Analyze the image and provide metadata in English:
                    TITLE: [A concise, commercial search-friendly title]
                    KEYWORDS: [Provide EXACTLY 45 relevant comma-separated keywords. DO NOT EXCEED 50.]
                    CATEGORY: [Pick one: Animals/Wildlife, Nature, Backgrounds, People, Technology, Food/Drink]
                    DESCRIPTION: [A detailed commercial description, minimum 6 words]
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[prompt, img]
                    )
                    
                    data_dict = {}
                    for line in response.text.split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            data_dict[key.strip()] = val.strip()
                            
                    desc = data_dict.get('DESCRIPTION', data_dict.get('TITLE', 'Stock Image'))
                    keyword_list = [k.strip() for k in data_dict.get('KEYWORDS', '').split(',') if k.strip()]
                    final_keywords = ','.join(keyword_list[:50])
                    
                    df = pd.DataFrame({
                        "Filename": [uploaded_file.name],
                        "Description": [desc],
                        "Keywords": [final_keywords],
                        "Categories": [data_dict.get('CATEGORY', 'Animals/Wildlife')],
                        "Illustration": ["No"],
                        "Mature Content": ["No"],
                        "Editorial": ["No"]
                    })
                    
                    st.success("🎉 Metadata berhasil disusun!")
                    st.dataframe(df, width='stretch')
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download CSV Siap Upload", 
                        data=csv, 
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_metadata.csv", 
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("💡 Silakan unggah foto terlebih dahulu di kolom sebelah kiri untuk mengaktifkan mesin AI.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer Watermark
st.markdown('<div class="footer">© 2026 Nyetok.Kuy - All Rights Reserved | powered by Pungs Creative</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy Pro | AI SEO Metadata", page_icon="✨", layout="wide")

# CSS Styling - Dark Mode Gradient, Dark Glassmorphism & Tombol Matching
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f1f5f9;
    }
    
    /* Background Gradasi Gelap yang Elegan */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #171035 35%, #2a0845 70%, #3b0764 100%);
        background-attachment: fixed;
    }
    
    /* Header Utama dengan Efek Kaca Gelap */
    .hero-container {
        text-align: center;
        padding: 25px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    .badge-text {
        font-size: 0.75rem;
        font-weight: 700;
        color: #c084fc;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .gradient-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 2.3rem;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* Kolom Utama sebagai Kartu Kaca Transparan Gelap */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4) !important;
    }

    /* Judul Kolom */
    .card-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        color: #f8fafc;
        margin-bottom: 15px;
    }

    /* Kotak Inner Box untuk File Uploader & Area Hasil AI Menyeluruh */
    [data-testid="stFileUploader"], .inner-result-box {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }

    .stFileUploader label p {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    
    /* Tombol Utama (Generate & Download) Matching dengan Background Gelap */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #c084fc 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #a855f7 100%) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6) !important;
    }
    
    p, span, label {
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# Header Utama dengan Badge
st.markdown("""
<div class="hero-container">
    <div class="badge-text">✨ AI-POWERED PUNGS CREATIVE</div>
    <h1 class="gradient-title">Nyetok.Kuy Pro</h1>
    <p style="color: #94a3b8; font-weight: 500; font-size: 0.95rem;">Sistem Otomatisasi Metadata Stok Foto Profesional & SEO Optimal</p>
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
    
    # Membungkus seluruh area hasil dan aksi di kolom kanan dengan efek kaca transparan
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
                    
                    # Parsing respons AI yang lebih aman & tangguh terhadap keyword kosong
                    data_dict = {}
                    for line in response.text.split('\n'):
                        if ':' in line:
                            parts = line.split(':', 1)
                            k_key = parts[0].strip().upper()
                            k_val = parts[1].strip().replace('[', '').replace(']', '')
                            data_dict[k_key] = k_val
                            
                    desc = data_dict.get('DESCRIPTION', data_dict.get('TITLE', 'Stock Image'))
                    
                    # Ekstraksi keyword dengan pengaman fallback
                    raw_keywords = data_dict.get('KEYWORDS', data_dict.get('KEYWORD', ''))
                    if not raw_keywords:
                        for line in response.text.split('\n'):
                            if 'keyword' in line.lower() and ':' in line:
                                raw_keywords = line.split(':', 1)[1].strip().replace('[', '').replace(']', '')
                                
                    keyword_list = [k.strip() for k in raw_keywords.split(',') if k.strip()]
                    final_keywords = ', '.join(keyword_list[:50]) if keyword_list else "stock photography, commercial photo, professional image, high quality"
                    
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
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download CSV Siap Upload", 
                        data=csv, 
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_metadata.csv", 
                        mime="text/csv",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada sistem AI: {e}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px;">⚡ Silakan unggah foto terlebih dahulu di kolom sebelah kiri untuk mengaktifkan mesin AI.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("🚀 Generate Metadata SEO", disabled=True, use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>© 2026 Nyetok.Kuy - All Rights Reserved | powered by Pungs Creative</p>", unsafe_allow_html=True)

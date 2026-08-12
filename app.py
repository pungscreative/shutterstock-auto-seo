import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy | SaaS Premium", page_icon="🚀", layout="wide")

# CSS Styling - Kotak transparan membungkus penuh kolom kiri & kanan
st.markdown("""
<style>
    :root {
        --primary: #8b5cf6;
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.75);
        --text-color: #f8fafc;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-color); }
    
    /* Header Container */
    .header-box {
        text-align: center;
        padding: 30px;
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Membuat kolom otomatis menjadi kotak transparan pembungkus */
    [data-testid="column"] {
        background-color: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* Tombol Utama */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4); }
    
    /* File Uploader Style */
    .stFileUploader { background: rgba(255,255,255,0.03); border-radius: 12px; }
    
    /* Footer */
    .footer { text-align: center; color: #64748b; font-size: 12px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# Layout Header
st.markdown("""
<div class="header-box">
    <h1 style="color: white; margin-bottom: 0;">🚀 Nyetok.Kuy Pro</h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">Sistem Otomatisasi Metadata Stok Foto AI Tingkat Lanjut</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("⚙️ Konfigurasi")
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None
        st.error("⚠️ API Key tidak terkonfigurasi. Silakan hubungi admin.")
    
    uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "jpeg", "png"], help="Maksimal 200MB per file")
    
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

with col2:
    st.subheader("📊 Hasil Pemrosesan")
    
    if uploaded_file and api_key:
        if st.button("Generate Metadata SEO"):
            with st.spinner("Menganalisis gambar dengan kecerdasan buatan..."):
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
                        model='gemini-2.5-flash',
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
                    
                    st.success("✅ Metadata berhasil disusun!")
                    st.dataframe(df, use_container_width=True)
                    
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
        st.info("Upload foto terlebih dahulu untuk memulai proses SEO.")

# Footer Watermark
st.markdown('<div class="footer">© 2026 Nyetok.Kuy - All Rights Reserved | powered by Pungs Creative</div>', unsafe_allow_html=True)

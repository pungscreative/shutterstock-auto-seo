import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
from datetime import datetime

# Konfigurasi Halaman & Tema Estetik Glassmorphism
st.set_page_config(page_title="Shutterstock Pro Studio", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .stApp { 
        background: radial-gradient(circle at 10% 20%, rgba(120, 119, 198, 0.25) 0%, transparent 40%), 
                    linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%); 
        color: #f8fafc; 
    }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(20px); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 24px; 
        padding: 30px; 
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); 
    }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; font-weight: 700; border: none; }
</style>
""", unsafe_allow_html=True)

st.title("✨ Shutterstock Pro Studio")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="Masukkan API Key Baginda...")
    uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if uploaded_file and api_key:
        if st.button("Generate SEO Metadata & CSV"):
            with st.spinner("✨ Mendeteksi model aktif & meracik metadata..."):
                try:
                    genai.configure(api_key=api_key)
                    
                    # Deteksi otomatis model yang mendukung generateContent agar kebal terhadap perubahan nama model oleh Google
                    valid_model = None
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            valid_model = m.name
                            break
                    
                    if not valid_model:
                        # Fallback manual jika deteksi gagal
                        valid_model = 'gemini-1.5-flash'
                    
                    model = genai.GenerativeModel(valid_model)
                    
                    img = Image.open(uploaded_file)
                    prompt = """
                    Act as a professional Shutterstock contributor. 
                    Analyze the image and provide metadata in English:
                    TITLE: [A concise, commercial search-friendly title]
                    KEYWORDS: [50 relevant comma-separated keywords]
                    CATEGORY: [Pick one: Animals/Wildlife, Nature, Backgrounds, People, Technology, Food/Drink]
                    DESCRIPTION: [A detailed commercial description]
                    """
                    response = model.generate_content([prompt, img])
                    
                    # Parsing hasil dari AI
                    data_dict = {}
                    for line in response.text.split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            data_dict[key.strip()] = val.strip()
                    
                    # Membuat DataFrame sesuai format standar Shutterstock
                    df = pd.DataFrame({
                        "Filename": [uploaded_file.name],
                        "Description": [f"{data_dict.get('TITLE', 'Image')} {data_dict.get('DESCRIPTION', '')}"],
                        "Keywords": [data_dict.get('KEYWORDS', '')],
                        "Categories": [data_dict.get('CATEGORY', 'Nature')],
                        "Editorial": [0],
                        "Date Created": [datetime.now().strftime("%Y-%m-%d")],
                        "Location": ["Mataram"]
                    })
                    
                    st.success(f"✅ Metadata & CSV Berhasil Digenerate menggunakan model `{valid_model}`!")
                    st.dataframe(df)
                    
                    # Tombol Download CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download File CSV Shutterstock", data=csv, file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_shutterstock.csv", mime="text/csv")
                
                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")
    else:
        st.info("Silakan masukkan API Key dan upload foto di sebelah kiri untuk memulai.")
    st.markdown('</div>', unsafe_allow_html=True)

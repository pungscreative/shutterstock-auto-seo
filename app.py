import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman & Tema Estetik
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
    api_key = st.text_input("Masukkan API Key (AQ...):", type="password", placeholder="Paste API Key di sini...")
    uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if uploaded_file and api_key:
        if st.button("Generate SEO Metadata & CSV"):
            with st.spinner("✨ Menghubungkan ke Gemini 3.5 Flash..."):
                try:
                    client = genai.Client(api_key=api_key.strip())
                    img = Image.open(uploaded_file)
                    
                    # PROMPT DIKEMBALIKAN KE FORMAT AWAL YANG SUDAH BENAR
                    # Hanya instruksi kategori yang diubah untuk meminta 2 kategori
                    prompt = """
                    Act as a professional Shutterstock contributor. 
                    Analyze the image and provide metadata in English:
                    TITLE: [A concise, commercial search-friendly title]
                    KEYWORDS: [Provide EXACTLY 45 relevant comma-separated keywords. DO NOT EXCEED 50.]
                    CATEGORY: [Pick TWO different relevant categories separated by a comma (e.g., Animals/Wildlife, Nature)]
                    DESCRIPTION: [A detailed commercial description, minimum 6 words]
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[prompt, img]
                    )
                    
                    # Parsing hasil dari AI (ditambahkan .upper() agar kata kunci kebal dari bug huruf kecil)
                    data_dict = {}
                    for line in response.text.split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            data_dict[key.strip().upper()] = val.strip()
                            
                    # 1. PENGAMAN DESKRIPSI (Min 5 kata)
                    desc = data_dict.get('DESCRIPTION', data_dict.get('TITLE', 'Stock Image'))
                    if len(desc.split()) < 5:
                        desc += " high quality premium stock photography"
                        
                    # 2. PENGAMAN KATA KUNCI (Maksimal 50 kata)
                    raw_keywords = data_dict.get('KEYWORDS', '')
                    keyword_list = [k.strip() for k in raw_keywords.split(',') if k.strip()]
                    keyword_list = keyword_list[:50]
                    final_keywords = ','.join(keyword_list)
                    
                    # 3. KATEGORI (AI akan otomatis memberikan 2 kategori yang dipisah koma)
                    final_categories = data_dict.get('CATEGORY', 'Animals/Wildlife')
                    
                    # 4. PEMBENTUKAN CSV
                    df = pd.DataFrame({
                        "Filename": [uploaded_file.name],
                        "Description": [desc],
                        "Keywords": [final_keywords],
                        "Categories": [final_categories],
                        "Illustration": ["No"],
                        "Mature Content": ["No"],
                        "Editorial": ["No"]
                    })
                    
                    st.success("✅ Metadata & CSV Berhasil Digenerate (Kata Kunci Aman & 2 Kategori Aktif)!")
                    st.dataframe(df)
                    
                    # Tombol Download CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download File CSV Shutterstock", 
                        data=csv, 
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_shutterstock.csv", 
                        mime="text/csv"
                    )
                
                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")
    else:
        st.info("Silakan masukkan API Key dan upload foto di sebelah kiri untuk memulai.")
    st.markdown('</div>', unsafe_allow_html=True)

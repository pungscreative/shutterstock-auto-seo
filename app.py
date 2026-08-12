import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman & Tema Estetik
st.set_page_config(page_title="Nyetok.Kuy", page_icon="✨", layout="wide")

st.markdown("""
<style>
    /* Latar Belakang Utama ala Kosmik Ungu Referensi */
    .stApp { 
        background: linear-gradient(135deg, #2e1065 0%, #4c1d95 50%, #1e1b4b 100%); 
        color: #f8fafc; 
    }
    
    /* Mengubah wadah utama Streamlit menjadi Bingkai Kartu Kaca Melayang (Main Window Frame) */
    .block-container {
        background: rgba(35, 15, 70, 0.65);
        backdrop-filter: blur(30px);
        border: 2px solid rgba(255, 255, 255, 0.22);
        border-radius: 35px;
        padding: 40px 50px !important;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.6);
        margin-top: 35px;
        margin-bottom: 35px;
        max-width: 1300px;
    }

    /* Kotak Transparan untuk Input & Upload */
    .stTextInput, .stFileUploader { 
        background: rgba(255, 255, 255, 0.06); 
        backdrop-filter: blur(20px); 
        border: 1px solid rgba(255, 255, 255, 0.15); 
        border-radius: 20px; 
        padding: 20px; 
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2); 
        margin-bottom: 20px; 
    }

    /* Kotak dalam input API Key agar kembar identik dengan upload foto */
    div[data-baseweb="input"] {
        background-color: rgba(20, 18, 45, 0.75) !important;
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
    }

    /* Area dalam file uploader */
    div[data-testid="stFileUploader"] section {
        background-color: rgba(20, 18, 45, 0.75) !important;
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
    }

    /* Kartu Kaca Sisi Kanan */
    .glass-card { 
        background: rgba(255, 255, 255, 0.06); 
        backdrop-filter: blur(20px); 
        border: 1px solid rgba(255, 255, 255, 0.15); 
        border-radius: 24px; 
        padding: 25px; 
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2); 
        margin-bottom: 20px;
    }

    /* Tombol Utama Bergaya Neon Gradient */
    .stButton>button { 
        width: 100%; 
        border-radius: 14px; 
        background: linear-gradient(135deg, #ec4899, #8b5cf6, #3b82f6); 
        color: white; 
        font-weight: 700; 
        border: none; 
        padding: 12px;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ Nyetok.Kuy")

col1, col2 = st.columns([1, 1.5])

with col1:
    api_key = st.text_input("Masukkan API Key (AQ...):", type="password", placeholder="Paste API Key di sini...")
    uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if uploaded_file and api_key:
        if st.button("Generate SEO Metadata & CSV"):
            with st.spinner("✨ Menghubungkan ke Gemini 3.5 Flash..."):
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
                    if len(desc.split()) < 5:
                        desc += " high quality premium stock photography"
                        
                    raw_keywords = data_dict.get('KEYWORDS', '')
                    keyword_list = [k.strip() for k in raw_keywords.split(',') if k.strip()]
                    keyword_list = keyword_list[:50]
                    final_keywords = ','.join(keyword_list)
                    
                    df = pd.DataFrame({
                        "Filename": [uploaded_file.name],
                        "Description": [desc],
                        "Keywords": [final_keywords],
                        "Categories": [data_dict.get('CATEGORY', 'Animals/Wildlife')],
                        "Illustration": ["No"],
                        "Mature Content": ["No"],
                        "Editorial": ["No"]
                    })
                    
                    st.success("✅ Metadata & CSV Berhasil Digenerate!")
                    st.dataframe(df)
                    
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

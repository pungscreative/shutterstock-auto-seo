import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
import io

st.set_page_config(page_title="Shutterstock Auto SEO & CSV", page_icon="📸", layout="wide")

st.title("📸 Shutterstock Auto-SEO & CSV Generator")
st.markdown("Upload foto, AI **Gemini 3.5 Flash** akan membuatkan metadata dan **file CSV siap upload** ke Shutterstock.")

api_key = st.text_input("Google Gemini API Key:", type="password")
uploaded_file = st.file_uploader("Pilih Foto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, width=300)

    if st.button("Generate SEO & CSV"):
        if not api_key:
            st.error("Masukkan API Key terlebih dahulu!")
        else:
            with st.spinner("🤖 Gemini 3.5 Flash sedang memproses..."):
                try:
                    genai.configure(api_key=api_key)
                    # PERBAIKAN: Menggunakan model gemini-3.5-flash
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    
                    prompt = """
                    Act as a Shutterstock Microstock Expert. Analyze the image.
                    Return ONLY this data structure:
                    TITLE: [A concise, descriptive title]
                    KEYWORDS: [50 relevant keywords, comma separated]
                    CATEGORY: [One category from Shutterstock list]
                    DESCRIPTION: [A detailed description]
                    """
                    
                    response = model.generate_content([prompt, image])
                    text = response.text
                    
                    # Parsing hasil dari AI
                    data_dict = {}
                    for line in text.split('\n'):
                        if ':' in line:
                            k, v = line.split(':', 1)
                            data_dict[k.strip()] = v.strip()
                    
                    # Format Data untuk Shutterstock CSV
                    csv_data = {
                        "Filename": [uploaded_file.name],
                        "Description": [f"{data_dict.get('TITLE', '')} {data_dict.get('DESCRIPTION', '')}"],
                        "Keywords": [data_dict.get('KEYWORDS', '')],
                        "Categories": [data_dict.get('CATEGORY', 'Photography')]
                    }
                    df = pd.DataFrame(csv_data)
                    
                    # Tampilkan preview di web
                    st.success("✅ SEO & CSV Berhasil dibuat dengan Gemini 3.5 Flash!")
                    st.dataframe(df)
                    
                    # Tombol Download CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download File CSV untuk Shutterstock",
                        data=csv,
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_metadata.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

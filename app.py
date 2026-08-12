import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Shutterstock Auto SEO (Gemini 3.5)", page_icon="📸", layout="centered")

st.title("📸 Shutterstock Auto-SEO & Reviewer")
st.markdown("Upload foto Anda dari device mana saja. AI **Gemini 3.5 Flash** akan mereview nilai komersialnya dan membuat **Judul**, **Deskripsi**, serta **50 Keyword** optimal untuk Shutterstock.")

st.info("Menggunakan model terbaru Gemini 3.5 Flash (100% Gratis via Google AI Studio). Masukkan API Key Anda di bawah.")
api_key = st.text_input("Google Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Pilih Foto (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Preview Foto", use_container_width=True)

    if st.button("Automasi Data SEO Shutterstock"):
        if not api_key:
            st.error("⚠️ Silakan masukkan API Key Gemini terlebih dahulu.")
        else:
            with st.spinner("🤖 Gemini 3.5 Flash sedang menganalisis foto dan menyusun SEO optimal..."):
                try:
                    # Konfigurasi API Gemini
                    genai.configure(api_key=api_key)
                    
                    # Menggunakan model gemini-3.5-flash
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    
                    prompt = """
                    Act as a Shutterstock Microstock Expert. Analyze this image and provide data to maximize downloads.
                    Please format the output clearly. Provide the output in this specific format:

                    ### 1. Commercial Review (Bahasa Indonesia)
                    Beri ulasan 2-3 kalimat mengapa foto ini bisa laku dijual, target pasarnya siapa, dan apa kekurangannya (jika ada).

                    ### 2. Title & Description (English - max 200 chars)
                    Provide a highly descriptive, search-friendly title in English. No spam words.

                    ### 3. Top 50 Keywords (English)
                    Provide exactly 50 highly relevant keywords separated by commas. 
                    Sort them strategically: Main subject first, then actions, setting, concepts, and emotional abstract words. DO NOT number them, just comma-separated.

                    ### 4. Suggested Categories
                    Provide 2 best matching Shutterstock categories.
                    """
                    
                    response = model.generate_content([prompt, image])
                    
                    st.success("✅ Data SEO Berhasil Dibuat dengan Gemini 3.5 Flash!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

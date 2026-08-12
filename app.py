import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(page_title="Shutterstock Auto SEO", page_icon="📸", layout="centered")

st.title("📸 Shutterstock Auto-SEO & Reviewer")
st.markdown("Upload foto Anda dari device mana saja. AI akan mereview nilai komersialnya dan membuat **Judul**, **Deskripsi**, serta **50 Keyword** optimal untuk Shutterstock.")

st.info("Aplikasi ini menggunakan OpenAI Vision AI. Masukkan API Key Anda di bawah ini (Aman, tidak disimpan di server).")
api_key = st.text_input("OpenAI API Key:", type="password")

uploaded_file = st.file_uploader("Pilih Foto (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Preview Foto", use_column_width=True)

    if st.button("Automasi Data SEO Shutterstock"):
        if not api_key:
            st.error("⚠️ Silakan masukkan API Key OpenAI terlebih dahulu.")
        else:
            with st.spinner("🤖 AI sedang menganalisis foto, mencari tren pasar, dan menyusun keyword..."):
                try:
                    client = OpenAI(api_key=api_key)
                    base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                    
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
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        },
                                    },
                                ],
                            }
                        ],
                        max_tokens=1000,
                    )
                    
                    result = response.choices[0].message.content
                    st.success("✅ Data SEO Berhasil Dibuat! Silakan copy data di bawah ke Shutterstock.")
                    st.markdown(result)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

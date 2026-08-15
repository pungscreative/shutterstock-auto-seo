import streamlit as st
import pandas as pd
import re
import time
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy Pro | AI SEO Metadata", page_icon="✨", layout="wide")

# CSS Styling - Dark Mode Gradient & Symmetrical Glassmorphism Cards
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

    /* Judul Kartu */
    .card-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        color: #f8fafc;
        margin-bottom: 15px;
    }

    /* Kontainer Kaca Transparan Pekat yang Simetris untuk Kiri & Kanan */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(20, 15, 35, 0.85) !important;
        background-color: rgba(20, 15, 35, 0.85) !important;
        border: 1px solid rgba(192, 132, 252, 0.4) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }

    .stFileUploader label p {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    
    /* Tombol Utama (Generate & Download) */
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

# Inisialisasi Session State untuk Hasil AI Multi-File
if "df_result" not in st.session_state:
    st.session_state.df_result = None

# Header Utama dengan Badge
st.markdown("""
<div class="hero-container">
    <div class="badge-text">✨ AI-POWERED PUNGS CREATIVE</div>
    <h1 class="gradient-title">Nyetok.Kuy Pro</h1>
    <p style="color: #94a3b8; font-weight: 500; font-size: 0.95rem;">Sistem Otomatisasi Metadata Stok Foto Profesional & SEO Optimal</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

# Kolom Kiri: Konfigurasi & Multi-Upload
with col1:
    with st.container(border=True):
        st.markdown('<div class="card-title">⚙️ Konfigurasi & Multi-Upload</div>', unsafe_allow_html=True)
        
        api_key = None
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
            
        if not api_key:
            api_key = st.text_input("🔑 Masukkan Gemini API Key", type="password")
        
        # Aktifkan accept_multiple_files=True
        uploaded_files = st.file_uploader(
            "📁 Drag & Drop atau Klik untuk Upload Banyak Foto (Max 200MB/file)", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} foto berhasil dipilih.")
            with st.expander("🔍 Pratinjau Foto yang Diunggah"):
                for uploaded_file in uploaded_files:
                    st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Kolom Kanan: Hasil Pemrosesan AI Massal
with col2:
    with st.container(border=True):
        st.markdown('<div class="card-title">📊 Hasil Pemrosesan AI Massal</div>', unsafe_allow_html=True)
        
        if uploaded_files and api_key:
            if st.button("🚀 Generate Semua Metadata SEO", type="primary", use_container_width=True):
                all_rows = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_files = len(uploaded_files)
                success_count = 0
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"✨ Memproses foto {idx+1} dari {total_files}: {uploaded_file.name}...")
                    
                    response = None
                    max_retries = 3
                    retry_delay = 2
                    
                    for attempt in range(max_retries):
                        try:
                            client = genai.Client(api_key=api_key.strip())
                            img = Image.open(uploaded_file)
                            
                            prompt = """
                            Act as a professional Shutterstock contributor. 
                            Analyze the image and provide metadata in English format:
                            TITLE: [A concise, commercial search-friendly title]
                            KEYWORDS: [Provide EXACTLY 45 relevant comma-separated keywords without any markdown symbols.]
                            CATEGORY: [Pick one: Animals/Wildlife, Nature, Backgrounds, People, Technology, Food/Drink]
                            DESCRIPTION: [A detailed commercial description]
                            """
                            
                            response = client.models.generate_content(
                                model='gemini-3.5-flash',
                                contents=[prompt, img]
                            )
                            break
                        except Exception as e:
                            err_str = str(e)
                            if ("503" in err_str or "UNAVAILABLE" in err_str) and attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            else:
                                break
                    
                    if response and hasattr(response, 'text'):
                        try:
                            data_dict = {}
                            for line in response.text.split('\n'):
                                if ':' in line:
                                    parts = line.split(':', 1)
                                    clean_key = re.sub(r'[\*\-\#]', '', parts[0]).strip().upper()
                                    clean_val = re.sub(r'^[\*\-\#\s]+', '', parts[1]).strip().replace('[', '').replace(']', '')
                                    data_dict[clean_key] = clean_val
                                    
                            desc = data_dict.get('DESCRIPTION', data_dict.get('TITLE', 'Stock Image'))
                            desc = re.sub(r'[\*]', '', desc)
                            
                            raw_keywords = data_dict.get('KEYWORDS', data_dict.get('KEYWORD', ''))
                            if not raw_keywords:
                                for line in response.text.split('\n'):
                                    if 'keyword' in line.lower() and ':' in line:
                                        raw_keywords = line.split(':', 1)[1].strip().replace('[', '').replace(']', '')
                                        
                            raw_keywords = raw_keywords.replace('**', '').replace('*', '')
                            keyword_list = [k.strip() for k in raw_keywords.split(',') if k.strip()]
                            final_keywords = ', '.join(keyword_list[:50]) if keyword_list else "stock photography, commercial photo, professional image, high quality"
                            
                            all_rows.append({
                                "Filename": uploaded_file.name,
                                "Description": desc,
                                "Keywords": final_keywords,
                                "Categories": data_dict.get('CATEGORY', 'Animals/Wildlife'),
                                "Illustration": "No",
                                "Mature Content": "No",
                                "Editorial": "No"
                            })
                            success_count += 1
                        except Exception:
                            pass
                    
                    progress_bar.progress((idx + 1) / total_files)
                    
                status_text.empty()
                progress_bar.empty()
                
                if all_rows:
                    st.session_state.df_result = pd.DataFrame(all_rows)
                    st.success(f"🎉 Berhasil memproses {success_count} dari {total_files} foto!")
                else:
                    st.error("Gagal memproses kumpulan foto. Periksa kembali API Key atau koneksi Anda.")
            
            # Tampilkan tabel hasil jika sudah ada
            if st.session_state.df_result is not None:
                st.dataframe(st.session_state.df_result, use_container_width=True)
                
                csv = st.session_state.df_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV Massal Siap Upload", 
                    data=csv, 
                    file_name="nyetok_kuy_bulk_metadata.csv", 
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px;">⚡ Silakan unggah beberapa foto di kolom sebelah kiri untuk mengaktifkan mesin AI massal.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("🚀 Generate Semua Metadata SEO", disabled=True, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>© 2026 Nyetok.Kuy - All Rights Reserved | powered by Pungs Creative</p>", unsafe_allow_html=True)

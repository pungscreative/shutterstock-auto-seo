import streamlit as st
import pandas as pd
from PIL import Image
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from datetime import datetime

st.set_page_config(page_title="Shutterstock Pro Studio", layout="wide")

st.title("✨ Shutterstock Pro Studio (Vertex AI Mode)")

# Masukkan Project ID yang terlihat di gambar Baginda (489544160497)
project_id = st.text_input("Project ID:", value="489544160497")
uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])

if uploaded_file and project_id:
    if st.button("Generate SEO Metadata"):
        try:
            # Inisialisasi Vertex AI
            vertexai.init(project=project_id, location="us-central1")
            model = GenerativeModel("gemini-1.5-flash-001")
            
            img_bytes = uploaded_file.getvalue()
            image_part = Part.from_data(data=img_bytes, mime_type="image/jpeg")
            
            prompt = """
            Act as a professional Shutterstock contributor. 
            Provide metadata in English:
            TITLE: [Concise title]
            KEYWORDS: [50 comma-separated keywords]
            CATEGORY: [Nature, People, Technology, or Backgrounds]
            DESCRIPTION: [Detailed description]
            """
            
            response = model.generate_content([prompt, image_part])
            
            st.success("Berhasil!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error Vertex AI: {e}")

# ... (Simpan bagian CSS/Header/Layout yang sama seperti sebelumnya)

# BAGIAN UTAMA LOGIKA PEMROSESAN CSV
                        # ... (Setelah mendapatkan response dari Gemini)
                        
                        # Parsing data dari AI (tetap dalam bahasa Inggris untuk SEO global)
                        data_dict = {}
                        for line in text.split('\n'):
                            if ':' in line:
                                k, v = line.split(':', 1)
                                data_dict[k.strip()] = v.strip()
                        
                        # FORMAT CSV YANG SESUAI STANDAR SHUTTERSTOCK
                        # Menambahkan kolom wajib: Editorial, Date Created, Location
                        csv_data = {
                            "Filename": [uploaded_file.name],
                            "Description": [f"{data_dict.get('TITLE', '')} {data_dict.get('DESCRIPTION', '')}"],
                            "Keywords": [data_dict.get('KEYWORDS', '')],
                            "Categories": [data_dict.get('CATEGORY', 'Animals/Wildlife')],
                            "Editorial": [0],             # 0 = Komersial, 1 = Editorial
                            "Date Created": ["2026-08-12"], 
                            "Location": ["Mataram"]
                        }
                        
                        df = pd.DataFrame(csv_data)
                        
                        st.success("✅ SEO & CSV Berhasil Digenerate dengan Format Standar Shutterstock!")
                        
                        # Preview Hasil Tabel
                        st.dataframe(df, use_container_width=True)
                        
                        # Download CSV dengan format yang benar
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download File CSV Shutterstock",
                            data=csv,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_shutterstock.csv",
                            mime="text/csv"
                        )
# ...

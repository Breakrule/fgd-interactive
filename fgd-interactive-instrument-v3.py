import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Aplikasi Web Kuesioner FGD Geopark Kotabaru",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "data_kuesioner_fgd.csv"

# Predefined Questions Definition
QUESTIONS = [
    {"id": "Q_01", "pilar": "Pilar 1: Geodiversity", "aspek": "Konservasi & Legalitas", "teks": "Pemerintah daerah dan masyarakat memiliki kesadaran tinggi untuk menjaga warisan batuan/geologi di Kotabaru agar terhindar dari perusakan."},
    {"id": "Q_02", "pilar": "Pilar 1: Geodiversity", "aspek": "Konservasi & Legalitas", "teks": "Dinas-dinas terkait sepakat bahwa penetapan Kawasan Cagar Alam Geologi (KCAG) sangat penting sebagai payung hukum awal perlindungan geosite."},
    {"id": "Q_03", "pilar": "Pilar 1: Geodiversity", "aspek": "Edukasi Kebumian", "teks": "Instansi Anda mendukung integrasi nilai geodiversity ke dalam kurikulum muatan lokal sekolah dasar (Bumi & Alam Saijaan Bersujud)."},
    {"id": "Q_04", "pilar": "Pilar 1: Geodiversity", "aspek": "Ekowisata & Geotourism", "teks": "Peta digital pariwisata geologi dan papan informasi (QR Code) di 3 geosite utama Kotabaru mendesak untuk segera diselesaikan dalam jangka pendek."},
    {"id": "Q_05", "pilar": "Pilar 2: Biodiversity", "aspek": "Konservasi Hayati", "teks": "Program rehabilitasi vegetasi khas pesisir/mangrove di sekitar geosite merupakan prioritas penting yang harus disinergikan antar instansi."},
    {"id": "Q_06", "pilar": "Pilar 2: Biodiversity", "aspek": "Edukasi & Eduwisata", "teks": "Masyarakat lokal di lingkar geosite memiliki potensi besar untuk menjadi agen aktif dalam perlindungan flora-fauna endemik."},
    {"id": "Q_07", "pilar": "Pilar 3: Cultural Diversity", "aspek": "Pelestarian Budaya", "teks": "Kesenian daerah dan tradisi adat pesisir Kotabaru harus dipadukan dalam pameran geosite sebagai representasi identitas Geopark."},
    {"id": "Q_08", "pilar": "Pilar 3: Cultural Diversity", "aspek": "Ekonomi Kreatif", "teks": "Pengembangan kuliner gastronomi lokal (Geo-products) bermerek Geopark Kotabaru dapat secara efektif mendongkrak kesejahteraan UMKM lokal."},
    {"id": "Q_09", "pilar": "Pilar 3: Cultural Diversity", "aspek": "Promosi Kebudayaan", "teks": "Integrasi pameran geopark ke dalam agenda tahunan Festival Budaya Saijaan merupakan langkah promosi yang ideal dan efisien."},
    {"id": "Q_10", "pilar": "Sinergi Lintas Sektor", "aspek": "Komitmen Sektoral", "teks": "Seluruh perangkat daerah/OPD di Kotabaru siap mengesampingkan ego sektoral untuk berkolaborasi mengelola program Geopark secara terpadu."},
    {"id": "Q_11", "pilar": "Sinergi Lintas Sektor", "aspek": "Pembagian Peran (RACI)", "teks": "Struktur pembagian peran (RACI Matrix) lintas OPD dalam draf Road Map V3 (termasuk peran strategis BKPSDMD dan Dinas ESDM) dinilai sudah adil, operasional, dan jelas."},
    {"id": "Q_12", "pilar": "Sinergi Lintas Sektor", "aspek": "Keberlanjutan Anggaran", "teks": "Instansi Anda berkomitmen untuk merefokusing dan menyinkronkan anggaran internal OPD guna mendukung pemeliharaan kawasan Geopark."},
    {"id": "Q_13", "pilar": "Sinergi Lintas Sektor", "aspek": "Kapasitas Pemandu (Geo-Guides)", "teks": "Pelatihan dan sertifikasi pemandu wisata lokal (Geo-Guides) sangat penting untuk segera dilakukan oleh Disparpora bersama akademisi."},
    {"id": "Q_14", "pilar": "Sinergi Lintas Sektor", "aspek": "Sistem Informasi Terintegrasi", "teks": "Pengembangan One Data Geopark sangat membantu OPD dalam berbagi data spasial, data kunjungan, dan data kelestarian lingkungan."},
    {"id": "Q_15", "pilar": "Sinergi Lintas Sektor", "aspek": "Pemantauan Kinerja", "teks": "Penggunaan Dashboard Monitoring dinilai efektif sebagai sistem pengawasan mandiri bagi pimpinan daerah (Bupati/Sekda) untuk melacak target OPD."}
]

OPD_LIST = [
    "Sekretariat Daerah (Setda)",
    "Bapperida",
    "Disparpora",
    "Disdikbud",
    "DLH (Dinas Lingkungan Hidup)",
    "Diskominfo",
    "Dinas PUPR",
    "BKPSDMD",
    "Dinas Koperasi, UKM & Perindag",
    "Dinas PMD (Pemberdayaan Masyarakat Desa)",
    "Dinas ESDM Provinsi Kalsel",
    "Badan Pengelola Geopark Meratus",
    "Lainnya / Perwakilan Komunitas / Akademisi"
]

HAMBATAN_OPTIONS = [
    "H-01. Belum dilakukannya refokusing/realokasi program rutin DPA OPD untuk kegiatan berdampak",
    "H-02. Keterbatasan staf teknis & kompetensi spesifik (butuh pembinaan/pelatihan BKPSDMD)",
    "H-03. Ketidakjelasan pembagian wewenang & rincian SOP teknis antar-instansi",
    "H-04. Kurangnya pemahaman & penyamaan persepsi internal OPD tentang Road Map Geopark",
    "H-05. Regulasi & juknis operasional tingkat daerah yang belum diundangkan",
    "H-06. Kendala geografis & integrasi pemetaan lokasi geosite",
    "Lainnya (Tulis pada Catatan Bebas)"
]

DUKUNGAN_OPTIONS = [
    "D-01. Merekalibrasi & merealokasi anggaran DPA OPD untuk program berdampak Geopark",
    "D-02. Menugaskan staf aktif masuk Tim Teknis Geopark (koordinasi BKPSDMD)",
    "D-03. Menyediakan & mengintegrasikan data sektoral ke One Data Geopark",
    "D-04. Menyinkronkan indikator program kerja rutin dengan Road Map Geopark",
    "D-05. Mengoptimalkan publikasi & kampanye edukasi melalui media resmi OPD",
    "Lainnya (Tulis pada Catatan Bebas)"
]

PRIORITAS_OPTIONS = [
    "P-01. Penguatan legalitas wilayah geosite & usulan Kawasan Cagar Alam Geologi (KCAG)",
    "P-02. Pembangunan infrastruktur dasar & papan info geosite",
    "P-03. Edukasi sekolah melalui kurikulum muatan lokal & ASN sharing session",
    "P-04. Pelatihan Pokdarwis & sertifikasi pemandu lokal (Geo-guides)",
    "P-05. Promosi ekowisata terpadu & fasilitasi kemitraan produk lokal (Geo-products)",
    "Lainnya (Tulis pada Catatan Bebas)"
]

# Helper function to load dataset
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create empty DataFrame with required schema
        columns = [
            "timestamp", "nama_responden", "jabatan", "instansi_opd",
            "Q_01", "Q_02", "Q_03", "Q_04", "Q_05", "Q_06", "Q_07", "Q_08",
            "Q_09", "Q_10", "Q_11", "Q_12", "Q_13", "Q_14", "Q_15",
            "hambatan_utama", "komitmen_dukungan", "prioritas_program", "catatan_bebas"
        ]
        return pd.DataFrame(columns=columns)

# Helper function to save dataset
def save_response(row_dict):
    df = load_data()
    df_new = pd.DataFrame([row_dict])
    df_updated = pd.concat([df, df_new], ignore_index=True)
    df_updated.to_csv(DATA_FILE, index=False)

# App UI
st.sidebar.image("https://img.icons8.com/color/96/earth-element.png", width=80)
st.sidebar.title("Kuesioner FGD Geopark")
st.sidebar.caption("Kabupaten Kotabaru - Klaster Saijaan Bersujud")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Pilih Menu Aplikasi:",
    ["📝 Input Kuesioner OPD", "📊 Quick Count Real-Time", "🗂️ Rekapitulasi Data Responden"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Sistem Pemantauan Terpadu FGD**\n\n"
    "Aplikasi ini secara otomatis merekam masukan OPD dan menghitung analisis kesiapan daerah secara real-time."
)

# ---------------------------------------------------------
# MENU 1: INPUT KUESIONER OPD
# ---------------------------------------------------------
if menu == "📝 Input Kuesioner OPD":
    st.title("📝 Form Kuesioner Persepsi Pemangku Kepentingan")
    st.caption("Aplikasi Input Data Resmi FGD I: Integrasi Road Map Geopark Kotabaru V3")
    
    st.markdown("""
    ---
    ### 👤 **Bagian 1: Identitas / Biodata Responden**
    *Mohon lengkapi data responden dari instansi/OPD Anda sebelum mengisi pertanyaan kuesioner.*
    """)
    
    with st.form("form_kuesioner_opd"):
        col_bio1, col_bio2, col_bio3 = st.columns(3)
        with col_bio1:
            nama = st.text_input("Nama Lengkap Responden *", placeholder="Contoh: Dr. H. Ahmad, M.Si")
        with col_bio2:
            jabatan = st.text_input("Jabatan Responden *", placeholder="Contoh: Kepala Bidang / Analis Kebijakan")
        with col_bio3:
            instansi = st.selectbox("Instansi / Perangkat Daerah (OPD) *", OPD_LIST)
            
        st.markdown("""
        ---
        ### 📊 **Bagian 2: Penilaian Kuantitatif (Skala Likert 1 - 5)**
        *Petunjuk Skor: **1** = Sangat Tidak Setuju, **2** = Tidak Setuju, **3** = Cukup Setuju, **4** = Setuju, **5** = Sangat Setuju.*
        """)
        
        scores = {}
        
        # Group questions by Pilar
        pilars = ["Pilar 1: Geodiversity", "Pilar 2: Biodiversity", "Pilar 3: Cultural Diversity", "Sinergi Lintas Sektor"]
        for pilar in pilars:
            st.subheader(f"📌 {pilar}")
            pilar_qs = [q for q in QUESTIONS if q["pilar"] == pilar]
            for q in pilar_qs:
                col_q1, col_q2 = st.columns([3, 1])
                with col_q1:
                    st.markdown(f"**[{q['id']}] {q['aspek']}**\n\n{q['teks']}")
                with col_q2:
                    scores[q["id"]] = st.slider(
                        f"Skor {q['id']}", 
                        min_value=1, 
                        max_value=5, 
                        value=4, 
                        key=f"slider_{q['id']}"
                    )
                st.markdown("<hr style='margin:5px 0; border:0.5px solid #eee;'>", unsafe_allow_html=True)
                
        st.markdown("""
        ---
        ### 🎯 **Bagian 3: Pilihan Terpandu Opsi Strategis (Analisis Kualitatif)**
        *Pilihlah satu opsi paling dominan untuk menggambarkan kondisi instansi Anda.*
        """)
        
        col_opt1, col_opt2, col_opt3 = st.columns(3)
        with col_opt1:
            hambatan = st.selectbox("Hambatan Utama Instansi:", HAMBATAN_OPTIONS)
        with col_opt2:
            dukungan = st.selectbox("Bentuk Komitmen Dukungan Riil:", DUKUNGAN_OPTIONS)
        with col_opt3:
            prioritas = st.selectbox("Prioritas Utama Program:", PRIORITAS_OPTIONS)
            
        st.markdown("---")
        st.markdown("### 💬 **Bagian 4: Catatan Bebas & Usulan Solusi**")
        catatan = st.text_area("Tuliskan argumen tambahan, penjelasan hambatan, atau usulan program baru dari instansi Anda:", placeholder="Tuliskan catatan teknis di sini...")
        
        submitted = st.form_submit_button("🚀 Kirim Jawaban Kuesioner OPD")
        
        if submitted:
            if not nama or not jabatan:
                st.error("⚠️ Nama Lengkap dan Jabatan wajib diisi!")
            else:
                row_dict = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nama_responden": nama,
                    "jabatan": jabatan,
                    "instansi_opd": instansi,
                    "hambatan_utama": hambatan,
                    "komitmen_dukungan": dukungan,
                    "prioritas_program": prioritas,
                    "catatan_bebas": catatan
                }
                # Add score values
                for q_id, val in scores.items():
                    row_dict[q_id] = val
                    
                save_response(row_dict)
                st.balloons()
                st.success(f"✅ Terima kasih **{nama}** ({instansi})! Jawaban kuesioner Anda berhasil disimpan dan langsung masuk ke Quick Count Real-Time.")

# ---------------------------------------------------------
# MENU 2: QUICK COUNT REAL-TIME
# ---------------------------------------------------------
elif menu == "📊 Quick Count Real-Time":
    st.title("📊 Quick Count Real-Time Hasil Kuesioner FGD")
    st.caption("Hasil analisis otomatis persepsi stakeholder dan kesiapan daerah")
    
    df = load_data()
    
    if df.empty:
        st.warning("📥 Belum ada data kuesioner yang masuk. Silakan isi kuesioner pada menu 'Input Kuesioner OPD'.")
    else:
        # Top KPI Cards
        total_respondents = len(df)
        total_opd = df["instansi_opd"].nunique()
        
        # Calculate overall score
        q_cols = [f"Q_{i:02d}" for i in range(1, 16)]
        avg_overall = df[q_cols].values.mean()
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Total Responden", f"{total_respondents} Orang")
        with col_m2:
            st.metric("OPD / Instansi Terlibat", f"{total_opd} OPD")
        with col_m3:
            st.metric("Rata-Rata Skor Total", f"{avg_overall:.2f} / 5.0")
        with col_m4:
            status_global = "Sangat Siap" if avg_overall >= 4.5 else "Siap / Setuju" if avg_overall >= 3.5 else "Cukup Siap" if avg_overall >= 2.5 else "Belum Siap"
            st.metric("Tingkat Kesiapan Kumulatif", status_global)
            
        st.markdown("---")
        
        # Pillar Progress Breakdown
        st.subheader("📈 Rata-Rata Skor Persepsi per Pilar Utama Geopark")
        
        pilar_mapping = {
            "Pilar 1: Geodiversity": ["Q_01", "Q_02", "Q_03", "Q_04"],
            "Pilar 2: Biodiversity": ["Q_05", "Q_06"],
            "Pilar 3: Cultural Diversity": ["Q_07", "Q_08", "Q_09"],
            "Sinergi Lintas Sektor & Tata Kelola": ["Q_10", "Q_11", "Q_12", "Q_13", "Q_14", "Q_15"]
        }
        
        pilar_scores = []
        for p_name, cols in pilar_mapping.items():
            score = df[cols].values.mean()
            status = "Sangat Siap" if score >= 4.5 else "Siap / Setuju" if score >= 3.5 else "Cukup Siap" if score >= 2.5 else "Belum Siap"
            pilar_scores.append({"Pilar / Dimensi": p_name, "Rerata Skor": round(score, 2), "Status Kesiapan": status})
            
        df_pilar = pd.DataFrame(pilar_scores)
        
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.bar_chart(df_pilar.set_index("Pilar / Dimensi")["Rerata Skor"])
        with col_p2:
            st.dataframe(df_pilar, use_container_width=True, hide_index=True)
            
        st.markdown("---")
        
        # Quick Count for Predefined Options (Hambatan, Dukungan, Prioritas)
        st.subheader("📊 Analytics Quick Count Pilihan Terpandu Kualitatif")
        
        tab_h, tab_d, tab_p = st.tabs(["⚠️ Hambatan Utama", "🤝 Komitmen Dukungan", "🎯 Prioritas Program"])
        
        with tab_h:
            st.markdown("#### **Frekuensi Hambatan Utama OPD**")
            h_counts = df["hambatan_utama"].value_counts().reset_index()
            h_counts.columns = ["Opsi Hambatan", "Jumlah OPD"]
            st.bar_chart(h_counts.set_index("Opsi Hambatan"))
            st.table(h_counts)
            
        with tab_d:
            st.markdown("#### **Frekuensi Komitmen Dukungan Riil OPD**")
            d_counts = df["komitmen_dukungan"].value_counts().reset_index()
            d_counts.columns = ["Opsi Komitmen", "Jumlah OPD"]
            st.bar_chart(d_counts.set_index("Opsi Komitmen"))
            st.table(d_counts)
            
        with tab_p:
            st.markdown("#### **Frekuensi Prioritas Utama Program**")
            p_counts = df["prioritas_program"].value_counts().reset_index()
            p_counts.columns = ["Opsi Prioritas", "Jumlah OPD"]
            st.bar_chart(p_counts.set_index("Opsi Prioritas"))
            st.table(p_counts)

# ---------------------------------------------------------
# MENU 3: REKAPITULASI DATA RESPONDEN
# ---------------------------------------------------------
else:
    st.title("🗂️ Rekapitulasi Data Responden & Jawaban Mentah")
    st.caption("Daftar lengkap masukan OPD yang siap diunduh untuk bahan Laporan Risalah FGD")
    
    df = load_data()
    
    if df.empty:
        st.info("📥 Belum ada data kuesioner yang tersimpan.")
    else:
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Seluruh Data Kuesioner (Format CSV / Excel)",
            data=csv,
            file_name=f"kuesioner_fgd_geopark_kotabaru_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.markdown("### 💬 **Daftar Catatan & Usulan Bebas OPD**")
        for idx, row in df.iterrows():
            if pd.notna(row['catatan_bebas']) and str(row['catatan_bebas']).strip() != "":
                st.info(f"**{row['instansi_opd']}** ({row['nama_responden']} - {row['jabatan']}):\n\n\"{row['catatan_bebas']}\"")

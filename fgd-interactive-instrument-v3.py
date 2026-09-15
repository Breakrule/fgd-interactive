import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Aplikasi Web Kuesioner FGD Geopark Kotabaru",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "data_kuesioner_fgd.csv"

# Separator used to join multiple selected options into a single CSV cell
MULTI_SEPARATOR = " | "

# Predefined Questions Definition
QUESTIONS = [
    {"id": "Q_01", "pilar": "Pilar 1: Geodiversity", "aspek": "Konservasi & Legalitas", "teks": "Pemerintah daerah dan masyarakat memiliki kesadaran tinggi untuk menjaga warisan batuan/geologi di Kotabaru agar terhindar dari perusakan."},
    {"id": "Q_02", "pilar": "Pilar 1: Geodiversity", "aspek": "Konservasi & Legalitas", "teks": "Dinas-dinas terkait sepakat bahwa penetapan Kawasan Cagar Alam Geologi (KCAG) sangat penting sebagai payung hukum awal perlindungan geosite."},
    {"id": "Q_03", "pilar": "Pilar 1: Geodiversity", "aspek": "Edukasi Kebumian", "teks": "Instansi Anda mendukung integrasi nilai geodiversity ke dalam kurikulum muatan lokal sekolah dasar (Bumi & Alam Saijaan)."},
    {"id": "Q_04", "pilar": "Pilar 1: Geodiversity", "aspek": "Ekowisata & Geotourism", "teks": "Peta digital pariwisata geologi dan papan informasi (QR Code) di geosite Kotabaru untuk segera diselesaikan dalam jangka pendek."},
    {"id": "Q_05", "pilar": "Pilar 2: Biodiversity", "aspek": "Konservasi Hayati", "teks": "Program rehabilitasi vegetasi khas di sekitar geosite merupakan prioritas penting yang harus disinergikan antar instansi."},
    {"id": "Q_06", "pilar": "Pilar 2: Biodiversity", "aspek": "Edukasi & Eduwisata", "teks": "Masyarakat lokal di lingkar geosite memiliki potensi besar untuk menjadi agen aktif dalam perlindungan flora-fauna endemik."},
    {"id": "Q_07", "pilar": "Pilar 3: Cultural Diversity", "aspek": "Pelestarian Budaya", "teks": "Kesenian daerah dan tradisi adat pesisir Kotabaru harus dipadukan dalam pameran geosite sebagai representasi identitas Geopark."},
    {"id": "Q_08", "pilar": "Pilar 3: Cultural Diversity", "aspek": "Ekonomi Kreatif", "teks": "Pengembangan kuliner gastronomi lokal (Geo-products) bermerek Geopark Kotabaru dapat secara efektif mendongkrak kesejahteraan UMKM lokal."},
    {"id": "Q_09", "pilar": "Pilar 3: Cultural Diversity", "aspek": "Promosi Kebudayaan", "teks": "Integrasi pameran geopark ke dalam agenda tahunan Festival Budaya Saijaan merupakan langkah promosi yang ideal dan efisien."},
    {"id": "Q_10", "pilar": "Sinergi Lintas Sektor", "aspek": "Komitmen Sektoral", "teks": "Perangkat daerah/OPD di Kotabaru siap mengesampingkan ego sektoral untuk berkolaborasi mengelola program Geopark secara terpadu."},
    {"id": "Q_11", "pilar": "Sinergi Lintas Sektor", "aspek": "Pembagian Peran (RACI)", "teks": "Struktur pembagian peran (RACI Matrix) lintas OPD dalam draf Road Map dinilai sudah adil, operasional, dan jelas."},
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

# Helper function to count multi-select options stored as joined strings
def count_multi_options(series, separator=MULTI_SEPARATOR):
    from collections import Counter
    counter = Counter()
    for val in series.dropna():
        for opt in str(val).split(separator):
            opt = opt.strip()
            if opt:
                counter[opt] += 1
    df_counts = pd.DataFrame(
        [(opt, cnt) for opt, cnt in counter.items()],
        columns=["Opsi", "Jumlah"]
    )
    if not df_counts.empty:
        df_counts = df_counts.sort_values("Jumlah", ascending=False).reset_index(drop=True)
    return df_counts


# =========================================================
# CGK MONITORING DASHBOARD - ROAD MAP V3 GROUNDED DATA
# =========================================================
CGK_RAW_DATA = [
    {
        "No": 1,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Kelembagaan",
        "Program / Kegiatan Kerja": "Pembentukan Tim Agile",
        "Deskripsi Ringkas Kegiatan": "Pembentukan tim koordinasi internal & agile team untuk menyusun pondasi awal rencana aksi.",
        "OPD Penanggung Jawab (Lead)": "Sekretariat Daerah (Asisten III)",
        "OPD Pendukung & Peran RACI": "Bapperida (R), Bagian Organisasi (R), Bagian Hukum (R), BKPSDMD (R)",
        "Indikator Keberhasilan (KPI)": "Tersusunnya SK Tim Kerja & pembagian tugas.",
        "Dashboard / One Data Integration": "Terintegrasi dalam platform monitoring Tim GCG.",
        "Timeline Detail": "Agustus 2026 (Mg 1-2)",
        "Status": "Selesai"
    },
    {
        "No": 2,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Regulasi",
        "Program / Kegiatan Kerja": "Penyusunan Draft Keputusan & Perbup GCG",
        "Deskripsi Ringkas Kegiatan": "Menyusun draf Peraturan Bupati tentang Tata Kelola Kolaboratif Lintas Perangkat Daerah dalam mendukung Geopark Kotabaru.",
        "OPD Penanggung Jawab (Lead)": "Sekretariat Daerah (Asisten III)",
        "OPD Pendukung & Peran RACI": "Bagian Hukum (R), Bapperida (C), Disparpora (C)",
        "Indikator Keberhasilan (KPI)": "Tersedianya Draft Perbup GCG & Keputusan Bupati.",
        "Dashboard / One Data Integration": "Dokumen draf diunggah ke One Data Geopark.",
        "Timeline Detail": "Agustus 2026 (Mg 3-4)",
        "Status": "Selesai"
    },
    {
        "No": 3,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "SOP",
        "Program / Kegiatan Kerja": "Penyusunan SOP Tata Kelola Kolaboratif",
        "Deskripsi Ringkas Kegiatan": "Penyusunan Standar Operasional Prosedur (SOP) Tata Kelola Kolaboratif Lintas Perangkat Daerah sebagai pedoman kerja bersama.",
        "OPD Penanggung Jawab (Lead)": "Sekretariat Daerah (Asisten III)",
        "OPD Pendukung & Peran RACI": "Bagian Organisasi (R), Bagian Hukum (R), Bapperida (C)",
        "Indikator Keberhasilan (KPI)": "Tersedianya dokumen SOP Tata Kelola Kolaboratif.",
        "Dashboard / One Data Integration": "Dokumen SOP diunggah ke One Data Geopark.",
        "Timeline Detail": "Agustus 2026 (Mg 4-5)",
        "Status": "Selesai"
    },
    {
        "No": 4,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Sinergi Lintas Sektor",
        "Program / Kegiatan Kerja": "Rapat Koordinasi & Sinkronisasi Awal Tim GCG",
        "Deskripsi Ringkas Kegiatan": "Rapat koordinasi awal dengan Dinas ESDM Provinsi Kalsel & Pengelola Geopark Meratus untuk sinkronisasi kerangka rencana aksi.",
        "OPD Penanggung Jawab (Lead)": "Bapperida",
        "OPD Pendukung & Peran RACI": "Sekretariat Daerah (R), Dinas ESDM Provinsi (C), Geopark Meratus (C)",
        "Indikator Keberhasilan (KPI)": "Berita Acara kesepakatan koordinasi & kerangka action plan.",
        "Dashboard / One Data Integration": "Hasil notulensi diintegrasikan ke Dashboard Monitoring.",
        "Timeline Detail": "Agustus 2026 (Mg 3-5)",
        "Status": "Selesai"
    },
    {
        "No": 5,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Pilar 1: Geodiversity",
        "Aspek Fungsional": "Konservasi",
        "Program / Kegiatan Kerja": "Pengenalan awal Geodiversity (Survei Lapangan)",
        "Deskripsi Ringkas Kegiatan": "Pengenalan lapangan kondisi fisik geosite unggulan di Kotabaru bersama tim agile dan ahli geologi.",
        "OPD Penanggung Jawab (Lead)": "Bapperida",
        "OPD Pendukung & Peran RACI": "Dinas ESDM Prov (R), Bapperida (R)",
        "Indikator Keberhasilan (KPI)": "Dokumen hasil survei, koordinat peta geosite, & foto dokumentasi.",
        "Dashboard / One Data Integration": "Data spasial geosite dipetakan ke One Data Geopark.",
        "Timeline Detail": "September 2026 (Mg 2-3)",
        "Status": "Belum Mulai"
    },
    {
        "No": 6,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Regulasi & Sosialisasi",
        "Program / Kegiatan Kerja": "Sosialisasi Potensi Geopark dan Perbup",
        "Deskripsi Ringkas Kegiatan": "Sosialisasi draf Peraturan Bupati tentang GCG dan potensi Geopark Kotabaru kepada seluruh perangkat daerah dan pemangku kepentingan.",
        "OPD Penanggung Jawab (Lead)": "Bapperida",
        "OPD Pendukung & Peran RACI": "Sekretariat Daerah (R), Disparpora (R), DLH (C)",
        "Indikator Keberhasilan (KPI)": "Terselenggaranya pertemuan sosialisasi draf Perbup GCG.",
        "Dashboard / One Data Integration": "Dokumen sosialisasi diunggah ke One Data Geopark.",
        "Timeline Detail": "September 2026 (Mg 1-2)",
        "Status": "Belum Mulai"
    },
    {
        "No": 7,
        "Jangka Waktu": "Jangka Pendek (0-2 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Regulasi dan Kelembagaan",
        "Program / Kegiatan Kerja": "Pengesahan & Sosialisasi Perbup GCG",
        "Deskripsi Ringkas Kegiatan": "Harmonisasi, pengesahan, dan sosialisasi Peraturan Bupati Kotabaru tentang Tata Kelola Kolaboratif Pendukung Geopark.",
        "OPD Penanggung Jawab (Lead)": "Sekretariat Daerah (Asisten III), Bapperida",
        "OPD Pendukung & Peran RACI": "Bagian Hukum (R), Disparpora (R), Bapperida (R), Seluruh OPD (I)",
        "Indikator Keberhasilan (KPI)": "Perbup GCG diundangkan dan disosialisasikan ke 100% OPD terkait.",
        "Dashboard / One Data Integration": "Salinan Perbup digital dipublikasikan di One Data Geopark.",
        "Timeline Detail": "November - Desember 2026",
        "Status": "Belum Mulai"
    },
    {
        "No": 8,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Kelembagaan",
        "Program / Kegiatan Kerja": "Pembentukan Tim Koordinasi Geopark Permanen",
        "Deskripsi Ringkas Kegiatan": "Pembentukan tim koordinasi permanen lintas perangkat daerah melalui Keputusan Bupati untuk mengawal keberlanjutan program.",
        "OPD Penanggung Jawab (Lead)": "Sekretariat Daerah (Asisten III)",
        "OPD Pendukung & Peran RACI": "Bapperida (R), Bagian Organisasi (R), Bagian Hukum (R), BKPSDMD (R)",
        "Indikator Keberhasilan (KPI)": "Terbitnya SK Bupati tentang pembentukan Tim Koordinasi Geopark.",
        "Dashboard / One Data Integration": "Struktur forum dan kontak person terintegrasi di Dashboard.",
        "Timeline Detail": "November 2026 - Januari 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 9,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Sistem Informasi",
        "Program / Kegiatan Kerja": "Pengembangan Dashboard Monitoring GCG / Forum KOLABORASI",
        "Deskripsi Ringkas Kegiatan": "Membangun prototype aplikasi Dashboard Monitoring terintegrasi untuk melacak realisasi program kerja fisik & keuangan geopark.",
        "OPD Penanggung Jawab (Lead)": "Diskominfo",
        "OPD Pendukung & Peran RACI": "Bapperida (R), Inspektorat (C), Seluruh OPD (I)",
        "Indikator Keberhasilan (KPI)": "Aplikasi dashboard monitoring GCG aktif dan dapat diakses tim.",
        "Dashboard / One Data Integration": "Sistem dashboard terintegrasi penuh dengan server One Data Kotabaru.",
        "Timeline Detail": "Januari - Maret 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 10,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Sistem Informasi",
        "Program / Kegiatan Kerja": "Penyebarluasan Informasi",
        "Deskripsi Ringkas Kegiatan": "Penyebarluasan informasi rutin terkait perkembangan dan pencapaian geopark di Kabupaten Kotabaru kepada masyarakat.",
        "OPD Penanggung Jawab (Lead)": "Diskominfo",
        "OPD Pendukung & Peran RACI": "Bapperida (C), Disparpora (C)",
        "Indikator Keberhasilan (KPI)": "Publikasi informasi rutin tentang Geopark di media daerah.",
        "Dashboard / One Data Integration": "Konten berita diintegrasikan ke portal resmi Geopark.",
        "Timeline Detail": "Desember 2026 - Februari 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 11,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Edukasi",
        "Program / Kegiatan Kerja": "FGD I: Integrasi Hasil Kajian Akademis",
        "Deskripsi Ringkas Kegiatan": "Focus Group Discussion ke-1 untuk mengintegrasikan hasil kajian akademis kebumian Dinas ESDM ke dalam program kegiatan SKPD terkait.",
        "OPD Penanggung Jawab (Lead)": "Bapperida",
        "OPD Pendukung & Peran RACI": "Dinas ESDM Prov (R), Disparpora (R), DLH (C), Tokoh Masyarakat (C)",
        "Indikator Keberhasilan (KPI)": "Draf rencana aksi terintegrasi pilar Geodiversity, Biodiversity, & Cultural Diversity.",
        "Dashboard / One Data Integration": "Dokumen FGD diunggah ke Dashboard GCG.",
        "Timeline Detail": "September 2026 (Mg 4-5)",
        "Status": "Belum Mulai"
    },
    {
        "No": 12,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Pilar 1: Geodiversity",
        "Aspek Fungsional": "Edukasi",
        "Program / Kegiatan Kerja": "Pembuatan Modul Ajar Muatan Lokal Geopark",
        "Deskripsi Ringkas Kegiatan": "Menyusun kurikulum muatan lokal sekolah dasar 'Bumi & Alam Saijaan Bersujud' untuk mengedukasi siswa tentang warisan geologi.",
        "OPD Penanggung Jawab (Lead)": "Disdikbud / BKPSDMD",
        "OPD Pendukung & Peran RACI": "Dinas ESDM Prov (C), Pengelola Geopark (C), Sekolah Dasar (I)",
        "Indikator Keberhasilan (KPI)": "Draf kurikulum & modul muatan lokal sekolah dasar rampung.",
        "Dashboard / One Data Integration": "E-book modul ajar diintegrasikan ke perpustakaan digital daerah.",
        "Timeline Detail": "Februari - April 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 13,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Edukasi & Pelatihan",
        "Program / Kegiatan Kerja": "Sosialisasi Publik & Gerakan 'Geopark Goes to School'",
        "Deskripsi Ringkas Kegiatan": "Kampanye edukasi awal ke sekolah-sekolah di Kotabaru untuk memperkenalkan warisan geologi, konservasi, dan nilai geopark kepada generasi muda.",
        "OPD Penanggung Jawab (Lead)": "Disdikbud",
        "OPD Pendukung & Peran RACI": "Disparpora (R), Dinas ESDM Prov (C), Pengelola Geopark (C), Sekolah (I)",
        "Indikator Keberhasilan (KPI)": "Terselenggaranya sosialisasi di minimal 10 sekolah dasar/menengah.",
        "Dashboard / One Data Integration": "Dokumen laporan sosialisasi terpantau di Dashboard GCG.",
        "Timeline Detail": "September 2026 (Mg 3-4)",
        "Status": "Belum Mulai"
    },
    {
        "No": 14,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Pilar 2: Biodiversity",
        "Aspek Fungsional": "Konservasi",
        "Program / Kegiatan Kerja": "Rehabilitasi Hutan Mangrove & Vegetasi Geosite",
        "Deskripsi Ringkas Kegiatan": "Program penanaman kembali bibit bakau dan tanaman endemik di sekitar pesisir geosite pesisir Kotabaru.",
        "OPD Penanggung Jawab (Lead)": "DLH",
        "OPD Pendukung & Peran RACI": "Dinas Perikanan (R), Komunitas Peduli Lingkungan (R), Swasta/CSR (C)",
        "Indikator Keberhasilan (KPI)": "Penanaman minimal 1.000 bibit mangrove dan vegetasi pelindung.",
        "Dashboard / One Data Integration": "Jumlah pohon tertanam & koordinat area dilaporkan di Dashboard.",
        "Timeline Detail": "Maret - Juni 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 15,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Pilar 3: Cultural Diversity",
        "Aspek Fungsional": "Kesejahteraan Ekonomi",
        "Program / Kegiatan Kerja": "Pembinaan UMKM & Pengembangan Geo-products",
        "Deskripsi Ringkas Kegiatan": "Pelatihan bagi UMKM lokal untuk meluncurkan produk gastronomi / kuliner khas dan kerajinan tangan bermerek Geopark Kotabaru.",
        "OPD Penanggung Jawab (Lead)": "Disparpora/Diskoperindag",
        "OPD Pendukung & Peran RACI": "Dinas Koperasi & UMKM (R), Komunitas Adat (C), Pelaku Usaha (I)",
        "Indikator Keberhasilan (KPI)": "Terbentuknya minimal 5 jenis 'Geo-products' kuliner/gastronomi lokal.",
        "Dashboard / One Data Integration": "Katalog digital Geo-products ditayangkan pada platform pariwisata.",
        "Timeline Detail": "Mei - Juli 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 16,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Pilar 3: Cultural Diversity",
        "Aspek Fungsional": "Kesejahteraan Ekonomi",
        "Program / Kegiatan Kerja": "Penyelenggaraan Festival Budaya & Ekowisata Geopark Kotabaru",
        "Deskripsi Ringkas Kegiatan": "Mengintegrasikan promosi warisan geologi dalam pameran khusus geosite di sela-sela event budaya tahunan (seperti Festival Budaya Saijaan) guna menarik wisatawan.",
        "OPD Penanggung Jawab (Lead)": "Disparpora",
        "OPD Pendukung & Peran RACI": "Disdikbud (R), DLH (C), Komunitas Seni/Budaya (R), Pelaku Usaha (I)",
        "Indikator Keberhasilan (KPI)": "Terlaksananya stand khusus pameran warisan geologi dan pertunjukan budaya bertema bumi.",
        "Dashboard / One Data Integration": "Data statistik kunjungan wisatawan festival dicatat di Dashboard GCG.",
        "Timeline Detail": "Maret - April 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 17,
        "Jangka Waktu": "Jangka Menengah (3-12 Bln)",
        "Pilar Utama": "Pilar 1: Geodiversity",
        "Aspek Fungsional": "Edukasi & Pelatihan",
        "Program / Kegiatan Kerja": "Pelatihan & Sertifikasi Pemandu Wisata Geologi (Geo-Guides)",
        "Deskripsi Ringkas Kegiatan": "Pelatihan teknis bagi pemuda lokal dan Pokdarwis mengenai sejarah geologi Kotabaru, teknik pemanduan, dan konservasi alam.",
        "OPD Penanggung Jawab (Lead)": "Disparpora",
        "OPD Pendukung & Peran RACI": "Dinas ESDM Prov (R), DLH (C), HPI Kotabaru (R), BKPSDMD (C), Komunitas Lokal (I)",
        "Indikator Keberhasilan (KPI)": "Lahirnya minimal 15 pemandu wisata lokal bersertifikat khusus Geopark.",
        "Dashboard / One Data Integration": "Database Geo-Guides berlisensi diunggah ke Dashboard Monitoring.",
        "Timeline Detail": "Mei - Juni 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 18,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Pilar 3: Cultural Diversity",
        "Aspek Fungsional": "Kesejahteraan Ekonomi",
        "Program / Kegiatan Kerja": "Seminar Klaster Saijaan-Bersujud",
        "Deskripsi Ringkas Kegiatan": "Menyelenggarakan seminar ilmiah nasional untuk mengenalkan potensi klaster Saijaan-Bersujud kepada publik dan menarik minat akademisi.",
        "OPD Penanggung Jawab (Lead)": "Bapperida",
        "OPD Pendukung & Peran RACI": "Dinas ESDM Prov (C), DPMD (R), Pelaku Usaha (I)",
        "Indikator Keberhasilan (KPI)": "Terselenggaranya seminar klaster Saijaan-Bersujud.",
        "Dashboard / One Data Integration": "Prosiding seminar digital diunggah ke One Data Geopark.",
        "Timeline Detail": "Maret 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 19,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Sinergi Lintas Sektor",
        "Program / Kegiatan Kerja": "Sinkronisasi Tata Ruang",
        "Deskripsi Ringkas Kegiatan": "Sinkronisasi dan harmonisasi pemanfaatan ruang di Kabupaten Kotabaru agar sesuai dengan zonasi konservasi Geopark.",
        "OPD Penanggung Jawab (Lead)": "PUPR",
        "OPD Pendukung & Peran RACI": "Bapperida (R), DLH (C)",
        "Indikator Keberhasilan (KPI)": "Terlaksananya sinkronisasi tata ruang wilayah Geopark.",
        "Dashboard / One Data Integration": "Data peta RTRW berbasis GIS diintegrasikan ke One Data Geopark.",
        "Timeline Detail": "Juni - Juli 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 20,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Pilar 1: Geodiversity",
        "Aspek Fungsional": "Kesejahteraan Ekonomi",
        "Program / Kegiatan Kerja": "Penyusunan Peta Wisata Geologi & Media Informasi Geosite",
        "Deskripsi Ringkas Kegiatan": "Inisiasi pembuatan brosur digital, peta rute geotourism, dan sistem QR code informasi sejarah geologi pada geosite unggulan Kotabaru.",
        "OPD Penanggung Jawab (Lead)": "Disparpora",
        "OPD Pendukung & Peran RACI": "Dinas ESDM Prov (R), Diskominfo (R)",
        "Indikator Keberhasilan (KPI)": "Rilis peta wisata digital geopark Kotabaru dan pemasangan QR code info di 3 geosite utama.",
        "Dashboard / One Data Integration": "Tautan peta digital dan data geosite diintegrasikan ke One Data Geopark.",
        "Timeline Detail": "September 2026 (Mg 4) - Oktober 2026 (Mg 1)",
        "Status": "Belum Mulai"
    },
    {
        "No": 21,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Kelembagaan",
        "Program / Kegiatan Kerja": "Pelembagaan GCG ke Dokumen Perencanaan Makro",
        "Deskripsi Ringkas Kegiatan": "Mengintegrasikan indikator kinerja geopark & rencana aksi kolaboratif ke dalam dokumen RPJMD, Renstra OPD, dan RKPD.",
        "OPD Penanggung Jawab (Lead)": "Bapperida",
        "OPD Pendukung & Peran RACI": "Sekretariat Daerah (Asisten III) (R), Seluruh OPD (R)",
        "Indikator Keberhasilan (KPI)": "Indikator GCG termuat dalam RKPD & APBD Kabupaten Kotabaru.",
        "Dashboard / One Data Integration": "Target tahunan disinkronkan langsung di Dashboard Perencanaan.",
        "Timeline Detail": "Juli - Agustus 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 22,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Enabler / Tata Kelola",
        "Aspek Fungsional": "Sistem Informasi",
        "Program / Kegiatan Kerja": "Implementasi Integrasi One Data Geopark",
        "Deskripsi Ringkas Kegiatan": "Menyatukan data spasial, data keanekaragaman hayati, data cagar budaya, dan statistik kunjungan ke platform One Data Kotabaru.",
        "OPD Penanggung Jawab (Lead)": "Diskominfo",
        "OPD Pendukung & Peran RACI": "Bapperida (R), Disparpora (R), Disdikbud (R), DLH (R)",
        "Indikator Keberhasilan (KPI)": "Portal data interaktif 'One Data Geopark' rilis publik.",
        "Dashboard / One Data Integration": "Seluruh data terintegrasi ke Portal Satu Data Indonesia (SDI).",
        "Timeline Detail": "September - Oktober 2027",
        "Status": "Belum Mulai"
    },
    {
        "No": 23,
        "Jangka Waktu": "Jangka Panjang (>12 Bln)",
        "Pilar Utama": "Pilar 3: Cultural Diversity",
        "Aspek Fungsional": "Kesejahteraan Ekonomi",
        "Program / Kegiatan Kerja": "Promosi & Sertifikasi Ekowisata Internasional",
        "Deskripsi Ringkas Kegiatan": "Mendaftarkan ekowisata Kotabaru untuk meraih sertifikasi pariwisata berkelanjutan dan mempromosikannya ke jejaring global.",
        "OPD Penanggung Jawab (Lead)": "Disparpora",
        "OPD Pendukung & Peran RACI": "ASCG / GGN Network (C), Agen Travel (I), Media Massa (I)",
        "Indikator Keberhasilan (KPI)": "Geopark Kotabaru masuk ke dalam kalender wisata nasional/global.",
        "Dashboard / One Data Integration": "Statistik wisatawan mancanegara terpantau langsung di Dashboard.",
        "Timeline Detail": "November 2027 - Seterusnya",
        "Status": "Belum Mulai"
    }
]

# =========================================================
# CGK MONITORING DASHBOARD - RENDER FUNCTION
# =========================================================
def render_cgk_dashboard(view_mode):
    # Custom CSS styling for professional executive dashboard look
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1F497D;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #555555;
            margin-bottom: 1.5rem;
        }
        .stMetric {
            background-color: #F8FBFD;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #E1E8ED;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .card-title {
            font-weight: 600;
            color: #1F497D;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize Session State DataFrame if not existing
    if "df_data" not in st.session_state:
        st.session_state.df_data = pd.DataFrame(CGK_RAW_DATA)

    df = st.session_state.df_data

    # ---------- Sidebar Filters ----------
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔎 Filter Dashboard CGK")

    opd_list = ["Semua OPD"] + sorted(list(df["OPD Penanggung Jawab (Lead)"].unique()))
    selected_opd = st.sidebar.selectbox("Filter OPD Penanggung Jawab (Lead):", opd_list)

    pilar_list = ["Semua Pilar"] + sorted(list(df["Pilar Utama"].unique()))
    selected_pilar = st.sidebar.selectbox("Filter Pilar Utama Geopark:", pilar_list)

    timeline_list = ["Semua Timeline"] + sorted(list(df["Jangka Waktu"].unique()))
    selected_timeline = st.sidebar.selectbox("Filter Skala Timeline:", timeline_list)

    status_list = ["Semua Status", "Selesai", "Dalam Proses", "Belum Mulai", "Tertunda"]
    selected_status = st.sidebar.selectbox("Filter Status Kegiatan:", status_list)

    # Apply Filters
    filtered_df = df.copy()
    if selected_opd != "Semua OPD":
        filtered_df = filtered_df[filtered_df["OPD Penanggung Jawab (Lead)"] == selected_opd]
    if selected_pilar != "Semua Pilar":
        filtered_df = filtered_df[filtered_df["Pilar Utama"] == selected_pilar]
    if selected_timeline != "Semua Timeline":
        filtered_df = filtered_df[filtered_df["Jangka Waktu"] == selected_timeline]
    if selected_status != "Semua Status":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]

    # ---------- Header ----------
    st.markdown('<div class="main-header">DASHBOARD MONITORING GEOPARK KOTABARU (CGK)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sistem Pemantauan Terintegrasi Berbasis Model Geopark Collaborative Governance (GCG) - Road Map V3</div>', unsafe_allow_html=True)

    # ---------- Top Executive KPI Cards ----------
    total_kegiatan = len(df)
    total_selesai = len(df[df["Status"] == "Selesai"])
    total_proses = len(df[df["Status"] == "Dalam Proses"])
    total_belum = len(df[df["Status"].isin(["Belum Mulai", "Tertunda"])])
    progress_pct = (total_selesai / total_kegiatan) * 100 if total_kegiatan > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Program", f"{total_kegiatan} Program")
    with col2:
        st.metric("Selesai (Completed)", f"{total_selesai} Program", f"{progress_pct:.1f}%")
    with col3:
        st.metric("Dalam Proses", f"{total_proses} Program")
    with col4:
        st.metric("Belum Mulai", f"{total_belum} Program")
    with col5:
        st.metric("Status Kinerja", "SANGAT BAIK" if progress_pct >= 15 else "ON TRACK")

    st.markdown("---")

    # ---------- Visualization (view_mode is chosen from the sidebar) ----------
    color_map = {
        "Selesai": "#2ECC71",
        "Dalam Proses": "#F39C12",
        "Belum Mulai": "#3498DB",
        "Tertunda": "#E74C3C"
    }

    if view_mode == "📊 Ringkasan & Grafik Performa":
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("🍩 Distribusi Status Program Kerja")
            status_counts = df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Jumlah"]
            fig_donut = px.pie(
                status_counts,
                values="Jumlah",
                names="Status",
                hole=0.5,
                color="Status",
                color_discrete_map=color_map
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            fig_donut.update_layout(showlegend=True, height=350, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_donut, use_container_width=True)

        with c2:
            st.subheader("🏛️ Progres Kinerja per OPD Penanggung Jawab (Lead)")
            opd_summary = df.groupby(["OPD Penanggung Jawab (Lead)", "Status"]).size().unstack(fill_value=0).reset_index()
            for col in ["Selesai", "Dalam Proses", "Belum Mulai"]:
                if col not in opd_summary.columns:
                    opd_summary[col] = 0
            fig_opd = px.bar(
                opd_summary,
                y="OPD Penanggung Jawab (Lead)",
                x=["Selesai", "Dalam Proses", "Belum Mulai"],
                orientation='h',
                title="Beban Kerja & Capaian Sektoral OPD",
                color_discrete_map=color_map,
                barmode="stack"
            )
            fig_opd.update_layout(height=350, margin=dict(t=30, b=20, l=20, r=20), xaxis_title="Jumlah Kegiatan", yaxis_title="")
            st.plotly_chart(fig_opd, use_container_width=True)

        st.markdown("---")

        c3, c4 = st.columns([1, 1])
        with c3:
            st.subheader("🌿 Distribusi Program per Pilar Utama Geopark")
            pilar_summary = df.groupby(["Pilar Utama", "Status"]).size().unstack(fill_value=0).reset_index()
            fig_pilar = px.bar(
                pilar_summary,
                x="Pilar Utama",
                y=[c for c in ["Selesai", "Dalam Proses", "Belum Mulai"] if c in pilar_summary.columns],
                barmode="group",
                color_discrete_map=color_map
            )
            fig_pilar.update_layout(height=320, margin=dict(t=20, b=20, l=20, r=20), yaxis_title="Jumlah Program", xaxis_title="")
            st.plotly_chart(fig_pilar, use_container_width=True)

        with c4:
            st.subheader("⏳ Beban Kerja Berdasarkan Skala Timeline")
            time_summary = df.groupby(["Jangka Waktu", "Status"]).size().unstack(fill_value=0).reset_index()
            fig_time = px.bar(
                time_summary,
                x="Jangka Waktu",
                y=[c for c in ["Selesai", "Dalam Proses", "Belum Mulai"] if c in time_summary.columns],
                barmode="stack",
                color_discrete_map=color_map
            )
            fig_time.update_layout(height=320, margin=dict(t=20, b=20, l=20, r=20), yaxis_title="Jumlah Program", xaxis_title="")
            st.plotly_chart(fig_time, use_container_width=True)

    elif view_mode == "✏️ Update Status Real-Time Interaktif":
        st.subheader("✏️ Pembaruan Status Real-Time oleh Tim Kerja / Admin OPD")
        st.info("💡 **Petunjuk:** Ubah status kegiatan secara langsung pada tabel di bawah ini. Seluruh angka KPI dan grafik pemantauan akan otomatis memperbarui nilainya secara real-time!")

        status_cols = ["No", "Program / Kegiatan Kerja", "OPD Penanggung Jawab (Lead)", "Jangka Waktu", "Timeline Detail", "Status"]
        edited_df = st.data_editor(
            df[status_cols],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status Pelaksanaan",
                    help="Pilih status terbaru kegiatan",
                    options=["Belum Mulai", "Dalam Proses", "Selesai", "Tertunda"],
                    required=True
                ),
                "No": st.column_config.NumberColumn(disabled=True),
                "Program / Kegiatan Kerja": st.column_config.TextColumn(disabled=True),
                "OPD Penanggung Jawab (Lead)": st.column_config.TextColumn(disabled=True),
                "Jangka Waktu": st.column_config.TextColumn(disabled=True),
                "Timeline Detail": st.column_config.TextColumn(disabled=True)
            },
            use_container_width=True,
            num_rows="fixed",
            height=500
        )

        if not edited_df.equals(df[status_cols]):
            for idx, row in edited_df.iterrows():
                st.session_state.df_data.loc[st.session_state.df_data["No"] == row["No"], "Status"] = row["Status"]
            st.success("✔️ Status kegiatan berhasil diperbarui secara real-time! Silakan kembali ke tab 'Ringkasan & Grafik Performa' untuk melihat hasilnya.")
            st.rerun()

    elif view_mode == "📋 Matriks Program Kerja (Filtered)":
        st.subheader("📋 Matriks Detail Road Map Geopark Kotabaru V3")
        st.write(f"Menampilkan **{len(filtered_df)}** dari total **{len(df)}** program kerja berdasarkan kriteria filter aktif.")

        search_query = st.text_input("🔍 Cari Program Kerja atau Kata Kunci:", "")
        display_df = filtered_df.copy()
        if search_query:
            display_df = display_df[
                display_df["Program / Kegiatan Kerja"].str.contains(search_query, case=False, na=False) |
                display_df["Deskripsi Ringkas Kegiatan"].str.contains(search_query, case=False, na=False) |
                display_df["OPD Penanggung Jawab (Lead)"].str.contains(search_query, case=False, na=False)
            ]

        st.dataframe(
            display_df[["No", "Jangka Waktu", "Pilar Utama", "Program / Kegiatan Kerja", "OPD Penanggung Jawab (Lead)", "OPD Pendukung & Peran RACI", "Indikator Keberhasilan (KPI)", "Timeline Detail", "Status"]],
            use_container_width=True,
            height=550
        )

    else:  # Ekspor & Integrasi One Data
        st.subheader("📥 Ekspor Data Matriks & Integrasi One Data Geopark")
        st.write("Unduh data pemantauan terbaru yang sudah dimutakhirkan sebagai berkas CSV/Excel untuk keperluan pelaporan pimpinan atau sinkronisasi dengan portal One Data Kotabaru.")

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Master Matriks Road Map V3 Terbaru (CSV)",
            data=csv_data,
            file_name=f"roadmap_geopark_kotabaru_v3_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("🔌 Skema Konektivitas API & Web Developer Integration")
        st.json({
            "system_name": "Dashboard Monitoring CGK Streamlit",
            "version": "3.0",
            "total_records": len(df),
            "completion_rate": f"{progress_pct:.2f}%",
            "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "key_actors_integrated": ["Bapperida", "Disparpora", "Diskominfo", "BKPSDMD", "Dinas ESDM Kalsel", "Geopark Meratus"]
        })

    # Footer
    st.markdown("---")
    st.caption("© 2026 Pemerintah Kabupaten Kotabaru - Sistem Pemantauan Geopark Collaborative Governance (GCG)")


# App UI
st.sidebar.image("https://img.icons8.com/color/96/earth-element.png", width=80)
st.sidebar.title("FGD Geopark Kotabaru")
st.sidebar.caption("Kabupaten Kotabaru - Klaster Saijaan Bersujud")
st.sidebar.markdown("---")

# Navigation option lists (two separate groups)
DASHBOARD_VIEWS = [
    "📊 Ringkasan & Grafik Performa",
    "✏️ Update Status Real-Time Interaktif",
    "📋 Matriks Program Kerja (Filtered)",
    "📥 Ekspor & Integrasi One Data"
]
KUESIONER_MENUS = [
    "📝 Input Kuesioner OPD",
    "📊 Quick Count Real-Time",
    "🗂️ Rekapitulasi Data Responden"
]

# First load: the Dashboard group is active and shows its first view
if "active_section" not in st.session_state:
    st.session_state.active_section = "dashboard"
    st.session_state.radio_dashboard = DASHBOARD_VIEWS[0]

def _activate_dashboard():
    st.session_state.active_section = "dashboard"

def _activate_kuesioner():
    st.session_state.active_section = "kuesioner"

# Keep only the ACTIVE group highlighted and clear the other one, so clicking any
# of its items always re-triggers navigation (a radio does not fire on_change when
# the already-selected item is clicked again).
if st.session_state.active_section == "dashboard":
    st.session_state.radio_kuesioner = None
else:
    st.session_state.radio_dashboard = None

# --- Group 1 (TOP): Dashboard Monitoring CGK ---
dashboard_view = st.sidebar.radio(
    "📈 Dashboard Monitoring CGK",
    DASHBOARD_VIEWS,
    key="radio_dashboard",
    index=None,
    on_change=_activate_dashboard
)
st.sidebar.markdown("---")

# --- Group 2 (BOTTOM): Kuesioner FGD ---
menu = st.sidebar.radio(
    "📋 Kuesioner FGD",
    KUESIONER_MENUS,
    key="radio_kuesioner",
    index=None,
    on_change=_activate_kuesioner
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Sistem Pemantauan Terpadu FGD**\n\n"
    "Aplikasi ini secara otomatis merekam masukan OPD dan menghitung analisis kesiapan daerah secara real-time."
)

# ---------------------------------------------------------
# DASHBOARD MONITORING CGK (top navigation group)
# ---------------------------------------------------------
if st.session_state.active_section == "dashboard":
    render_cgk_dashboard(dashboard_view or DASHBOARD_VIEWS[0])

# ---------------------------------------------------------
# KUESIONER GROUP - MENU 1: INPUT KUESIONER OPD
# ---------------------------------------------------------
elif menu == "📝 Input Kuesioner OPD":
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
        *Pilihlah **maksimal 3 opsi** paling dominan pada setiap kategori untuk menggambarkan kondisi instansi Anda.*
        """)

        # CSS: force FULL text visibility in multiselect tags & dropdown options
        st.markdown(
            """
            <style>
            /* Select container: let tags wrap onto multiple lines and grow */
            div[data-baseweb="select"] > div {
                height: auto !important;
                min-height: 2.6rem !important;
                flex-wrap: wrap !important;
                overflow: visible !important;
            }
            /* Selected tag chips: show the FULL text (kill ellipsis clipping) */
            div[data-baseweb="tag"] {
                max-width: 100% !important;
                height: auto !important;
                margin: 2px 4px 2px 0 !important;
                overflow: visible !important;
            }
            div[data-baseweb="tag"] span,
            div[data-baseweb="tag"] div {
                white-space: normal !important;
                overflow: visible !important;
                text-overflow: clip !important;
                overflow-wrap: anywhere !important;
                word-break: break-word !important;
                line-height: 1.3 !important;
                max-width: 100% !important;
            }
            /* Dropdown options: show FULL text (kill ellipsis clipping) */
            div[data-baseweb="popover"] li,
            div[data-baseweb="popover"] li div,
            div[data-baseweb="popover"] li span {
                white-space: normal !important;
                overflow: visible !important;
                text-overflow: clip !important;
                overflow-wrap: anywhere !important;
                word-break: break-word !important;
                height: auto !important;
                line-height: 1.35 !important;
            }
            div[data-baseweb="popover"] li {
                padding-top: 6px !important;
                padding-bottom: 6px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        hambatan = st.multiselect(
            "Hambatan Utama Instansi (maks. 3 opsi):",
            HAMBATAN_OPTIONS,
            max_selections=3,
            placeholder="Klik untuk memilih hingga 3 hambatan..."
        )
        dukungan = st.multiselect(
            "Bentuk Komitmen Dukungan Riil (maks. 3 opsi):",
            DUKUNGAN_OPTIONS,
            max_selections=3,
            placeholder="Klik untuk memilih hingga 3 komitmen..."
        )
        prioritas = st.multiselect(
            "Prioritas Utama Program (maks. 3 opsi):",
            PRIORITAS_OPTIONS,
            max_selections=3,
            placeholder="Klik untuk memilih hingga 3 prioritas..."
        )
            
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
                    "hambatan_utama": MULTI_SEPARATOR.join(hambatan),
                    "komitmen_dukungan": MULTI_SEPARATOR.join(dukungan),
                    "prioritas_program": MULTI_SEPARATOR.join(prioritas),
                    "catatan_bebas": catatan
                }
                # Add score values
                for q_id, val in scores.items():
                    row_dict[q_id] = val
                    
                save_response(row_dict)
                st.balloons()
                st.success(f"✅ Terima kasih **{nama}** ({instansi})! Jawaban kuesioner Anda berhasil disimpan dan langsung masuk ke Quick Count Real-Time.")

# ---------------------------------------------------------
# KUESIONER GROUP - MENU 2: QUICK COUNT REAL-TIME
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
            h_counts = count_multi_options(df["hambatan_utama"])
            if not h_counts.empty:
                h_counts.columns = ["Opsi Hambatan", "Jumlah OPD"]
                st.bar_chart(h_counts.set_index("Opsi Hambatan"))
                st.table(h_counts)
            else:
                st.info("Belum ada pilihan hambatan yang tercatat.")
            
        with tab_d:
            st.markdown("#### **Frekuensi Komitmen Dukungan Riil OPD**")
            d_counts = count_multi_options(df["komitmen_dukungan"])
            if not d_counts.empty:
                d_counts.columns = ["Opsi Komitmen", "Jumlah OPD"]
                st.bar_chart(d_counts.set_index("Opsi Komitmen"))
                st.table(d_counts)
            else:
                st.info("Belum ada komitmen dukungan yang tercatat.")
            
        with tab_p:
            st.markdown("#### **Frekuensi Prioritas Utama Program**")
            p_counts = count_multi_options(df["prioritas_program"])
            if not p_counts.empty:
                p_counts.columns = ["Opsi Prioritas", "Jumlah OPD"]
                st.bar_chart(p_counts.set_index("Opsi Prioritas"))
                st.table(p_counts)
            else:
                st.info("Belum ada prioritas program yang tercatat.")

# ---------------------------------------------------------
# KUESIONER GROUP - MENU 3: REKAPITULASI DATA RESPONDEN
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

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Dashboard Monitoring CGK - Geopark Kotabaru",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
""", unsafe_allow_allow_html=True)

# ==========================================
# INITIAL DATASET (ROAD MAP V3 GROUNDED DATA)
# ==========================================
RAW_DATA = [
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

# Initialize Session State DataFrame if not existing
if "df_data" not in st.session_state:
    st.session_state.df_data = pd.DataFrame(RAW_DATA)

df = st.session_state.df_data

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/earth-exploration.png", width=70)
st.sidebar.title("🌍 Navigasi & Filter CGK")
st.sidebar.markdown("**Collaborative Geopark Kotabaru**\n*Sistem Pemantauan Terintegrasi Road Map V3*")
st.sidebar.markdown("---")

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

# ==========================================
# HEADER SECTION
# ==========================================
st.markdown('<div class="main-header">DASHBOARD MONITORING GEOPARK KOTABARU (CGK)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistem Pemantauan Terintegrasi Berbasis Model Geopark Collaborative Governance (GCG) - Road Map V3</div>', unsafe_allow_html=True)

# ==========================================
# TOP EXECUTIVE KPI CARDS
# ==========================================
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

# ==========================================
# VISUALIZATION TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.columns([1, 1, 1, 1])

# Tab selection radio
view_mode = st.radio(
    "Pilih Tampilan Visualisasi Monitoring:",
    ["📊 Ringkasan & Grafik Performa", "✏️ Update Status Real-Time Interaktif", "📋 Matriks Program Kerja (Filtered)", "📥 Ekspor & Integrasi One Data"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

if view_mode == "📊 Ringkasan & Grafik Performa":
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("🍩 Distribusi Status Program Kerja")
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Jumlah"]
        
        color_map = {
            "Selesai": "#2ECC71",
            "Dalam Proses": "#F39C12",
            "Belum Mulai": "#3498DB",
            "Tertunda": "#E74C3C"
        }
        
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
        st.subheader("⏳ Bebas Kerja Berdasarkan Skala Timeline")
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
    
    # Data editor widget for interactive status update
    edited_df = st.data_editor(
        df[["No", "Program / Kegiatan Kerja", "OPD Penanggung Jawab (Lead)", "Jangka Waktu", "Timeline Detail", "Status"]],
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
    
    # Update main session state dataframe if edits are made
    if not edited_df.equals(df[["No", "Program / Kegiatan Kerja", "OPD Penanggung Jawab (Lead)", "Jangka Waktu", "Timeline Detail", "Status"]]):
        for idx, row in edited_df.iterrows():
            st.session_state.df_data.loc[st.session_state.df_data["No"] == row["No"], "Status"] = row["Status"]
        st.success("✔️ Status kegiatan berhasil diperbarui secara real-time! Silakan kembali ke tab 'Ringkasan & Grafik Performa' untuk melihat hasilnya.")
        st.rerun()

elif view_mode == "📋 Matriks Program Kerja (Filtered)":
    st.subheader("📋 Matriks Detail Road Map Geopark Kotabaru V3")
    st.write(f"Menampilkan **{len(filtered_df)}** dari total **{len(df)}** program kerja berdasarkan kriteria filter aktif.")
    
    # Search box within table
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

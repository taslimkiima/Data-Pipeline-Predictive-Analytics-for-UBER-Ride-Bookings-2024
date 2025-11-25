import streamlit as st
from segmentasi_page import show_segmentasi
from global_demand_page import show_global_demand
from vehicle_demand_page import show_vehicle_demand
from cluster_demand_page import show_cluster_demand
from evaluasi_segment_page import show_evaluasi_segment
from utils import get_theme_tokens, inject_css

# ========================================
# Fungsi untuk inisialisasi session state
# ========================================
def init_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"  # Default to Light theme
    if "page" not in st.session_state:
        st.session_state.page = "Segmentasi Pelanggan"  # Default page

# ========================================
# Inisialisasi session state dan tema
# ========================================
init_state()

# Dapatkan tema yang sesuai
t = get_theme_tokens(st.session_state.theme)

# Inject CSS untuk styling
inject_css(t)

# ========================================
# Sidebar untuk memilih tema dan halaman
# ========================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🔧 Dashboard Analisis Permintaan</div>', unsafe_allow_html=True)

    # Pilihan Tema
    theme_choice = st.radio(
        "Pilih Tema",
        ["🌤️ Terang", "🌙 Gelap"],
        index=0 if st.session_state.theme == "Light" else 1,
        label_visibility="collapsed"
    )

    # Sesuaikan tema yang dipilih
    if "🌤️ Terang" in theme_choice:
        st.session_state.theme = "Light"
    else:
        st.session_state.theme = "Dark"

    # Navigasi Halaman
    st.markdown("---")
    st.markdown('<div class="sidebar-section">Navigasi</div>', unsafe_allow_html=True)
    page_choice = st.radio("Pilih Halaman", ["Segmentasi Pelanggan", "Permintaan Global", "Permintaan Kendaraan", "Permintaan Berdasarkan Cluster", "Evaluasi Segmentasi"])

    # Menetapkan halaman yang dipilih
    if page_choice == "Segmentasi Pelanggan":
        st.session_state.page = "Segmentasi Pelanggan"
    elif page_choice == "Permintaan Global":
        st.session_state.page = "Permintaan Global"
    elif page_choice == "Permintaan Kendaraan":
        st.session_state.page = "Permintaan Kendaraan"
    elif page_choice == "Permintaan Berdasarkan Cluster":
        st.session_state.page = "Permintaan Berdasarkan Cluster"
    elif page_choice == "Evaluasi Segmentasi":
        st.session_state.page = "Evaluasi Segmentasi"

# Update tema setelah navigasi
t = get_theme_tokens(st.session_state.theme)
inject_css(t)

# ========================================
# Konten untuk setiap halaman
# ========================================
if st.session_state.page == "Segmentasi Pelanggan":
    show_segmentasi()  # Halaman untuk segmentasi
elif st.session_state.page == "Permintaan Global":
    show_global_demand()  # Halaman untuk permintaan global
elif st.session_state.page == "Permintaan Kendaraan":
    show_vehicle_demand()  # Halaman untuk permintaan kendaraan
elif st.session_state.page == "Permintaan Berdasarkan Cluster":
    show_cluster_demand()  # Halaman untuk permintaan berdasarkan cluster
elif st.session_state.page == "Evaluasi Segmentasi":
    show_evaluasi_segment()  # Halaman untuk evaluasi segmentasi

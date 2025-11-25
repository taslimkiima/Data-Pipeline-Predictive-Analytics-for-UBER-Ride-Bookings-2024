import streamlit as st
import pandas as pd

# Fungsi untuk menampilkan halaman segmentasi pelanggan
def show_segmentasi():
    st.title('Segmentasi Pelanggan (Clustering)')

    st.markdown("""
    **Segmentasi Pelanggan** ini digunakan untuk mengelompokkan pelanggan atau trip ke dalam segmen-segmen yang berbeda berdasarkan pola perilaku mereka.
    
    Metode yang digunakan dalam segmentasi ini adalah **KMeans Clustering**, yang dikelompokkan berdasarkan trip.

    Hasil segmentasi ini akan memberikan wawasan tentang tipe-tipe pelanggan yang berbeda dan bagaimana mereka berinteraksi dengan layanan kita. Hal ini sangat penting dalam mengoptimalkan pengalaman pengguna, mempersonalisasi penawaran, dan merencanakan strategi bisnis.
    """)

    # Misalnya, load hasil segmentasi dari file atau model yang telah dilatih
    segmented_data = pd.read_csv("outputs_segmentation/segmented_trips.csv")
    st.subheader("Data Segmentasi Pelanggan")
    st.write(segmented_data.head())

    # Visualisasi segmentasi
    st.subheader("Distribusi Cluster")
    st.bar_chart(segmented_data['trip_segment'].value_counts())

    st.subheader("Ringkasan Profil Cluster")

    # Pisahkan kolom numerik dan non-numerik
    numeric_cols = segmented_data.select_dtypes(include=['number']).columns.tolist()

    # Hitung rata-rata hanya untuk kolom numerik
    if numeric_cols:
        cluster_summary = segmented_data.groupby('trip_segment')[numeric_cols].mean()
        st.write(cluster_summary)
    else:
        st.warning("Tidak ada kolom numerik yang ditemukan untuk perhitungan rata-rata.")

    st.subheader("Pentingnya Fitur dalam Cluster")
    feature_importance = pd.read_csv("outputs_segmentation/cluster_feature_importance.csv")
    st.write(feature_importance)
    
    # Menambahkan unduhan data segmentasi
    st.download_button(
        label="Unduh Data Segmentasi",
        data=segmented_data.to_csv(index=False),
        file_name="segmented_trips.csv",
        mime="text/csv"
    )

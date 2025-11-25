import streamlit as st

# Fungsi untuk menampilkan halaman permintaan global
def show_global_demand():
    st.title('Permintaan Global')

    st.markdown("""
    Di halaman ini, kita akan melihat analisis permintaan secara keseluruhan di platform. Ini termasuk analisis dari model demand forecasting yang digunakan untuk memprediksi permintaan secara global.

    Perbandingan antara model baseline dan model Prophet akan diperlihatkan untuk memberikan gambaran yang lebih jelas.
    """)

    # Misalnya, menampilkan grafik dan data terkait permintaan global
    st.subheader("Permintaan Global Forecast")
    st.image("output_global_demand/global_forecast_plot_baseline.png", caption="Model Baseline")
    st.image("output_global_demand/global_forecast_plot_prophet.png", caption="Model Prophet")

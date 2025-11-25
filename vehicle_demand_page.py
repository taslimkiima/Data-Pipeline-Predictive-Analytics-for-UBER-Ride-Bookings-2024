import streamlit as st

# Fungsi untuk menampilkan halaman permintaan kendaraan
def show_vehicle_demand():
    st.title('Permintaan Kendaraan')

    st.markdown("""
    Di halaman ini, kita akan menampilkan analisis permintaan kendaraan untuk berbagai tipe kendaraan yang tersedia.
    """)

    # Misalnya, menampilkan grafik dan data terkait permintaan kendaraan
    st.subheader("Permintaan Kendaraan Forecast")
    st.image("output_vehicle_demand/vehicle_uber_xl_forecast_plot_baseline.png", caption="Model Baseline")
    st.image("output_vehicle_demand/vehicle_uber_xl_forecast_plot_prophet.png", caption="Model Prophet")

import streamlit as st

# Fungsi untuk mendapatkan tema sesuai dengan pilihan pengguna
def get_theme_tokens(theme_name: str):
    if theme_name == "Dark":
        return {
            "bg": "#0B0F17",
            "bg2": "#111827",
            "card": "#0F172A",
            "text": "#E5E7EB",
            "muted": "#9CA3AF",
            "primary": "#60A5FA",
            "accent": "#34D399",
            "warning": "#FBBF24",
            "danger": "#F87171",
            "border": "rgba(255,255,255,0.07)",
            "chart_line": "#60A5FA",
            "chart_grid": "#243040",
            "sidebar_bg": "#0A0E15",
            "ok_bg": "rgba(52,211,153,0.12)",
            "warn_bg": "rgba(251,191,36,0.14)",
            "bad_bg": "rgba(248,113,113,0.12)"
        }
    return {
        "bg": "#EAF0F6",
        "bg2": "#FFFFFF",
        "card": "#FFFFFF",
        "text": "#0F172A",
        "muted": "#64748B",
        "primary": "#2563EB",
        "accent": "#16A34A",
        "warning": "#D97706",
        "danger": "#DC2626",
        "border": "rgba(15,23,42,0.08)",
        "chart_line": "#111827",
        "chart_grid": "#E6EAF2",
        "sidebar_bg": "#0F172A",
        "ok_bg": "rgba(22,163,74,0.10)",
        "warn_bg": "rgba(217,119,6,0.12)",
        "bad_bg": "rgba(220,38,38,0.10)"
    }

# Fungsi untuk menyuntikkan CSS ke aplikasi
def inject_css(t):
    st.markdown(
        f"""
        <style>
        /* Custom styling here */
        </style>
        """,
        unsafe_allow_html=True
    )

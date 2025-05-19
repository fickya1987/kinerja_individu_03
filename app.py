import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup halaman
st.set_page_config(page_title="Distribusi & Analisis Kinerja", layout="wide")
st.title("📊 Distribusi Skor Penilaian & Analisis GPT-4o")

# Upload data
uploaded_file = st.file_uploader("Unggah file CSV Penilaian Kinerja", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Pastikan skor numerik
    for col in ["Skor_KPI_Final", "Skor_Assessment", "Skor_Kinerja_Individu"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Distribusi 3 grafik
    st.subheader("Distribusi Skor Penilaian")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig, ax = plt.subplots()
        sns.histplot(df["Skor_KPI_Final"].dropna(), kde=True, ax=ax, color="steelblue")
        ax.set_title("Distribusi Skor KPI Final")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.histplot(df["Skor_Assessment"].dropna(), kde=True, ax=ax, color="orange")
        ax.set_title("Distribusi Skor Assessment AKHLAK")
        st.pyplot(fig)

    with col3:
        fig, ax = plt.subplots()
        sns.histplot(df["Skor_Kinerja_Individu"].dropna(), kde=True, ax=ax, color="green")
        ax.set_title("Distribusi Skor Kinerja Individu")
        st.pyplot(fig)

    # Narasi otomatis dengan GPT-4o
    if openai.api_key:
        with st.expander("🧠 Narasi Analisis dari GPT-4o"):
            prompt = f"""
            Anda adalah analis SDM. Berdasarkan distribusi berikut:

            - Skor KPI Final memiliki distribusi: min {df['Skor_KPI_Final'].min():.2f}, max {df['Skor_KPI_Final'].max():.2f}, mean {df['Skor_KPI_Final'].mean():.2f}
            - Skor Assessment: min {df['Skor_Assessment'].min():.2f}, max {df['Skor_Assessment'].max():.2f}, mean {df['Skor_Assessment'].mean():.2f}
            - Skor Kinerja Individu: min {df['Skor_Kinerja_Individu'].min():.2f}, max {df['Skor_Kinerja_Individu'].max():.2f}, mean {df['Skor_Kinerja_Individu'].mean():.2f}

            Buatkan analisis naratif singkat (3 paragraf) mengenai pola persebaran kinerja, tren skor, serta insight terhadap evaluasi sistem penilaian.
            """
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("OPENAI_API_KEY belum tersedia di file .env.")

    # Analisis tiap pekerja (NIPP)
    st.subheader("📌 Analisis Per Pekerja")
    selected_nipp = st.selectbox("Pilih NIPP", df["NIPP_Pekerja"].unique())
    selected_row = df[df["NIPP_Pekerja"] == selected_nipp].iloc[0]

    st.markdown(
        f"**Nama Posisi**: {selected_row['Nama_Posisi']}  \n"
        f"**Skor KPI Final**: {selected_row['Skor_KPI_Final']}  \n"
        f"**Skor Assessment AKHLAK**: {selected_row['Skor_Assessment']}  \n"
        f"**Skor Kinerja Individu**: {selected_row['Skor_Kinerja_Individu']}  \n"
    )

    if openai.api_key:
        with st.expander("🔍 Narasi GPT-4o untuk Pekerja Ini"):
            prompt = f"""
            Analisis performa individu berdasarkan data berikut:
            - Posisi: {selected_row['Nama_Posisi']}
            - Skor KPI: {selected_row['Skor_KPI_Final']}
            - Skor Assessment: {selected_row['Skor_Assessment']}
            - Skor Kinerja Individu: {selected_row['Skor_Kinerja_Individu']}

            Berikan interpretasi ringkas tentang kekuatan dan area pengembangan yang mungkin perlu diperhatikan.
            """
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown(response.choices[0].message.content)

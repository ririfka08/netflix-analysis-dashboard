# 🎬 Netflix Content Strategy Analysis

Analisis ~5.800 judul film & TV show di Netflix untuk membantu tim konten platform streaming menentukan genre, negara produksi, dan format konten yang worth diinvestasikan lebih banyak.

🔗 **Live Dashboard**: [https://netflix-analysis-dashboard-rifka.streamlit.app/](#) 

---

## Business Problem

Platform streaming perlu terus mengevaluasi konten mana yang worth diproduksi/dibeli lebih banyak berdasarkan performa historis. Analisis ini menjawab 5+ pertanyaan bisnis kunci:

1. Genre apa yang rating-nya (IMDb score) tinggi tapi jumlah kontennya masih sedikit — peluang ekspansi?
2. Movie vs TV Show, mana yang secara rata-rata lebih diterima penonton?
3. Negara produksi mana yang paling "efisien" — rating tinggi meski volume produksi kecil?
4. Apakah durasi (runtime) konten mempengaruhi rating? Ada sweet spot ideal?
5. Bagaimana tren rating konten dari tahun ke tahun?
6. Aktor mana yang paling sering muncul di konten-konten dengan rating tinggi (≥7.5)?

## Data Source

[Netflix TV Shows and Movies](https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies) by Victor Soeiro — terdiri dari 2 tabel:
- `titles.csv`: ~5.850 judul dengan genre, negara produksi, durasi, IMDb & TMDB score
- `credits.csv`: ~77.800 baris data cast & crew

Kedua tabel di-**join** menggunakan kolom `id` untuk memungkinkan analisis level cast, sebuah pendekatan yang membedakan project ini dari analisis single-table biasa.

## Tech Stack

- **Python**: Pandas (cleaning, join & analysis), Plotly (visualisasi)
- **Dashboard**: Streamlit, di-deploy ke Streamlit Community Cloud
- **Version control**: Git + GitHub

---

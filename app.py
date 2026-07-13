import streamlit as st
import pandas as pd
import plotly.express as px
import ast

# PAGE CONFIG
st.set_page_config(
    page_title="Netflix Content Strategy",
    page_icon="🎬",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    titles = pd.read_csv("titles_cleaned.csv")
    titles_exploded = pd.read_csv("titles_exploded.csv")
    country_exploded = pd.read_csv("titles_country_exploded.csv")
    return titles, titles_exploded, country_exploded

titles, titles_exploded, country_exploded = load_data()

# HEADER
st.title("🎬 Netflix Content Strategy Dashboard")
st.markdown("Analisis genre, negara produksi, dan tren rating untuk strategi produksi konten")

# SIDEBAR FILTERS
st.sidebar.header("Filter")

content_type = st.sidebar.multiselect(
    "Tipe Konten",
    options=titles["type"].unique().tolist(),
    default=titles["type"].unique().tolist()
)

min_titles_genre = st.sidebar.slider(
    "Minimal jumlah judul per genre",
    min_value=5, max_value=100, value=20, step=5
)

year_range = st.sidebar.slider(
    "Rentang tahun rilis",
    min_value=int(titles["release_year"].min()),
    max_value=int(titles["release_year"].max()),
    value=(2010, int(titles["release_year"].max()))
)

# Filter data sesuai pilihan sidebar
titles_f = titles[
    (titles["type"].isin(content_type)) &
    (titles["release_year"] >= year_range[0]) &
    (titles["release_year"] <= year_range[1])
]

# KEY METRICS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Judul", f"{len(titles_f):,}")
col2.metric("Rating Rata-rata", f"{titles_f['imdb_score'].mean():.2f}")
col3.metric("Movie", f"{(titles_f['type']=='MOVIE').sum():,}")
col4.metric("TV Show", f"{(titles_f['type']=='SHOW').sum():,}")

st.divider()

# CHART 1 - Genre Underserved (Volume vs Rating)
st.subheader("1. Genre Underserved — peluang ekspansi konten")

genre_stats = titles_exploded.groupby("genres_list").agg(
    avg_rating=("imdb_score", "mean"),
    total_titles=("title", "count")
).reset_index()
genre_stats = genre_stats[genre_stats["total_titles"] >= min_titles_genre]
genre_stats = genre_stats.sort_values("avg_rating", ascending=False)

fig1 = px.scatter(
    genre_stats, x="total_titles", y="avg_rating",
    text="genres_list", size="total_titles",
    color="avg_rating", color_continuous_scale="Reds",
    labels={"total_titles": "Jumlah Judul", "avg_rating": "Rating Rata-rata"}
)
fig1.update_traces(textposition="top center")
st.plotly_chart(fig1, width="stretch")

st.info("💡 **Insight**: Genre di kiri-atas (rating tinggi, jumlah judul sedikit) adalah kandidat kuat untuk ekspansi konten karena demand kualitasnya sudah terbukti tapi belum banyak pesaing di katalog.")

st.divider()

# CHART 2 - Movie vs TV Show
st.subheader("2. Movie vs TV Show")

col_a, col_b = st.columns(2)

type_comparison = titles_f.groupby("type").agg(
    avg_rating=("imdb_score", "mean"),
    avg_popularity=("tmdb_popularity", "mean"),
    total=("title", "count")
).reset_index()

with col_a:
    fig2 = px.bar(type_comparison, x="type", y="avg_rating", color="type",
                  labels={"type": "Tipe", "avg_rating": "Rating Rata-rata"})
    st.plotly_chart(fig2, width="stretch")

with col_b:
    fig2b = px.bar(type_comparison, x="type", y="total", color="type",
                   labels={"type": "Tipe", "total": "Jumlah Judul"})
    st.plotly_chart(fig2b, width="stretch")

st.divider()

# CHART 3 - Negara Produksi Paling Efisien
st.subheader("3. Negara Produksi Paling Efisien")

country_stats = country_exploded.groupby("country_list").agg(
    avg_rating=("imdb_score", "mean"),
    total_titles=("title", "count")
).reset_index()
country_stats = country_stats[country_stats["total_titles"] >= 10]
country_stats = country_stats.sort_values("avg_rating", ascending=False).head(15)

fig3 = px.bar(country_stats, x="country_list", y="avg_rating",
              labels={"country_list": "Negara", "avg_rating": "Rating Rata-rata"})
st.plotly_chart(fig3, width="stretch")

st.divider()

# CHART 4 - Durasi vs Rating
st.subheader("4. Durasi vs Rating")

fig4 = px.scatter(titles_f, x="runtime", y="imdb_score", color="type",
                   opacity=0.5,
                   labels={"runtime": "Durasi (menit)", "imdb_score": "IMDb Score"})
st.plotly_chart(fig4, width="stretch")

st.divider()

# CHART 5 - Tren Rating per Tahun
st.subheader("5. Tren Rating per Tahun Rilis")

yearly = titles_f.groupby("release_year")["imdb_score"].mean().reset_index()
fig5 = px.line(yearly, x="release_year", y="imdb_score",
                labels={"release_year": "Tahun Rilis", "imdb_score": "Rating Rata-rata"})
st.plotly_chart(fig5, width="stretch")

st.info("💡 **Insight**: Gunakan tren ini untuk melihat apakah kualitas konten (berdasarkan IMDb score) membaik atau menurun seiring waktu — bisa jadi sinyal evaluasi strategi kurasi konten.")
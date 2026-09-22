import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("movie.csv")

st.title("영화 데이터 분석")

# 숫자형 데이터 변환
df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce")

# --------------------------------------------------
# 1. 기존 첫 번째 그래프
# --------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_count = df["genre"].value_counts().reset_index()
genre_count.columns = ["genre", "movie_count"]

fig1 = px.bar(
    genre_count,
    x="genre",
    y="movie_count",
    labels={
        "genre": "장르",
        "movie_count": "영화 편수"
    },
    title="장르별 영화 편수"
)

st.plotly_chart(fig1, use_container_width=True)


# --------------------------------------------------
# 2. 장르 → 영화 트리맵
# --------------------------------------------------
st.subheader("2. 장르별 영화 총 관객 수 트리맵")

treemap_df = df.dropna(subset=["genre", "movieNm", "total_audi"]).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "total_audi": ":,",
        "genre": True
    },
    labels={
        "genre": "장르",
        "movieNm": "영화",
        "total_audi": "총 관객 수"
    },
    title="장르별 영화 총 관객 수"
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# 3. 총 관객 수 히스토그램
# --------------------------------------------------
st.subheader("3. 영화별 총 관객 수 분포")

audi_data = df["total_audi"].dropna()

fig3 = px.histogram(
    audi_data,
    x="total_audi",
    nbins=20,
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 수"
    },
    title="영화별 총 관객 수 분포"
)

fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 수"
)

st.plotly_chart(fig3, use_container_width=True)


# 가장 많이 몰린 구간 계산
bin_counts, bin_edges = pd.cut(
    audi_data,
    bins=20,
    include_lowest=True,
    retbins=True
)

most_common_bin = bin_counts.value_counts().idxmax()

low = most_common_bin.left
high = most_common_bin.right


# 총 관객이 가장 많은 영화
max_idx = df["total_audi"].idxmax()
max_movie = df.loc[max_idx, "movieNm"]
max_audi = df.loc[max_idx, "total_audi"]


# 그래프 아래 문구
st.write(
    f"📊 대부분의 영화는 **{low:,.0f}명 ~ {high:,.0f}명** "
    f"구간에 몰려 있습니다."
)

st.write(
    f"🏆 총 관객이 가장 많은 영화는 **{max_movie}**이며, "
    f"총 관객 수는 **{max_audi:,.0f}명**입니다."
)

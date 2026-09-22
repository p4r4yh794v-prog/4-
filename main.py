import streamlit as st
import pandas as pd
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    return df

df = load_data()

# -----------------------------
# 1. 장르별 영화 편수
# -----------------------------
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)

fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 어떤 장르의 영화가 가장 많이 개봉했는지 알 수 있다.",
    key="graph1_fact"
)

st.divider()

import streamlit as st
import pandas as pd
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    return df

df = load_data()

# -----------------------------
# 1. 장르별 영화 편수
# -----------------------------
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)

fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 어떤 장르의 영화가 가장 많이 개봉했는지 알 수 있다.",
    key="graph1_fact"
)

st.divider()

# -----------------------------
# 2. 장르별 영화 트리맵
# -----------------------------
st.header("2. 장르별 영화 트리맵")

treemap_df = df[["genre", "movieNm", "total_audi"]].copy()
treemap_df["total_audi"] = pd.to_numeric(treemap_df["total_audi"], errors="coerce").fillna(0)

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객",
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 장르별로 어떤 영화가 많은 관객을 모았는지 알 수 있다.",
    key="graph2_fact"
)

st.divider()

# 3. 총 관객 수(total_audi) 히스토그램
st.subheader("3. 영화별 총 관객 수 분포")

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(df["total_audi"].dropna(), bins=20, edgecolor="black")

ax.set_xlabel("총 관객 수")
ax.set_ylabel("영화 수")
ax.set_title("영화별 총 관객 수 분포")
ax.ticklabel_format(style="plain", axis="x")

st.pyplot(fig)

# 가장 많은 영화 찾기
max_idx = df["total_audi"].idxmax()
max_movie = df.loc[max_idx, "movieNm"]
max_audi = df.loc[max_idx, "total_audi"]

# 가장 많이 몰린 구간 찾기
counts, bins = np.histogram(df["total_audi"].dropna(), bins=20)
most_common_bin = np.argmax(counts)

low = bins[most_common_bin]
high = bins[most_common_bin + 1]

st.write(
    f"📊 대부분의 영화는 **{low:,.0f}명 ~ {high:,.0f}명** 구간에 몰려 있습니다."
)
st.write(
    f"🏆 총 관객이 가장 많은 영화는 **{max_movie}**이며, "
    f"총 관객 수는 **{max_audi:,.0f}명**입니다."
)

# 4. 개봉일 스크린 수와 총 관객의 관계
st.subheader("4. 개봉일 스크린 수와 총 관객의 관계")

fig = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": True,
        "total_audi": True,
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    },
    title="개봉일 스크린 수와 총 관객의 관계"
)

fig.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig, use_container_width=True)

# 5. 장르별 총 관객 수 상자 그림
st.subheader("5. 장르별 총 관객 수 분포")

# 영화가 10편 이상인 장르만 선택
genre_counts = df["genre"].value_counts()
valid_genres = genre_counts[genre_counts >= 10].index

box_df = df[df["genre"].isin(valid_genres)].copy()

fig = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    },
    title="영화가 10편 이상인 장르별 총 관객 수 분포"
)

fig.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# 6. 첫 주 관객 수를 점 크기로 표현한 버블 그래프
st.subheader("6. 개봉일 스크린 수와 총 관객의 관계 - 버블 그래프")

fig = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": True,
        "total_audi": True,
        "first_week_audi": True,
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르"
    },
    title="개봉일 스크린 수와 총 관객의 관계 (첫 주 관객 수 크기)"
)

fig.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig, use_container_width=True)

# 7. 제작 국가 → 장르 선버스트 그래프
st.subheader("7. 제작 국가별 장르 분포")

sunburst_df = (
    df.groupby(["nation", "genre"])
      .size()
      .reset_index(name="movie_count")
)

fig = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    values="movie_count",
    title="제작 국가 → 장르별 영화 편수",
)

fig.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

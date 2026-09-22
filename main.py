import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 분석",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 분석")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df


df = load_data()


# --------------------------------------------------
# 데이터 전처리
# --------------------------------------------------

# 숫자형으로 변환할 컬럼
numeric_columns = [
    "total_audi",
    "first_scrn",
    "first_week_audi"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# --------------------------------------------------
# 1. 장르별 영화 편수
# --------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .dropna()
    .value_counts()
    .reset_index()
)

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

fig1.update_layout(
    xaxis_title="장르",
    yaxis_title="영화 편수"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# --------------------------------------------------
# 2. 장르 → 영화 트리맵
# --------------------------------------------------
st.subheader("2. 장르별 영화 총 관객 수 트리맵")

treemap_df = df.dropna(
    subset=["genre", "movieNm", "total_audi"]
).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={
        "genre": "장르",
        "movieNm": "영화",
        "total_audi": "총 관객 수"
    },
    title="장르 → 영화별 총 관객 수"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b>"
        "<br>총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# --------------------------------------------------
# 3. 총 관객 수 히스토그램
# --------------------------------------------------
st.subheader("3. 영화별 총 관객 수 분포")

audi_df = df.dropna(
    subset=["total_audi"]
).copy()

fig3 = px.histogram(
    audi_df,
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

st.plotly_chart(
    fig3,
    use_container_width=True
)


# 가장 많이 몰린 구간 계산
if len(audi_df) > 0:

    # pandas의 cut을 이용해서 20개 구간으로 나눔
    bins = pd.cut(
        audi_df["total_audi"],
        bins=20,
        include_lowest=True
    )

    most_common_bin = bins.value_counts().idxmax()

    low = most_common_bin.left
    high = most_common_bin.right

    # 총 관객이 가장 많은 영화
    max_idx = audi_df["total_audi"].idxmax()

    max_movie = audi_df.loc[
        max_idx,
        "movieNm"
    ]

    max_audi = audi_df.loc[
        max_idx,
        "total_audi"
    ]

    st.write(
        f"📊 대부분의 영화는 "
        f"**{low:,.0f}명 ~ {high:,.0f}명** "
        f"구간에 몰려 있습니다."
    )

    st.write(
        f"🏆 총 관객이 가장 많은 영화는 "
        f"**{max_movie}**이며, "
        f"총 관객 수는 **{max_audi:,.0f}명**입니다."
    )


# --------------------------------------------------
# 4. 개봉일 스크린 수 × 총 관객 산점도
# --------------------------------------------------
st.subheader("4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "genre",
        "movieNm"
    ]
).copy()

fig4 = px.scatter(
    scatter_df,
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

fig4.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# --------------------------------------------------
# 5. 장르별 총 관객 수 박스플롯
# --------------------------------------------------
st.subheader("5. 장르별 총 관객 수 분포")

# 장르별 영화 편수 계산
genre_counts = (
    df["genre"]
    .dropna()
    .value_counts()
)

# 영화가 10편 이상인 장르만 선택
valid_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["genre"].isin(valid_genres)
].dropna(
    subset=[
        "genre",
        "total_audi",
        "movieNm"
    ]
).copy()

fig5 = px.box(
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

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    showlegend=False
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# --------------------------------------------------
# 6. 버블 그래프
# --------------------------------------------------
st.subheader(
    "6. 개봉일 스크린 수와 총 관객의 관계 - 버블 그래프"
)

bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "genre",
        "movieNm"
    ]
).copy()

fig6 = px.scatter(
    bubble_df,
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
    title="개봉일 스크린 수와 총 관객의 관계"
)

fig6.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)


# --------------------------------------------------
# 7. 제작 국가 → 장르 선버스트
# --------------------------------------------------
st.subheader("7. 제작 국가별 장르 분포")

sunburst_df = df.dropna(
    subset=[
        "nation",
        "genre"
    ]
).copy()

# 국가와 장르 조합별 영화 편수
sunburst_df = (
    sunburst_df
    .groupby(
        ["nation", "genre"],
        as_index=False
    )
    .size()
)

sunburst_df = sunburst_df.rename(
    columns={"size": "movie_count"}
)

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    values="movie_count",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b>"
        "<br>영화 편수: %{value}편"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

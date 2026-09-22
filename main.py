import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)
    # 장르가 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].str.split("|").str[0]
    return df


df = load_data()

# ── 그래프 1. 장르별 영화 편수 도넛 ──
st.header("1. 장르별 영화 편수 (도넛)")
genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45,  # 가운데 구멍을 뚫어 도넛 모양으로
)
# 조각에 마우스를 올리면 편수와 비율이 보이게 합니다
fig.update_traces(hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>")
st.plotly_chart(fig, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note1")

st.divider()
# 앞으로 그래프를 계속 추가할 구역
st.header("2. (다음 그래프를 여기에 추가)")
# 2. 장르 → 영화 트리맵
st.subheader("2. 장르별 영화 총 관객 수 트리맵")

fig = px.treemap(
    df,
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

fig.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)
# 3. 총 관객 수 히스토그램
st.subheader("3. 영화별 총 관객 수 분포")

audi_data = df["total_audi"].dropna()

fig = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 수"
    },
    title="영화별 총 관객 수 분포"
)

fig.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 수"
)

st.plotly_chart(fig, use_container_width=True)

# 가장 많이 몰린 구간 계산
counts, bins = np.histogram(audi_data, bins=20)
most_common_bin = np.argmax(counts)

low = bins[most_common_bin]
high = bins[most_common_bin + 1]

# 총 관객이 가장 많은 영화
max_idx = df["total_audi"].idxmax()
max_movie = df.loc[max_idx, "movieNm"]
max_audi = df.loc[max_idx, "total_audi"]

st.write(
    f"📊 대부분의 영화는 **{low:,.0f}명 ~ {high:,.0f}명** 구간에 몰려 있습니다."
)

st.write(
    f"🏆 총 관객이 가장 많은 영화는 **{max_movie}**이며, "
    f"총 관객 수는 **{max_audi:,.0f}명**입니다."
)

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
counts, bins = pd.cut(
    audi_data,
    bins=20,
    retbins=True
)

most_common_range = counts.value_counts().idxmax()

# 총 관객이 가장 많은 영화
max_idx = df["total_audi"].idxmax()
max_movie = df.loc[max_idx, "movieNm"]
max_audi = df.loc[max_idx, "total_audi"]

st.write(
    f"📊 대부분의 영화는 **{most_common_range.left:,.0f}명 ~ "
    f"{most_common_range.right:,.0f}명** 구간에 몰려 있습니다."
)

st.write(
    f"🏆 총 관객이 가장 많은 영화는 **{max_movie}**이며, "
    f"총 관객 수는 **{max_audi:,.0f}명**입니다."
)

import streamlit as st
st.set_page_config(page_title="모델 대시보드", layout='wide')

#사이드바
with st.sidebar:
    st.header("필터")
    dataset = st.selectbox("데이터셋", ['Train', 'Test', 'Val'])
    smooth = st.slider('Smooth', 1,25,5)
    show_points = st.checkbox("포인트표시", False)

#kpi - key performance indicator : 핵심 성과 지표
k1, k2, k3, k4 = st.columns(4)
k1.metric("Best Val Acc", '93.8%', '+0.2%')
k2.metric("Min Val Loss", '0.183', '-0.5%')
k3.metric("Latency(ms)", '12.3')
k4.metric("Params(M)", '21.8')

#Tab
t1, t2, t3 = st.tabs(['학습곡선', '지표/혼동행렬', '예측샘플'])

with t1:
    c1, c2 = st.columns([5,5])
    with c1:
        st.subheader("Loss Curve")
        st.line_chart({'train': [0.9, 0.6, 0.4, 0.25], 'Val':[1.0, 0.7, 0.5, 0.3]})

    with c2:
        st.subheader("Accuracy Curve")
        st.line_chart({'train': [0.9, 0.6, 0.4, 0.25], 'Val':[1.0, 0.7, 0.5, 0.3]})

with t2:
    st.subheader("지표 테이블")
    st.table({"precision": [0.91, 0.88], 'recall':[0.9, 0.86], 'f1':[0.905, 0.87]})

    with st.expander("혼동행렬"):
        st.dataframe({'Pred 0':[88,5], 'Pred 1':[7, 100]})

with t3:
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("입력샘플")
        st.image('https://placehold.co/300x300', caption="업로드 샘플")

    with c2:
        st.subheader("Top-K 확률")
        st.bar_chart({'A':95, 'B':3, 'C':2})
import streamlit as st


st.title("꿈돌이는 귀여웡")
st.write("------------------------------------------------")

tab1, tab2, tab3 =st.tabs(['개요', '지표', '결과'])

if 'cnt' not in st.session_state: 
    st.session_state.cnt= 0

with tab1:
    # st.header("원티드 매출분석")
    # container = st.container()
    # container.write('컨테이너 안에 들어가는 글')
    # st.write('컨테이너 밖')
    if st.button('증가'):
        st.session_state.cnt += 1
    if st.button('감소'):
        st.session_state.cnt -= 1

    st.write(st.session_state.cnt)


    with st.expander("이안에 숨겨진기능이 있지롱~~"):
        st.write('숨겨진 기능')

with tab2:
    col1, col2, col3 =st.columns([2,5,3])
    with col1: 
        st.subheader("요약지표")
        st.metric("Accuracy", "94.3%", '+0.7%')

    with col2:
        st.subheader('라인차트')
        st.line_chart({'acc':[0.8, 1.2, 0.4, 0.9]})

    with col3:
        st.subheader("세부옵션")
        st.checkbox("원티드")
with tab3:
    st.metric('최종예측', "999,999,999,999원", "+520.7%")
# st.header("헤더입니도")

# st.subheader("서브헤더입니도")

# st.text("일반텍스트")

# st.markdown("**마크다운 지원** 정말좋아용")

# st.markdown("*마크다운 지원* 정말좋아요")

#st.markdown("![이미지](https://i.namu.wiki/i/NF9n1fBQ4PHwJdkDJVqiIpxYqMs5ClOnkQQ77DNyNgmRPAS9PLXfFnjhnOTcH2CsqySC1ap7o-Zgm89INjiNaA.webp)")

# st.code("print('Hello, World!')", language="python")


st.set_page_config(page_title="레이아웃", layout="wide")


with st.sidebar:
    userId =st.text_input("ID를 입력하세요.", key='id')

    st.write('session_state.id: ', st.session_state.id)

    st.header("옵션")
    date = st.date_input("날짜")
    clas = st.selectbox("클래스", ["A", "B", "C"])


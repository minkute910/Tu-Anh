import streamlit as st

def run_insight():
    import streamlit as st

def run_insight():
    
    st.title("🧠 Titanic 분석 인사이트")
    st.markdown("---")

    # 탭 생성
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚢 구조 우선순위", "👩‍🦰 성별", "💺 객실 등급", "🎟️ 요금", "👨‍👩‍👧 가족", "🧒 나이"
    ])

    with tab1:
        st.markdown("#### 구조선은 누구를 구했을까?")
        st.info("Titanic호에서 구조의 우선순위는 분명했습니다 — 여성, 아이, 그리고 상류층.")

    with tab2:
        st.markdown("#### 성별은 생존의 열쇠")
        st.success("여성의 생존률은 **남성보다 4배 이상 높게** 나타났습니다. 성별은 생존 예측의 가장 강력한 변수입니다.")

    with tab3:
        st.markdown("#### 객실 등급의 불평등")
        st.warning("1등석 승객의 생존률은 가장 높았고, 3등석 남성의 생존률은 가장 낮았습니다.  \n\n**'부유할수록 생존할 확률이 높았다'**는 점이 데이터로 확인됩니다.")

    with tab4:
        st.markdown("#### 요금은 생존 투자?")
        st.info("지불한 요금(Fare)이 높을수록 생존률도 증가했습니다. 사회적 지위가 곧 생존 확률로 연결된 것입니다.")

    with tab5:
        st.markdown("#### 함께 탑승한 사람은?")
        st.success("가족과 함께(1~2명) 탑승한 승객은 생존률이 높았습니다.  \n\n**단독 탑승** 또는 **대가족** 승객은 생존률이 낮았습니다.")

    with tab6:
        st.markdown("#### 나이에 따른 차이")
        st.info("어린이(Child)와 중년층(Adult)의 생존률이 높았고, 십대 및 고령층은 생존률이 낮았습니다.  \n\n**'아이들 먼저' 원칙이 실제로 적용된 듯 보입니다.**")

    st.markdown("---")
    st.subheader("🎯 전략적 인사이트 요약")

    st.warning("**✔ 주요 변수 중심 모델링 필요**\n\n성별, 객실 등급, 요금, 동반자 수는 생존률에 가장 큰 영향을 줍니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.warning("**✔ 전처리만으로도 예측력 향상**\n\n결측치 보완과 이상치 제거는 모델 안정성과 정확도 개선에 효과적입니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.warning("**✔ 파생 변수 활용 가능성 높음**\n\nAgeGroup, 성별, 등급 조합 분석은 피처 엔지니어링에 유용합니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.warning("**✔ 시각화는 강력한 설득 도구**\n\n분석 결과를 직관적으로 전달할 수 있어 의사결정과 발표에 효과적입니다.")
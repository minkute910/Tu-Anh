import streamlit as st
from streamlit_option_menu import option_menu
from home import run_eda
from analyse import run_analyse
from prediction import run_prediction
from utils import load_train_and_test
from insight import run_insight

def main():

    
    with st.sidebar:
        selected = option_menu(
            "대시보드 메뉴",
            ["🏠 홈", "📊 data 시각화 및 분석", "🧠 insight 정리", "🔮 set data 결과 예측"],
    
            menu_icon="cast",
            default_index=0,
        )
    if selected == "🏠 홈":
        run_eda()
    elif selected == "📊 data 시각화 및 분석":
        run_analyse()
    elif selected == "🧠 insight 정리":
        run_insight()
    elif selected == "🔮 set data 결과 예측":
        run_prediction()
    else:
        st.error("❌ 메뉴 선택에 오류가 발생했습니다.")


if __name__ == "__main__":
    main()

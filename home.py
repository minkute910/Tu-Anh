import pandas as pd
from utils import load_data
import streamlit as st
from millify import prettify

def run_eda():
    st.markdown(
        "## 대시보드 개요\n"
        "본 프로젝트는 titanic train data를 통해서 예측 모델을 만드는 대시보드입니다.\n"
        "\n모델을 통해서 set data의 결과를 예측해서 정확도가 얼마인지 평가합니다.\n"
    )
    st.subheader("📁 데이터 Overview")
    data_choice = st.selectbox("확인할 데이터를 선택하세요:", ["train data", "set data"])

    if data_choice == 'train data':
        df = pd.read_csv('train.csv')
    else:
        df = pd.read_csv('test.csv')

    option = st.selectbox(
                "확인하고 싶은 항목을 선택하세요:",
                ["데이터 요소", "Unique values", "통계적 분석", "Missing data"]
            )


    if option == "데이터 요소":
        st.write("### 데이터 미리보기 (train.head())")
        st.dataframe(df.head())

    elif option == "Unique values":
        st.write("### 고유값 보기 (train.nunique())")
        st.write(df.nunique())

    elif option == "통계적 분석":
        st.write("### 통계 요약 (train.describe())")
        st.write(df.describe())

    elif option == "Missing data":
        st.write("### 결측치 확인 (train.isnull().sum())")
        st.write(df.isnull().sum())


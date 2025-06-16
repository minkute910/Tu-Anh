import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils import load_train_and_test

def run_analyse():
    
    st.title("📊 데이터 시각화 및 분석")

    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")

    train['Age'] = train['Age'].fillna(train['Age'].mean())
    train = train.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
    train['Embarked'] = train['Embarked'].fillna(train['Embarked'].mode()[0])

    test['Age'] = test['Age'].fillna(test['Age'].mean())
    test['Fare'] = test['Fare'].fillna(test['Fare'].mean())
    test = test.drop(['Cabin'], axis=1)

    def remove_outliers_iqr(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[column] >= lower) & (df[column] <= upper)]

    train_cleaned = remove_outliers_iqr(train, 'Fare')
    train_cleaned = remove_outliers_iqr(train_cleaned, 'Age')

    train_cleaned['AgeGroup'] = pd.cut(train_cleaned['Age'], bins=[0, 12, 18, 35, 60, 100],
                                       labels=['Child', 'Teen', 'Young Adult', 'Adult', 'Senior'])

    with st.expander("📦 Boxplots (Before & After Cleaning)"):
        fig1, ax = plt.subplots(1, 2, figsize=(14, 5))
        sns.boxplot(x=train["Fare"], ax=ax[0])
        ax[0].set_title("Original Fare")
        sns.boxplot(x=train["Age"], ax=ax[1])
        ax[1].set_title("Original Age")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots(1, 2, figsize=(14, 5))
        sns.boxplot(x=train_cleaned["Fare"], ax=ax2[0])
        ax2[0].set_title("Cleaned Fare")
        sns.boxplot(x=train_cleaned["Age"], ax=ax2[1])
        ax2[1].set_title("Cleaned Age")
        st.pyplot(fig2)
        st.info("💡 Outliners 제거함으로써 모델 안정성을 향상시킴")

    with st.expander("📊 Correlation Heatmap"):
        correlation = train_cleaned[['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']].corr()
        fig3 = plt.figure(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, cmap="coolwarm")
        plt.title("Correlation Matrix")
        st.pyplot(fig3)
        st.info("💡 요금과 생존율은 중간 정도의 양의 상관관계를 보이며, 이는 더 많은 요금을 지불한 승객의 생존 확률이 더 높음을 의미함 \n\n"
                "💡P등급은 생존율과 음의 상관관계를 보이며, 이는 하위 등급 승객의 생존 확률이 더 낮음을 확인시켜 줌.")

    with st.expander("📈 Survival Rate (Sex, Embarked, Pclass)"):
        survival_by_sex = train_cleaned.groupby('Sex')['Survived'].mean().reset_index()
        survival_by_embarked = train_cleaned.groupby('Embarked')['Survived'].mean().reset_index()
        survival_by_pclass = train_cleaned.groupby('Pclass')['Survived'].mean().reset_index()


        col1, col2 = st.columns(2)
        with col1:
            fig4 = plt.figure()
            sns.barplot(data=survival_by_sex, x='Sex', y='Survived')
            plt.title("Survival by Sex")
            st.pyplot(fig4)
            st.info("💡 성별: 여성의 생존율이 남성보다 훨씬 높음.")

        with col2:
            fig5 = plt.figure()
            sns.barplot(data=survival_by_embarked, x='Embarked', y='Survived')
            plt.title("Survival by Embarked")
            st.pyplot(fig5)
            st.info("💡 등급별(P등급): 등급이 높을수록 생존율이 높음")

        fig6 = plt.figure()
        sns.barplot(data=survival_by_pclass, x='Pclass', y='Survived')
        plt.title("Survival by Pclass")
        st.pyplot(fig6)
        st.info(" 💡 탑승 항구별 생존율 요약:\n\n"
        "- 셰르부르(C): 가장 높은 생존율 (~53%)\n"
        "- 퀸스타운(Q): 가장 낮은 생존율 (~29%)\n"
        "- 사우샘프턴(S): 중간 등급 (~33%)")

    with st.expander("📌 Heatmap: Survival by Sex × Pclass"):
        heatmap_data = train_cleaned.pivot_table(index='Sex', columns='Pclass', values='Survived', aggfunc='mean')
        fig7 = plt.figure(figsize=(8, 5))
        sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt=".2f")
        st.pyplot(fig7)
        st.info("💡여성 + 1등석석 조합은 가장 높은 생존율을 보임 \n\n"
                "💡남성 + 3등석 조합은 가장 낮음")

    with st.expander("🧒 Survival by Age Group"):
        agegroup_survival = train_cleaned.groupby('AgeGroup')['Survived'].mean().reset_index()
        fig8 = plt.figure()
        sns.barplot(data=agegroup_survival, x='AgeGroup', y='Survived', palette='Blues_d')
        plt.ylim(0, 1)
        st.pyplot(fig8)
        st.info("💡어린이 (12세미만)와 성인(35~60세)은 상대적으로 생존율이 높음")

    with st.expander("👨‍👩‍👧 Survival by Age Group & Sex"):
        age_sex_group = train_cleaned.groupby(['AgeGroup', 'Sex'])['Survived'].mean().reset_index()
        fig9 = plt.figure(figsize=(10, 6))
        sns.barplot(data=age_sex_group, x='AgeGroup', y='Survived', hue='Sex', palette='Set2')
        plt.ylim(0, 1)
        st.pyplot(fig9)
        st.info("💡여성 생존율은 거의 모든 연령대에서 남성보다 높음")

    with st.expander("🔀 Survival by AgeGroup × Pclass × Sex"):
        age_pclass_sex_group = train_cleaned.groupby(['AgeGroup', 'Pclass', 'Sex'])['Survived'].mean().reset_index()
        g = sns.catplot(data=age_pclass_sex_group,
                        x='AgeGroup', y='Survived', hue='Sex',
                        col='Pclass', kind='bar', palette='Set2',
                        height=5, aspect=1)
        g.set_titles("Pclass {col_name}")
        g.set_axis_labels("Age Group", "Survival Rate")
        g.set(ylim=(0, 1))
        g.fig.subplots_adjust(top=0.8)
        g.fig.suptitle("Survival Rate by Age Group, Sex, and Pclass")
        st.pyplot(g)
        st.info("💡여성 생존율이 모든 연령대에서 더 높음\n\n "
                "💡어린이 생존율이 가장 높음 \n\n"
                "💡3등급은 남성 생존율은 거의 없음"
                )

    with st.expander("👪 Survival by Siblings/Spouses (SibSp)"):
        sibsp_survival = train_cleaned.groupby('SibSp')['Survived'].mean().reset_index()
        fig10 = plt.figure(figsize=(8, 5))
        sns.barplot(data=sibsp_survival, x='SibSp', y='Survived', palette='viridis')
        plt.ylim(0, 1) 
        plt.title("Survival by SibSp")
        st.pyplot(fig10)
        st.info("💡 적당한 수의 동반 가족 (1~2명)이 있을 때 생존율이 가장 높음, 동반자가 없거나 너무 많으면 생존율이 낮아짐")

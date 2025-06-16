import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from utils import load_train_and_test

def run_prediction():
    train,test = load_train_and_test()
    st.title("🔮 set data 결과 예측")

    # Load data
    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")


    # ==== Data Cleaning ====
    train['Age'] = train['Age'].fillna(train['Age'].mean())
    train['Embarked'] = train['Embarked'].fillna(train['Embarked'].mode()[0])
    train['Fare'] = train['Fare'].fillna(train['Fare'].mean())
    train = train.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)

    test['Age'] = test['Age'].fillna(test['Age'].mean())
    test['Fare'] = test['Fare'].fillna(test['Fare'].mean())
    test['Embarked'] = test['Embarked'].fillna(test['Embarked'].mode()[0])
    # Save PassengerId before dropping
    if 'PassengerId' in test.columns:
        test_ids = test['PassengerId']
        test = test.drop('PassengerId', axis=1)
    else:
        test_ids = test.index

# Drop unnecessary columns
    test = test.drop(['Cabin', 'Name', 'Ticket'], axis=1, errors='ignore')


    # ==== Encoding ====
    label_cols = ['Sex', 'Embarked']
    le = LabelEncoder()
    for col in label_cols:
        train[col] = le.fit_transform(train[col])
        test[col] = le.transform(test[col])

    # ==== Split Data ====
    X = train.drop('Survived', axis=1)
    y = train['Survived']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    # ==== Predict ====
    predictions = model.predict(test)

    # ==== Display ====
    st.subheader("✅ 예측 결과 미리보기")
    results = pd.DataFrame({
        "PassengerId": test_ids,
        "Survived": predictions
    })
    st.dataframe(results.head())

    # ==== Download Button ====
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 예측 결과 CSV 다운로드",
        data=csv,
        file_name='submission_logistic.csv',
        mime='text/csv',
    )

    st.subheader("📊 예측 결과 평가")

    # Load prediction and ground truth files
    prediction = pd.read_csv("submission_logistic.csv")
    ground_truth = pd.read_csv("gender_submission.csv")

    # Merge and compare
    merged = pd.merge(prediction, ground_truth, on="PassengerId", suffixes=("_pred", "_true"))
    merged["Match"] = merged["Survived_pred"] == merged["Survived_true"]
    accuracy = merged["Match"].mean()

    # Show accuracy
    st.metric(label="🎯 Accuracy", value=f"{accuracy*100:.2f}%")

    # Expandable: show comparison table
    with st.expander("📋 예측 결과 상세 비교"):
        st.dataframe(merged)

    # Confusion Matrix
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import matplotlib.pyplot as plt

    st.subheader("🔍 Confusion Matrix")

    y_true = merged["Survived_true"]
    y_pred = merged["Survived_pred"]
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Not Survived", "Survived"])

    fig, ax = plt.subplots(figsize=(6, 4))
    disp.plot(ax=ax, cmap='Blues', values_format='d')
    st.pyplot(fig)
    st.warning(" ⚠️ 모델 약점 :\n\n - False Negatives 많음 -> 실제 생존자 놓침 \n - False Positive 많음 -> 예측 실패한 사람이 생존이라고 예측")

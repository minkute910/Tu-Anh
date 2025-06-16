
import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    data = pd.read_csv('train.csv')
    return data

def load_train_and_test():
    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")
    return train,test


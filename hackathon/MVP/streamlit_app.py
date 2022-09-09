# Core Pkgs
import streamlit as st

# EDA Pkgs
import pandas as pd

# Data Viz Pkg
import matplotlib

# ML Packages

matplotlib.use("Agg")
st.set_page_config(layout="wide")
st.header("Прогноз результативности игрока по данным велоэргометрии")


def main():
    """Semi Automated ML App with Streamlit """

    activities = ["Загрузка данных", "Таблица игроков"]


if __name__ == '__main__':
    main()
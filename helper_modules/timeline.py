from helper_modules.imports import *
import streamlit as st
from streamlit_timeline import timeline


def plot_timeline():
    # load data
    with open('covid_timeline.json', "r") as f:
        data = f.read()

    # render timeline
    timeline(data, height=600)
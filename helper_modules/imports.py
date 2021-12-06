import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json, ast
import plotly.figure_factory as ff
import geopandas as gpd
from colour import Color
import plotly.express as px
import datetime as dt
import plotly.graph_objects as go
import calendar
import json
from urllib.request import urlopen
from plotly.subplots import make_subplots

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI"
}

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()
            }


@st.cache(allow_output_mutation=True)
def load_data():
    cases = pd.read_csv("cleaned/final_transformations/cleaned_cases.csv")
    cases_groups = pd.read_csv("cleaned/final_transformations/cleaned_case_groups.csv")
    vaccines = pd.read_csv("cleaned/final_transformations/cleaned_vaccinations.csv")
    mental_health_statewise = pd.read_csv("cleaned/final_transformations/df_mental_by_state_clean.csv")
    mental_health_nationwide = pd.read_csv("cleaned/final_transformations/df_mental_national_clean.csv")
    mental_health = pd.read_csv("cleaned/final_transformations/df_mental.csv")
    apple_mobility_state = pd.read_csv("cleaned/final_transformations/apple_mobility_states.csv")
    apple_mobility_time = pd.read_csv("cleaned/final_transformations/apple_mobility_time.csv")
    google_national_data = pd.read_csv('cleaned/googleNational.csv')
    google_state_data = pd.read_csv('cleaned/googleState.csv').set_index('sub_region_1')
    mobility_policy = pd.read_csv("cleaned/cleaned_mobility_policy_data.csv")
    mobility_groups = pd.read_csv("cleaned/cleaned_formatted_mobility.csv")
    energy_change_states_negative = pd.read_csv("cleaned/energy__change-states-negative.csv")
    energy_change_states_positive = pd.read_csv("cleaned/energy__change-states-positive.csv")
    energy_change_states = pd.read_csv("cleaned/energy__change-states.csv")
    energy_change_states_heatmap = pd.read_csv("cleaned/energy__state-aggregation-heatmap.csv")


    return cases, vaccines, mental_health_statewise, mental_health_nationwide, mental_health, apple_mobility_state, \
           apple_mobility_time, google_national_data, google_state_data, mobility_policy, mobility_groups, cases_groups, \
          energy_change_states_negative, energy_change_states_positive, energy_change_states, energy_change_states_heatmap

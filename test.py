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

# import plotly, plotly.graph_objects as go

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

st.set_page_config(layout="wide")


@st.cache
def load_data():
    cases = pd.read_csv("cleaned/final_transformations/cleaned_cases.csv")
    vaccines = pd.read_csv("cleaned/final_transformations/cleaned_vaccinations.csv")

    mental_health_statewise = pd.read_csv("cleaned/final_transformations/df_mental_by_state_clean.csv")
    mental_health_nationwide = pd.read_csv("cleaned/final_transformations/df_mental_national_clean.csv")
    mental_health = pd.read_csv("cleaned/final_transformations/df_mental.csv")
    apple_mobility_state = pd.read_csv("cleaned/final_transformations/apple_mobility_states.csv")
    apple_mobility_time = pd.read_csv("cleaned/final_transformations/apple_mobility_time.csv")
    return cases, vaccines, mental_health_statewise, mental_health_nationwide, mental_health, apple_mobility_state, apple_mobility_time


st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True)

st.markdown("""

<script language="javascript">

function changeHeader() {
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('p');
    var element = document.getElementById(myParam);
    
    
    console.log(element);
    element.classList.add("active");
}

console.log('Hello');
changeHeader();
console.log('Done');

</script>

<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" target="_blank">Covid Impact Analysis</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="nav navbar-nav">
      <li class="nav-item active" id="home">
        <a class="nav-link" href="http://localhost:8501?p=home">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item" id="traffic">
        <a class="nav-link" href="http://localhost:8501?p=traffic">Traffic</a>
      </li>
      <li class="nav-item" id="power">
        <a class="nav-link" href="http://localhost:8501?p=power">Power</a>
      </li>
      <li class="nav-item" id="well-being">
        <a class="nav-link" href="http://localhost:8501?p=well-being">Well being</a>
      </li>
      <li class="nav-item" id="life-today">
        <a class="nav-link" href="http://localhost:8501?p=life-today">Life Today</a>
      </li>
      <li class="nav-item" id="life-tomorrow">
        <a class="nav-link" href="http://localhost:8501?p=life-tomorrow">Life Tomorrow</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)


def navigation():
    try:
        path = st.experimental_get_query_params()['p'][0]
    except Exception as e:
        st.error('Please use the main app.')
        return None
    return path

def plot_cases_data(cases):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many cases have been registered in the United States?")

def plot_vaccination_data(vaccines):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many vaccines have been distributed in the United States?")
    types_of_vaccines = col.multiselect("Types of Vaccine Doses",
                                        ["Total Doses", "Moderna Doses", "Pfizer Doses", "Booster Doses",
                                         "Johnson & Johnson Doses"], default=["Total Doses"])

    vaccine_columns = types_of_vaccines
    vaccine_columns.append('Date')
    vaccines_filtered = vaccines[vaccine_columns]

    fig = px.line(vaccines_filtered, x="Date", y=vaccine_columns, markers=True)
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(legend_title_text='Types of Vaccines',
                      title='Number of Vaccines distributed per day (Smoothed over a week)',
                      xaxis_title='Date',
                      yaxis_title='No of Vaccines Administered (In Millions)')
    col.plotly_chart(fig, use_container_width=True)


# Loading the data from the cache
cases, vaccines, mental_health_statewise, mental_health_nationwide, mental_health, apple_mobility_state, apple_mobility_time = load_data()


def plot_mental_health(mental_health_statewise, mental_health, mental_health_nationwide):
    buff, col, buff2 = st.columns([1, 3, 1])

    types_of_groups = col.multiselect("Types of Groups", ['National Estimate', 'By Age', 'By Sex',
                                         'By Race/Hispanic ethnicity', 'By Education'], default=["National Estimate"])

    mental_health_nationwide_filtered = mental_health_nationwide[mental_health_nationwide['Group'].isin(types_of_groups)].rename(columns={"Time Period End Date":"Date"})

    national_pivot = pd.pivot_table(
        mental_health_nationwide_filtered[mental_health_nationwide_filtered["Indicator"] == 'Symptoms of Anxiety Disorder or Depressive Disorder'],
        values='Value',
        index='Date',
        columns='Subgroup'
    )

    fig = px.line(national_pivot, title="Symptoms of Anxiety Disorder or Depressive Disorder Nationally", markers=True)
    fig.update_xaxes(
        tickformat='%d-%b-%Y',
        tickangle=45,
        showticklabels=True,
        title="Date of Response",
        gridwidth=0.5, gridcolor='lightslategray'
    )
    fig.update_yaxes(title='Percentage of Participants With Symptoms', gridwidth=0.5, gridcolor='lightslategray')
    fig.update_layout(width=1000, height=500)
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    col.plotly_chart(fig, use_container_width=True)


def plot_apple_data(apple_mobility_state, apple_mobility_time):
    buff, col, buff2 = st.columns([1, 3, 1])
    fig = px.line(apple_mobility_time.dropna(), x="month_year", y="transit", hover_data=['transit'])
    fig.update_layout(title='Changes in transit patterns in the United States',
                      xaxis_title='Time',
                      yaxis_title='% change in transit from baseline')
    col.plotly_chart(fig, use_container_width=True)

    def df_to_plotly(df):
        return {'z': df.values.tolist(),
                'x': df.index.tolist(),
                'y': df.columns.tolist()
        }

    apple_mobility_state = apple_mobility_state.set_index('month_year')
    apple_mobility_state.columns = apple_mobility_state.columns.map(us_state_to_abbrev)
    fig = go.Figure(
        data=go.Heatmap(df_to_plotly(apple_mobility_state), type='heatmap', colorscale='rdbu'),
        layout=go.Layout(width=600, height=1000,
                         title="Percentage change in transit traffic compared to baseline (2019)"))

    col.plotly_chart(fig, use_container_width=True)


if navigation() == "home":
    st.title('Home')
    st.write('This is the home page.')

    plot_cases_data(cases)
    plot_vaccination_data(vaccines)


elif navigation() == "traffic":
    st.title('Traffic')
    st.write('This is the Traffic page.')

    plot_apple_data(apple_mobility_state, apple_mobility_time)

elif navigation() == "power":
    st.title('Power')
    st.write('This is the Power page.')

elif navigation() == "well-being":
    st.title('Well being')
    st.write('This is the Well being page.')
    plot_mental_health(mental_health_statewise, mental_health, mental_health_nationwide)


elif navigation() == "life-today":
    st.title('Life Today')
    st.write('This is the Life Today page.')

elif navigation() == "life-tomorrow":
    st.title('Life Tomorrow')
    st.write('This is the Life Tomorrow page.')

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
#import plotly, plotly.graph_objects as go

st.set_page_config(layout="wide")

@st.cache 
def load_data():

    # Reading engagement data
    engagements = pd.read_csv("cleaned/cleaned_engagement_data.csv")
    
    # Reading State wise School Policy data 
    school_policy = pd.read_csv("cleaned/cleaned_school_policy_data.csv")
    
    # Reading Google Mobility data
    mobility = pd.read_csv("cleaned/cleaned_formatted_mobility.csv")
    
    # Reading State wise Mobility Policy data 
    mobility_policy = pd.read_csv("cleaned/cleaned_mobility_policy_data.csv")
    
    # Reading Apple Mobility traffic information based on years
    apple_mobility2020 = pd.read_csv('cleaned/cleaned_apple_mobility2020.csv').set_index('state')
    apple_mobility2021 = pd.read_csv('cleaned/cleaned_apple_mobility2021.csv').set_index('state')
    
    return engagements, school_policy, mobility, mobility_policy, apple_mobility2020, apple_mobility2021

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" target="_blank">Covid Impact Analysis</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="http://localhost:8501">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="http://localhost:8501?p=analysis" >Analysis</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="http://localhost:8501?p=results">Results</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="http://localhost:8501?p=logs">Logs</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)


engagements, school_policy, mobilityGroups, mobility_policy, apple_mobility2020, apple_mobility2021 = load_data()
def navigation():
    try:
        path = st.experimental_get_query_params()['p'][0]
    except Exception as e:
        st.error('Please use the main app.')
        return None
    return path


if navigation() == "home":
    st.title('Home')
    st.write('This is the home page.')

elif navigation() == "results":
    buff, col, buff2 = st.columns([1,3,1])
    col.title("How has COVID affected the daily lives of people?")
    col.markdown("On 17th November 2019 the first case of COVID-19 was detected. It has been almost two years since then and the world continues to change and adapt to the ever-evolving pandemic. These changes can be classfied as macro and micro level changes. The former refers to changes at a global scale whereas the latter refers to changes at an individual's scale. Macro level changes include the effects on global economy, trade and commerce. Such changes have been quantified and presented in numerous studies. However, the effects of COVID at a micro level are just as apparent and important. The pandemic has led to subtle and not-so-subtle adjustments in the daily routines of people. These adjustments will cumulate over time and lead to several social and psychological repercussions. This is a study to attempt to quantify these adjustments and discuss the possible implications. The visualizations have been ordered in a descending order according to impact. Thus the impact on the lives of children has been discussed first and we then go on to discuss the changes for adults.")
    col.markdown("******")
    col.header("How has COVID-19 affected the lives of children?")
    col.markdown("To prevent the spread of infection, public schools were shut down all across the United States. Different schools were shut at different times in accordance with state policies.")

    buff, col2, buff2 = st.columns([2,3,2])
    slider = col2.slider('Move the slider below to view schools in states getting shut over the course of 2020.', min_value = dt.date(year=2020,month=3,day=10), max_value = dt.date(year=2020,month=4,day=4), format='MM-DD-YYYY')
    school_policy = school_policy.dropna(subset=["date"])[['State Abbreviation','date']]
    school_policy['Public Schools Closed'] = (pd.to_datetime(school_policy['date'], format='%d/%m/%y') < pd.to_datetime(slider)).astype('str')

    # Plotting the closed states based on the selected date
    fig = px.choropleth(school_policy,  # Input Pandas DataFrame
                        locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                        hover_name="State Abbreviation", # DataFrame column hover info
                        locationmode = 'USA-states',
                        color='Public Schools Closed',
                       color_discrete_map={'True':'red',
                                            'False':'blue'}) # Set to plot as US States
    fig.add_scattergeo(name='State Names',
        locations=school_policy['State Abbreviation'],
        locationmode='USA-states',
        text=school_policy['State Abbreviation'],
        mode='text')
    fig.update_layout( # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
        
    )
    buff, col, buff2 = st.columns([1,3,1])
    col.plotly_chart(fig, use_container_width=True)

    col.markdown("******")

    buff, col, buff2 = st.columns([1,3,1])
    col.header("How have schools adapted to these changes?")
    tools = col.multiselect("Educational Tools", ["Zoom", "Google Classroom","Canvas","Schoology", "Google Docs", "Google Sheets", "Duolingo",  "Grammarly", "Quizlet","i-Ready"], default=["Duolingo", "Zoom"])

    columns = tools
    columns.append('time')
    engagements_df = engagements[columns]
    # Plotting the engagemnet data 
    fig = px.line(engagements_df, x = "time", y = tools, markers=True)
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_layout(legend_title_text='Educational tools', title='Usage of various Education tools during 2020',
                       xaxis_title='Month',
                       yaxis_title='Usage')
    col.plotly_chart(fig, use_container_width=True)
    col.markdown("Interestingly, one can clearly see the sharp or gradual rise in the usage of these tools around March and April. Another interesting observation is that Duolingo is the only tool that shows a sharp decline since March. This can be explained by the imposition of travel restrictions around that time.")
    buff, col, buff2 = st.columns([1,3,1])
    col.markdown("The long term impact of these changes is currently unknown and can merely be guessed. Both physical and mental development of children is bound to be affected. Increased screen time has become unavoidable and children are missing out on peer interactions that are vital for soft skills development. Another case to consider would be of infants who have spent the first 2 years of their lives completely indoors. ")
    col.markdown("******")
    col.header("What about adults?")
    col.markdown("The government issued stay-at-home regulations to curb the growing number of cases. Different states issued orders at different times in as a reactionary response to the number of active cases.")
    


elif navigation() == "analysis":
    buff, col2, buff2 = st.columns([2,3,2])
    slider = col2.slider('Move the slider below to view states issuing stay-at-home orders over the course of 2020.', min_value = dt.date(year=2020,month=2,day=28), max_value = dt.date(year=2020,month=3,day=22), format='MM-DD-YYYY')
    mobility_policy = mobility_policy.dropna(subset=["MobilityRestrictedDate"])[['State Abbreviation','MobilityRestrictedDate']]
    mobility_policy['Stay at Home Policy declared'] = (pd.to_datetime(mobility_policy['MobilityRestrictedDate'], format='%m/%d/%Y') < pd.to_datetime(slider,errors='coerce')).astype('str')

    # Plotting the closed states based on the selected date
    fig = px.choropleth(mobility_policy,  # Input Pandas DataFrame
                        locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                        hover_name="State Abbreviation", # DataFrame column hover info
                        locationmode = 'USA-states',
                        color='Stay at Home Policy declared',
                       color_discrete_map={'True':'red',
                                            'False':'blue'}) # Set to plot as US States
    fig.add_scattergeo(name='State Names',
        locations=mobility_policy['State Abbreviation'],
        locationmode='USA-states',
        text=school_policy['State Abbreviation'],
        mode='text')
    fig.update_layout(# Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
        
    )
    buff, col, buff2 = st.columns([1,3,1])
    col.plotly_chart(fig, use_container_width=True)
    col.markdown("The daily activities of adults have changed quite a bit due to restrictions on movements in public areas. These changes can be tracked by measuring the percent change in frequency of commonly visited places. Workplaces were the first to shut and we see a large negative change from our baseline (pre-pandemic times). Parks were frequented more often and there was a sharp decline in mall visits.")
    fig = make_subplots(rows=2, cols=2, start_cell="top-left", shared_yaxes=True)

    fig.add_trace(go.Scatter(x=mobilityGroups["date"].values,y=mobilityGroups["Workplaces"].values.tolist(), fill='tozeroy', name='Workplaces'),row=1, col=1)
    fig.add_trace(go.Scatter( x=mobilityGroups["date"].values,y=mobilityGroups['Parks'].values.tolist(),fill='tozeroy', name='Parks'),row=1, col=2)
    fig.add_trace(go.Scatter( x=mobilityGroups["date"].values,y=mobilityGroups['Grocery and Pharmacy'].values.tolist(),fill='tozeroy', name='Grocery and Pharmacy'),row=2, col=1)
    fig.add_trace(go.Scatter( x=mobilityGroups["date"].values,y=mobilityGroups['Retail and Recreation'].values.tolist(), fill='tozeroy', name='Retail and Recreation'),row=2, col=2)

    fig.update_xaxes(title_text="Workplaces", row = 1, col = 1,showticklabels=True)
    fig.update_xaxes(title_text="Parks", row = 1, col = 2,showticklabels=True)
    fig.update_xaxes(title_text="Grocery and Pharmacy", row = 2, col = 1,showticklabels=True)
    fig.update_xaxes(title_text="Retail and Recreation", row = 2, col = 2,showticklabels=True)

    # Update yaxis properties
    fig.update_yaxes(title_text="Percentage change", row=1, col=1,showticklabels=True)
    fig.update_yaxes( row=1, col=2,showticklabels=True)
    fig.update_yaxes(title_text="Percentage change", row=2, col=1,showticklabels=True)
    fig.update_yaxes( row=2, col=2,showticklabels=True)

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_layout(width=int(1500), height = int(750))
    fig.update_layout(legend_title_text='Commonly Visited Places', title='Percentage Change in Frequency of commonly visited places compared to baseline (2019)')
    # fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    # fig = px.line(mobilityGroups, x='date' , y='value',color='variable')
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    st.plotly_chart(fig, use_container_width=True)
    buff, col, buff2 = st.columns([1,3,1])
    col.markdown("******")


elif navigation() == "examples":
    st.title('Examples Menu')
    st.write('Select an example.')


elif navigation() == "logs":
    def convert(month_idx):
        return calendar.month_abbr[int(month_idx)]
    def df_to_plotly(df):
        x = df.columns.tolist()
        x = list(map(convert, x))
        return {'z': df.values.tolist(),
                'x': x,
                'y': df.index.tolist()}

    buff, col, buff2 = st.columns([1,3,1])
    col.markdown("******")
    col.markdown("To look at the positive side of things, in response to schools shutting and stay-at-home orders being issued, transit traffic reduced significantly in 2020. This year as few workplaces opened up and restrictions have been eased, traffic levels have increased again. This can be seen in the heatmap below.")

    buff, col, buff2 = st.columns([6,1,6])
    yearOption = col.selectbox('Year',('2020','2021'))

    if(yearOption == '2020'):
        fig = go.Figure(
                data=go.Heatmap(df_to_plotly(apple_mobility2020), type = 'heatmap', colorscale = 'rdbu'),
                layout=go.Layout(width = 600,height = 1000, title="Percentage change in transit traffic compared to baseline (2019)"))
    else:
        fig = go.Figure(
                data=go.Heatmap(df_to_plotly(apple_mobility2021), type = 'heatmap', colorscale = 'rdbu'),
                layout=go.Layout(width = 600,height = 1000, title="Percentage change in transit traffic compared to baseline (2019)"))

    buff, col, buff2 = st.columns([1,3,1])
    col.plotly_chart(fig, use_container_width=True)
    col.markdown("******")


elif navigation() == "verify":
    st.title('Data verification is started...')
    st.write('Please stand by....')


elif navigation() == "config":
    st.title('Configuration of the app.')
    st.write('Here you can configure the application')

st.markdown('''# **Binance Price App**
A simple cryptocurrency price app pulling price data from *Binance API*.
''')

st.header('**Selected Price**')

# Load market data from Binance API
df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')

# Custom function for rounding values
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a

col1, col2, col3 = st.columns(3)

# Widget (Cryptocurrency selection box)
col1_selection = st.sidebar.selectbox('Price 1', df.symbol, list(df.symbol).index('BTCBUSD') )
col2_selection = st.sidebar.selectbox('Price 2', df.symbol, list(df.symbol).index('ETHBUSD') )
col3_selection = st.sidebar.selectbox('Price 3', df.symbol, list(df.symbol).index('BNBBUSD') )
col4_selection = st.sidebar.selectbox('Price 4', df.symbol, list(df.symbol).index('XRPBUSD') )
col5_selection = st.sidebar.selectbox('Price 5', df.symbol, list(df.symbol).index('ADABUSD') )
col6_selection = st.sidebar.selectbox('Price 6', df.symbol, list(df.symbol).index('DOGEBUSD') )
col7_selection = st.sidebar.selectbox('Price 7', df.symbol, list(df.symbol).index('SHIBBUSD') )
col8_selection = st.sidebar.selectbox('Price 8', df.symbol, list(df.symbol).index('DOTBUSD') )
col9_selection = st.sidebar.selectbox('Price 9', df.symbol, list(df.symbol).index('MATICBUSD') )

# DataFrame of selected Cryptocurrency
col1_df = df[df.symbol == col1_selection]
col2_df = df[df.symbol == col2_selection]
col3_df = df[df.symbol == col3_selection]
col4_df = df[df.symbol == col4_selection]
col5_df = df[df.symbol == col5_selection]
col6_df = df[df.symbol == col6_selection]
col7_df = df[df.symbol == col7_selection]
col8_df = df[df.symbol == col8_selection]
col9_df = df[df.symbol == col9_selection]

# Apply a custom function to conditionally round values
col1_price = round_value(col1_df.weightedAvgPrice)
col2_price = round_value(col2_df.weightedAvgPrice)
col3_price = round_value(col3_df.weightedAvgPrice)
col4_price = round_value(col4_df.weightedAvgPrice)
col5_price = round_value(col5_df.weightedAvgPrice)
col6_price = round_value(col6_df.weightedAvgPrice)
col7_price = round_value(col7_df.weightedAvgPrice)
col8_price = round_value(col8_df.weightedAvgPrice)
col9_price = round_value(col9_df.weightedAvgPrice)

# Select the priceChangePercent column
col1_percent = f'{float(col1_df.priceChangePercent)}%'
col2_percent = f'{float(col2_df.priceChangePercent)}%'
col3_percent = f'{float(col3_df.priceChangePercent)}%'
col4_percent = f'{float(col4_df.priceChangePercent)}%'
col5_percent = f'{float(col5_df.priceChangePercent)}%'
col6_percent = f'{float(col6_df.priceChangePercent)}%'
col7_percent = f'{float(col7_df.priceChangePercent)}%'
col8_percent = f'{float(col8_df.priceChangePercent)}%'
col9_percent = f'{float(col9_df.priceChangePercent)}%'

# Create a metrics price box
col1.metric(col1_selection, col1_price, col1_percent)
col2.metric(col2_selection, col2_price, col2_percent)
col3.metric(col3_selection, col3_price, col3_percent)
col1.metric(col4_selection, col4_price, col4_percent)
col2.metric(col5_selection, col5_price, col5_percent)
col3.metric(col6_selection, col6_price, col6_percent)
col1.metric(col7_selection, col7_price, col7_percent)
col2.metric(col8_selection, col8_price, col8_percent)
col3.metric(col9_selection, col9_price, col9_percent)

st.header('**All Price**')
st.dataframe(df)

st.info('Credit: Created by Chanin Nantasenamat (aka [Data Professor](https://youtube.com/dataprofessor/))')

st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)


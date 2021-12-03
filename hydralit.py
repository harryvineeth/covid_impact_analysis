import streamlit as st
import hydralit_components as hc
import datetime
from helper_modules.imports import *
from helper_modules.cases import *
from helper_modules.home import *
from helper_modules.mental_health import *
from helper_modules.life_today import *
from helper_modules.life_tomorrow import *
from helper_modules.power import *
from helper_modules.mobility import *

#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# specify the primary menu definition
menu_data = [
    {'id':'traffic','icon': "🚦", 'label':"Traffic"},
    {'id':'power','icon': "⚡", 'label':"Power"},
    {'id':'well-being','icon':"🎗",'label':"Well-Being"},
    {'id':'life-today','icon':"🦠",'label':"Life-Today"},
    {'id':'life-tomorrow','icon':"❓",'label':"Life-Tomorrow"},
    # {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    # {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
    # {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
    # {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    # {'icon': "far fa-copy", 'label':"Right End"},
    # {'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
]

#over_theme = {'txc_inactive': '#FFFFFF','menu_background':'red','txc_active':'yellow','option_active':'blue'}
over_theme = {'txc_inactive': '#FFFFFF','menu_background':'blue'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if st.button('click me'):
  st.info('You clicked at: {}'.format(datetime.datetime.now()))


if st.sidebar.button('click me too'):
  st.info('You clicked at: {}'.format(datetime.datetime.now()))

#get the id of the menu item clicked
st.info(f"{menu_id}")

cases, vaccines, mental_health_statewise, mental_health_nationwide, mental_health, apple_mobility_state, apple_mobility_time, google_national_data, google_state_data = load_data()


if menu_id == "Home":
    run_home(cases, vaccines)

elif menu_id == "traffic":
    run_mobility(apple_mobility_state, apple_mobility_time, google_national_data, google_state_data)

elif menu_id == "power":
    run_power()

elif menu_id == "well-being":
    run_mental_health(mental_health_statewise, mental_health, mental_health_nationwide)

elif menu_id == "life-today":
    run_life_today()

elif menu_id == "life-tomorrow":
    run_life_tomorrow()

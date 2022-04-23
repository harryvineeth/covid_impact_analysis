from helper_modules.imports import *
from helper_modules.cases import *
from helper_modules.home import *
from helper_modules.mental_health import *
from helper_modules.conclusion import *
from helper_modules.power import *
from helper_modules.mobility import *


st.set_page_config(layout="wide")

st.markdown(
    """<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;1,200;1,300;1,400;1,600&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #700B97; height: 80px; font-family: 'Source Serif Pro', serif;">
  <a class="navbar-brand" style="font-size: 30px;" target="_blank">COVID Impact Analysis</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="nav navbar-nav">
      <li class="nav-item active" id="home" style="font-size: 20px;">
        <a class="nav-link" href="https://share.streamlit.io/harryvineeth/covid_impact_analysis/streamlit/covid_analysis.py?p=home">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active" id="traffic"  style="font-size: 20px;">
        <a class="nav-link" href="https://share.streamlit.io/harryvineeth/covid_impact_analysis/streamlit/covid_analysis.py?p=traffic">Traffic</a>
      </li>
      <li class="nav-item active" id="power"  style="font-size: 20px;">
        <a class="nav-link" href="https://share.streamlit.io/harryvineeth/covid_impact_analysis/streamlit/covid_analysis.py?p=power">Power</a>
      </li>
      <li class="nav-item active" id="well-being"  style="font-size: 20px;">
        <a class="nav-link" href="https://share.streamlit.io/harryvineeth/covid_impact_analysis/streamlit/covid_analysis.py?p=well-being">Well being</a>
      </li>
      <li class="nav-item active" id="conclusion" style="font-size: 20px;">
        <a class="nav-link" href="https://share.streamlit.io/harryvineeth/covid_impact_analysis/streamlit/covid_analysis.py?p=Conclusion">Conclusion</a>
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


# Loading the data from the cache
cases, vaccines, mental_health_statewise, mental_health_nationwide, mental_health, apple_mobility_state, apple_mobility_time, google_national_data, google_state_data, mobility_policy, mobility_groups, cases_groups, energy_change_national, energy_change_states, energy_change_states_heatmap = load_data()

# -------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                NAVIGATION
# -------------------------------------------------------------------------------------------------------------------------------------------------

def navigation():
    try:
        path = st.experimental_get_query_params()['p'][0]
    except Exception as e:
        path = 'home'
    return path


if navigation() == "home":
    run_home(cases, vaccines, mobility_policy, cases_groups)

elif navigation() == "traffic":
    run_mobility(apple_mobility_state, apple_mobility_time, google_national_data, google_state_data, mobility_groups)

elif navigation() == "power":
    run_power( energy_change_national, energy_change_states, energy_change_states_heatmap)

elif navigation() == "well-being":
    run_mental_health(mental_health_statewise, mental_health, mental_health_nationwide)

elif navigation() == "Conclusion":
    run_conclusion()

else:
    run_home(cases, vaccines, mobility_policy, cases_groups)

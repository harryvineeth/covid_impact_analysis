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
    """,
    unsafe_allow_html=True)

st.markdown("""
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
      <li class="nav-item active" id="traffic">
        <a class="nav-link" href="http://localhost:8501?p=traffic">Traffic</a>
      </li>
      <li class="nav-item active" id="power">
        <a class="nav-link" href="http://localhost:8501?p=power">Power</a>
      </li>
      <li class="nav-item active" id="well-being">
        <a class="nav-link" href="http://localhost:8501?p=well-being">Well being</a>
      </li>
      <li class="nav-item active" id="conclusion">
        <a class="nav-link" href="http://localhost:8501?p=Conclusion">Conclusion</a>
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
cases, vaccines, mental_health_statewise, mental_health_nationwide, mental_health, apple_mobility_state, apple_mobility_time, google_national_data, google_state_data, mobility_policy, mobility_groups, cases_groups, energy_change_states_combined, energy_change_states, energy_change_states_heatmap = load_data()

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
    run_power( energy_change_states_combined, energy_change_states, energy_change_states_heatmap)

elif navigation() == "well-being":
    run_mental_health(mental_health_statewise, mental_health, mental_health_nationwide)

elif navigation() == "conclusion":
    run_conclusion()

else:
    run_home(cases, vaccines, mobility_policy, cases_groups)

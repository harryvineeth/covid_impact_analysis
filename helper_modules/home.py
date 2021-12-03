from helper_modules.imports import *
from helper_modules.cases import *


def run_home(cases, vaccines, mobility_policy):
    st.title('Home')
    st.write('This is the home page.')

    plot_policy_data(mobility_policy)
    plot_cases_data(cases)
    plot_vaccination_data(vaccines)
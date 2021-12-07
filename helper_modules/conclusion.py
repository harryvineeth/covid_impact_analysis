from helper_modules.imports import *
from helper_modules.model import *


def plot_model():
    buff, col1, col2, buff2 = st.columns([1, 1.5, 1.5, 1])

    with col1:
        state_option = st.selectbox(' Please select the location you want to infect', (
            "Alabama", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
            "Georgia", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
            "Maryland",
            "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
            "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
            "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
            "Vermont",
            "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "District of Columbia", "American Samoa",
            "Guam",
            "Northern Mariana Islands", "Puerto Rico", "United States Minor Outlying Islands", "U.S. Virgin Islands"))
    with buff2:
        months_option = col2.selectbox(' Please select the number of levels you want to see the game',
                                      ("1", "2", "3", "4", "5", "6", "7", "8", "10"))
    state = us_state_to_abbrev[state_option]
    buff, col, buff2 = st.columns([1, 3, 1])
    model_df = run_model(state, int(months_option))
    months = ['Nov 2021', 'Dec 2021', 'Jan 2022', 'Feb 2022', 'Mar 2022', 'Apr 2022', 'May 2022', 'Jun 2022',
              'Jul 2022', 'Aug 2022', 'Sep 2022', 'Oct 2022', 'Nov 2022', 'Dec 2022']
    months_cumulative = []
    months_filtered = months[: int(months_option) + 1]
    for i in range(55):
        months_cumulative = months_cumulative + months_filtered
    df = model_df.melt(var_name='State', value_name='Cases')
    df['Date'] = months_cumulative
    fig = px.choropleth(df,
                        locations='State',
                        color="Cases",
                        hover_name="State",
                        color_continuous_scale="reds",
                        animation_frame='Date',
                        locationmode='USA-states',
                        scope="usa",
                        range_color=(10000,350000000),
                        title='Number of cases by state (logarithmic scale)',
                        height=600,
                        )
    fig.update_layout(  # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#4E5D6C'))
    col.plotly_chart(fig, use_container_width=True)


def run_conclusion():
    st.title('Conclusion')
    st.write('This is the Life Today page')
    plot_model()

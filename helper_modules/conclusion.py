from helper_modules.imports import *
from helper_modules.model import *


def plot_model():

    buff, col, buff2 = st.columns([1, 3, 1])
    col.markdown("From our analysis it is pretty evident that COVID-19 has affected many aspects of our lives. An action as simple as turning the door knob of your apartment building could set a chain reaction of COVID cases. On the more positive side, the simple choice of getting vaccinated could get us a step closer to reaching herd immunity. To truly understand the consequences of our actions let us play a game. ")
    infect_option = col.selectbox("Please choose an action.",("Infect","Vaccinate"))
    if(infect_option =="Infect"):
        col.markdown("The date is December 30th. You are excited to come back home to your family in the United States to ring in the New Year. Your flight leaves Wuhan airport soon. You are feeling a bit under the weather but nothing a good night’s rest can’t fix. Due to the news of a recent disease spreading, authorities in China have advised you to “quarantine” for 15 days. The disease sounds pretty rare and looks like the news will die down soon. What are the chances that you could have it anyway? Besides, you are excited to spend the New Years with your family. You choose to ignore the warnings and book the last leg of your flight. (Spolier alert: Your choices could affect the entire county!)")
    else:
        col.markdown("The date is December 6th. You and your team of hardworking researchers have been working on creating a vaccine that is immune to all possible future strains of COVID. After multiple rounds of testing in Europe, you can say with some certainty that the team succeeded in achieving its goal. You fly down from your laboratory in the Netherlands to start the initial rounds of vaccination in the United States. You have been talking to multiple state governments and advising them to start vaccination as soon as possible. Choose the first state that follows your advice.")

    buff, col1, col2, buff2 = st.columns([1, 1.5, 1.5, 1])
    state_option = col1.selectbox(' Please select the location you want to land in', (
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

    months_option = col2.selectbox(' Please select how much you want to propagate the virus/vaccine',
                                   ("4", "5", "6", "7", "8", "10"))
    state = us_state_to_abbrev[state_option]
    buff, col, buff2 = st.columns([1, 3, 1])
    model_df = run_model(state, int(months_option),infect_option)
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
                        color_continuous_scale="purpor",
                        animation_frame='Date',
                        locationmode='USA-states',
                        scope="usa",
                        range_color=(10000,90000000),
                        title='Number of cases by state (logarithmic scale)',
                        height=600,
                        )
    fig.update_layout(  # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#4E5D6C'))
    col.plotly_chart(fig, use_container_width=True)


def run_conclusion():
    plot_model()

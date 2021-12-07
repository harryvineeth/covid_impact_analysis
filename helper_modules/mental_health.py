from helper_modules.imports import *


def run_mental_health(mental_health_statewise, mental_health, mental_health_nationwide):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How do you measure a change in mental wellbeing?")
    col.markdown(
        "In the graph below, we tracked some of the results of the National Health Pulse Survey, conducted every week since April 2020, which sought to measure the general health of the nation through online self-reported polls [CDC]. Although the survey consists of over 40 questions, we focused on two: have you experienced any symptoms of anxiety disorder and have you experienced any symptoms of depressive disorder. Since this survey uses the same questions as the National Health Interview Survey (NHIS), we can compare the national averages from 2020 and 2021 to 2019. The NHIS is only conducted yearly, however, so we included the 2019 average, 16.5%,  as a baseline in the above graph  [Villaroel]. The difference is striking. During the COVID-19 pandemic period the average number of reported symptoms for anxiety or depressive disorder was 35.8% higher, than the pre-covid average.")

    plot_mental_health(mental_health_statewise, mental_health, mental_health_nationwide)


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
    fig.add_hline(y=20, line_dash="dot",
                  annotation_text="2019 baseline",
                  annotation_position="bottom right",
                  annotation_font_size=15,
                  annotation_font_color="white"
                  )
    fig.add_hline(y=10)
    fig.add_vrect(x0="2020-11-15",
                   x1="2021-01-15",
                  annotation_text="     Covid Cases Peak", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.add_vrect(x0="2021-06-01",
                  x1="2021-07-01",
                  annotation_text="Delta Variant Starts", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)

    fig.update_xaxes(
        tickformat='%b %Y',
        showticklabels=True,
        title="Date of Response",
        gridwidth=0.5, gridcolor='lightslategray'
    )
    fig.update_yaxes(title='Percentage of Participants With Symptoms', gridwidth=0.5, gridcolor='lightslategray')
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    col.plotly_chart(fig, use_container_width=True)

    col.header("Are COVID-19 waves visible?")
    col.markdown(
        'There are two major peaks, which are visible in every sub-group. The first centers on the month of July 2020, the second spans from roughly November through January of 2021. Both these periods match to peaks in COVID cases, with December 2020 breaking many of the records for most single-day COVID-19 cases set in July 2020. Now, this indicates a high correlation, but does it show causation? In the summer of 2020, the U.S. saw mass Black Lives Matter (BLM) protests across the country, showing greater civil unrest than just the pandemic. A time graph of those demonstrations, however, has the vast majority of BLM protests happening in May and early June, with only two happening in early July and around three in late July[ACLED].  The COVID-19 cases however, have a sharp rise in early July, and then begin to reduce later in the month, matching the peak, and fall, for anxiety or depressive disorder symptoms from our graph.')

    col.markdown("Similarly, November 2020 also had several political factors to consider when looking at the nation’s mental wellbeing. The elections of 2020 were extremely contentious, with tensions eventually rising to a head during the storming of the capitol on January 6th 2021. Likewise, the national average for anxiety or depressive disorders stayed at their highest, with roughly 45% of participants reporting symptoms. Moreover, January 2021 saw the highest number of case counts and deaths due to COVID-19 the U.S. has experienced to date. Nothing can be looked at in a vacuum, but to have over double the previous year’s national average of symptoms for four straight months suggests the COVID-19 wave from November 2020 through February 2021 had an impact on the nation’s wellbeing. Especially when considering isolation measures likely prevented families from celebrating the holidays normally, adding even more stress to the situation.")
    state_pivot = pd.pivot_table(
    mental_health_statewise,
    values= 'Value',
    index = 'Time Period End Date',
    columns = 'State')

    fig2 = go.Figure(data=go.Heatmap(df_to_plotly(state_pivot.T), type='heatmap', colorscale='blues'))

    fig2.update_layout(
        width=600, height=1000,
        title='Symptoms of Anxiety or Depression by State'
        )

    col.header("How did states affect mental health during COVID-19?")

    col.plotly_chart(fig2, use_container_width=True)
    col.markdown(
    'Looking at mental health from a state perspective, the same trends can be seen as before. With the exceptions of Hawaii and Kentucky, every state saw an increase in symptoms between October and November 2020, which then stayed high until February 2021. The worst hit was Mississippi, with 51% of participants recording symptoms, the highest of any state, in January 2021. Looking a bit closer at this number, it appears the extended benefits program ended at the end of December within the state. This program had been enacted in May of 2020, to give pay benefits to the unemployed who had already used up their basic entitlement due to COVID [MDES].')
    col.markdown(
        "On the opposite side of the spectrum, both North and South Dakota maintained relatively low levels throughout the pandemic period, although still higher than the 2019 national average. This is especially strange because both states set global records. In November 2020, North Dakota had the highest coronavirus infection rate per capita in the world, with South Dakota not far behind [Sullivan]. Cases stayed high through the winter, but neither closed their restaurants or restricted public gatherings. North Dakota did implement a mask policy, but South Dakota did not. A lack of social restrictions and isolation could have kept the two states from the same peaks of negative mental health as other states. Even still, no state failed to follow the spikes in symptoms which mirrored the spikes in COVID cases.")

    col.header("Citations:")
    col.markdown("Demonstrations & Political Violence in America: New Data for Summer 2020. (2021, May 26). ACLED. https://acleddata.com/2020/09/03/demonstrations-political-violence-in-america-new-data-for-summer-2020/")
    col.markdown("MDES - Extended Benefits Program Ended in Mississippi. (2021, January 4). MDES. https://mdes.ms.gov/news/2021/01/04/extended-benefits-program-ended-in-mississippi/")
    col.markdown("Mental Health - Household Pulse Survey - COVID-19. (2021, October 20). CDC. https://www.cdc.gov/nchs/covid19/pulse/mental-health.htm")
    col.markdown("Sullivan, K. (2021, February 15). North Dakota and South Dakota set global Covid records. How did they turn the tide? NBC News. https://www.nbcnews.com/health/health-news/north-dakota-south-dakota-set-global-covid-records-how-did-n1257004")
    col.markdown("Terlizzi EP, Villarroel MA. Symptoms of generalized anxiety disorder among adults: United States, 2019. NCHS Data Brief, no 378. Hyattsville, MD: National Center for Health Statistics. 2020.")
    col.markdown("Villarroel MA, Terlizzi EP. Symptoms of depression among adults: United States, 2019. NCHS Data Brief, no 379. Hyattsville, MD: National Center for Health Statistics. 2020.")

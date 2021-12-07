from helper_modules.imports import *


def plot_cases_data(cases, cases_groups, mobility_policy):

    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("The Unseen Impacts of COVID-19")
    col.markdown(
        "The first cases of COVID-19 were recorded in December of, 2019. In the two years since, the world has experienced the greatest change in life expectancy since World War Two (Jack). Global industry and commerce have been disrupted in ways we are only now beginning to feel the effects of. Countries have faced shortages of goods once commonplace. The habits and routines of the entire world have been forced to adapt in response to a disease. What toll then has the pandemic taken on the habits and wellbeing of people? What are these changes and can they be measured in correlation with COVID-related events? Through this site, we seek to answer these questions and examine how the coronavirus has impacted the movement habits, power usage, and mental wellbeing of the people of the United States.")

    col.header("The Common Factors")
    col.markdown(
        "Two primary factors come into play when analyzing data gathered from the U.S. during the pandemic: time and the state in which the data was collected. In order to assess how COVID has affected the lives of everyday people, a shared timeline must be established to correlate other data to COVID. There are the number of new cases to consider, the vaccination rates, new variants, COVID waves, and policy changes which may reflect differently in each topic at hand. In the graph below, you can see that certain time periods are associated with dramatic rises in case numbers. Specifically, the period from November 2020 to February 2021, where new cases were at their highest levels, and July through September 2021, when the delta variant began to hit the United States.")

    fig = px.line(cases_groups, x="month_year", y="Cases", hover_data=['Cases'], markers=True)
    fig.update_layout(title='Number of Cases registered in the United States',
                      xaxis_title='Time',
                      yaxis_title='Sum of Cases per month')
    fig.layout.plot_bgcolor = '#121212'
    fig.layout.paper_bgcolor = '#121212'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.add_vrect(x0="10.5",
                   x1="12.5",
                  annotation_text=" Covid Cases Peak", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.add_vrect(x0="1.8",
                   x1="3",
                  annotation_text="Stay at Home Policy", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.add_vrect(x0="17",
                  x1="18",
                  annotation_text="Delta Variant starts", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    col.plotly_chart(fig, use_container_width=True)

    col.markdown(
    "Moreover, each individual state executed their own policies and would have different populations and industries which were likely affected differently. To find correlations between movement, power consumption, and mental health and COVID data then, we must consider both the time and state we see trends in to confirm if there are other factors in play than only the coronavirus. See below, where many other countries imposed federal mandates, even the initial stay at home order was implemented across a month long period for each state.")
    plot_policy_data(mobility_policy)

    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many cases have been registered in the United States?")
    col.markdown(
    "You can further see the differences in each states’ reaction and impact of COVID-19 in an analysis of each state’s case rate. The more populated states, like California, Texas, Florida, or New York, had high case rates for much of the pandemic so far. Less populated states, like North Dakota or Montana, had distinct flare ups, but then returned to lowercase rates. Nearly every state maintained high case rates during the peak COVID period of November 2020 - February 2021, with the worst month being January, when cases spiked to nearly 300,000 new cases during one week. .")
    cases_filtered = cases
    cases_filtered['state_code'] = (cases_filtered['state']).map(us_state_to_abbrev)
    cases_filtered['month'] = pd.to_datetime(cases_filtered["date"]).dt.month
    cases_filtered['year'] = pd.to_datetime(cases_filtered["date"]).dt.year
    cases_filtered = cases_filtered[(cases_filtered['state'] != 'District of Columbia')]
    cases_filtered = cases_filtered.groupby(['year', 'month','state_code']).sum().reset_index()
    cases_filtered["Date"] = cases_filtered['month'].apply(lambda x: calendar.month_abbr[x]).astype(str) + " " + \
                                   cases_filtered['year'].astype(str)

    cases_filtered['Cases'] = np.log(cases_filtered['Cases'])
    fig = px.choropleth(cases_filtered,
                        locations='state_code',
                        color="Cases",
                        hover_name="state_code",
                        animation_frame="Date",
                        color_continuous_scale="reds",
                        locationmode='USA-states',
                        scope="usa",
                        range_color=(0, 18),
                        title='Number of cases by state (logarithmic scale)',
                        height=600,
                        )
    fig.update_layout(  # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#4E5D6C'))
    col.plotly_chart(fig, use_container_width=True)


def plot_policy_data(mobility_policy):
    buff, col2, buff2 = st.columns([2, 3, 2])
    #col2.markdown(
    #    "The government issued stay-at-home regulations to curb the growing number of cases. Different states issued orders at different times in as a reactionary response to the number of active cases.")
    slider = col2.slider('Move the slider below to view states issuing stay-at-home orders over the course of 2020.',
                         min_value=dt.date(year=2020, month=2, day=28), max_value=dt.date(year=2020, month=3, day=22),
                         format='MM-DD-YYYY')

    mobility_policy = mobility_policy.dropna(subset=["MobilityRestrictedDate"])[
        ['State Abbreviation', 'MobilityRestrictedDate']]
    mobility_policy['Stay at Home Policy declared'] = (
            pd.to_datetime(mobility_policy['MobilityRestrictedDate'], format='%m/%d/%Y') < pd.to_datetime(slider,
                                                                                                          errors='coerce')).astype(
        'str')

    # Plotting the closed states based on the selected date
    fig = px.choropleth(mobility_policy,  # Input Pandas DataFrame
                        locations="State Abbreviation",
                        # DataFrame column with locations  # DataFrame column with color values
                        hover_name="State Abbreviation",  # DataFrame column hover info
                        locationmode='USA-states',
                        color='Stay at Home Policy declared',
                        color_discrete_map={'True': 'red',
                                            'False': 'blue'})  # Set to plot as US States
    fig.add_scattergeo(name='State Names',
                       locations=mobility_policy['State Abbreviation'],
                       locationmode='USA-states',
                       text=mobility_policy['State Abbreviation'],
                       mode='text')
    fig.update_layout(  # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#4E5D6C'),
    )
    buff, col, buff2 = st.columns([1, 3, 1])
    col.plotly_chart(fig, use_container_width=True)


def plot_vaccination_data(vaccines):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many vaccines have been distributed in the United States?")
    col.markdown(
    "How then have vaccinations impacted the number of COVID-19 cases? Interestingly,  when more people are being vaccinated there appear to be fewer new COVID cases. You can see this most clearly in the after the peak of cases in January, which corresponds with the implementation of wide scale vaccinations in the U.S. After the incredibly high caseloads of December and January, the number declines sharply, exactly while vaccinations rates begin to skyrocket. The number of cases remains low for the entire peak of the vaccination rates, from January through to June. Unfortunately, in June the vaccination rates plateau, just as the delta variant begins to increase COVID case numbers again. After the rise of cases, and government efforts to get more people vaccinated, like mandatory vaccination requirements for federal and state employees, we begin to see a slight increase in vaccination rates.")

    types_of_vaccines = col.multiselect("Types of Vaccine Doses",
                                        ["Total Doses", "Moderna Doses", "Pfizer Doses", "Booster Doses",
                                         "Johnson & Johnson Doses"], default=["Total Doses"])

    vaccine_columns = types_of_vaccines
    vaccine_columns.append('Date')
    vaccines_filtered = vaccines[vaccine_columns]

    fig = px.line(vaccines_filtered, x="Date", y=vaccine_columns)
    fig.layout.plot_bgcolor = '#121212'
    fig.layout.paper_bgcolor = '#121212'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.add_vrect(x0="2020-11-15",
                  x1="2021-01-15",
                  annotation_text=" Covid Cases Peak", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.add_vrect(x0="2021-06-01",
                  x1="2021-07-01",
                  annotation_text="Delta Variant Starts", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.update_layout(legend_title_text='Types of Vaccines',
                      title='Number of Vaccines distributed per day (Smoothed over a week)',
                      xaxis_title='Date',
                      yaxis_title='No of Vaccines Administered (In Millions)')
    col.plotly_chart(fig, use_container_width=True)

    col.markdown("It is unlikely that the U.S. will return to the same vaccination rates as were seen in the initial vaccination period, simply because the people who wanted to become vaccinated have already done so.  Unless we see a wide scale adoption of booster shots, or if the original vaccines begin to fail in the face of new coronavirus strains. A not insignificant portion of the U.S. population have bought into the vaccine misinformation campaigns and refuse to be vaccinated, even at the risk of unemployment.")

    dict_check = col.checkbox("Citations")

    if dict_check:
        col.header("Citations:")
        col.markdown("Jack, V. (2021, September 27). COVID-19 pandemic cut life expectancy by most since World War Two –study. Reuters.")
        col.markdown("The New York Times. (2021). Coronavirus (Covid-19) Data in the United States. Retrieved 06 Dec. 2021, from https://github.com/nytimes/covid-19-data.")

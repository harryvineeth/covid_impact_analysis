from helper_modules.imports import *


def plot_cases_data(cases, cases_groups):

    buff, col, buff2 = st.columns([1, 3, 1])
    fig = px.line(cases_groups, x="month_year", y="Cases", hover_data=['Cases'], markers=True)
    fig.update_layout(title='Number of Cases registered in the United States',
                      xaxis_title='Time',
                      yaxis_title='Sum of Cases per month')
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.add_vrect(x0="10.5",
                   x1="12.5",
                  annotation_text=" Covid Cases Peak", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0="1.8",
                   x1="3",
                  annotation_text="Stay at Home Policy", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0="17",
                  x1="18",
                  annotation_text="Delta Variant starts", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    col.plotly_chart(fig, use_container_width=True)

    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many cases have been registered in the United States?")
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
    col2.markdown(
        "The government issued stay-at-home regulations to curb the growing number of cases. Different states issued orders at different times in as a reactionary response to the number of active cases.")
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
    types_of_vaccines = col.multiselect("Types of Vaccine Doses",
                                        ["Total Doses", "Moderna Doses", "Pfizer Doses", "Booster Doses",
                                         "Johnson & Johnson Doses"], default=["Total Doses"])

    vaccine_columns = types_of_vaccines
    vaccine_columns.append('Date')
    vaccines_filtered = vaccines[vaccine_columns]

    fig = px.line(vaccines_filtered, x="Date", y=vaccine_columns)
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.add_vrect(x0="2020-11-15",
                  x1="2021-01-15",
                  annotation_text=" Covid Cases Peak", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0="2021-06-01",
                  x1="2021-07-01",
                  annotation_text="Delta Variant Starts", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    fig.update_layout(legend_title_text='Types of Vaccines',
                      title='Number of Vaccines distributed per day (Smoothed over a week)',
                      xaxis_title='Date',
                      yaxis_title='No of Vaccines Administered (In Millions)')
    col.plotly_chart(fig, use_container_width=True)

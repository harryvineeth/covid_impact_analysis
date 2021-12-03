from helper_modules.imports import *

def plot_cases_data(cases):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many cases have been registered in the United States?")

def plot_vaccination_data(vaccines):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How many vaccines have been distributed in the United States?")
    types_of_vaccines = col.multiselect("Types of Vaccine Doses",
                                        ["Total Doses", "Moderna Doses", "Pfizer Doses", "Booster Doses",
                                         "Johnson & Johnson Doses"], default=["Total Doses"])

    vaccine_columns = types_of_vaccines
    vaccine_columns.append('Date')
    vaccines_filtered = vaccines[vaccine_columns]

    fig = px.line(vaccines_filtered, x="Date", y=vaccine_columns, markers=True)
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(legend_title_text='Types of Vaccines',
                      title='Number of Vaccines distributed per day (Smoothed over a week)',
                      xaxis_title='Date',
                      yaxis_title='No of Vaccines Administered (In Millions)')
    col.plotly_chart(fig, use_container_width=True)


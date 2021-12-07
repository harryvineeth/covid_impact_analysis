from helper_modules.imports import *

def run_mobility(apple_mobility_state, apple_mobility_time, google_national_data, google_state_data, mobility_groups):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How do you measure travel?")
    col.markdown("In order to measure travel, we used two different datasets: Apple’s COVID-19 Mobility Trend Report and Google’s COVID-19 Community Mobility Report. The Apple dataset reports overall transit by the selected region as a percentage change from a baseline established on 13 January 2020. The Google dataset reports similar numbers, but is broken down by destination type (workplaces, parks, groceries and pharmacies, and retail and recreation). The Google dataset’s baseline was established between Jan 3 – Feb 6, 2020 and reports separate values for each day of the week. Neither dataset can properly account for holidays, local events, and seasonal differences.")

    plot_apple_data(apple_mobility_state, apple_mobility_time)
    plot_google_data(google_national_data, google_state_data, mobility_groups)



def plot_apple_data(apple_mobility_state, apple_mobility_time):
    buff, col, buff2 = st.columns([1, 3, 1])
    fig = px.line(apple_mobility_time.dropna(), x="month_year", y="transit", hover_data=['transit'], markers=True)
    fig.update_layout(title='Changes in transit patterns in the United States',
                      xaxis_title='Time',
                      yaxis_title='% change in transit from baseline')
    fig.layout.plot_bgcolor = '#121212'
    fig.layout.paper_bgcolor = '#121212'
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
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    col.plotly_chart(fig, use_container_width=True)

    col.header("How has COVID-19 affected road transit?")
    col.markdown("The plot above shows the change in overall transit at a national level from the Apple dataset. There is a clear decrease in transit following the initial wave of COVID-19 cases in the US in March 2020. However, the largest change in transit occurred during April 2020, following the state of national emergency declaration by President Trump and the shutdown of major public institutions by state governments starting in March 2020. These changes began to quickly recover however, until the second wave hit in late 2020. With this new wave starting in September 2020, transit levels declined once more until December 2020. Though, there may be some compounding impact caused by seasonal winter trends.")
    col.markdown("After the second wave, the nation’s transit saw a continual upward trend until October 2021. Even during the Delta variant outbreak, transit rates continued to increase, though at a lower rate than both directly before and after. The return to normal transit numbers indicates that, in 2021, the U.S. population appears to be ignoring the impacts of COVID in their daily travel. While this behavior may be influenced by vaccination numbers, it also may show Americans have grown indifferent to COVID, potentially increasing the spread of future outbreaks. ")
    buff, col, buff2 = st.columns([5, 2, 5])
    yearOption = col.selectbox('Year', ('2020', '2021', '2020 and 2021'))

    buff, col, buff2 = st.columns([1, 3, 1])
    apple_mobility_state = apple_mobility_state.set_index('month_year')
    if yearOption != '2020 and 2021':
        apple_mobility_state = apple_mobility_state[apple_mobility_state.index.str.contains(yearOption)]
    fig = go.Figure(
        data=go.Heatmap(df_to_plotly(apple_mobility_state.T), type='heatmap', colorscale='plotly3', opacity=0.6),
        layout=go.Layout(width=600, height=1000,
                         title="Percentage change in transit traffic compared to baseline (2019)"))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    col.plotly_chart(fig, use_container_width=True)
    col.markdown("The above plot shows the Apple transit data grouped by state and maintains the overall trends of the national data. Wisconsin immediately pops out as an outlier during September-November 2021. This may be due to a combination of unseasonably warm weather in late 2021, along with the baseline being established in the middle of winter where transit would be relatively low [National Weather Service]. Another possible factor may have been events returning to full capacity for 2021, for example sporting events. While this effect may be less evident in larger states, Wisconsin has a low population with several  popular teams, such as the Packers. A sudden increase in the movement of football fans would be much more apparent in Wisconsin than in, say, California. ")
    col.markdown("Another general trend is a higher transit rate among several Northeastern states, like New Jersey, Rhode Island, and Massachusetts, starting in the summer of 2021. Seasonal differences may be coming into play, as these states are typically hit harder by winter effects than the rest of the nation, resulting in a skewed baseline. ")

def df_to_plotly_google(df):
    x = df.columns.tolist()
    return {'z': df.values.tolist(),
            'x': x,
            'y': df.index.tolist()}

def plot_google_groups(mobility_groups):
    buff, col, buff2 = st.columns([1, 6, 1])
    fig = make_subplots(rows=2, cols=2, start_cell="top-left", shared_yaxes=True)

    fig.add_trace(
        go.Scatter(x=mobility_groups["date"].values, y=mobility_groups["Workplaces"].values.tolist(), fill='tozeroy',
                   name='Workplaces'), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=mobility_groups["date"].values, y=mobility_groups['Parks'].values.tolist(), fill='tozeroy',
                   name='Parks'), row=1, col=2)
    fig.add_trace(
        go.Scatter(x=mobility_groups["date"].values, y=mobility_groups['Grocery and Pharmacy'].values.tolist(),
                   fill='tozeroy', name='Grocery and Pharmacy'), row=2, col=1)
    fig.add_trace(
        go.Scatter(x=mobility_groups["date"].values, y=mobility_groups['Retail and Recreation'].values.tolist(),
                   fill='tozeroy', name='Retail and Recreation'), row=2, col=2)

    fig.update_xaxes(title_text="Workplaces", row=1, col=1, showticklabels=True)
    fig.update_xaxes(title_text="Parks", row=1, col=2, showticklabels=True)
    fig.update_xaxes(title_text="Grocery and Pharmacy", row=2, col=1, showticklabels=True)
    fig.update_xaxes(title_text="Retail and Recreation", row=2, col=2, showticklabels=True)

    # Update yaxis properties
    fig.update_yaxes(title_text="Percentage change", row=1, col=1, showticklabels=True)
    fig.update_yaxes(row=1, col=2, showticklabels=True)
    fig.update_yaxes(title_text="Percentage change", row=2, col=1, showticklabels=True)
    fig.update_yaxes(row=2, col=2, showticklabels=True)
    fig.update_layout(width=int(1500), height=int(750))
    fig.update_layout(legend_title_text='Commonly Visited Places',
                      title='Percentage Change in Frequency of commonly visited places compared to baseline (2019)')
    # fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    # fig = px.line(mobilityGroups, x='date' , y='value',color='variable')
    fig.layout.plot_bgcolor = '#121212'
    fig.layout.paper_bgcolor = '#121212'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    col.plotly_chart(fig, use_container_width=True)



def plot_google_national(google_national_data, month_year):
    buff, col, buff2 = st.columns([1, 3, 1])

    col.header("Are there any trends based on destination?")
    col.markdown("The above plot shows the percent change in Google’s data in visits to workplaces, grocery stores, parks, and retail and recreation establishments compared to the pre-COVID baseline at a national level. This figure is interesting as it shows the distribution of transit across the nation since 2020. As expected, the number of visitors for each category dropped significantly in early 2020 as a response to the initial COVID wave and the restrictions that followed. However, the only category that remained below the baseline throughout the entirety of 2020 and 2021 is workplace transit. Retail and recreation visits remained below the baseline until mid-March 2021, but have remained above the baseline since. Similarly, grocery shop visits were above the baseline from May-August 2020, but have otherwise remained below the baseline throughout 2020 and up to mid-March 2021.")
    col.markdown("Park visits are the largest outlier, as they have been significantly higher than the baseline throughout most of 2020 and 2021, with the exception of December 2020 - February 2021. However, this may be due to the baseline being established in January-February 2020 and does not account for seasonal trends. Generally, park visits would be significantly lower in the middle of the winter months. Parks are also the only category that is outdoors, and are likely not as heavily impacted by COVID restrictions. Overall, all of the plots have local minima correlating to the various outbreaks in the US. The largest decrease occurred in April 2020 with the initial outbreak, and another decrease in December 2020 due to the third and most severe outbreak. Smaller decreases can be observed during the second and Delta variant outbreaks during August 2020 and July 2021 respectively.")

    national_work_figure = px.line(
        google_national_data, x= month_year, y= google_national_data['workplaces_percent_change_from_baseline'],
        title = 'National Workplace Mobility Percentage of Change',
        labels={
            'workplaces_percent_change_from_baseline':'Percent Change From Baseline',
            'x':'Date'
        }
    , markers=True)
    national_work_figure.add_vrect(x0="9.5",
                  x1="11.5",
                  annotation_text=" Covid Cases Peak", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    national_work_figure.add_vrect(x0="0.8",
                  x1="2",
                  annotation_text="Stay at Home Policy", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    national_work_figure.add_vrect(x0="16",
                  x1="17",
                  annotation_text="Delta Variant starts", annotation_position="top left",
                  fillcolor="#AB63FA", opacity=0.2, line_width=0)
    national_work_figure.layout.plot_bgcolor = '#0E1117'
    national_work_figure.layout.paper_bgcolor = '#0E1117'
    national_work_figure.update_xaxes(showgrid=False, zeroline=False)
    national_work_figure.update_yaxes(showgrid=False, zeroline=False)

    col.plotly_chart(national_work_figure, use_container_width=True)
    col.header("Deep Dive into Workplace Transit")
    col.markdown("The figure above shows the mobility changes for transit to and from workplaces from Google data at a national level. The figure shows similar trends to the Apple overall transit data in early 2020, but diverges significantly during 2021. However, the two diverge significantly in 2021. The Apple data indicates overall transit has recovered to pre-COVID levels by late 2021, while the Google workplace transit data indicates that travel to and from work has remained steadily below baseline levels. As stated previously, this may indicate that the population’s response to COVID has largely died down, though employers may still be following manning protocols. However, this may also be due to other factors such as unemployment and remote work becoming more accepted and facilitated. An interesting side-effect of COVID may be remote work being offered in more jobs moving forward, with transit rates never fully returning to pre-COVID levels.")

def plot_google_state(google_state_data, month_year):
    buff, col, buff2 = st.columns([5, 2, 5])
    yearOption = col.selectbox('Year', ('2020', '2021', '2020 and 2021'), key="year2")

    if yearOption != '2020 and 2021':
        month_year = [string for string in month_year if yearOption in string]
    buff, col, buff2 = st.columns([1, 3, 1])
    stateWork = go.Figure(
                data=go.Heatmap(df_to_plotly_google(google_state_data[month_year]), type = 'heatmap', colorscale = 'plotly3'),
                layout=go.Layout(width = 600,height = 1000, title="Percent Change in Workplace Mobility By State"))
    stateWork.update_layout(
        xaxis_title='Date',
        yaxis_title= 'State')

    col.plotly_chart(stateWork, use_container_width=True)
    col.markdown("The heat map above shows a by-state breakdown of the workplace mobility trends over the same time period as the national plot. Overall, the trends follow those of the national data, with decreases during each wave and general recovery to a steady state in between waves. As a general trend, low population density states such as Missouri, Nebraska, Montana, and Idaho tend to recover faster. Of note, some states seem to recover at slower rates than others. Hawaii’s recovery is likely due to its geography as a set of islands isolated from the rest of the continental United States.")
    col.markdown("California is an interesting outlier, as though the state is very large by area, 95% of the population resides in densely populated urban clusters [US Census Bureau].  Similarly, New Jersey also lags behind in mobility recovery and is the 2nd highest state in terms of urban population percentage. The north east as a whole is highly urbanized, and correspondingly, several outlier states that lag behind are in that region such as Massachusetts, Rhode Island, and Vermont.")
    dict_check = col.checkbox("Citations")
    if dict_check:
        col.header("Citations:")
        col.markdown("Apple. (2021, November). COVID‑19 - Mobility Trends Reports. https://covid19.apple.com/mobility")
        col.markdown("Google. (2021, November). See how your community is moving around differently due to COVID-19. https://www.google.com/covid19/mobility/index.html?hl=en)")
        col.markdown("National Weather Service. (2021, September). Very Dry and Warm across Southern Wisconsin in September. Weather. https://www.weather.gov/mkx/septemberclimate")
        col.markdown("US Census Bureau Public Information Office. (2012, March 26). Growth in Urban Population Outpaces Rest of Nation, Census Bureau Reports - 2010 Census - Newsroom - U.S. Census Bureau. Census. ")


def plot_google_data(google_national_data, google_state_data, mobility_groups):
    month_year = ['Feb 2020', 'Mar 2020', 'Apr 2020', 'May 2020', 'Jun 2020',
       'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020',
       'Dec 2020', 'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021',
       'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021',
       'Oct 2021', 'Nov 2021']

    plot_google_groups(mobility_groups)
    plot_google_national(google_national_data, month_year)
    plot_google_state(google_state_data, month_year)

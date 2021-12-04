from helper_modules.imports import *

def run_mobility(apple_mobility_state, apple_mobility_time, google_national_data, google_state_data, mobility_groups):
    st.title('Traffic')
    st.write('This is the Traffic page.')

    plot_apple_data(apple_mobility_state, apple_mobility_time)
    plot_google_data(google_national_data, google_state_data, mobility_groups)


def plot_apple_data(apple_mobility_state, apple_mobility_time):
    buff, col, buff2 = st.columns([1, 3, 1])
    fig = px.line(apple_mobility_time.dropna(), x="month_year", y="transit", hover_data=['transit'], markers=True)
    fig.update_layout(title='Changes in transit patterns in the United States',
                      xaxis_title='Time',
                      yaxis_title='% change in transit from baseline')
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.add_shape(type="rect",
                  xref="x",
                  yref="paper",
                  x0=10.5,
                  y0=0,
                  x1=12.5,
                  y1=1,
                  line=dict(color="rgba(0,0,0,0)",width=3,),
                  fillcolor='rgba(255,0,0,0.2)',
                  layer='below')
    col.plotly_chart(fig, use_container_width=True)

    buff, col, buff2 = st.columns([5, 2, 5])
    yearOption = col.selectbox('Year', ('2020', '2021', '2020 and 2021'))

    buff, col, buff2 = st.columns([1, 3, 1])
    apple_mobility_state = apple_mobility_state.set_index('month_year')
    if yearOption != '2020 and 2021':
        apple_mobility_state = apple_mobility_state[apple_mobility_state.index.str.contains(yearOption)]
    fig = go.Figure(
        data=go.Heatmap(df_to_plotly(apple_mobility_state.T), type='heatmap', colorscale='rdbu'),
        layout=go.Layout(width=600, height=1000,
                         title="Percentage change in transit traffic compared to baseline (2019)"))

    col.plotly_chart(fig, use_container_width=True)


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
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    col.plotly_chart(fig, use_container_width=True)


def plot_google_national(google_national_data, month_year):
    buff, col, buff2 = st.columns([1, 3, 1])

    national_work_figure = px.line(
        google_national_data, x= month_year, y= google_national_data['workplaces_percent_change_from_baseline'],
        title = 'Google Mobility - Workplace (National)',
        labels={
            'workplaces_percent_change_from_baseline':'Percent Change From Baseline',
            'x':'Date'
        }
    , markers=True)
    national_work_figure.add_shape(type="rect",
                  xref="x",
                  yref="paper",
                  x0=9.5,
                  y0=0,
                  x1=11.5,
                  y1=1,
                  line=dict(color="rgba(0,0,0,0)", width=3, ),
                  fillcolor='rgba(255,0,0,0.2)',
                  layer='below')
    national_work_figure.layout.plot_bgcolor = '#0E1117'
    national_work_figure.layout.paper_bgcolor = '#0E1117'
    national_work_figure.update_xaxes(showgrid=False, zeroline=False)
    national_work_figure.update_yaxes(showgrid=False, zeroline=False)

    col.plotly_chart(national_work_figure, use_container_width=True)


def plot_google_state(google_state_data, month_year):
    buff, col, buff2 = st.columns([5, 2, 5])
    yearOption = col.selectbox('YEAR', ('2020', '2021', '2020 and 2021'))

    if yearOption != '2020 and 2021':
        month_year = [string for string in month_year if yearOption in string]
    buff, col, buff2 = st.columns([1, 3, 1])
    stateWork = go.Figure(
                data=go.Heatmap(df_to_plotly_google(google_state_data[month_year]), type = 'heatmap', colorscale = 'rdbu'),
                layout=go.Layout(width = 600,height = 1000, title="Google Mobility - Percent Change in Workplace Mobility (By State)"))
    stateWork.update_layout(
        xaxis_title='Date',
        yaxis_title= 'State')

    col.plotly_chart(stateWork, use_container_width=True)


def plot_google_data(google_national_data, google_state_data, mobility_groups):
    month_year = ['Feb 2020', 'Mar 2020', 'Apr 2020', 'May 2020', 'Jun 2020',
       'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020',
       'Dec 2020', 'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021',
       'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021',
       'Oct 2021', 'Nov 2021']

    plot_google_groups(mobility_groups)
    plot_google_national(google_national_data, month_year)
    plot_google_state(google_state_data, month_year)
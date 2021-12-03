from helper_modules.imports import *

def run_mobility(apple_mobility_state, apple_mobility_time, google_national_data, google_state_data):
    st.title('Traffic')
    st.write('This is the Traffic page.')

    plot_apple_data(apple_mobility_state, apple_mobility_time)
    plot_google_data(google_national_data, google_state_data)


def plot_apple_data(apple_mobility_state, apple_mobility_time):
    buff, col, buff2 = st.columns([1, 3, 1])
    fig = px.line(apple_mobility_time.dropna(), x="month_year", y="transit", hover_data=['transit'])
    fig.update_layout(title='Changes in transit patterns in the United States',
                      xaxis_title='Time',
                      yaxis_title='% change in transit from baseline')
    col.plotly_chart(fig, use_container_width=True)

    apple_mobility_state = apple_mobility_state.set_index('month_year')
    apple_mobility_state.columns = apple_mobility_state.columns.map(us_state_to_abbrev)
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

def plot_google_national(google_national_data, month_year):
    buff, col, buff2 = st.columns([1, 3, 1])

    national_work_figure = px.line(
        google_national_data, x= month_year, y= google_national_data['workplaces_percent_change_from_baseline'],
        title = 'Google Mobility - Workplace (National)',
        labels={
            'workplaces_percent_change_from_baseline':'Percent Change From Baseline',
            'x':'Date'
        }
    )

    col.plotly_chart(national_work_figure, use_container_width=True)

def plot_google_state(google_state_data, month_year):
    buff, col, buff2 = st.columns([1, 3, 1])
    stateWork = go.Figure(
                data=go.Heatmap(df_to_plotly_google(google_state_data[month_year]), type = 'heatmap', colorscale = 'rdbu'),
                layout=go.Layout(width = 600,height = 1000, title="Google Mobility - Percent Change in Workplace Mobility (By State)"))
    stateWork.update_layout(
        xaxis_title='Date',
        yaxis_title= 'State')

    col.plotly_chart(stateWork, use_container_width=True)

def plot_google_data(google_national_data, google_state_data):
    month_year = ['Feb 2020', 'Mar 2020', 'Apr 2020', 'May 2020', 'Jun 2020',
       'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020',
       'Dec 2020', 'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021',
       'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021',
       'Oct 2021', 'Nov 2021']

    plot_google_national(google_national_data, month_year)
    plot_google_state(google_state_data, month_year)
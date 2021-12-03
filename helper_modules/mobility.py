from helper_modules.imports import *

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

def run_mobility(apple_mobility_state, apple_mobility_time):
    st.title('Apple Mobility')
    st.write('This is Apple Mobility data page')
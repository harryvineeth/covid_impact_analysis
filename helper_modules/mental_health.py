from helper_modules.imports import *


def run_mental_health(mental_health_statewise, mental_health, mental_health_nationwide):
    st.title('Well being')
    st.write('This is the Well being page.')

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
    fig.update_xaxes(
        tickformat='%d-%b-%Y',
        tickangle=45,
        showticklabels=True,
        title="Date of Response",
        gridwidth=0.5, gridcolor='lightslategray'
    )
    fig.update_yaxes(title='Percentage of Participants With Symptoms', gridwidth=0.5, gridcolor='lightslategray')
    fig.update_layout(width=1000, height=500, yaxis_range=[10, 60])
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    col.plotly_chart(fig, use_container_width=True)

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

    col.plotly_chart(fig2, use_container_width=True)
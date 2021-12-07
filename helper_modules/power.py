from helper_modules.imports import *


def energy_timeline_graph(energy_change_national, energy_change_states):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How do you measure Power?")
    col.markdown("We used the U.S. Energy Information Administration’s dataset for the total electric power industry for 2019-2022. This dataset reports electricity generation reported in Megawatt Hours. We subtracted monthly energy generation values from 2020 and 2021 from the 2019 data, and divided by the 2019 value to calculate the percent change by month for each state.")

    fig = px.line(energy_change_national, x='Date',y='change', markers=True)
    fig.add_vrect(x0="9.5",
                   x1="11.5",
                   annotation_text=" Covid Cases Peak", annotation_position="top left",
                   fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.add_vrect(x0="0.8",
                   x1="2",
                   annotation_text="Stay at Home Policy", annotation_position="top left",
                   fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.add_vrect(x0="16",
                   x1="17",
                   annotation_text="Delta Variant starts", annotation_position="top left",
                   fillcolor="#AB63FA", opacity=0.2, line_width=0)
    fig.layout.plot_bgcolor = '#121212'
    fig.layout.paper_bgcolor = '#121212'
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(legend_title_text='States',
                      title='Percentage Change of Electricity generated from 2019 to 2020',
                      xaxis_title='Date',
                      yaxis_title='% Change')
    col.plotly_chart(fig, use_container_width=True)

    col.header("Has power generation changed due to COVID-19?")
    col.markdown("The above figure shows the change in national electric power generation per month compared to a baseline value from 2019. Overall, total energy generation remained slightly lower than that of 2019.  There was a distinct decrease between March-May 2020, corresponding to the initial spread of COVID-19 in the US. After this minimum value, the plot generally trends upwards, indicating a gradual recovery. This may also indicate that electricity requirements are gradually increasing from year to year.")
    col.markdown("The main driver of monthly variation appears to be seasonal trends, with spikes during winter and summer months. However, COVID-19 cases do appear to be playing a role as the rate of power generation increases during the period of the largest wave of COVID cases during the winter of 2020 and the Delta variant outbreak in the summer of 2021. This may be due to an increase in residential power consumption for climate control, without a corresponding decrease in workplace power consumption as their climate control needs do not change. The monthly fluctuations remain relatively small, as national energy requirements should not change drastically and stay at home policies would only shift energy demand from commercial to residential.")


    colors = {
        'Negative': '#ef553b',
        'Positive': '#636efa',
    }

    # First graph is a simple comparison Bar graph showing different deltas
    fig = px.bar(
        energy_change_states,
        x='change',
        y='state_name',
        orientation='h',
    )
    fig.update_traces(marker_color=energy_change_states['Impact'].map(colors), showlegend=False)
    fig.update_layout(width=1000, height=600)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(
        title='% Change in Energy Generation between 2019 & 2020',
        title_x=0.5,
        xaxis_title='Change %',
        yaxis_title='States'
    )
    fig.layout.plot_bgcolor = '#121212'
    fig.layout.paper_bgcolor = '#121212'
    col.plotly_chart(fig, use_container_width=True)
    col.header("Are there any trends in state electricity generation?")
    col.markdown("The above plot shows the top 5 states that experienced the largest mean differences for both negative and positive energy generation since 2019. In general, the states with low energy consumption per capita tended to have higher energy generation than the baseline and vice versa [EIA]. The outliers to this trend are Massachusetts and Rhode Island, as both have relatively low energy consumption per capita but also have large negative changes in energy generation. There may also be a regional trend, as both states are in the northeast.")

    # col.subheader(
    #     'Observing change in usage on a monthly basis, on positive and negative states'
    # )
    #
    # types_of_groups = col.multiselect("Choose to observe states with positive and negative impact", ['Positive','Negative'],
    #                                   default=["Positive"])
    #
    # energy_change_states_combined = energy_change_states_combined[energy_change_states_combined['Change type'].isin(types_of_groups)]



def df_energy_to_heatmap_format(df):
    return {
        'z': df['change'],
        'y': df['state'],
        'x': df['month_year']
    }


def plot_energy_heatmap(energy_change_states_heatmap):
    buff, col, buff2 = st.columns([5, 2, 5])
    # yearOption = col.multiselect('Year', ['2019','2020', '2021'], default=['2020'])
    # total_years = [int(i) for i in yearOption]
    # #energy_change_states_heatmap = energy_change_states_heatmap[energy_change_states_heatmap.isin(['2019'])]
    # energy_change_states_heatmap = energy_change_states_heatmap[
    #     energy_change_states_heatmap['year'].isin(total_years)]
    # print (energy_change_states_heatmap)
    buff, col, buff2 = st.columns([1, 3, 1])
    fig = go.Figure(
        data=go.Heatmap(df_energy_to_heatmap_format(energy_change_states_heatmap), type='heatmap', colorscale='purpor', opacity=0.6),
        layout=go.Layout(width=600, height=1000,
                         title='Total Electric Power Industry')
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    col.plotly_chart(fig, use_container_width=True)
    col.markdown("The figure shows the percent change in electricity generation by state from 2020-2021. Generally, the patterns follow those of the national data. This plot highlights the two outliers identified in the previous plot. Rhode Island is the lowest energy consumer by capita, one of the highest percent of residential electricity consumption, and very little commercial and industrial electricity consumption [EIA]. Therefore, a stay at home policy would impact Rhode Island more heavily than other states.")
    col.markdown("On the other hand, Massachusetts electricity generation has consistently been below its 2019 value. Massachusetts consumes 15 times more energy than it generates, with half of its energy consumed by the commercial sector [EIA]. The compounding effect of a low baseline generation value and changes to the commercial energy consumption due to COVID-19 may explain its drastic difference from the 2019 value. Overall, individual state analysis of electricity generation heavily depends on energy profiles and national trends should be not applied without further analysis.")

    dict_check = col.checkbox("Citations")

    if dict_check:
        col.header("Citations:")
        col.markdown("EIA. (2021, November). Net Generation by State by Type of Producer by Energy Source. https://www.eia.gov/electricity/data/state/")


def run_power( energy_change_national, energy_change_states, energy_change_states_heatmap):
    energy_timeline_graph(energy_change_national, energy_change_states)
    plot_energy_heatmap(energy_change_states_heatmap)

from helper_modules.imports import *


def energy_timeline_graph(energy_change_national, energy_change_states):
    buff, col, buff2 = st.columns([1, 3, 1])

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

    col.header("How has COVID-19 affected Energy Generation in various states?")


    colors = {
        'Negative': 'LightCoral',
        'Positive': 'ForestGreen',
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
        data=go.Heatmap(df_energy_to_heatmap_format(energy_change_states_heatmap), type='heatmap', colorscale='rdbu_r'),
        layout=go.Layout(width=600, height=1000,
                         title='Total Electric Power Industry')
    )
    col.plotly_chart(fig, use_container_width=True)

    dict_check = col.checkbox("Citations")

    if dict_check:
        col.header("Citations:")
        col.markdown("EIA. (2021, November). Net Generation by State by Type of Producer by Energy Source. https://www.eia.gov/electricity/data/state/")


def run_power( energy_change_national, energy_change_states, energy_change_states_heatmap):
    st.title('Power')
    energy_timeline_graph(energy_change_national, energy_change_states)
    plot_energy_heatmap(energy_change_states_heatmap)

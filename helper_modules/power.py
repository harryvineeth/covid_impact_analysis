from helper_modules.imports import *

def energy_timeline_graph(energy_change_states_negative, energy_change_states_positive, energy_change_states):
    buff, col, buff2 = st.columns([1, 3, 1])
    col.header("How has COVID-19 affected Energy Generation in various states?")


    colors = {
        'Negative': 'LightCoral',
        'Positive': 'ForestGreen',
    }

    # First graph is a simple comparison Bar graph showing different deltas
    fig = px.bar(
        energy_change_states, 
        x='Change',
        y='State',
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
    fig.layout.plot_bgcolor = '#0E1117'
    fig.layout.paper_bgcolor = '#0E1117'
    col.plotly_chart(fig, use_container_width=True)

    col.subheader(
        'Observing change in usage on a monthly basis, on positive and negative states'
    )

    type_state = col.selectbox('Choose to observe states with positive and negative impact', options=['Positive Impact', 'Negative Impact', 'Both'])

    if type_state == 'Positive Impact':
        data = energy_change_states_positive

        fig = px.line(
            energy_change_states_positive,
            x='month',
            y='change',
        )
        col.plotly_chart(fig, use_container_width=True)

    if type_state == 'Negative Impact':
        data = energy_change_states_negative
    
    if type_state == 'Both':
        data_positive = energy_change_states_positive
        data_negative = energy_change_states_negative








def run_power(energy_change_states_negative, energy_change_states_positive, energy_change_states, energy_change_states_heatmap):
    st.title('Power')
    energy_timeline_graph(energy_change_states_negative, energy_change_states_positive, energy_change_states)
    
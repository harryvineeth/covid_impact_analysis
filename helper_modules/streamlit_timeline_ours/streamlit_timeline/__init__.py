import json
import streamlit.components.v1 as components


def timeline(data, height=800):

    """Create a new timeline component.

    Parameters
    ----------
    data: str or dict
        String or dict in the timeline json format: https://timeline.knightlab.com/docs/json-format.html
    height: int or None
        Height of the timeline in px

    Returns
    -------
    static_component: Boolean
        Returns a static component with a timeline
    """

    # if string then to json
    if isinstance(data, str):
        data = json.loads(data)

    # json to string
    json_text = json.dumps(data) 

    # load json
    source_param = 'timeline_json'
    source_block = f'var {source_param} = {json_text};'

    # load css + js
    cdn_path = 'https://cdn.knightlab.com/libs/timeline3/latest'
    # css_block = f'<link title="timeline-styles" rel="stylesheet" href="{cdn_path}/css/timeline.css">'
    css_block = f'<link title="timeline-styles" rel="stylesheet" href="https://drive.google.com/uc?export=download&id=1_M_KFfIzpOFZIaURtAe9xZ8Cc2HhKZ98">'
    js_block  = f'<script src="{cdn_path}/js/timeline.js"></script>'


    # write html block
    htmlcode = css_block + ''' 
    ''' + js_block + '''

        <div id='timeline-embed' style="width: 95%; height: '''+str(height)+'''px; margin: 1px;"></div>

        <script type="text/javascript">
            var additionalOptions = {
                start_at_end: false, is_embed:true,
            }
            '''+source_block+'''
            timeline = new TL.Timeline('timeline-embed', '''+source_param+''', additionalOptions);
        </script>'''


    # return rendered html
    static_component = components.html(htmlcode, height=height,)

    return static_component

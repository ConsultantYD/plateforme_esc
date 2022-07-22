"""
PathLayer
=========

Locations of the Bay Area Rapid Transit lines.
"""

import pandas as pd
import pydeck as pdk

# Note: Pydeck expects lon,lat (X,Y)
def load_ais_data(filename):
    df_in = pd.read_excel(filename, sheet_name='coordonnes')
    points_list = [[df_in.values[i, -1], df_in.values[i, -2]]
                   for i in range(1, len(df_in))
                   if [df_in.values[i, -2], df_in.values[i, -1]] != [df_in.values[i - 1, -2], df_in.values[i - 1, -1]]]
    return points_list


points = load_ais_data('ais_data_18_06.xlsx')
#points2 = load_ais_data('ais_data_20_06.xlsx')

plot_df_dict = {
    'name': ['test_path1'],
    'color': [(255, 166, 26)],
    'path': [points]
}

df = pd.DataFrame(plot_df_dict)

view_state = pdk.ViewState(
    latitude=points[0][1], longitude=points[0][0], zoom=11)

layer = pdk.Layer(
    type="PathLayer",
    data=df,
    pickable=True,
    get_color="color",
    width_scale=20,
    width_min_pixels=2,
    get_path="path",
    get_width=1,
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state,
             tooltip={"text": "{name}"},
             map_provider="mapbox",
             map_style=pdk.map_styles.CARTO_LIGHT)


r.to_html("path_layer.html")

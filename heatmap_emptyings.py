import folium
import pandas as pd
import requests
import json


url = "https://raw.githubusercontent.com/Luke-but-not-Skywalker/OperationsManagement/main/data"

location_geo = f"{url}/geo_json_upper_tyrol.json"
location_poe = f"{url}/location_poe_2019.csv"
location_data = pd.read_csv(location_poe)
map_data = json.loads(requests.get(location_geo).text)

location_data['cont_cummunal_number'] = location_data['cont_cummunal_number'].astype('str')


m = folium.Map(location=[47.2,11.123672], zoom_start=9)

folium.Marker(
    location=[47.28851, 11.587031],
    popup="Swarco",
    icon=folium.Icon(icon="info-sign"),
).add_to(m)


choropleth = folium.Choropleth(
    geo_data=map_data,
    name="choropleth",
    data=location_data,
    columns=["cont_cummunal_number", "percentage_of_emptyings"],
    key_on="feature.properties.iso",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Emptyings (%)",
    highlight=True
).add_to(m)

folium.LayerControl().add_to(m)

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(["name"], labels=False)
)

m.save("index.html")


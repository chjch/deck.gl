import pydeck
import pandas as pd

COUNTRIES = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson"
POWER_PLANTS = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/global_power_plant_database.csv"

df = pd.read_csv(POWER_PLANTS)


def is_green(fuel_type):
    if fuel_type.lower() in ("nuclear", "water", "wind", "hydro", "biomass", "solar", "geothermal"):
        return [0, 255, 0]
    return [255, 255, 0]


df["color"] = df["primary_fuel"].apply(is_green)

view_state = pydeck.ViewState(latitude=51.47, longitude=0.45, zoom=4)

layers = []
# Set height and width variables
view = pydeck.View(type="_GlobeView", controller=True, width=1000, height=700)


layers = [
    pydeck.Layer(
        "GeoJsonLayer",
        id="base-map",
        data=COUNTRIES,
        stroked=False,
        filled=True,
        get_line_color=[60, 60, 60],
        get_fill_color=[200, 200, 200],
    ),
    pydeck.Layer(
        "ColumnLayer",
        id="power-plant",
        data=df,
        get_elevation="capacity_mw",
        get_position=["longitude", "latitude"],
        elevation_scale=100,
        pickable=True,
        auto_highlight=True,
        radius=40000,
        get_fill_color="color",
    ),
]

deck = pydeck.Deck(
    views=[view],
    initial_view_state=view_state,
    tooltip={"text": "{name}, {primary_fuel} plant, {country}"},
    layers=layers,
    # Note that this must be set for the globe to be opaque
    parameters={"cull": True}
)

deck.to_html("pydeck_globe.html", css_background_color="black")

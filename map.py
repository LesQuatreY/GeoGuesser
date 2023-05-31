import folium

class Map:
  def __init__(self):
    fond = r'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}' #'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    self.carte = folium.Map(
      location=[46.5, 2.3],
      zoom_start=6, 
      tiles=fond, 
      attr='© OpenStreetMap © CartoDB'
      )
    folium.Choropleth(
    "data/contour-des-departements.geojson",
    fill_opacity=.1
    ).add_to(self.carte)

  def marker(self, coord, popup="", icon=None):
    if icon is not None: icon=folium.features.CustomIcon(icon)
    folium.Marker(
        location=coord, popup=popup, icon_size=(50, 35),
        icon=icon
        ).add_to(self.carte)

  def line(self,point_a, point_b):
    folium.PolyLine(
      [tuple(point_a),tuple(point_b)], color="red", weight=2.5, opacity=.6, dash_array='10'
      ).add_to(self.carte)

  def circle(self, center, rayon):
    import math
    folium.Circle(center, opacity=.7, radius=1000*rayon).add_to(self.carte)

  def map(self):
    return self.carte
        
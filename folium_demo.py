import folium
import pandas
import csv
"""
    Creates a map showing the location of US volcanoes and their height. Also shows US State and World Country boundry layers.

"""
""""
# Early code without pandas
# fg = folium.FeatureGroup(name='myFeatureGroup')
# map10 = folium.Map(location=[47.620422,-122.349358],zoom_start=6, tiles="openstreetmap")
# popuptext='<i>I am the Space Needle. There are many like it but this one is mine. I must use the space needle to destroy the enemy, who is trying to kill me</1>'

#with open('seattle.txt','r') as f:
#    text = csv.reader(f,delimiter=',')
#    for row in text:
#        lat, long = float(row[1]), float(row[2])
#        loc = (lat, long)
#        tooltip = row[0]
#        ttname = row[0]
#        popuptext = f'I am {ttname}'
#        print(tooltip, lat, long, popuptext)
#        fg.add_child(folium.Marker(location=loc, popup=popuptext,tooltip=ttname, icon=folium.Icon(color='green')))
#        map10.add_child(fg)
#map10.save('map10.html')
"""

def elevation_color(elevation):
    if elevation < 1000:
        return 'green'
    elif  1000 <=  elevation < 3000:
        return 'orange'
    else:
        return 'red'

data = pandas.read_csv("Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
state = list(data["LOCATION"])
names = list(data["NAME"])

map = folium.Map(location=[41.4198990,-122.2009964], zoom_start=6, tiles="stamenterrain")

fgv = folium.FeatureGroup(name="Volcanoes")

# Add html links to google maps
google="https://www.google.com/search?q="
# html = f"""
# Volcano name:<br>
# <a href="https://www.google.com/search?q=%22{name}%22" target="_blank">{name}</a><br>
# Height: {el}m
# """

for lt, ln, el, name in zip(lat, lon, elev, names):
    """"
    # TODO: fix HTML links 
    #section for html iframes that pop up with a link. Currently borked.
    #htmlpopup = f"Volcano name:<br> <a href="{google}%22{name}%22" target="_blank">{name}</a><br> Height: {el}m"
    #iframe = folium.IFrame(html=htmlpopup, width=200, height=100)
    #fgv.add_child(folium.CircleMarker(location=[lt, ln], radius =10, popup=iframe,
    """
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius =10, popup=f"{name}  {el} meters",
    tooltip=f"{name} {el}m", fill=True, color = elevation_color(el), fill_opacity=0.4, line_color='#00000',
    icon=folium.Icon(color='green')))


# TODO: remove coloring from US so State pop coloring can occur
# adding world country outlines and population data
fgpw = folium.FeatureGroup(name="World Population")
fgpw.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000001 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# TODO: get GeoJSON data that includes population to show VolcanoToPopulation in colors
# adding US State outlines and population data
fgus = folium.FeatureGroup(name="US Population")
fgus.add_child(folium.GeoJson(data=open('us_2010.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda us: {'fillColor':'green' if us['properties']['CENSUSAREA'] < 100000
else 'orange' if 100000 <= us['properties']['CENSUSAREA'] < 200000 else 'red'}))


# CENSUSAREA
# Individual FeatureGroups as Children:
map.add_child(fgv)
map.add_child(fgpw)
map.add_child(fgus)

# This adds Layer control - turning on and off the add_child() layers - e.g. fgv (Volcanoes) and fgp (Population/Choropleth)
map.add_child(folium.LayerControl())

#Save with output name
map.save("newmap.html")

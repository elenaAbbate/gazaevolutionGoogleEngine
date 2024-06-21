import folium
import geemap
import ee
import branca.colormap as cm

# Inizializza l'API di Google Earth Engine
geemap.ee_initialize()

# Definisci l'area di interesse: la Striscia di Gaza
gaza = ee.Geometry.Rectangle([34.2, 31.2, 34.6, 31.6])

# Carica il dataset Landsat (ad esempio, Landsat 8)
landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterBounds(gaza)

# Funzione per ottenere un'immagine Landsat per una specifica data
def get_landsat_image(date):
    date = ee.Date(date)
    image = landsat.filterDate(date, date.advance(1, 'month')).median()
    vis_params = {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0,
        'max': 0.3,
        'gamma': [0.95, 1.1, 1]
    }
    return image.visualize(**vis_params).clip(gaza)

# Date di interesse
dates = [f'{year}-01-01' for year in range(2013, 2024)]

# Colleziona le immagini per le date specificate
images = [get_landsat_image(date).getMapId() for date in dates]

# Crea una mappa di base
m = folium.Map(location=[31.4, 34.4], zoom_start=10)

# Crea una barra temporale utilizzando branca
time_index = [f"{date[:4]}" for date in dates]
colormap = cm.linear.YlGnBu_09.scale(0, 1).to_step(len(time_index))

# Aggiungi le immagini alla mappa con la barra temporale
for index, image in enumerate(images):
    folium.raster_layers.TileLayer(
        tiles=image['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        overlay=True,
        name=f"Year {time_index[index]}",
        show=True if index == 0 else False
    ).add_to(m)

# Aggiungi layer control e colormap
folium.LayerControl().add_to(m)
colormap.caption = 'Year'
m.add_child(colormap)

# Salva la mappa come file HTML
m.save("gaza_timeseries_map.html")

print("Mappa salvata come gaza_timeseries_map.html")

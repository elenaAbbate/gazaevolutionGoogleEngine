import geemap
import folium
import ee
import branca.colormap as cm

# Inizializza l'API di Google Earth Engine
geemap.ee_initialize()

# Definisci l'area di interesse: la Striscia di Gaza
gaza = ee.Geometry.Rectangle([34.2, 31.2, 34.6, 31.6])

# Carica il dataset Sentinel-2
sentinel = ee.ImageCollection('COPERNICUS/S2').filterBounds(gaza).filterDate('2015-06-23', '2024-01-01')

# Funzione per ottenere un'immagine Sentinel-2 per una specifica data
def get_sentinel_image(date):
    date = ee.Date(date)
    image = sentinel.filterDate(date, date.advance(1, 'month')).median()
    vis_params = {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0,
        'max': 3000,
    }
    return image.visualize(**vis_params).clip(gaza)

# Date di interesse
dates = [f'{year}-01-01' for year in range(2016, 2024)]

# Colleziona le immagini per le date specificate
images = [get_sentinel_image(date).getMapId() for date in dates]

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
m.save("gaza_timeseries_map2.html")

print("Mappa salvata come gaza_timeseries_map.html")

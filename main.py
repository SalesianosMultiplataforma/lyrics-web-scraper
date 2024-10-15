import requests
from bs4 import BeautifulSoup
import os
import re

# URL base de letras.com
base_url = "https://www.letras.com"

artist_url = "https://www.letras.com/melendi/"

# Extraer el nombre del artista de la URL
artist_name = artist_url.rstrip('/').split('/')[-1]

# Crear una carpeta para guardar las letras
if not os.path.exists("letras"):
    os.makedirs("letras")

# Crear una subcarpeta con el nombre del artista
artist_folder = os.path.join("letras", artist_name)
if not os.path.exists(artist_folder):
    os.makedirs(artist_folder)

# Función para limpiar nombres de archivos
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Hacer una solicitud a la página del artista
response = requests.get(artist_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar todos los enlaces a las canciones
song_links = soup.find_all('a', class_='songList-table-songName')

for link in song_links:
    song_url = base_url + link['href']
    song_title = link.text.strip()
    sanitized_title = sanitize_filename(song_title)

    # Hacer una solicitud a la página de la canción
    song_response = requests.get(song_url)
    song_soup = BeautifulSoup(song_response.text, 'html.parser')

    # Extraer la letra de la canción
    lyrics = song_soup.find('div', class_='lyric-original').get_text(separator='\n').strip()

    # Guardar la letra en un archivo .txt dentro de la subcarpeta del artista
    with open(os.path.join(artist_folder, f"{sanitized_title}.txt"), 'w', encoding='utf-8') as file:
        file.write(lyrics)

print(f"Letras descargadas y guardadas en la carpeta '{artist_folder}'.")
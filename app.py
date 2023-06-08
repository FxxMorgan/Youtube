from flask import Flask, render_template, request
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
import youtube_dl

# -*- coding: utf-8 -*-

app = Flask(__name__)

# Configuración de opciones de descarga
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': 'video.mp4',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']

        # Obtener icono de la página
        page_icon_url = get_page_icon_url(video_url)
        page_icon = get_page_icon(page_icon_url)
        if page_icon:
            page_icon = page_icon.resize((64, 64), Image.ANTIALIAS)

        # Descargar el video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return render_template('index.html', page_icon=page_icon)
    
    return render_template('index.html')

def get_page_icon_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    icon_link = soup.find('link', rel='icon')
    if icon_link:
        icon_url = icon_link['href']
        if not icon_url.startswith('http'):
            icon_url = url + icon_url
        return icon_url
    return None

def get_page_icon(url):
    response = requests.get(url)
    favicon = None
    if response.ok:
        content_type = response.headers.get('content-type')
        if content_type == 'image/png' or content_type == 'image/x-icon':
            favicon = Image.open(BytesIO(response.content))
    return favicon

if __name__ == '__main__':
    app.run()

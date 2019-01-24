# SentinelDownloader
Collezione di script Python per lo scarico dei dati Sentinel-2 da **Copernicus Open Access Hub**<br/>
https://scihub.copernicus.eu/userguide/OpenSearchAPI

Dipende dal pacchetto **Sentinelsat**, installabile via **pip**<br/>
https://sentinelsat.readthedocs.io/en/stable/index.html

### Esempio di utilizzo con Anaconda

>I comandi possono differire sulla base del sistema operativo in uso.<br/> 
>Fare riferimento alla guida di Anaconda.

Installare Anaconda e creare un ambiente dedicato con:
```
conda create --name sentinelenv pip
```

Attivare l'ambiente:
```
conda activate sentinelenv
```

Installare sentinelsat:
```
pip install sentinelsat
```

Lanciare uno degli script per il download:
```
python download_ByTiles.py
```

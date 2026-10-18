import os
import requests
from dotenv import load_dotenv
from folium import Icon, Map, Marker

load_dotenv(".env")

URL = "http://api.olhovivo.sptrans.com.br/v2.1"

s = requests.Session()
res = s.post(f"{URL}/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}")
print("Status autenticação:", res.text)

referencia = "Barra Funda"
linha_busca = s.get(f"{URL}/Linha/Buscar?termosBusca={referencia}").json()
linha = linha_busca[0]["cl"]

paradas = s.get(f"{URL}/Parada/BuscarParadasPorLinha?codigoLinha={linha}").json()
onibus = s.get(f"{URL}/Posicao/Linha?codigoLinha={linha}").json()["vs"]

m = Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=14)

for i in paradas:
    Marker(location=[i["py"], i["px"]], popup=i["np"], icon=Icon(color="blue")).add_to(m)

for i in onibus:
    Marker(location=[i["py"], i["px"]], popup=i["p"], icon=Icon(color="red")).add_to(m)

m.save("mapa.html")
print("O arquivo 'mapa.html' foi salvo com sucesso!")
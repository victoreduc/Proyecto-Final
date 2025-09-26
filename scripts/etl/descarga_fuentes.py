# Descarga DGT, INE y AEMET a data/raw/. En este entorno sin internet se deja placeholder.
import os, pathlib
from dotenv import load_dotenv

RAW = pathlib.Path("data/raw"); RAW.mkdir(parents=True, exist_ok=True)
load_dotenv()
AEMET_API_KEY = os.getenv("AEMET_API_KEY")
YEARS = os.getenv("YEARS","2023").split(",")
AEMET_STATIONS = os.getenv("AEMET_STATIONS","").split(",")

DGT_URLS = {
 "2022":"https://www.dgt.es/menusecundario/dgt-en-cifras/dgt-en-cifras-resultados/dgt-en-cifras-detalle/Ficheros-microdatos-de-accidentes-con-victimas-2022/",
 "2023":"https://www.dgt.es/menusecundario/dgt-en-cifras/dgt-en-cifras-resultados/dgt-en-cifras-detalle/Ficheros-microdatos-de-accidentes-con-victimas-2023/"
}
INE_URL = "https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&idp=1254734710990&menu=ultiDatos"
AEMET_DOC = "https://opendata.aemet.es/dist/index.html"

def placeholder(url, name):
    (RAW/name).write_text(f"Descarga manual: {url}\n", encoding="utf-8")
    print("[placeholder]", name, "->", url)

def main():
    for y in YEARS:
        placeholder(DGT_URLS.get(y.strip(), "https://www.dgt.es/menusecundario/dgt-en-cifras/"), f"dgt_{y.strip()}.txt")
    placeholder(INE_URL, "ine_codigos_municipios.txt")
    if not AEMET_API_KEY: print("[WARN] Falta AEMET_API_KEY en .env")
    for y in YEARS:
        for st in filter(None, AEMET_STATIONS):
            placeholder(AEMET_DOC, f"aemet_obs_{st.strip()}_{y.strip()}.txt")

if __name__ == "__main__":
    main()

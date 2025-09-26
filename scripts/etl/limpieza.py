# Normalización con datos sintéticos (para que funcione sin Internet).
import pathlib, pandas as pd
RAW = pathlib.Path("data/raw")
INTERIM = pathlib.Path("data/interim"); INTERIM.mkdir(parents=True, exist_ok=True)

def dummy_read_dgt():
    rows=[]; 
    for i in range(60000):
        rows.append({
            "fecha": f"2023-06-{(i%28)+1:02d}",
            "hora": f"{(i%24):02d}:00",
            "provincia": (i%52)+1,
            "municipio": (i%999)+1,
            "tipo_via": "Urbana" if i%2==0 else "Interurbana",
            "num_victimas": (i%5),
            "meteorologia": "Lluvia" if i%7==0 else "Despejado",
            "lat": 40.4 + (i%100)/1000.0,
            "lon": -3.7 + (i%100)/1000.0,
        })
    return pd.DataFrame(rows)

def dummy_read_aemet():
    df = pd.DataFrame({"fecha": pd.date_range("2023-06-01", periods=24*30, freq="H")})
    df["hora"] = df["fecha"].dt.hour
    df["tmed"] = 20.0; df["prec"] = 0.0; df["racha"] = 30; df["vis"]=10000
    df["fecha"] = df["fecha"].dt.date
    return df

def main():
    dgt = dummy_read_dgt(); met = dummy_read_aemet()
    dgt["fecha"] = pd.to_datetime(dgt["fecha"])
    dgt["hora"] = pd.to_datetime(dgt["hora"], format="%H:%M").dt.hour
    met["fecha"] = pd.to_datetime(met["fecha"])
    dgt.to_parquet(INTERIM/"dgt_clean.parquet", index=False)
    met.to_parquet(INTERIM/"aemet_clean.parquet", index=False)
    print("[OK] Guardados intermedios")

if __name__ == "__main__":
    main()

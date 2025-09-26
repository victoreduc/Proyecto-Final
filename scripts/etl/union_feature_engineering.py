# Unión + features + validación + guardado final.parquet
import pathlib, json, pandas as pd
from great_expectations.dataset import PandasDataset
INTERIM = pathlib.Path("data/interim")
PROCESSED = pathlib.Path("data/processed"); PROCESSED.mkdir(parents=True, exist_ok=True)

def feature_engineering(df):
    df["anio"]=df["fecha"].dt.year
    df["mes"]=df["fecha"].dt.month
    df["dia_semana"]=df["fecha"].dt.dayofweek
    df["finde"]=df["dia_semana"].isin([5,6]).astype(int)
    df["lluvia"]=(df.get("prec",0)>0).astype(int)
    df["noche"]=((df["hora"]>=22)|(df["hora"]<=6)).astype(int)
    return df

def validate(df):
    ds=PandasDataset(df.copy())
    ds.expect_table_row_count_to_be_between(min_value=50000)
    ds.expect_column_values_to_not_be_null("fecha")
    return ds.validate()

def main():
    dgt=pd.read_parquet(INTERIM/"dgt_clean.parquet")
    met=pd.read_parquet(INTERIM/"aemet_clean.parquet")
    merged=dgt.merge(met,on=["fecha","hora"],how="left")
    merged=feature_engineering(merged)
    res=validate(merged)
    merged.to_parquet(PROCESSED/"final.parquet", index=False)
    with open(PROCESSED/"dictionary.json","w",encoding="utf-8") as f:
        json.dump({c:str(merged[c].dtype) for c in merged.columns}, f, ensure_ascii=False, indent=2)
    print("[OK] final.parquet", len(merged),"filas", len(merged.columns),"columnas"); print(res["statistics"])

if __name__ == "__main__":
    main()

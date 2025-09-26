import streamlit as st, pandas as pd
from pathlib import Path
import altair as alt

st.set_page_config(page_title="Siniestralidad y Meteo (España)", layout="wide")
st.title("Siniestralidad vial y meteorología — España")
path = Path("data/processed/final.parquet")
if not path.exists():
    st.warning("No encuentro `data/processed/final.parquet`. Ejecuta el ETL primero.")
else:
    df = pd.read_parquet(path)
    st.success(f"Dataset cargado: {len(df):,} filas · {len(df.columns)} columnas")
    cols = st.columns(4)
    with cols[0]:
        anios = sorted(df["anio"].dropna().unique().tolist())
        anio = st.selectbox("Año", options=anios, index=0 if anios else None)
    with cols[1]:
        tipo = st.multiselect("Tipo de vía", options=sorted(df["tipo_via"].dropna().unique()), default=None)
    with cols[2]:
        lluvia = st.selectbox("Lluvia", options=["Todos","Con lluvia","Sin lluvia"])
    with cols[3]:
        finde = st.selectbox("Fin de semana", options=["Todos","Sí","No"])
    filtered = df[df["anio"]==anio] if anios else df.copy()
    if tipo: filtered = filtered[filtered["tipo_via"].isin(tipo)]
    if lluvia!="Todos": filtered = filtered[filtered["lluvia"]==(1 if lluvia=="Con lluvia" else 0)]
    if finde!="Todos": filtered = filtered[filtered["finde"]==(1 if finde=="Sí" else 0)]
    k1,k2,k3,k4 = st.columns(4)
    with k1: st.metric("Accidentes", f"{len(filtered):,}")
    with k2: st.metric("Víctimas mediana", f"{filtered['num_victimas'].median():.1f}")
    with k3: st.metric("% con lluvia", f"{100*filtered['lluvia'].mean():.1f}%")
    with k4: st.metric("Nocturnos %", f"{100*filtered['noche'].mean():.1f}%")
    heat = alt.Chart(filtered).mark_rect().encode(
        x=alt.X("hora:O", title="Hora"),
        y=alt.Y("dia_semana:O", title="Día semana (0=Lun)"),
        color=alt.Color("count():Q", title="Accidentes")
    ).properties(height=260)
    st.altair_chart(heat, use_container_width=True)

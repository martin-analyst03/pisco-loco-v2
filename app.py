import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="Portal Pisco Loco", page_icon="🍸", layout="wide")
st.title("🍸 Portal de Gestión Operativa - Pisco Loco")

tab1, tab2 = st.tabs(["📊 Simulador de Costos", "🤖 Diagnóstico Financiero con IA"])

with tab1:
    st.header("Simulador de Costos y Escala Operativa")
    costos_fijos = st.slider("Costos Fijos Mensuales ($ CLP)", 1000000, 10000000, 4000000, 250000)
    costo_variable_unitario = st.slider("Costo Variable por Botella ($ CLP)", 1500, 6000, 3590, 10)
    unidades = st.slider("Botellas Producidas al Mes", 100, 10000, 2000, 100)

    costo_total = costos_fijos + (costo_variable_unitario * unidades)
    costo_medio = costo_total / unidades

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Costo Total Operativo", f"${costo_total:,.0f} CLP")
    with col2:
        st.metric("Costo Medio por Botella", f"${costo_medio:,.0f} CLP")

with tab2:
    st.header("Auditoría y Análisis de Gastos con IA")
    api_key = st.text_input("Ingresa tu API Key de Google AI Studio:", type="password")
    archivo_subido = st.file_uploader("Carga tu archivo CSV de gastos", type=["csv"])

    if archivo_subido is not None and api_key:
        df = pd.read_csv(archivo_subido)
        st.subheader("📋 Vista Previa de Gastos")
        st.dataframe(df)

        if st.button("🚀 Generar Diagnóstico Financiero"):
            with st.spinner("La IA está analizando los datos..."):
                try:
                    client = genai.Client(api_key=api_key)
                    datos_str = df.to_string(index=False)

                    prompt = f"""
                    Actúa como un Analista Financiero Senior de la empresa 'Pisco Loco'.
                    Tu objetivo es recortar gastos para maximizar el margen de ganancia por botella.
                    
                    Analiza la siguiente tabla de datos:
                    {datos_str}

                    Genera un informe estructurado que responda:
                    1. Mes con mayor gasto y tendencia general.
                    2. Ítems que generan mayor y menor gasto.
                    3. Clasificación entre gastos IMPRESCINDIBLES y PRESCINDIBLES.
                    4. Plan de acción de 3 pasos concretos para reducir costos sin afectar la calidad.
                    """

                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                    )
                    st.subheader("💡 Diagnóstico Estratégico")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error al conectar con la API de Google: {e}")

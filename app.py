import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# --- Configuración de la página ---
st.set_page_config(page_title="Finanzas Familiares", page_icon="🏠", layout="wide")

# --- Estilos CSS para un look moderno ---
st.markdown("""
    <style>
    /* Fondo general más limpio */
    .stApp { background-color: #f4f7f6; }
    
    /* Tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #2e7d32;
    }
    
    /* Títulos */
    h1, h2, h3 { color: #1a237e; font-family: 'Segoe UI', sans-serif; }
    
    /* Texto de alerta */
    .stAlert { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Utilidades ---
def fmt(n):
    if pd.isna(n) or n == 0: return "$0"
    return f"${n:,.0f}".replace(",", ".")

# --- Datos Base ---
sueldos = {"Alexander": 1746582, "Mariana": 1958386}
# Lista de compromisos (puedes ir ajustando estos valores)
compromisos = {
    "Dividendos Propiedades": 1208288,
    "Colegios y Niños": 543000,
    "Tarjetas de Crédito": 213478,
    "Servicios y Gastos Fijos": 450000
}

# --- Selector de Mes Financiero (19 al 18) ---
st.title("🏠 Panel de Finanzas del Hogar")
st.write("Bienvenido. Aquí tienes el resumen de tu mes financiero.")

meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
col_mes, _ = st.columns([1, 2])
with col_mes:
    mes_sel = st.selectbox("Selecciona el ciclo (inicia el 19)", options=meses, index=22, format_func=lambda d: d.strftime("%B %Y").capitalize())

inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
st.info(f"📅 **Ciclo actual:** {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")

st.divider()

# --- 1. Ingresos ---
st.header("💵 Ingresos del Mes")
c1, c2, c3 = st.columns(3)
ingreso_total = sueldos["Alexander"] + sueldos["Mariana"]
c1.metric("Sueldo Alexander", fmt(sueldos["Alexander"]))
c2.metric("Sueldo Mariana", fmt(sueldos["Mariana"]))
c3.metric("Ingreso Total Hogar", fmt(ingreso_total), delta="Mes Actual")

st.divider()

# --- 2. Compromisos ---
st.header("📌 Compromisos Pendientes")
st.write("Estos son los gastos comprometidos para este ciclo:")
total_compromisos = sum(compromisos.values())

for concepto, monto in compromisos.items():
    st.write(f"- **{concepto}:** {fmt(monto)}")

st.markdown(f"### Total Comprometido: {fmt(total_compromisos)}")

st.divider()

# --- 3. Libre Disposición ---
st.header("💸 Saldo de Libre Disposición")
st.write("Es lo que queda después de cubrir todos los compromisos del mes.")

plata_libre = ingreso_total - total_compromisos

if plata_libre > 0:
    c_libre, _ = st.columns([1, 1])
    with c_libre:
        st.metric("Plata disponible para gastar", fmt(plata_libre))
    st.success("¡Buen trabajo! Este es el monto que puedes transferir a tus cuentas de Libre Disposición (Falabella).")
else:
    st.error("⚠️ Alerta: Los compromisos de este mes superan los ingresos totales del hogar.")

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# --- Configuración de la página ---
st.set_page_config(page_title="Finanzas Alexander & Mariana", page_icon="🏠", layout="wide")

# --- Estilos CSS para un look moderno y ordenado ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: #f8f9fa; }
    
    /* Tarjetas blancas */
    .custom-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Títulos de las tarjetas */
    .card-title {
        color: #1f2937;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 10px;
    }
    
    /* Filas de datos */
    .data-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .data-label { color: #4b5563; }
    .data-value { font-weight: 600; color: #111827; }
    
    /* Total */
    .total-row {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid #e5e7eb;
        font-size: 16px;
        font-weight: bold;
        color: #1d4ed8;
    }
    </style>
""", unsafe_allow_html=True)

# --- Utilidades ---
def fmt(n):
    if pd.isna(n) or n == 0: return "$0"
    return f"${n:,.0f}".replace(",", ".")

# --- Datos Base (Extraídos de tu Excel) ---
# Aquí luego agregaremos los formularios para que estos datos se puedan editar
ingresos_data = {
    "Alexander": {
        "Sueldo líquido": 1746582,
        "Sobresueldo": 0,
        "Trimestral": 0,
        "Asesorías": 0,
        "Otro": 0
    },
    "Mariana": {
        "Sueldo líquido": 1958386,
        "Sobresueldo": 0,
        "Trimestral": 0,
        "Asesorías": 500000, # Dato extraído de tu archivo
        "Otro": 0
    }
}

# Compromisos pendientes (los sacamos del Excel)
compromisos = {
    "Dividendos Propiedades": 1208288,
    "Colegios y Niños": 543000,
    "Tarjetas de Crédito": 213478,
    "Servicios y Gastos Fijos": 450000
}

# --- Título ---
st.title("🏠 Panel de Finanzas del Hogar de Alexander y Mariana")
st.write("Bienvenido. Aquí tienes el resumen de tu mes financiero.")

# --- Selector de Mes Financiero (19 al 18) ---
meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
col_mes, _ = st.columns([1, 2])
with col_mes:
    # Por defecto seleccionamos Noviembre 2026 (índice 22)
    mes_sel = st.selectbox("Selecciona el ciclo (inicia el 19)", options=meses, index=22, format_func=lambda d: d.strftime("%B %Y").capitalize())

inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
st.info(f"📅 **Ciclo actual de trabajo:** {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")

st.divider()

# --- 1. Ingresos del Mes ---
st.header("💵 Ingresos del Mes")

col_ing_1, col_ing_2 = st.columns(2)

# Tarjeta Alexander
with col_ing_1:
    html_alex = '<div class="custom-card">'
    html_alex += '<div class="card-title">Alexander</div>'
    total_alex = sum(ingresos_data["Alexander"].values())
    for k, v in ingresos_data["Alexander"].items():
        html_alex += f'<div class="data-row"><span class="data-label">{k}</span><span class="data-value">{fmt(v)}</span></div>'
    html_alex += f'<div class="total-row"><span>Total Recibido</span><span>{fmt(total_alex)}</span></div>'
    html_alex += '</div>'
    st.markdown(html_alex, unsafe_allow_html=True)

# Tarjeta Mariana
with col_ing_2:
    html_mar = '<div class="custom-card">'
    html_mar += '<div class="card-title">Mariana</div>'
    total_mar = sum(ingresos_data["Mariana"].values())
    for k, v in ingresos_data["Mariana"].items():
        html_mar += f'<div class="data-row"><span class="data-label">{k}</span><span class="data-value">{fmt(v)}</span></div>'
    html_mar += f'<div class="total-row"><span>Total Recibido</span><span>{fmt(total_mar)}</span></div>'
    html_mar += '</div>'
    st.markdown(html_mar, unsafe_allow_html=True)

# Total Hogar
st.markdown(f"""
<div class="custom-card" style="background-color: #eff6ff; border: 1px solid #bfdbfe;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 18px; font-weight: bold; color: #1e3a8a;">Ingreso Total del Hogar</span>
        <span style="font-size: 24px; font-weight: bold; color: #1d4ed8;">{fmt(total_alex + total_mar)}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 2. Compromisos Pendientes ---
st.header("📌 Compromisos Pendientes")
st.write("Gastos comprometidos para este ciclo:")

total_compromisos = sum(compromisos.values())

# Mostramos los compromisos en una tarjeta
html_comp = '<div class="custom-card">'
for concepto, monto in compromisos.items():
    html_comp += f'<div class="data-row"><span class="data-label">{concepto}</span><span class="data-value" style="color: #dc2626;">{fmt(monto)}</span></div>'
html_comp += f'<div class="total-row" style="color: #dc2626;"><span>Total Comprometido</span><span>{fmt(total_compromisos)}</span></div>'
html_comp += '</div>'
st.markdown(html_comp, unsafe_allow_html=True)

st.divider()

# --- 3. Saldo de Libre Disposición ---
st.header("💸 Saldo de Libre Disposición")
st.write("Es lo que queda después de cubrir todos los compromisos del mes. Se calcula del ingreso total menos los compromisos (y luego se divide o asigna a cada uno según corresponda).")

plata_libre = (total_alex + total_mar) - total_compromisos

# Para esta vista inicial, mostramos el total. Luego podemos hacer el cálculo exacto por persona.
col_libre_1, col_libre_2 = st.columns(2)

with col_libre_1:
    st.markdown(f"""
    <div class="custom-card" style="border-left: 5px solid #16a34a;">
        <div class="card-title">Disponible Total</div>
        <div style="font-size: 28px; font-weight: bold; color: #15803d;">{fmt(plata_libre)}</div>
        <p style="font-size: 12px; color: #6b7280; margin-top: 10px;">Monto total sobrante para el hogar.</p>
    </div>
    """, unsafe_allow_html=True)

with col_libre_2:
    # Este cálculo exacto por persona requiere el motor de reparto, pero dejamos el espacio listo
    st.markdown(f"""
    <div class="custom-card" style="border-left: 5px solid #2563eb;">
        <div class="card-title">Próximo paso</div>
        <p style="font-size: 14px; color: #4b5563;">En la próxima actualización, aquí verás el saldo exacto para <b>Alexander</b> y para <b>Mariana</b>, aplicando las reglas de reparto.</p>
    </div>
    """, unsafe_allow_html=True)

if plata_libre <= 0:
    st.error("⚠️ Alerta: Los compromisos de este mes superan los ingresos totales del hogar.")

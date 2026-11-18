import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# --- Configuración de la página ---
st.set_page_config(page_title="Finanzas Alexander & Mariana", page_icon="🏠", layout="wide")

# --- Estilos CSS (Colores y Diseño) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Contenedor general de tarjetas */
    .custom-card {
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Colores específicos */
    .card-alexander { background-color: #e0f2fe; border-top: 5px solid #38bdf8; } /* Celeste suave */
    .card-mariana { background-color: #ffe4e6; border-top: 5px solid #fb7185; }   /* Rosado suave */
    .card-neutral { background-color: #ffffff; border-top: 5px solid #cbd5e1; }
    
    /* Títulos y textos */
    .card-title {
        color: #1f2937;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(0,0,0,0.1);
        padding-bottom: 10px;
    }
    .data-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .data-label { color: #374151; }
    .data-value { font-weight: 600; color: #111827; }
    
    .total-row {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid rgba(0,0,0,0.1);
        font-size: 16px;
        font-weight: bold;
    }
    .total-alexander { color: #0369a1; }
    .total-mariana { color: #be123c; }
    </style>
""", unsafe_allow_html=True)

# --- Utilidades ---
def fmt(n):
    if pd.isna(n) or n == 0: return "$0"
    return f"${n:,.0f}".replace(",", ".")

# --- Datos Base ---
ingresos_data = {
    "Alexander": {
        "Sueldo líquido": 1746582,
        "Sobresueldo": 0,
        "Trimestral": 0,
        "Asesorías": 500000, # Agregado
        "Otro": 0
    },
    "Mariana": {
        "Sueldo líquido": 1958386,
        "Sobresueldo": 0,
        "Trimestral": 0,
        "Asesorías": 0,
        "Otro": 0
    }
}

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
nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

col_mes, _ = st.columns([1, 2])
with col_mes:
    # Función para mostrar "Noviembre 2026"
    def formato_mes(d):
        return f"{nombres_meses[d.month-1]} {d.year}"
    
    mes_sel = st.selectbox("Selecciona el mes para trabajar (ciclo del 19 al 18)", options=meses, index=22, format_func=formato_mes)

# Cálculo del período real 19 al 18
inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
st.info(f"📅 **Ciclo actual de trabajo:** {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")

st.divider()

# --- 1. Ingresos del Mes ---
st.header("💵 Ingresos del Mes")

col_ing_1, col_ing_2 = st.columns(2)

# Tarjeta Alexander
with col_ing_1:
    total_alex = sum(ingresos_data["Alexander"].values())
    html_alex = '<div class="custom-card card-alexander">'
    html_alex += '<div class="card-title">Alexander</div>'
    for k, v in ingresos_data["Alexander"].items():
        html_alex += f'<div class="data-row"><span class="data-label">{k}</span><span class="data-value">{fmt(v)}</span></div>'
    html_alex += f'<div class="total-row total-alexander"><span>Total Recibido</span><span>{fmt(total_alex)}</span></div>'
    html_alex += '</div>'
    st.markdown(html_alex, unsafe_allow_html=True)

# Tarjeta Mariana
with col_ing_2:
    total_mar = sum(ingresos_data["Mariana"].values())
    html_mar = '<div class="custom-card card-mariana">'
    html_mar += '<div class="card-title">Mariana</div>'
    for k, v in ingresos_data["Mariana"].items():
        html_mar += f'<div class="data-row"><span class="data-label">{k}</span><span class="data-value">{fmt(v)}</span></div>'
    html_mar += f'<div class="total-row total-mariana"><span>Total Recibido</span><span>{fmt(total_mar)}</span></div>'
    html_mar += '</div>'
    st.markdown(html_mar, unsafe_allow_html=True)

# Total Hogar
st.markdown(f"""
<div class="custom-card card-neutral" style="background-color: #f1f5f9;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 18px; font-weight: bold; color: #334155;">Ingreso Total del Hogar</span>
        <span style="font-size: 24px; font-weight: bold; color: #0f172a;">{fmt(total_alex + total_mar)}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 2. Compromisos Pendientes ---
st.header("📌 Compromisos Pendientes")
st.write("Gastos comprometidos para este ciclo:")

total_compromisos = sum(compromisos.values())

html_comp = '<div class="custom-card card-neutral">'
for concepto, monto in compromisos.items():
    html_comp += f'<div class="data-row"><span class="data-label">{concepto}</span><span class="data-value" style="color: #dc2626;">{fmt(monto)}</span></div>'
html_comp += f'<div class="total-row" style="color: #dc2626;"><span>Total Comprometido</span><span>{fmt(total_compromisos)}</span></div>'
html_comp += '</div>'
st.markdown(html_comp, unsafe_allow_html=True)

st.divider()

# --- 3. Saldo de Libre Disposición ---
st.header("💸 Saldo de Libre Disposición")
st.write("Es lo que queda después de cubrir todos los compromisos del mes.")

plata_libre = (total_alex + total_mar) - total_compromisos

col_libre_1, col_libre_2 = st.columns(2)

with col_libre_1:
    st.markdown(f"""
    <div class="custom-card" style="border-left: 5px solid #16a34a; background-color: #f0fdf4;">
        <div class="card-title" style="border-bottom: none; color: #166534;">Disponible Total</div>
        <div style="font-size: 28px; font-weight: bold; color: #15803d;">{fmt(plata_libre)}</div>
        <p style="font-size: 12px; color: #4b5563; margin-top: 10px;">Monto total sobrante para el hogar.</p>
    </div>
    """, unsafe_allow_html=True)

with col_libre_2:
    st.markdown(f"""
    <div class="custom-card card-neutral">
        <div class="card-title">Próximo paso</div>
        <p style="font-size: 14px; color: #4b5563;">En la próxima actualización, aquí verás el saldo exacto para <b>Alexander</b> y <b>Mariana</b>, aplicando las reglas de reparto.</p>
    </div>
    """, unsafe_allow_html=True)

if plata_libre <= 0:
    st.error("⚠️ Alerta: Los compromisos de este mes superan los ingresos totales del hogar.")

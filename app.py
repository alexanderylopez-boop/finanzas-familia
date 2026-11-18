import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Finanzas Alexander & Mariana", page_icon="🏠", layout="wide")

# --- Estilos CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .custom-card { padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .card-alexander { background-color: #e0f2fe; border-top: 5px solid #38bdf8; } 
    .card-mariana { background-color: #ffe4e6; border-top: 5px solid #fb7185; }   
    .card-title { color: #1f2937; font-size: 18px; font-weight: 600; margin-bottom: 15px; border-bottom: 1px solid rgba(0,0,0,0.1); padding-bottom: 10px; }
    .data-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 15px; }
    .data-label { color: #374151; }
    .data-value { font-weight: 600; color: #111827; }
    .total-row { display: flex; justify-content: space-between; margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.1); font-size: 16px; font-weight: bold; }
    .total-alexander { color: #0369a1; }
    .total-mariana { color: #be123c; }
    .libre-value { font-size: 28px; font-weight: bold; color: #15803d; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

def fmt(n):
    if pd.isna(n) or n == 0: return "$0"
    return f"${n:,.0f}".replace(",", ".")

# --- 1. INICIALIZACIÓN DE DATOS EN MEMORIA (Session State) ---
# Si es la primera vez que abre la app, cargamos los valores por defecto
if 'sueldos' not in st.session_state:
    st.session_state.sueldos = {
        "Alexander": 1746582,
        "Mariana": 1958386
    }

if 'asesorias' not in st.session_state:
    st.session_state.asesorias = {
        "Alexander": 500000,
        "Mariana": 500000
    }

# --- Datos fijos (por ahora) ---
compromisos = {"Dividendos Propiedades": 1208288, "Colegios y Niños": 543000, "Tarjetas de Crédito": 213478, "Servicios y Gastos Fijos": 450000}

# --- BANCOS Y BOLSILLOS (Hoja 2) ---
cuentas_bancos = {
    "Alexander": [
        {"Banco": "BCI", "Cuenta": "Cta. Cte. Alexander", "Bolsillos": [{"Nombre": "Saldo sin asignar", "Monto": 1746582}, {"Nombre": "Compras grandes familiares", "Monto": 1000000}, {"Nombre": "Garantía Los Diamelos", "Monto": 920000}, {"Nombre": "Fondo propio Los Diamelos", "Monto": 867572}]},
        {"Banco": "BancoEstado", "Cuenta": "Cta. Cte. Alexander", "Bolsillos": [{"Nombre": "Fondo común Casa 716 / Filipo", "Monto": 305000}, {"Nombre": "Reserva dividendo Casa 716", "Monto": 400000}]},
        {"Banco": "BancoEstado", "Cuenta": "Cuenta RUT Alexander", "Bolsillos": [{"Nombre": "Primer respaldo de Alexander", "Monto": 250000}]},
        {"Banco": "Scotiabank", "Cuenta": "Cta. Cte. Alexander", "Bolsillos": [{"Nombre": "Fondo de combustible", "Monto": 75325}, {"Nombre": "Reserva para generador", "Monto": 550000}]},
        {"Banco": "Falabella", "Cuenta": "Cta. Cte. Alexander", "Bolsillos": [{"Nombre": "Libre disposición de Alexander", "Monto": 183550}]}
    ],
    "Mariana": [
        {"Banco": "Itaú", "Cuenta": "Cta. Cte. Mariana", "Bolsillos": [{"Nombre": "Saldo sin asignar", "Monto": 1958386}, {"Nombre": "Fondo Capellán y reparaciones", "Monto": 0}]},
        {"Banco": "BancoEstado", "Cuenta": "Cta. Cte. Mariana", "Bolsillos": [{"Nombre": "Presupuesto mensual de hogar", "Monto": 0}]},
        {"Banco": "BancoEstado", "Cuenta": "Cuenta RUT Mariana", "Bolsillos": [{"Nombre": "Primer respaldo de Mariana", "Monto": 19052}]},
        {"Banco": "Falabella", "Cuenta": "Cta. Cte. Mariana", "Bolsillos": [{"Nombre": "Libre disposición de Mariana", "Monto": 80}]}
    ]
}

# --- INTERFAZ GRÁFICA ---
st.title("🏠 Panel de Finanzas del Hogar")

# Selector de mes
meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
col_mes, _ = st.columns([1, 2])
with col_mes:
    mes_sel = st.selectbox("Selecciona el mes", options=meses, index=22, format_func=lambda d: f"{nombres_meses[d.month-1]} {d.year}")

inicio = mes_sel.replace(day=19) 
fin = (inicio + relativedelta(months=1)).replace(day=18)
st.info(f"📅 **Ciclo actual:** {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📊 Resumen (Hoja 1)", "🏦 Cuentas y Bolsillos (Hoja 2)"])

# ==========================================
# PESTAÑA 1: HOJA 1
# ==========================================
with tab1:
    # --- FORMULARIO DE INGRESO MANUAL (La prueba que pediste) ---
    with st.expander("✏️ Modificar Ingresos del Mes (Prueba de ingreso manual)", expanded=False):
        st.write("Escribe los montos y presiona 'Guardar' para ver cómo se actualiza la app.")
        
        with st.form("form_ingresos"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nuevo_sueldo_a = st.number_input("Sueldo Líquido Alexander", value=st.session_state.sueldos["Alexander"], step=1000)
                nueva_asesoria_a = st.number_input("Asesorías Alexander", value=st.session_state.asesorias["Alexander"], step=1000)
            with col_f2:
                nuevo_sueldo_m = st.number_input("Sueldo Líquido Mariana", value=st.session_state.sueldos["Mariana"], step=1000)
                nueva_asesoria_m = st.number_input("Asesorías Mariana", value=st.session_state.asesorias["Mariana"], step=1000)
            
            boton_guardar = st.form_submit_button("💾 Guardar Cambios")
            
            if boton_guardar:
                st.session_state.sueldos["Alexander"] = nuevo_sueldo_a
                st.session_state.sueldos["Mariana"] = nuevo_sueldo_m
                st.session_state.asesorias["Alexander"] = nueva_asesoria_a
                st.session_state.asesorias["Mariana"] = nueva_asesoria_m
                st.success("¡Datos guardados en la memoria de la app!")

    # --- VISUALIZACIÓN DE INGRESOS ---
    st.header("💵 Ingresos del Mes")
    col_ing_1, col_ing_2 = st.columns(2)

    with col_ing_1:
        total_alex = st.session_state.sueldos["Alexander"] + st.session_state.asesorias["Alexander"]
        html_alex = '<div class="custom-card card-alexander">'
        html_alex += '<div class="card-title">Alexander</div>'
        html_alex += f'<div class="data-row"><span class="data-label">Sueldo Líquido</span><span class="data-value">{fmt(st.session_state.sueldos["Alexander"])}</span></div>'
        html_alex += f'<div class="data-row"><span class="data-label">Asesorías</span><span class="data-value">{fmt(st.session_state.asesorias["Alexander"])}</span></div>'
        html_alex += f'<div class="total-row total-alexander"><span>Total Recibido</span><span>{fmt(total_alex)}</span></div>'
        html_alex += '</div>'
        st.markdown(html_alex, unsafe_allow_html=True)

    with col_ing_2:
        total_mar = st.session_state.sueldos["Mariana"] + st.session_state.asesorias["Mariana"]
        html_mar = '<div class="custom-card card-mariana">'
        html_mar += '<div class="card-title">Mariana</div>'
        html_mar += f'<div class="data-row"><span class="data-label">Sueldo Líquido</span><span class="data-value">{fmt(st.session_state.sueldos["Mariana"])}</span></div>'
        html_mar += f'<div class="data-row"><span class="data-label">Asesorías</span><span class="data-value">{fmt(st.session_state.asesorias["Mariana"])}</span></div>'
        html_mar += f'<div class="total-row total-mariana"><span>Total Recibido</span><span>{fmt(total_mar)}</span></div>'
        html_mar += '</div>'
        st.markdown(html_mar, unsafe_allow_html=True)

    # Total Hogar
    st.markdown(f"""
    <div class="custom-card" style="background-color: #f1f5f9; border-top: 5px solid #cbd5e1;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 18px; font-weight: bold; color: #334155;">Ingreso Total del Hogar</span>
            <span style="font-size: 24px; font-weight: bold; color: #0f172a;">{fmt(total_alex + total_mar)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- COMPROMISOS ---
    st.header("📌 Compromisos Pendientes")
    total_compromisos = sum(compromisos.values())
    html_comp = '<div class="custom-card" style="background-color: #ffffff; border-top: 5px solid #cbd5e1;">'
    for concepto, monto in compromisos.items():
        html_comp += f'<div class="data-row"><span class="data-label">{concepto}</span><span class="data-value" style="color: #dc2626;">{fmt(monto)}</span></div>'
    html_comp += f'<div class="total-row" style="color: #dc2626;"><span>Total Comprometido</span><span>{fmt(total_compromisos)}</span></div>'
    html_comp += '</div>'
    st.markdown(html_comp, unsafe_allow_html=True)

    st.divider()

    # --- LIBRE DISPOSICIÓN ---
    st.header("💸 Saldo de Libre Disposición")
    plata_libre_total = (total_alex + total_mar) - total_compromisos
    libre_alex = plata_libre_total // 2
    libre_mar = plata_libre_total - libre_alex

    col_libre_1, col_libre_2 = st.columns(2)
    with col_libre_1:
        st.markdown(f"""
        <div class="custom-card" style="background-color: #f0fdf4; border-left: 5px solid #16a34a;">
            <div class="card-title" style="color: #166534; border-bottom: none;">Disponible Total de Alexander</div>
            <div class="libre-value">{fmt(libre_alex)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_libre_2:
        st.markdown(f"""
        <div class="custom-card" style="background-color: #f0fdf4; border-left: 5px solid #16a34a;">
            <div class="card-title" style="color: #166534; border-bottom: none;">Disponible Total de Mariana</div>
            <div class="libre-value">{fmt(libre_mar)}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 2: HOJA 2 (BANCOS)
# ==========================================
with tab2:
    st.header("🏦 Bancos, Cuentas y Bolsillos")
    
    col_bancos_1, col_bancos_2 = st.columns(2)

    def render_bancos(persona, columna):
        with columna:
            st.subheader(f"Cuentas de {persona}")
            for cuenta in cuentas_bancos[persona]:
                total_cuenta = sum(b["Monto"] for b in cuenta["Bolsillos"])
                with st.expander(f"**{cuenta['Banco']}** - {cuenta['Cuenta']} (Total: {fmt(total_cuenta)})", expanded=False):
                    for b in cuenta["Bolsillos"]:
                        st.markdown(f"<div class='data-row'><span class='data-label'>↳ {b['Nombre']}</span><span class='data-value'>{fmt(b['Monto'])}</span></div>", unsafe_allow_html=True)

    render_bancos("Alexander", col_bancos_1)
    render_bancos("Mariana", col_bancos_2)

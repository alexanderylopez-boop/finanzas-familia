import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Finanzas Familiares", page_icon="💰", layout="wide")

# ---------- Utilidades ----------
def nombre_mes(d):
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    return f"{meses[d.month-1]} {d.year}"

def fmt(n):
    return f"${n:,.0f}".replace(",", ".")

# ---------- Base de Datos en Memoria ----------
if 'movimientos' not in st.session_state:
    # Datos de ejemplo iniciales
    st.session_state.movimientos = pd.DataFrame([
        {"Fecha":"2026-10-20","Concepto":"Supermercado","Monto":85000,"Pagó":"Alexander","Regla":"50/50","Categoría":"Supermercado","Estado":"Pagado"},
        {"Fecha":"2026-10-21","Concepto":"Colegio hijos","Monto":250000,"Pagó":"Alexander","Regla":"Proporcional","Categoría":"Colegio","Estado":"Pagado"},
        {"Fecha":"2026-10-22","Concepto":"Gas licuado 45 kg","Monto":65000,"Pagó":"Mariana","Regla":"50/50","Categoría":"Gas Licuado Hogar","Estado":"Pagado"},
        {"Fecha":"2026-10-23","Concepto":"Bencina vehículos","Monto":60000,"Pagó":"Alexander","Regla":"50/50","Categoría":"Combustible Vehículos","Estado":"Pagado"},
    ])

if 'ingresos' not in st.session_state:
    st.session_state.ingresos = pd.DataFrame([
        {"Persona":"Alexander","Sueldo":1746582},
        {"Persona":"Mariana","Sueldo":1958386},
    ])

if 'propiedades' not in st.session_state:
    st.session_state.propiedades = pd.DataFrame([
        {"Propiedad":"Casa 716","Dueño":"Alexander","Tipo arriendo":"Mensual","Dividendo":0},
        {"Propiedad":"Filipo","Dueño":"Alexander","Tipo arriendo":"Anual","Dividendo":0},
        {"Propiedad":"Los Diamelos","Dueño":"Alexander","Tipo arriendo":"Anual","Dividendo":0},
        {"Propiedad":"Capellán Florencio","Dueño":"Mariana","Tipo arriendo":"Diario","Dividendo":0},
    ])

# ---------- Motor de reparto ----------
def calcular_reparto(monto, regla, sueldo_a, sueldo_m):
    if regla == "100% Alexander": return monto, 0
    if regla == "100% Mariana": return 0, monto
    if regla == "50/50": return monto - (monto // 2), monto // 2
    if regla == "Proporcional":
        total = sueldo_a + sueldo_m
        if total == 0: return 0, 0
        parte_m = round(monto * sueldo_m / total)
        return monto - parte_m, parte_m
    return 0, 0

# ---------- Interfaz ----------
st.title("💰 Finanzas Familiares · Alexander & Mariana")

# Selector de mes (corregido para que empiece el 19)
meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
col1, col2, col3 = st.columns([1,2,1])
with col2:
    mes_sel = st.selectbox("Mes financiero (inicio el 19)", options=meses, index=22, format_func=lambda d: nombre_mes(d))

inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
# Ajuste visual del período 19 al 18
fin_visual = inicio + relativedelta(months=1) - timedelta(days=1)
st.caption(f"Período: **{inicio.strftime('%d/%m/%Y')}** → **{fin_visual.strftime('%d/%m/%Y')}**")

tabs = st.tabs(["🏠 Inicio","💵 Ingresos","📝 Movimientos","🔁 Deudas Internas","🏡 Propiedades"])

# --- Inicio ---
with tabs[0]:
    st.subheader("Resumen del mes")
    total_a = st.session_state.ingresos[st.session_state.ingresos.Persona=="Alexander"].Sueldo.sum()
    total_m = st.session_state.ingresos[st.session_state.ingresos.Persona=="Mariana"].Sueldo.sum()
    c1,c2,c3 = st.columns(3)
    c1.metric("Ingresos Alexander", fmt(total_a))
    c2.metric("Ingresos Mariana", fmt(total_m))
    c3.metric("Total hogar", fmt(total_a+total_m))

# --- Ingresos ---
with tabs[1]:
    st.subheader("Ingresos del mes financiero")
    for i, row in st.session_state.ingresos.iterrows():
        st.markdown(f"**{row['Persona']}** - Sueldo líquido: {fmt(row['Sueldo'])}")

# --- Movimientos ---
with tabs[2]:
    st.subheader("Registrar Nuevo Gasto")
    with st.form("nuevo_gasto"):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del gasto")
            concepto = st.text_input("Concepto (ej. Supermercado, Gas)")
            monto = st.number_input("Monto ($)", min_value=1, step=1000)
        with col2:
            pago = st.selectbox("¿Quién pagó?", ["Alexander", "Mariana"])
            regla = st.selectbox("Regla de reparto", ["50/50", "Proporcional", "100% Alexander", "100% Mariana"])
            cat = st.selectbox("Categoría", ["Supermercado", "Colegio", "Gas Licuado Hogar", "Combustible Vehículos", "Propiedades", "Otros"])
        
        submitted = st.form_submit_button("Guardar Gasto")
        if submitted:
            nuevo = pd.DataFrame([{"Fecha":fecha.strftime("%Y-%m-%d"),"Concepto":concepto,"Monto":monto,"Pagó":pago,"Regla":regla,"Categoría":cat,"Estado":"Pagado"}])
            st.session_state.movimientos = pd.concat([st.session_state.movimientos, nuevo], ignore_index=True)
            st.success("¡Gasto guardado!")
            st.rerun()

    st.divider()
    st.subheader("Historial de Movimientos")
    
    # Calcular reparto para mostrar
    sueldo_a = total_a
    sueldo_m = total_m
    df_mostrar = st.session_state.movimientos.copy()
    
    # Formatear montos para visualización
    df_mostrar["Monto"] = df_mostrar["Monto"].apply(fmt)
    
    st.dataframe(df_mostrar, use_container_width=True)

# --- Deudas ---
with tabs[3]:
    st.subheader("Deudas internas")
    debe_m = 0
    debe_a = 0
    for _, m in st.session_state.movimientos.iterrows():
        pa, pm = calcular_reparto(m["Monto"], m["Regla"], total_a, total_m)
        if m["Pagó"]=="Alexander": debe_m += pm
        elif m["Pagó"]=="Mariana": debe_a += pa
    
    c1,c2 = st.columns(2)
    c1.metric("Mariana debe a Alexander", fmt(debe_m))
    c2.metric("Alexander debe a Mariana", fmt(debe_a))
    neto = debe_m - debe_a
    if neto > 0: st.success(f"Transferencia: Mariana → Alexander  {fmt(neto)}")
    elif neto < 0: st.success(f"Transferencia: Alexander → Mariana  {fmt(-neto)}")
    else: st.info("No hay deudas pendientes.")

# --- Propiedades ---
with tabs[4]:
    st.subheader("Propiedades")
    st.dataframe(st.session_state.propiedades, use_container_width=True)

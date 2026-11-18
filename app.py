"""
App de Finanzas Familiares - Alexander & Mariana
Fase 1: Núcleo completo (mes financiero 19->18, repartos, saldos, propiedades)
"""
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Finanzas Familiares", page_icon="💰", layout="wide")

# ---------- Utilidades ----------
def mes_financiero_actual(hoy=None):
    hoy = hoy or date.today()
    if hoy.day >= 19:
        inicio = date(hoy.year, hoy.month, 19)
    else:
        prev = hoy - relativedelta(months=1)
        inicio = date(prev.year, prev.month, 19)
    fin = inicio + relativedelta(months=1) - timedelta(days=1)
    return inicio, fin

def nombre_mes(d):
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    return f"{meses[d.month-1]} {d.year}"

def fmt(n):
    return f"${n:,.0f}".replace(",", ".")

# ---------- Datos semilla (estructura octubre 2026) ----------
@st.cache_data
def cargar_datos_semilla():
    personas = ["Alexander", "Mariana"]
    ingresos = pd.DataFrame([
        {"Persona":"Alexander","Tipo":"Sueldo líquido","Monto":1746582},
        {"Persona":"Alexander","Tipo":"Sobresueldo","Monto":0},
        {"Persona":"Alexander","Tipo":"Trimestral","Monto":0},
        {"Persona":"Alexander","Tipo":"Otro","Monto":0},
        {"Persona":"Mariana","Tipo":"Sueldo líquido","Monto":1958386},
        {"Persona":"Mariana","Tipo":"Sobresueldo","Monto":0},
        {"Persona":"Mariana","Tipo":"Trimestral","Monto":0},
        {"Persona":"Mariana","Tipo":"Otro","Monto":0},
    ])
    cuentas = pd.DataFrame([
        {"Cuenta":"BCI Cuenta Corriente Alexander","Banco":"BCI","Tipo":"Cta. Cte.","Persona":"Alexander"},
        {"Cuenta":"BancoEstado Cuenta Corriente Alexander","Banco":"BancoEstado","Tipo":"Cta. Cte.","Persona":"Alexander"},
        {"Cuenta":"Scotiabank Cuenta Corriente Alexander","Banco":"Scotiabank","Tipo":"Cta. Cte.","Persona":"Alexander"},
        {"Cuenta":"Falabella Cuenta Corriente Alexander","Banco":"Falabella","Tipo":"Cta. Cte.","Persona":"Alexander"},
        {"Cuenta":"BancoEstado Cuenta Corriente Mariana","Banco":"BancoEstado","Tipo":"Cta. Cte.","Persona":"Mariana"},
        {"Cuenta":"Itaú Cuenta Corriente Mariana","Banco":"Itaú","Tipo":"Cta. Cte.","Persona":"Mariana"},
        {"Cuenta":"Falabella Cuenta Corriente Mariana","Banco":"Falabella","Tipo":"Cta. Cte.","Persona":"Mariana"},
        {"Cuenta":"Scotiabank Ahorro CLP Alexander","Banco":"Scotiabank","Tipo":"Ahorro","Persona":"Alexander"},
        {"Cuenta":"Scotiabank Ahorro USD Alexander","Banco":"Scotiabank","Tipo":"Ahorro","Persona":"Alexander"},
    ])
    bolsillos = pd.DataFrame([
        {"Cuenta":"BCI Cuenta Corriente Alexander","Bolsillo":"Sueldo","Monto":0},
        {"Cuenta":"BCI Cuenta Corriente Alexander","Bolsillo":"Compras Grandes","Monto":1000000},
        {"Cuenta":"BCI Cuenta Corriente Alexander","Bolsillo":"Garantía Los Diamelos","Monto":920000},
        {"Cuenta":"BCI Cuenta Corriente Alexander","Bolsillo":"Los Diamelos (arriendo + remanente)","Monto":867572},
        {"Cuenta":"BCI Cuenta Corriente Alexander","Bolsillo":"Por Distribuir","Monto":0},
        {"Cuenta":"BancoEstado Cuenta Corriente Alexander","Bolsillo":"Casa 716","Monto":400000},
        {"Cuenta":"BancoEstado Cuenta Corriente Alexander","Bolsillo":"Reserva dividendo Capellán","Monto":0},
        {"Cuenta":"BancoEstado Cuenta Corriente Alexander","Bolsillo":"Reserva dividendo Casa 716","Monto":0},
        {"Cuenta":"BancoEstado Cuenta Corriente Alexander","Bolsillo":"Propiedades","Monto":305000},
        {"Cuenta":"Scotiabank Cuenta Corriente Alexander","Bolsillo":"Combustible","Monto":0},
        {"Cuenta":"Scotiabank Cuenta Corriente Alexander","Bolsillo":"Generador","Monto":0},
        {"Cuenta":"Scotiabank Cuenta Corriente Alexander","Bolsillo":"Crédito","Monto":0},
        {"Cuenta":"Falabella Cuenta Corriente Alexander","Bolsillo":"Libre Disposición","Monto":0},
        {"Cuenta":"BancoEstado Cuenta Corriente Mariana","Bolsillo":"Hogar","Monto":19052},
        {"Cuenta":"BancoEstado Cuenta Corriente Mariana","Bolsillo":"Primer respaldo","Monto":19052},
        {"Cuenta":"Itaú Cuenta Corriente Mariana","Bolsillo":"Capellán","Monto":0},
        {"Cuenta":"Itaú Cuenta Corriente Mariana","Bolsillo":"Pagos","Monto":0},
        {"Cuenta":"Itaú Cuenta Corriente Mariana","Bolsillo":"Remanente","Monto":0},
        {"Cuenta":"Itaú Cuenta Corriente Mariana","Bolsillo":"Contingencia","Monto":0},
        {"Cuenta":"Falabella Cuenta Corriente Mariana","Bolsillo":"Libre Disposición","Monto":0},
    ])
    propiedades = pd.DataFrame([
        {"Propiedad":"Casa 716","Dueño":"Alexander","Tipo arriendo":"Mensual","Dividendo":0},
        {"Propiedad":"Filipo","Dueño":"Alexander","Tipo arriendo":"Anual","Dividendo":0},
        {"Propiedad":"Los Diamelos","Dueño":"Alexander","Tipo arriendo":"Anual","Dividendo":0},
        {"Propiedad":"Capellán Florencio","Dueño":"Mariana","Tipo arriendo":"Diario","Dividendo":0},
    ])
    movimientos = pd.DataFrame([
        {"Fecha":"2026-10-20","Concepto":"Supermercado","Monto":85000,"Pagó":"Alexander","Regla":"50/50","Categoría":"Supermercado","Estado":"Pagado"},
        {"Fecha":"2026-10-21","Concepto":"Colegio hijos","Monto":250000,"Pagó":"Alexander","Regla":"Proporcional","Categoría":"Colegio","Estado":"Pagado"},
        {"Fecha":"2026-10-22","Concepto":"Gas licuado 45 kg","Monto":65000,"Pagó":"Mariana","Regla":"50/50","Categoría":"Gas Licuado Hogar","Estado":"Pagado"},
        {"Fecha":"2026-10-23","Concepto":"Bencina vehículos","Monto":60000,"Pagó":"Alexander","Regla":"50/50","Categoría":"Combustible Vehículos","Estado":"Pagado"},
        {"Fecha":"2026-10-25","Concepto":"Delivery","Monto":25000,"Pagó":"Mariana","Regla":"50/50","Categoría":"Delivery","Estado":"Pagado"},
        {"Fecha":"2026-10-26","Concepto":"Regalo cumpleaños","Monto":40000,"Pagó":"Alexander","Regla":"100% Alexander","Categoría":"Regalos","Estado":"Pagado"},
        {"Fecha":"2026-10-27","Concepto":"Arriendo Los Diamelos","Monto":600000,"Pagó":"Alexander","Regla":"100% Alexander","Categoría":"Propiedades","Estado":"Pagado"},
        {"Fecha":"2026-10-28","Concepto":"Reserva estadía Capellán (50%)","Monto":100000,"Pagó":"Huésped","Regla":"100% Mariana","Categoría":"Propiedades","Estado":"Pagado"},
        {"Fecha":"2026-10-29","Concepto":"Dividendo Casa 716","Monto":400000,"Pagó":"Alexander","Regla":"100% Alexander","Categoría":"Propiedades","Estado":"Pendiente"},
    ])
    return personas, ingresos, cuentas, bolsillos, propiedades, movimientos

# ---------- Motor de reparto ----------
def calcular_reparto(mov, sueldo_a, sueldo_m):
    monto = mov["Monto"]
    regla = mov["Regla"]
    if regla == "100% Alexander":
        return monto, 0
    if regla == "100% Mariana":
        return 0, monto
    if regla == "50/50":
        parte_m = monto // 2
        return monto - parte_m, parte_m
    if regla == "Proporcional":
        total = sueldo_a + sueldo_m
        if total == 0:
            return 0, 0
        parte_m = round(monto * sueldo_m / total)
        return monto - parte_m, parte_m
    if regla == "Montos Definidos":
        return monto, 0
    return 0, 0

# ---------- UI ----------
st.title("💰 Finanzas Familiares · Alexander & Mariana")
personas, ingresos, cuentas, bolsillos, propiedades, movimientos = cargar_datos_semilla()

# Selector de mes financiero
hoy = date.today()
inicio_def, fin_def = mes_financiero_actual(hoy)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
    mes_sel = st.selectbox("Mes financiero (inicio el 19)", options=meses,
                           index=len(meses)-1, format_func=lambda d: nombre_mes(d))
inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
st.caption(f"Período: **{inicio.strftime('%d/%m/%Y')}** → **{fin.strftime('%d/%m/%Y')}**")

tabs = st.tabs(["🏠 Inicio","💵 Ingresos","🏦 Cuentas y Bolsillos","📝 Movimientos",
                "🔁 Deudas Internas","💸 Libre Disposición","📌 Compromisos",
                "🏡 Propiedades","⚠️ Alertas"])

# --- Inicio ---
with tabs[0]:
    st.subheader("Resumen del mes")
    total_a = ingresos[ingresos.Persona=="Alexander"].Monto.sum()
    total_m = ingresos[ingresos.Persona=="Mariana"].Monto.sum()
    c1,c2,c3 = st.columns(3)
    c1.metric("Ingresos Alexander", fmt(total_a))
    c2.metric("Ingresos Mariana", fmt(total_m))
    c3.metric("Total hogar", fmt(total_a+total_m))
    st.info("Usa las pestañas para navegar. Los cálculos de reparto se actualizan automáticamente.")

# --- Ingresos ---
with tabs[1]:
    st.subheader("Ingresos del mes financiero")
    for p in personas:
        st.markdown(f"**{p}**")
        df = ingresos[ingresos.Persona==p].copy()
        df["Monto"] = df["Monto"].apply(fmt)
        st.table(df[["Tipo","Monto"]])
        st.markdown(f"Total {p}: **{fmt(ingresos[ingresos.Persona==p].Monto.sum())}**")

# --- Cuentas y Bolsillos ---
with tabs[2]:
    st.subheader("Cuentas reales y bolsillos")
    for p in personas:
        st.markdown(f"### {p}")
        for _, c in cuentas[cuentas.Persona==p].iterrows():
            with st.expander(f"{c['Cuenta']}"):
                b = bolsillos[bolsillos.Cuenta==c["Cuenta"]].copy()
                if b.empty:
                    st.write("Sin bolsillos registrados.")
                else:
                    b["Monto"] = b["Monto"].apply(fmt)
                    st.table(b[["Bolsillo","Monto"]])
                    st.markdown(f"**Total cuenta:** {fmt(bolsillos[bolsillos.Cuenta==c['Cuenta']].Monto.sum())}")

# --- Movimientos ---
with tabs[3]:
    st.subheader("Movimientos del mes")
    sueldo_a = ingresos[(ingresos.Persona=="Alexander")&(ingresos.Tipo=="Sueldo líquido")].Monto.sum()
    sueldo_m = ingresos[(ingresos.Persona=="Mariana")&(ingresos.Tipo=="Sueldo líquido")].Monto.sum()
    rows = []
    for _, m in movimientos.iterrows():
        pa, pm = calcular_reparto(m, sueldo_a, sueldo_m)
        rows.append({**m, "Parte Alexander":fmt(pa), "Parte Mariana":fmt(pm)})
    df = pd.DataFrame(rows)
    df["Monto"] = df["Monto"].apply(fmt)
    st.dataframe(df[["Fecha","Concepto","Monto","Pagó","Regla","Categoría","Parte Alexander","Parte Mariana","Estado"]], use_container_width=True)

# --- Deudas Internas ---
with tabs[4]:
    st.subheader("Deudas internas y orden compensable")
    sueldo_a = ingresos[(ingresos.Persona=="Alexander")&(ingresos.Tipo=="Sueldo líquido")].Monto.sum()
    sueldo_m = ingresos[(ingresos.Persona=="Mariana")&(ingresos.Tipo=="Sueldo líquido")].Monto.sum()
    debe_m = 0; debe_a = 0
    for _, m in movimientos[movimientos.Estado=="Pagado"].iterrows():
        pa, pm = calcular_reparto(m, sueldo_a, sueldo_m)
        if m["Pagó"]=="Alexander":
            debe_m += pm
        elif m["Pagó"]=="Mariana":
            debe_a += pa
    c1,c2 = st.columns(2)
    c1.metric("Mariana debe a Alexander", fmt(debe_m))
    c2.metric("Alexander debe a Mariana", fmt(debe_a))
    neto = debe_m - debe_a
    if neto > 0:
        st.success(f"**Transferencia para saldar: Mariana → Alexander  {fmt(neto)}**")
    elif neto < 0:
        st.success(f"**Transferencia para saldar: Alexander → Mariana  {fmt(-neto)}**")
    else:
        st.info("No hay deudas internas pendientes.")

# --- Libre Disposición ---
with tabs[5]:
    st.subheader("Saldo de libre disposición (va a Falabella Libre)")
    st.caption("Se calcula después de pagar todos los compromisos y apartar ahorros/fondos.")
    for p in personas:
        libre = bolsillos[(bolsillos.Cuenta.str.contains("Falabella"))&(bolsillos.Cuenta.str.contains(p))&(bolsillos.Bolsillo=="Libre Disposición")].Monto.sum()
        st.metric(f"Libre disposición {p}", fmt(libre))
    st.info("En Fase 1, este saldo se calcula a partir de los bolsillos 'Libre Disposición'. En Fase 2 se calculará automáticamente restando compromisos y reservas.")

# --- Compromisos ---
with tabs[6]:
    st.subheader("Compromisos pendientes")
    pend = movimientos[movimientos.Estado=="Pendiente"]
    if pend.empty:
        st.info("No hay compromisos pendientes.")
    else:
        for _, m in pend.iterrows():
            st.warning(f"{m['Fecha']} · {m['Concepto']} · {fmt(m['Monto'])} · Pagó {m['Pagó']}")

# --- Propiedades ---
with tabs[7]:
    st.subheader("Propiedades")
    for _, pr in propiedades.iterrows():
        with st.expander(f"{pr['Propiedad']} — dueño: {pr['Dueño']} — arriendo {pr['Tipo arriendo']}"):
            st.write(f"**Dividendo:** {fmt(pr['Dividendo'])}")
            st.write("**Garantía:** se registra por arrendatario (Fase 2)")
            st.write("**Reserva de fondos:** se registra por propiedad (Fase 2)")
            if pr["Tipo arriendo"]=="Diario":
                st.write("**Reserva de estadía:** abono 50% + 50% al check-in")
                st.write("**Calendario de noches:** disponible en Fase 2")
            st.write("**Ingresos/gastos:** van 100% al dueño")

# --- Alertas ---
with tabs[8]:
    st.subheader("Alertas de control")
    st.write("**Fase 1 activas:**")
    st.write("- Compromisos pendientes (ver pestaña Compromisos)")
    st.write("- Movimientos sin categoría o sin regla")
    st.write("**Fase 2:** pago duplicado, revisar conciliación, dividendo por vencer, garantía por devolver, saldo de estadía pendiente.")

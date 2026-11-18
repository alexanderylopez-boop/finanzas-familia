import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import io

st.set_page_config(page_title="Finanzas Familiares", page_icon="💰", layout="wide")

# ---------- Utilidades ----------
def nombre_mes(d):
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    return f"{meses[d.month-1]} {d.year}"

def fmt(n):
    if pd.isna(n): return "$0"
    return f"${n:,.0f}".replace(",", ".")

# ---------- Datos Reales Extraídos ----------
@st.cache_data
def cargar_datos():
    movimientos_csv = """Fecha,Concepto,Monto,Quien_pago,Regla_de_reparto
,Movistar Móvil,11172,Alexander,100% Alexander
,Bencina Mariana,174675,Mariana,Montos Definidos
,Bencina Alexander,150000,Alexander,Montos Definidos
,WOM Móvil,7596,Mariana,100% Mariana
,Mensualidad Isabela,90000,Alexander,100% Alexander
,Autopistas Mariana,44254,Mariana,100% Mariana
,Dobby,42990,Alexander,100% Alexander
,Seguro oncológico BCI,10215,Alexander,100% Alexander
,Ahorro Para Niños,30000,Mariana,Montos Definidos
,Comisión cuenta corriente BCI,4934,Alexander,100% Alexander
,Entel Móvil Ignacio,12990,Mariana,100% Mariana
,Autopistas Alexander,6349,Alexander,100% Alexander
,Deuda Carola Por Seguro,79950,Mariana,100% Mariana
,PlayStation Plus Felipe,9715,Alexander,100% Alexander
,Fondo Mensual de Hogar,343579,Mariana,Montos Definidos
,Contribuciones Trimestrales,111658,Mariana,100% Mariana
,Fondo Mensual de Hogar,306421,Alexander,Montos Definidos
,Mantención motocicleta,434000,Alexander,100% Alexander
,Ahorro Para Niños,30000,Alexander,Montos Definidos
,Cumpleaños Mamá,72427,Alexander,100% Alexander
,Aporte a reserva Capellán desde sueldo,400000,Mariana,Montos Definidos
,Movistar Hogar,36250,Alexander,Proporcional
,Luz,123523,Mariana,Proporcional
,VTR Hogar,25990,Alexander,Proporcional
,Agua,22100,Mariana,Proporcional
,Entel Móvil Niños,39960,Alexander,Proporcional
,Ticket Gas 45 kg,68000,Mariana,Proporcional
,Gas 45 kg,89300,Alexander,Proporcional
,Mensualidad Maite,71000,Mariana,Proporcional
,Mensualidad Felipe,71000,Mariana,Proporcional
,Mensualidad Tomy,71000,Mariana,Proporcional
,Nieves,260000,Mariana,Proporcional
,Otros gastos colegio,23500,Mariana,50/50
,Devolucion y pago de Licencia,89424,Mariana,50/50
,Spotify,8250,Mariana,50/50
,Entel Movil Radio Auto,12990,Mariana,50/50
,Cumpleaños Tomas,162000,Mariana,50/50
,CMR Elite · Tecnomas.cl,36996,Alexander,50/50
,CMR · CMR · resumen del estado,6670,Mariana,100% Mariana
,CMR Elite · OpenAI,19990,Alexander,50/50
,CMR Elite · OpenAI Chat,22015,Alexander,50/50
,CMR Elite · Apple.com/bi,3290,Alexander,100% Alexander
,CMR Elite · Desgravamen CMR,987,Alexander,100% Alexander
,CMR Elite · Administración CMR,14395,Alexander,100% Alexander
,CMR Elite · Netflix,12990,Alexander,50/50
,Ripley · TV dormitorio principal,90005,Alexander,50/50
,Ripley · Administración Ripley,5064,Alexander,50/50
,Ripley · Desgravamen Ripley,1076,Alexander,50/50
,Isapre de Alexander pagada por Mariana,93206,Mariana,100% Alexander
2026-11-10,Dividendo Capellán Florencio,387123,Mariana,No registrada
2026-11-02,Dividendo Casa 716 (arriendo anual),363772,Alexander,No registrada
2026-10-26,Dividendo Los Diamelos,372424,Alexander,No registrada
,Dividendo Filipo,84969,Alexander,No registrada"""
    
    df = pd.read_csv(io.StringIO(movimientos_csv))
    # Llenar fechas vacías con el mes de octubre para el filtro
    df['Fecha'] = df['Fecha'].fillna('2026-10-19') 
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

df_movimientos = cargar_datos()

# Datos base
sueldos = {"Alexander": 1746582, "Mariana": 1958386}
cuentas_data = [
    {"Titular":"Alexander","Banco":"BCI","Cuenta":"Cta. Cte. Alexander","Saldo":4534154},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Cta. Cte. Alexander","Saldo":705000},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Cuenta RUT Alexander","Saldo":250000},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Cuenta Vista Alexander","Saldo":500000},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Ahorro Premium Alexander","Saldo":3143103},
    {"Titular":"Alexander","Banco":"Scotiabank","Cuenta":"Cta. Cte. Alexander","Saldo":625325},
    {"Titular":"Alexander","Banco":"Scotiabank","Cuenta":"Ahorro CLP Alexander","Saldo":50161},
    {"Titular":"Alexander","Banco":"Scotiabank","Cuenta":"Ahorro USD Alexander","Saldo":20},
    {"Titular":"Alexander","Banco":"Falabella","Cuenta":"Cta. Cte. Alexander","Saldo":183550},
    {"Titular":"Alexander","Banco":"MACH BCI","Cuenta":"Prepago Alexander","Saldo":4341},
    {"Titular":"Mariana","Banco":"Itaú","Cuenta":"Cta. Cte. Mariana","Saldo":1958386},
    {"Titular":"Mariana","Banco":"BancoEstado","Cuenta":"Cta. Cte. Mariana","Saldo":0},
    {"Titular":"Mariana","Banco":"BancoEstado","Cuenta":"Cuenta RUT Mariana","Saldo":19052},
    {"Titular":"Mariana","Banco":"BancoEstado","Cuenta":"Ahorro Giro Diferido Mariana","Saldo":22},
    {"Titular":"Mariana","Banco":"BancoEstado","Cuenta":"Fondo Mutuo Mariana","Saldo":5175257},
    {"Titular":"Mariana","Banco":"Falabella","Cuenta":"Cta. Cte. Mariana","Saldo":80},
]

# ---------- Motor de reparto ----------
def calcular_reparto(monto, regla, sueldo_a, sueldo_m):
    if pd.isna(monto): return 0, 0
    if regla == "100% Alexander": return monto, 0
    if regla == "100% Mariana": return 0, monto
    if regla == "50/50": return monto - (monto // 2), monto // 2
    if regla == "Proporcional":
        total = sueldo_a + sueldo_m
        if total == 0: return 0, 0
        parte_m = round(monto * sueldo_m / total)
        return monto - parte_m, parte_m
    if regla == "Montos Definidos": return monto, 0 # Simplificación temporal
    return monto, 0 # Por defecto a Alexander si no hay regla clara

# ---------- Interfaz ----------
st.title("💰 Finanzas Familiares · Alexander & Mariana")

# Selector de mes (Ciclo 19 al 18)
meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
col1, col2, col3 = st.columns([1,2,1])
with col2:
    mes_sel = st.selectbox("Mes financiero (inicio el 19)", options=meses, index=22, format_func=lambda d: nombre_mes(d))

inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
# Mostrar el período real 19 al 18
st.caption(f"Período: **{inicio.strftime('%d/%m/%Y')}** → **{fin.strftime('%d/%m/%Y')}**")

tabs = st.tabs(["🏠 Inicio", "💵 Ingresos", "🏦 Cuentas", "📝 Movimientos", "🔁 Deudas Internas", "🏡 Propiedades"])

# --- Inicio ---
with tabs[0]:
    st.subheader("Resumen del mes")
    c1,c2,c3 = st.columns(3)
    c1.metric("Ingresos Alexander", fmt(sueldos["Alexander"]))
    c2.metric("Ingresos Mariana", fmt(sueldos["Mariana"]))
    c3.metric("Total hogar", fmt(sueldos["Alexander"]+sueldos["Mariana"]))
    st.info("Usa las pestañas para navegar. Los cálculos se basan en los datos reales extraídos de tu Excel.")

# --- Ingresos ---
with tabs[1]:
    st.subheader("Ingresos del mes financiero")
    st.write(f"**Alexander** - Sueldo líquido: {fmt(sueldos['Alexander'])}")
    st.write(f"**Mariana** - Sueldo líquido: {fmt(sueldos['Mariana'])}")

# --- Cuentas ---
with tabs[2]:
    st.subheader("Saldos de Cuentas y Fondos")
    df_cuentas = pd.DataFrame(cuentas_data)
    df_cuentas["Saldo"] = df_cuentas["Saldo"].apply(fmt)
    st.table(df_cuentas)

# --- Movimientos ---
with tabs[3]:
    st.subheader("Historial de Movimientos (Datos Reales)")
    df_mostrar = df_movimientos.copy()
    df_mostrar["Fecha"] = df_mostrar["Fecha"].dt.strftime('%d/%m/%Y')
    df_mostrar["Monto"] = df_mostrar["Monto"].apply(fmt)
    st.dataframe(df_mostrar[["Fecha", "Concepto", "Monto", "Quien_pago", "Regla_de_reparto"]], use_container_width=True)

# --- Deudas ---
with tabs[4]:
    st.subheader("Deudas internas y compensación")
    debe_m = 0
    debe_a = 0
    for _, m in df_movimientos.iterrows():
        pa, pm = calcular_reparto(m["Monto"], m["Regla_de_reparto"], sueldos["Alexander"], sueldos["Mariana"])
        if m["Quien_pago"] == "Alexander": debe_m += pm
        elif m["Quien_pago"] == "Mariana": debe_a += pa
    
    c1,c2 = st.columns(2)
    c1.metric("Mariana debe a Alexander", fmt(debe_m))
    c2.metric("Alexander debe a Mariana", fmt(debe_a))
    neto = debe_m - debe_a
    if neto > 0: st.success(f"**Transferencia para saldar: Mariana → Alexander  {fmt(neto)}**")
    elif neto < 0: st.success(f"**Transferencia para saldar: Alexander → Mariana  {fmt(-neto)}**")
    else: st.info("No hay deudas pendientes.")

# --- Propiedades ---
with tabs[5]:
    st.subheader("Propiedades")
    props = [
        {"Propiedad": "Capellán Florencio", "Dueño": "Mariana", "Tipo": "Vivienda propia; sin arriendo"},
        {"Propiedad": "Casa 716", "Dueño": "Alexander", "Tipo": "Anual y por noche"},
        {"Propiedad": "Filipo", "Dueño": "Alexander", "Tipo": "Mensual; fondo compartido con Casa 716"},
        {"Propiedad": "Los Diamelos", "Dueño": "Alexander", "Tipo": "Mensual"},
    ]
    st.table(pd.DataFrame(props))

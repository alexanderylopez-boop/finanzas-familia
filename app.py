import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import io
import plotly.express as px

st.set_page_config(page_title="Finanzas Alexander & Mariana", page_icon="💰", layout="wide")

# ---------- Estilos CSS para que se vea moderno ----------
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 10px 16px; }
    .stTabs [aria-selected="true"] { background-color: #e0e5ec; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ---------- Utilidades ----------
def nombre_mes(d):
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    return f"{meses[d.month-1]} {d.year}"

def fmt(n):
    if pd.isna(n) or n == 0: return "$0"
    return f"${n:,.0f}".replace(",", ".")

# ---------- Carga de Datos Reales ----------
@st.cache_data
def cargar_datos():
    movimientos_csv = """Fecha,Concepto,Monto,Quien_pago,Regla_de_reparto,Categoria,Tipo
2026-10-19,Movistar Móvil,11172,Alexander,100% Alexander,Telefonía,Obligación
2026-10-19,Bencina Mariana,174675,Mariana,Montos Definidos,Combustible,Gasto Variable
2026-10-19,Bencina Alexander,150000,Alexander,Montos Definidos,Combustible,Gasto Variable
2026-10-19,WOM Móvil,7596,Mariana,100% Mariana,Telefonía,Obligación
2026-10-19,Mensualidad Isabela,90000,Alexander,100% Alexander,Colegio,Obligación
2026-10-19,Autopistas Mariana,44254,Mariana,100% Mariana,Transporte,Obligación
2026-10-19,Dobby,42990,Alexander,100% Alexander,Mascotas,Obligación
2026-10-19,Seguro oncológico BCI,10215,Alexander,100% Alexander,Salud,Obligación
2026-10-19,Ahorro Para Niños,30000,Mariana,Montos Definidos,Ahorro,Aporte
2026-10-19,Comisión cuenta corriente BCI,4934,Alexander,100% Alexander,Banco,Obligación
2026-10-19,Entel Móvil Ignacio,12990,Mariana,100% Mariana,Telefonía,Obligación
2026-10-19,Autopistas Alexander,6349,Alexander,100% Alexander,Transporte,Obligación
2026-10-19,Deuda Carola Por Seguro,79950,Mariana,100% Mariana,Deuda,Obligación
2026-10-19,PlayStation Plus Felipe,9715,Alexander,100% Alexander,Suscripciones,Obligación
2026-10-19,Fondo Mensual de Hogar,343579,Mariana,Montos Definidos,Hogar,Aporte
2026-10-19,Contribuciones Trimestrales,111658,Mariana,100% Mariana,Impuestos,Obligación
2026-10-19,Fondo Mensual de Hogar,306421,Alexander,Montos Definidos,Hogar,Aporte
2026-10-19,Mantención motocicleta,434000,Alexander,100% Alexander,Transporte,Obligación
2026-10-19,Ahorro Para Niños,30000,Alexander,Montos Definidos,Ahorro,Aporte
2026-10-19,Cumpleaños Mamá,72427,Alexander,100% Alexander,Regalos,Obligación
2026-10-19,Aporte a reserva Capellán,400000,Mariana,Montos Definidos,Propiedades,Aporte
2026-10-19,Movistar Hogar,36250,Alexander,Proporcional,Servicios Básicos,Gasto Variable
2026-10-19,Luz,123523,Mariana,Proporcional,Servicios Básicos,Gasto Variable
2026-10-19,VTR Hogar,25990,Alexander,Proporcional,Servicios Básicos,Gasto Variable
2026-10-19,Agua,22100,Mariana,Proporcional,Servicios Básicos,Gasto Variable
2026-10-19,Entel Móvil Niños,39960,Alexander,Proporcional,Telefonía,Gasto Variable
2026-10-19,Ticket Gas 45 kg,68000,Mariana,Proporcional,Gas Licuado Hogar,Gasto Variable
2026-10-19,Gas 45 kg,89300,Alexander,Proporcional,Gas Licuado Hogar,Gasto Variable
2026-10-19,Mensualidad Maite,71000,Mariana,Proporcional,Colegio,Gasto Variable
2026-10-19,Mensualidad Felipe,71000,Mariana,Proporcional,Colegio,Gasto Variable
2026-10-19,Mensualidad Tomy,71000,Mariana,Proporcional,Colegio,Gasto Variable
2026-10-19,Nieves,260000,Mariana,Proporcional,Colegio,Gasto Variable
2026-10-19,Otros gastos colegio,23500,Mariana,50/50,Colegio,Gasto Variable
2026-10-19,Devolucion y pago de Licencia,89424,Mariana,50/50,Transporte,Gasto Variable
2026-10-19,Spotify,8250,Mariana,50/50,Suscripciones,Gasto Variable
2026-10-19,Entel Movil Radio Auto,12990,Mariana,50/50,Telefonía,Gasto Variable
2026-10-19,Cumpleaños Tomas,162000,Mariana,50/50,Regalos,Gasto Variable
2026-10-19,CMR Elite · Tecnomas.cl,36996,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,CMR · CMR · resumen del estado,6670,Mariana,100% Mariana,Tarjeta de Crédito,Cuota
2026-10-19,CMR Elite · OpenAI,19990,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,CMR Elite · OpenAI Chat,22015,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,CMR Elite · Apple.com/bi,3290,Alexander,100% Alexander,Tarjeta de Crédito,Cuota
2026-10-19,CMR Elite · Desgravamen CMR,987,Alexander,100% Alexander,Tarjeta de Crédito,Cuota
2026-10-19,CMR Elite · Administración CMR,14395,Alexander,100% Alexander,Tarjeta de Crédito,Cuota
2026-10-19,CMR Elite · Netflix,12990,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,Ripley · TV dormitorio principal,90005,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,Ripley · Administración Ripley,5064,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,Ripley · Desgravamen Ripley,1076,Alexander,50/50,Tarjeta de Crédito,Cuota
2026-10-19,Isapre de Alexander pagada por Mariana,93206,Mariana,100% Alexander,Salud,Pago Cruzado
2026-11-10,Dividendo Capellán Florencio,387123,Mariana,No registrada,Propiedades,Dividendo
2026-11-02,Dividendo Casa 716 (anual),363772,Alexander,No registrada,Propiedades,Dividendo
2026-10-26,Dividendo Los Diamelos,372424,Alexander,No registrada,Propiedades,Dividendo
2026-10-19,Dividendo Filipo,84969,Alexander,No registrada,Propiedades,Dividendo"""
    
    df = pd.read_csv(io.StringIO(movimientos_csv))
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

df_movimientos = cargar_datos()

sueldos = {"Alexander": 1746582, "Mariana": 1958386}
cuentas_data = [
    {"Titular":"Alexander","Banco":"BCI","Cuenta":"Cta. Cte. Alexander","Saldo":4534154},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Cta. Cte. Alexander","Saldo":705000},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Cuenta RUT Alexander","Saldo":250000},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Cuenta Vista Alexander","Saldo":500000},
    {"Titular":"Alexander","Banco":"BancoEstado","Cuenta":"Ahorro Premium Alexander","Saldo":3143103},
    {"Titular":"Alexander","Banco":"Scotiabank","Cuenta":"Cta. Cte. Alexander","Saldo":625325},
    {"Titular":"Alexander","Banco":"Falabella","Cuenta":"Cta. Cte. Alexander","Saldo":183550},
    {"Titular":"Mariana","Banco":"Itaú","Cuenta":"Cta. Cte. Mariana","Saldo":1958386},
    {"Titular":"Mariana","Banco":"BancoEstado","Cuenta":"Cta. Cte. Mariana","Saldo":0},
    {"Titular":"Mariana","Banco":"BancoEstado","Cuenta":"Cuenta RUT Mariana","Saldo":19052},
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
    if regla == "Montos Definidos": return monto, 0 
    return monto, 0 

# ---------- INTERFAZ GRÁFICA ----------
st.title("💰 Panel de Finanzas Familiares")

# Selector de mes (Ciclo 19 al 18)
meses = pd.date_range("2025-01-19", "2027-12-19", freq="MS").date
col_sel, _ = st.columns([1, 2])
with col_sel:
    mes_sel = st.selectbox("Mes financiero", options=meses, index=22, format_func=lambda d: nombre_mes(d))

inicio = mes_sel
fin = inicio + relativedelta(months=1) - timedelta(days=1)
st.info(f"📅 **Período en curso:** {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")

tabs = st.tabs(["📊 Resumen", "🏦 Cuentas y Fondos", "📝 Movimientos", "🔁 Deudas", "🏡 Propiedades"])

# --- TAB 1: RESUMEN ---
with tabs[0]:
    st.subheader("Flujo del Mes")
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingreso Alexander", fmt(sueldos["Alexander"]))
    c2.metric("Ingreso Mariana", fmt(sueldos["Mariana"]))
    c3.metric("Ingreso Total Hogar", fmt(sueldos["Alexander"]+sueldos["Mariana"]), delta="Sueldos Líquidos")
    
    st.divider()
    
    st.subheader("Gastos por Categoría")
    df_gastos = df_movimientos[df_movimientos['Tipo'] != 'Aporte']
    df_agrupado = df_gastos.groupby('Categoria')['Monto'].sum().reset_index()
    fig = px.pie(df_agrupado, values='Monto', names='Categoria', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: CUENTAS ---
with tabs[1]:
    st.subheader("Saldos por Banco y Fondo")
    for titular in ["Alexander", "Mariana"]:
        st.markdown(f"### 👤 Cuentas de {titular}")
        df_t = pd.DataFrame([c for c in cuentas_data if c["Titular"] == titular])
        for _, row in df_t.iterrows():
            with st.expander(f"🏦 **{row['Banco']}** - {row['Cuenta']} (Saldo: {fmt(row['Saldo'])})"):
                st.write("Aquí se detallarán los fondos específicos de esta cuenta en la próxima actualización.")

# --- TAB 3: MOVIMIENTOS ---
with tabs[2]:
    st.subheader("Detalle de Movimientos")
    
    # Filtro visual
    tipo_filtro = st.radio("Filtrar por tipo:", ["Todos", "Gastos Corrientes", "Tarjetas de Crédito", "Dividendos Propiedades"], horizontal=True)
    
    df_mostrar = df_movimientos.copy()
    if tipo_filtro == "Gastos Corrientes":
        df_mostrar = df_mostrar[df_mostrar['Tipo'].isin(['Obligación', 'Gasto Variable'])]
    elif tipo_filtro == "Tarjetas de Crédito":
        df_mostrar = df_mostrar[df_mostrar['Tipo'] == 'Cuota']
    elif tipo_filtro == "Dividendos Propiedades":
        df_mostrar = df_mostrar[df_mostrar['Tipo'] == 'Dividendo']

    # Formatear para mostrar
    df_mostrar["Fecha"] = df_mostrar["Fecha"].dt.strftime('%d/%m/%Y')
    df_mostrar["Monto"] = df_mostrar["Monto"].apply(fmt)
    
    # Ocultar columnas innecesarias
    st.dataframe(df_mostrar[["Fecha", "Concepto", "Monto", "Quien_pago", "Regla_de_reparto", "Categoria"]], use_container_width=True, hide_index=True)

# --- TAB 4: DEUDAS ---
with tabs[3]:
    st.subheader("Balance y Compensación entre Ustedes")
    st.write("Este cálculo suma automáticamente quién pagó qué, aplicando las reglas (50/50, proporcional, etc.).")
    
    debe_m = 0
    debe_a = 0
    for _, m in df_movimientos.iterrows():
        pa, pm = calcular_reparto(m["Monto"], m["Regla_de_reparto"], sueldos["Alexander"], sueldos["Mariana"])
        if m["Quien_pago"] == "Alexander": debe_m += pm
        elif m["Quien_pago"] == "Mariana": debe_a += pa
    
    neto = debe_m - debe_a
    
    c1, c2 = st.columns(2)
    c1.error(f"**Mariana debe a Alexander:** {fmt(debe_m)}")
    c2.error(f"**Alexander debe a Mariana:** {fmt(debe_a)}")
    
    st.divider()
    if neto > 0:
        st.success(f"### 💸 Transferencia final: Mariana le transfiere a Alexander {fmt(neto)}")
    elif neto < 0:
        st.success(f"### 💸 Transferencia final: Alexander le transfiere a Mariana {fmt(-neto)}")
    else:
        st.info("¡Están a mano! No hay deudas cruzadas pendientes este mes.")

# --- TAB 5: PROPIEDADES ---
with tabs[4]:
    st.subheader("Resumen de Propiedades")
    props = [
        {"Propiedad": "Capellán Florencio", "Dueño": "Mariana", "Arriendo": "Vivienda propia (Sin arriendo)", "Dividendo": "$387.123"},
        {"Propiedad": "Casa 716", "Dueño": "Alexander", "Arriendo": "Anual y por noche", "Dividendo": "$363.772"},
        {"Propiedad": "Filipo", "Dueño": "Alexander", "Arriendo": "Mensual (Fondo compartido)", "Dividendo": "$84.969"},
        {"Propiedad": "Los Diamelos", "Dueño": "Alexander", "Arriendo": "Mensual", "Dividendo": "$372.424"},
    ]
    st.table(pd.DataFrame(props))

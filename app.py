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

# --- 1. MEMORIA DE DATOS (Inicialización) ---
if 'datos_ingresos' not in st.session_state:
    st.session_state.datos_ingresos = {}

if 'datos_cuentas' not in st.session_state:
    # CORRECCIÓN DE ESTRUCTURA: Datos de cuentas indexados directamente por persona
    st.session_state.datos_cuentas = {
        "Alexander": {
            "BCI": {
                "Cta. Cte.": {"Saldo sin asignar": 1746582, "Compras grandes familiares": 1000000, "Garantía Los Diamelos": 920000, "Fondo propio Los Diamelos": 867572}
            },
            "BancoEstado": {
                "Cta. Cte.": {"Fondo común Casa 716 / Filipo": 305000, "Reserva dividendo Casa 716": 400000},
                "Cuenta RUT": {"Primer respaldo de Alexander": 250000},
                "Cuenta Vista": {"Segundo respaldo de Alexander": 500000},
                "Ahorro Premium": {"Ahorro personal Premium": 3143103}
            },
            "Scotiabank": {
                "Cta. Cte.": {"Fondo de combustible": 75325, "Reserva para generador": 550000},
                "Ahorro CLP": {"Vacaciones en Chile": 50161}
            },
            "Falabella": {
                "Cta. Cte.": {"Libre disposición de Alexander": 183550}
            }
        },
        "Mariana": {
            "Itaú": {
                "Cta. Cte.": {"Saldo sin asignar": 1958386, "Fondo Capellán y reparaciones": 0}
            },
            "BancoEstado": {
                "Cta. Cte.": {"Presupuesto mensual de hogar": 0},
                "Cuenta RUT": {"Primer respaldo de Mariana": 19052},
                "Ahorro Giro Diferido": {"Segundo respaldo de Mariana": 22},
                "Fondo Mutuo": {"Ahorro para estudios de los niños": 5175257}
            },
            "Falabella": {
                "Cta. Cte.": {"Libre disposición de Mariana": 80}
            }
        }
    }

# Memoria del mes: Guardamos la fecha exacta (año y mes) en lugar de solo un índice
if 'mes_actual' not in st.session_state:
    st.session_state.mes_actual = date(2026, 11, 19) # Noviembre 2026 por defecto

# --- INTERFAZ GRÁFICA ---
st.title("🏠 Panel de Finanzas del Hogar")

# --- NUEVO SELECTOR DE MES POR BOTONES ---
col_btn1, col_txt, col_btn2 = st.columns([1, 3, 1])

with col_btn1:
    if st.button("◀ Mes Anterior"):
        # Restamos un mes a la fecha guardada
        st.session_state.mes_actual = st.session_state.mes_actual - relativedelta(months=1)
        st.rerun()

with col_txt:
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    nombre_mes_actual = f"{meses[st.session_state.mes_actual.month-1]} {st.session_state.mes_actual.year}"
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>{nombre_mes_actual}</h3>", unsafe_allow_html=True)

with col_btn2:
    if st.button("Mes Siguiente ▶"):
        # Sumamos un mes a la fecha guardada
        st.session_state.mes_actual = st.session_state.mes_actual + relativedelta(months=1)
        st.rerun()

inicio = st.session_state.mes_actual.replace(day=19) 
fin = (inicio + relativedelta(months=1)).replace(day=18)
st.info(f"📅 **Ciclo actual de trabajo:** {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")

# Creamos una "llave" única para este mes (ej. "2026-11")
mes_key = inicio.strftime("%Y-%m")

if mes_key not in st.session_state.datos_ingresos:
    st.session_state.datos_ingresos[mes_key] = {
        "Alexander": {"Sueldo líquido": 1746582, "Sobresueldo": 0, "Trimestral": 0, "Asesorías": 500000, "Otro": 0},
        "Mariana": {"Sueldo líquido": 1958386, "Sobresueldo": 0, "Trimestral": 0, "Asesorías": 500000, "Otro": 0}
    }

compromisos = {"Dividendos Propiedades": 1208288, "Colegios y Niños": 543000, "Tarjetas de Crédito": 213478, "Servicios y Gastos Fijos": 450000}

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📊 Resumen (Hoja 1)", "🏦 Cuentas y Bolsillos (Hoja 2)"])

# ==========================================
# PESTAÑA 1: HOJA 1 (RESUMEN)
# ==========================================
with tab1:
    with st.expander(f"✏️ Modificar Ingresos de {nombre_mes_actual}", expanded=False):
        with st.form("form_ingresos"):
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                st.markdown("**Alexander**")
                ing_a = st.session_state.datos_ingresos[mes_key]["Alexander"]
                sueldo_a = st.number_input("Sueldo líquido A.", value=ing_a["Sueldo líquido"], step=1000)
                sobre_a = st.number_input("Sobresueldo A.", value=ing_a["Sobresueldo"], step=1000)
                trim_a = st.number_input("Trimestral A.", value=ing_a["Trimestral"], step=1000)
                ases_a = st.number_input("Asesorías A.", value=ing_a["Asesorías"], step=1000)
                otro_a = st.number_input("Otro A.", value=ing_a["Otro"], step=1000)
                
            with col_f2:
                st.markdown("**Mariana**")
                ing_m = st.session_state.datos_ingresos[mes_key]["Mariana"]
                sueldo_m = st.number_input("Sueldo líquido M.", value=ing_m["Sueldo líquido"], step=1000)
                sobre_m = st.number_input("Sobresueldo M.", value=ing_m["Sobresueldo"], step=1000)
                trim_m = st.number_input("Trimestral M.", value=ing_m["Trimestral"], step=1000)
                ases_m = st.number_input("Asesorías M.", value=ing_m["Asesorías"], step=1000)
                otro_m = st.number_input("Otro M.", value=ing_m["Otro"], step=1000)
            
            boton_guardar = st.form_submit_button("💾 Guardar Cambios del Mes")
            
            if boton_guardar:
                st.session_state.datos_ingresos[mes_key]["Alexander"] = {"Sueldo líquido": sueldo_a, "Sobresueldo": sobre_a, "Trimestral": trim_a, "Asesorías": ases_a, "Otro": otro_a}
                st.session_state.datos_ingresos[mes_key]["Mariana"] = {"Sueldo líquido": sueldo_m, "Sobresueldo": sobre_m, "Trimestral": trim_m, "Asesorías": ases_m, "Otro": otro_m}
                st.success("¡Datos guardados para este mes!")

    st.header("💵 Ingresos del Mes")
    col_ing_1, col_ing_2 = st.columns(2)

    with col_ing_1:
        datos_a = st.session_state.datos_ingresos[mes_key]["Alexander"]
        total_alex = sum(datos_a.values())
        html_alex = '<div class="custom-card card-alexander">'
        html_alex += '<div class="card-title">Alexander</div>'
        for k, v in datos_a.items():
            html_alex += f'<div class="data-row"><span class="data-label">{k}</span><span class="data-value">{fmt(v)}</span></div>'
        html_alex += f'<div class="total-row total-alexander"><span>Total Recibido</span><span>{fmt(total_alex)}</span></div>'
        html_alex += '</div>'
        st.markdown(html_alex, unsafe_allow_html=True)

    with col_ing_2:
        datos_m = st.session_state.datos_ingresos[mes_key]["Mariana"]
        total_mar = sum(datos_m.values())
        html_mar = '<div class="custom-card card-mariana">'
        html_mar += '<div class="card-title">Mariana</div>'
        for k, v in datos_m.items():
            html_mar += f'<div class="data-row"><span class="data-label">{k}</span><span class="data-value">{fmt(v)}</span></div>'
        html_mar += f'<div class="total-row total-mariana"><span>Total Recibido</span><span>{fmt(total_mar)}</span></div>'
        html_mar += '</div>'
        st.markdown(html_mar, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="custom-card" style="background-color: #f1f5f9; border-top: 5px solid #cbd5e1;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 18px; font-weight: bold; color: #334155;">Ingreso Total del Hogar</span>
            <span style="font-size: 24px; font-weight: bold; color: #0f172a;">{fmt(total_alex + total_mar)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("📌 Compromisos Pendientes")
    total_compromisos = sum(compromisos.values())
    html_comp = '<div class="custom-card" style="background-color: #ffffff; border-top: 5px solid #cbd5e1;">'
    for concepto, monto in compromisos.items():
        html_comp += f'<div class="data-row"><span class="data-label">{concepto}</span><span class="data-value" style="color: #dc2626;">{fmt(monto)}</span></div>'
    html_comp += f'<div class="total-row" style="color: #dc2626;"><span>Total Comprometido</span><span>{fmt(total_compromisos)}</span></div>'
    html_comp += '</div>'
    st.markdown(html_comp, unsafe_allow_html=True)

    st.divider()

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
# PESTAÑA 2: HOJA 2 (BANCOS Y BOLSILLOS)
# ==========================================
with tab2:
    st.header("🏦 Bancos, Cuentas y Bolsillos")
    st.write("Haz clic en un banco para ver sus cuentas y bolsillos, y editar sus saldos.")

    col_bancos_1, col_bancos_2 = st.columns(2)

    def render_por_banco(persona, columna):
        with columna:
            st.subheader(f"Bancos de {persona}")
            # CORRECCIÓN AQUÍ: Buscamos directamente en la llave de la persona
            bancos_persona = st.session_state.datos_cuentas[persona]
            
            for banco_nombre, cuentas in bancos_persona.items():
                total_banco = 0
                for bolsillos in cuentas.values():
                    total_banco += sum(bolsillos.values())
                
                with st.expander(f"🏦 **{banco_nombre}** (Total: {fmt(total_banco)})", expanded=False):
                    for cuenta_nombre, bolsillos in cuentas.items():
                        st.markdown(f"**{cuenta_nombre}**")
                        for b_nombre, b_monto in bolsillos.items():
                            st.markdown(f"<div class='data-row'><span class='data-label'>↳ {b_nombre}</span><span class='data-value'>{fmt(b_monto)}</span></div>", unsafe_allow_html=True)
                    
                    st.divider()
                    # Formulario de edición dinámico para este banco
                    with st.form(f"form_edit_{persona}_{banco_nombre}"):
                        st.write(f"**Editar saldos de {banco_nombre}**")
                        nuevos_valores = {}
                        for cuenta_nombre, bolsillos in cuentas.items():
                            for b_nombre, b_monto in bolsillos.items():
                                nuevo_monto = st.number_input(f"{cuenta_nombre} - {b_nombre}", value=b_monto, step=1000, key=f"input_{persona}_{banco_nombre}_{cuenta_nombre}_{b_nombre}")
                                nuevos_valores[(cuenta_nombre, b_nombre)] = nuevo_monto
                        
                        if st.form_submit_button("💾 Guardar Saldos de este Banco"):
                            for (cuenta_nombre, b_nombre), nuevo_monto in nuevos_valores.items():
                                st.session_state.datos_cuentas[persona][banco_nombre][cuenta_nombre][b_nombre] = nuevo_monto
                            st.success(f"Saldos de {banco_nombre} actualizados.")
                            st.rerun()

    render_por_banco("Alexander", col_bancos_1)
    render_por_banco("Mariana", col_bancos_2)

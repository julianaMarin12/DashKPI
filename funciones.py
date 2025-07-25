from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import plotly.express as px
import io 
import base64
import unicodedata
from estilos import COLOR_ACENTO, COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_TEXTO_OSCURO, COLOR_TEXTO_CLARO

COLOR_FONDO = "#F8F9FA"
COLOR_PROYECTADO = "#F4869C"

def cargar_excel(path, sheet):
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.strip()
    return df

def mostrar_tipologia(dataframe, etiqueta_col, referencia):    
    df_tabla = dataframe[[etiqueta_col, "UTILIDAD NETA FINAL", "MARGEN NETO FINAL"]].copy()
    df_tabla["MARGEN NETO FINAL"] = df_tabla["MARGEN NETO FINAL"] * 100
    df_tabla.rename(columns={
        etiqueta_col: "Tipología",
        "UTILIDAD NETA FINAL": "Utilidad Neta",
        "MARGEN NETO FINAL": "Margen Neto (%)"
    }, inplace=True)

    df_tabla["Utilidad Neta"] = df_tabla["Utilidad Neta"].apply(lambda x: f"${formatear_valor_colombiano(x)}")

    def barra_progreso_primaria(margen):
        return f'<div style="position:relative; width:100%; height:28px; background:#eee; border-radius:7px; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{max(0,min(margen,100))}%; background:{COLOR_PRIMARIO}; opacity:0.25;"></div><div style="position:relative; z-index:2; color:#222; font-weight:700; line-height:28px; text-align:center; font-size:1rem;">{margen:.2f}%</div></div>'
    df_tabla["Margen Neto (%)"] = df_tabla["Margen Neto (%)"].astype(float).apply(barra_progreso_primaria)

    html = df_tabla.to_html(escape=False, index=False, classes="tabla-tipologia")
    st.markdown(html, unsafe_allow_html=True)

def crear_donut(indicador, color=COLOR_PRIMARIO, height=200, width=200, font_size=14):
    fig = go.Figure(data=[go.Pie(
        values=[indicador, 100 - indicador],
        labels=["Avance", "Restante"],
        hole=0.65,
        marker=dict(colors=[color, "#F0F0F0"]),
        textinfo="none",
        hoverinfo="label+percent",
        sort=False
    )])
    fig.update_layout(
        showlegend=False,
        annotations=[dict(
            text=f"<b>{indicador:.2f}%</b>",
            x=0.5, y=0.5,
            font=dict(size=font_size, color="black"),
            showarrow=False
        )],
        margin=dict(t=10, b=10, l=10, r=10),
        height=height,
        width=width
    )
    return fig

def aplicar_jitter(df, factor=0.03):
    zona_counts = df['ZONA'].value_counts()
    df_jitter = df.copy()
    for zona, count in zona_counts.items():
        if count > 1:
            idx = df_jitter[df_jitter['ZONA'] == zona].index
            lat_jitter = np.linspace(-factor, factor, count)
            lon_jitter = np.linspace(-factor, factor, count)
            df_jitter.loc[idx, 'lat'] += lat_jitter
            df_jitter.loc[idx, 'lon'] += lon_jitter
    return df_jitter

def crear_mapa(df):
    df_mapa = df.dropna(subset=["lat", "lon", "INDICADOR"])
    df_mapa = df_mapa[df_mapa['ZONA'] != "GENERAL"]
    df_mapa = aplicar_jitter(df_mapa)

    fig = go.Figure()
    color_scale = ['#25ABB9', '#28BBCA', '#2BC5D5', '#3CC9D8', '#52CFDC', '#70D7E2']
    df_mapa['color'] = df_mapa['INDICADOR'].apply(lambda x: sample_colorscale(color_scale, x)[0])

    for _, row in df_mapa.iterrows():
        fig.add_trace(go.Scattermapbox(
            lon=[row['lon']],
            lat=[row['lat']],
            mode="markers+text",
            marker=dict(size=10 + row['INDICADOR'] * 40, color=row['color']),
            text=[(
                f"{row['Supervisor']}<br>"
                f"{row['INDICADOR'] * 100:.2f}%<br>"
                f"${row['TOTAL VENCIDO']:,.0f} vencido<br>"
                f"${row['TOTAL CORRIENTE']:,.0f} corriente<br>"
                f"${row['TOTAL CARTERA']:,.0f} cartera"
            )],
            textposition="bottom right",
            showlegend=False
        ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=5,
        mapbox_center={"lat": df_mapa['lat'].mean(), "lon": df_mapa['lon'].mean()},
        margin=dict(l=0, r=0, t=30, b=0),
        height=600
    )
    return fig, df_mapa

def crear_gauge_base64(valor, referencia):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor,
        number={
            'suffix': '%',
            'font': {'size': 28}
        },
        delta={
            'reference': referencia,
            'increasing': {'color': "green", 'symbol': "▲"},
            'decreasing': {'color': "red", 'symbol': "▼"},
            'relative': False,
            'valueformat': '.1f',
            'suffix': '%',
            'position': "bottom" 
        },
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, referencia], 'color': "#ffe6e6"},
                {'range': [referencia, 100], 'color': "#e6ffe6"}
            ]
        }
    ))
    fig.update_layout(width=200, height=180, margin=dict(l=10, r=10, t=10, b=10))

    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{img_base64}" width="150"/>'

def normalizar_columna(col):
    return ''.join((c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')).lower()

def render_df_html(df):
    import unicodedata
    def normalizar_columna(col):
        return ''.join((c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')).lower()
    formatters = {}
    palabras_monetarias = ["venta", "presupuesto", "utilidad", "cartera", "total", "meta"]
    for col in df.columns:
        col_norm = normalizar_columna(col)
        if col.strip().endswith(" (%)") or "%" in col:
            formatters[col] = lambda x: f"{x:.2f}%" if pd.notnull(x) else ""
        elif any(palabra in col_norm for palabra in palabras_monetarias):
            formatters[col] = lambda x: f"${formatear_valor_colombiano(x)}" if pd.notnull(x) else ""
        elif "porcentaje" in col_norm or "ejecutado" in col_norm or "margen" in col_norm or "diferencia" in col_norm:
            formatters[col] = lambda x: f"{x:.2f}%" if pd.notnull(x) else ""
    return df.to_html(escape=False, index=False, formatters=formatters)

def imagen_base64(ruta):
        try:
            img = Image.open(ruta).convert("RGBA")
            fondo_blanco = Image.new("RGBA", img.size, (255, 255, 255, 255))
            img_con_fondo_blanco = Image.alpha_composite(fondo_blanco, img).convert("RGB")
                
            buffered = BytesIO()
            img_con_fondo_blanco.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"<img src='data:image/png;base64,{img_str}' width='100'/>"
        except Exception as e:
            return f"<div style='color:red;'>X</div>"
            
def crear_indicador_estado(valor, referencia, titulo):
    diferencia = valor - referencia
    
    if diferencia >= 0:
        estado_color = "#28A745"
        estado_icon = "✓"
        estado_text = "OBJETIVO ALCANZADO"
        bg_color = f"linear-gradient(135deg, #28A745 0%, #20C997 100%)"
    elif -50 <= diferencia < 0 :
        estado_color = "#EFCE4B"
        estado_icon = "↑"
        estado_text = "ESTA EN AUMENTO"
        bg_color = f"linear-gradient(135deg, #FFD700 0%, #EFCE4B 100%)"
    else:
        estado_color = "#DC3545"
        estado_icon = "⚠"
        estado_text = "REQUIERE ATENCIÓN"
        bg_color = f"linear-gradient(135deg, #DC3545 0%, #E74C3C 100%)"
    
    st.markdown(f"""
    <div style="
        background: {bg_color};
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 6px 24px rgba(0,0,0,0.15);
        border: 2px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">{estado_icon}</div>
        <h3 style="margin: 0; color: white; font-size: 1rem; font-weight: 600; letter-spacing: 1px;">{estado_text}</h3>
        <h1 style="margin: 1rem 0; color: white; font-size: 2.5rem; font-weight: 700;">{diferencia:+.1f}%</h1>
        <p style="margin: 0; opacity: 1; font-size: 1.4rem;"> Objetivo: {referencia}%</p>
        <div style="
            width: 60px;
            height: 3px;
            background: rgba(255, 255, 255, 0.5);
            margin: 1rem auto 0;
            border-radius: 2px;
        "></div>
    </div>
    """, unsafe_allow_html=True)

def formatear_valor_colombiano(valor):
    valor_str = f"{valor:,.0f}"
    valor_str = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
    return valor_str

def mostrar_metrica_corporativa_mercadeo(titulo, valor, prefijo="", sufijo="", tipo="default"):
    if isinstance(valor, (int, float)):
        if sufijo == "%":
            valor_formateado = f"{valor:,.2f}"
        else:
            if abs(valor) >= 1_000_000_000:
                valor_formateado = valor / 1_000_000_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
            elif abs(valor) >= 1_000_000:
                valor_formateado = valor / 1_000_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
            elif abs(valor) >= 1_000:
                valor_formateado = valor / 1_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
    else:
        valor_formateado = formatear_valor_colombiano(valor)
    
    if tipo == "primario":
        background = f"linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%)"
        text_color = COLOR_TEXTO_CLARO
    elif tipo == "secundario":
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #E0DDD8 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"2px solid {COLOR_PRIMARIO}"
    else:
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #F5F3F1 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"1px solid {COLOR_PRIMARIO}40"
    
    border_style = f"border: {border};" if tipo == "secundario" else f"border: 1px solid {COLOR_PRIMARIO}20;"
    
    st.markdown(f"""
    <div style="
        background: {background};
        padding: 1.8rem;
        border-radius: 12px;
        {border_style}
        box-shadow: 0 4px 20px rgba(0, 176, 178, 0.15);
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    ">
        <h4 style="
            color: {text_color};
            margin: 0 0 0.8rem 0;
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            opacity: 0.9;
        ">{titulo}</h4>
        <h2 style="
            color: {text_color};
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1.1;
            font-family: 'Segoe UI', sans-serif;
        ">{prefijo}{valor_formateado}{sufijo}</h2>
    </div>
    """, unsafe_allow_html=True)

def mostrar_metrica_corporativa_mercadeo(titulo, valor, prefijo="", sufijo="", tipo="default"):
    if isinstance(valor, (int, float)):
        if sufijo == "%":
            valor_formateado = f"{valor:,.2f}"
        else:
            if abs(valor) >= 1_000_000_000:
                valor_formateado = valor / 1_000_000_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
            elif abs(valor) >= 1_000_000:
                valor_formateado = valor / 1_000_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
            elif abs(valor) >= 1_000:
                valor_formateado = valor / 1_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
    else:
        valor_formateado = formatear_valor_colombiano(valor)
    
    if tipo == "primario":
        background = f"linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%)"
        text_color = COLOR_TEXTO_CLARO
    elif tipo == "secundario":
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #E0DDD8 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"2px solid {COLOR_PRIMARIO}"
    else:
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #F5F3F1 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"1px solid {COLOR_PRIMARIO}40"
    
    border_style = f"border: {border};" if tipo == "secundario" else f"border: 1px solid {COLOR_PRIMARIO}20;"
    
    st.markdown(f"""
    <div style="
        background: {background};
        padding: 1.8rem;
        border-radius: 12px;
        {border_style}
        box-shadow: 0 4px 20px rgba(0, 176, 178, 0.15);
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    ">
        <h4 style="
            color: {text_color};
            margin: 0 0 0.8rem 0;
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            opacity: 0.9;
        ">{titulo}</h4>
        <h2 style="
            color: {text_color};
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1.1;
            font-family: 'Segoe UI', sans-serif;
        ">{prefijo}{valor_formateado}{sufijo}</h2>
    </div>
    """, unsafe_allow_html=True)

def mostrar_metrica_corporativa(titulo, valor, prefijo="", sufijo="", tipo="default"):
    if isinstance(valor, (int, float)):
        if sufijo == "%":
            valor_formateado = f"{valor:,.2f}"
        else:
            valor_formateado = formatear_valor_colombiano(valor)
    else:
        valor_formateado = str(valor)
            
    
    if tipo == "primario":
        background = f"linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%)"
        text_color = COLOR_TEXTO_CLARO
    elif tipo == "secundario":
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #E0DDD8 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"2px solid {COLOR_PRIMARIO}"
    else:
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #F5F3F1 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"1px solid {COLOR_PRIMARIO}40"
    
    border_style = f"border: {border};" if tipo == "secundario" else f"border: 1px solid {COLOR_PRIMARIO}20;"
    
    st.markdown(f"""
    <div style="
        background: {background};
        padding: 1.8rem;
        border-radius: 12px;
        {border_style}
        box-shadow: 0 4px 20px rgba(0, 176, 178, 0.15);
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    ">
        <h4 style="
            color: {text_color};
            margin: 0 0 0.8rem 0;
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            opacity: 0.9;
        ">{titulo}</h4>
        <h2 style="
            color: {text_color};
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1.1;
            font-family: 'Segoe UI', sans-serif;
        ">{prefijo}{valor_formateado}{sufijo}</h2>
    </div>
    """, unsafe_allow_html=True)

def crear_gauge_corporativo(valor, titulo, referencia=None):
    """Crea un gauge con diseño corporativo"""
    if referencia:
        if valor >= referencia:
            color_principal = COLOR_PRIMARIO
            color_fondo = "#E8F8F8"
            color_threshold = "#28A745"
        else:
            color_principal = "#DC3545"
            color_fondo = "#FDEAEA"
            color_threshold = "#FFC107"
    else:
        color_principal = COLOR_PRIMARIO
        color_fondo = "#E8F8F8"
        color_threshold = COLOR_ACENTO
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': titulo, 
            'font': {
                'size': 18, 
                'color': COLOR_TEXTO_OSCURO, 
                'family': 'Segoe UI, Arial',
                'weight': 600
            }
        },
        delta = {
            'reference': referencia if referencia else 0, 
            'suffix': '%',
            'font': {'size': 16, 'color': COLOR_TEXTO_OSCURO}
        },
        gauge = {
            'axis': {
                'range': [0, referencia], 
                'tickwidth': 2, 
                'tickcolor': COLOR_TEXTO_OSCURO,
                'tickfont': {'size': 12, 'color': COLOR_TEXTO_OSCURO}
            },
            'bar': {'color': color_principal, 'thickness': 0.35},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': COLOR_SECUNDARIO,
            'steps': [
                {'range': [0, referencia if referencia else 25], 'color': color_fondo},
                {'range': [referencia if referencia else 25, max(50, valor * 1.2)], 'color': '#F8F9FA'}
            ],
            'threshold': {
                'line': {'color': color_threshold, 'width': 4},
                'thickness': 0.75,
                'value': referencia if referencia else 30
            }
        },
        number = {
            'font': {
                'size': 36, 
                'color': color_principal, 
                'family': 'Segoe UI, sans-serif',
                'weight': 700
            },
            'suffix': '%'
        }
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(l=30, r=30, t=80, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': COLOR_TEXTO_OSCURO, 'family': "Segoe UI, sans-serif"}
    )
    
    return fig

def grafico_linea_corporativo(df, x, y, color=None, titulo="", etiquetas=None, colores=None, formato_y="%", mostrar_valores=True):
    colores_corporativos = ["#00B0B2", "#F4869C"]
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=True,
        title=titulo,
        labels=etiquetas if etiquetas else None,
        color_discrete_sequence=colores if colores is not None else colores_corporativos
    )
    fig.update_layout(
        xaxis_tickangle=35,
        height=500,
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font=dict(family="Segoe UI, Arial", size=16, color="#2C3E50"),
        legend=dict(
            bgcolor="#F8F9FA",
            bordercolor="#00B0B2",
            borderwidth=1,
            font=dict(size=14)
        ),
        title=dict(
            font=dict(size=22, color="#2C3E50", family="Segoe UI, Arial"),
            x=0
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#EDEBE9",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EDEBE9",
            zeroline=False
        ),
        margin=dict(l=30, r=30, t=60, b=60)
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=10, symbol="circle"))

    if mostrar_valores:
        for trace in fig.data:
            xs = trace.x
            ys = trace.y
            color_trace = trace.line.color if hasattr(trace.line, 'color') and trace.line.color else "#00B0B2"
            for xi, yi in zip(xs, ys):
                if yi is not None:
                    if formato_y == "%":
                        texto = f"{yi:.2f}%"
                    elif formato_y == "$":
                        texto = f"${yi:,.0f}"
                    else:
                        texto = f"{yi:.2f}"
                    fig.add_annotation(
                        x=xi,
                        y=yi,
                        text=texto,
                        showarrow=False,
                        yshift=18,
                        font=dict(size=15, color=color_trace, family="Segoe UI, Arial"),
                        align="center",
                        bgcolor="rgba(255,255,255,0.7)",
                        bordercolor=color_trace,
                        borderwidth=0
                    )
    st.plotly_chart(fig, use_container_width=True)

def grafico_barras_corporativo(df, x, y, color=None, titulo="", etiquetas=None, colores=None, formato_y="%", apilado=False, mostrar_valores=True, key=None):
    color_proyectado = COLOR_PROYECTADO
    color_ejecutado = COLOR_PRIMARIO
    color_linea_proy = "#E6758A"
    color_acento = COLOR_ACENTO
    color_texto = COLOR_TEXTO_OSCURO
    color_fondo = "rgba(0,0,0,0)"
    categorias = df[x].unique().tolist()
    indicadores = df[color].unique().tolist() if color else [y]
    fig = go.Figure()
    for i, indicador in enumerate(indicadores):
        df_filtrado = df[df[color] == indicador] if color else df
        valores = df_filtrado[y].tolist()
        if indicador.lower().startswith("ref") or indicador.lower().startswith("proy"):
            color_barra = color_proyectado
            color_linea = color_linea_proy
            nombre = "Proyectado" if "Proy" in indicador or "ref" in indicador.lower() else indicador
        else:
            color_barra = color_ejecutado
            color_linea = color_acento
            nombre = "Ejecutado" if "Ejec" in indicador or "ejec" in indicador.lower() else indicador
        fig.add_trace(go.Bar(
            name=nombre,
            x=categorias,
            y=valores,
            marker=dict(
                color=color_barra,
                line=dict(color=color_linea, width=2),
                opacity=0.9 if nombre=="Ejecutado" else 0.8
            ),
            text=[f"{v:.1f}%" if formato_y=="%" else f"${v:,.0f}" if formato_y=="$" else f"{v:.2f}" for v in valores],
            textposition="inside",
            textfont=dict(size=16, color="white", family="Arial Black"),
            hovertemplate=f"<b>{nombre}</b><br>Tipo: %{{x}}<br>Valor: %{{y:.1f}}%<br><extra></extra>",
            width=0.6
        ))
    fig.update_layout(
        barmode='stack' if apilado else 'group',
        title=dict(
            text=f"<b>{titulo}</b>" if titulo else None,
            font=dict(size=20, color=color_texto, family="Arial"),
            x=0.3
        ),
        yaxis=dict(
            title=dict(text=f"<b>{etiquetas[y]}</b>" if etiquetas and y in etiquetas else "<b>Porcentaje (%)</b>", font=dict(size=14, color=color_texto)),
            tickfont=dict(size=14, color=color_texto),
            gridcolor="rgba(0, 176, 178, 0.1)",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="rgba(0, 176, 178, 0.3)",
            zerolinewidth=2
        ),
        xaxis=dict(
            title=dict(text=f"<b>{etiquetas[x]}</b>" if etiquetas and x in etiquetas else "<b>Tipo de Rentabilidad</b>", font=dict(size=16, color=color_texto)),
            tickfont=dict(size=14, color=color_texto),
            gridcolor="rgba(0, 176, 178, 0.1)"
        ),
        height=500,
        legend=dict(
            title=dict(text="<b>Indicadores</b>", font=dict(size=12, color=color_texto)),
            font=dict(size=10, color=color_texto),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor=COLOR_PRIMARIO,
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor=color_fondo,
        paper_bgcolor=color_fondo,
        bargap=0.4,
        bargroupgap=0.1,
        font=dict(size=14, color=color_texto, family="Arial"),
        margin=dict(l=30, r=30, t=60, b=30),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=COLOR_PRIMARIO,
            font_size=12,
            font_family="Arial"
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=key)

def grafico_barras_dinero(df, x, y, titulo="", etiquetas=None, color_barra="#00B0B2"):
    categorias = df[x].tolist()
    valores = df[y].tolist()
    textos = [f"${v:,.0f}".replace(",", ".") if pd.notnull(v) else "" for v in valores]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categorias,
        y=valores,
        marker=dict(
            color=color_barra,
            line=dict(color="#008080", width=2),
            opacity=0.9
        ),
        text=textos,
        textposition="inside",
        textfont=dict(size=16, color="white", family="Arial Black"),
        hovertemplate="<b>%{x}</b><br>Valor: %{text}<extra></extra>",
        width=0.6
    ))
    fig.update_layout(
        barmode='group',
        title=dict(
            text=f"<b>{titulo}</b>" if titulo else None,
            font=dict(size=20, color="#2C3E50", family="Arial"),
            x=0.2
        ),
        yaxis=dict(
            title=dict(text=f"<b>{etiquetas[y]}</b>" if etiquetas and y in etiquetas else "<b>Dinero</b>", font=dict(size=14, color="#2C3E50")),
            tickfont=dict(size=14, color="#2C3E50"),
            gridcolor="rgba(0, 176, 178, 0.1)",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="rgba(0, 176, 178, 0.3)",
            zerolinewidth=2
        ),
        xaxis=dict(
            title=dict(text=f"<b>{etiquetas[x]}</b>" if etiquetas and x in etiquetas else "<b>Categoría</b>", font=dict(size=16, color="#2C3E50")),
            tickfont=dict(size=14, color="#2C3E50"),
            gridcolor="rgba(0, 176, 178, 0.1)"
        ),
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.4,
        bargroupgap=0.1,
        font=dict(size=14, color="#2C3E50", family="Arial"),
        margin=dict(l=30, r=30, t=60, b=30),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#00B0B2",
            font_size=12,
            font_family="Arial"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def grafico_barras_dinero_horizontal(df, x, y, titulo="", etiquetas=None, color_barra=None, key=None,orden_descendente=True):
    df = df.sort_values(by=y, ascending=not orden_descendente)

    categorias = df[x].tolist()
    valores = df[y].tolist()
    textos = [f"${v:,.0f}".replace(",", ".") if pd.notnull(v) else "" for v in valores]

    fig = go.Figure()
    categorias = df[x]
    valores = df[y]
    bar_kwargs = {}
    if color_barra is not None:
        bar_kwargs["marker_color"] = color_barra if isinstance(color_barra, list) else [color_barra]*len(valores)
    fig.add_trace(go.Bar(
        y=categorias,
        x=valores,
        orientation='h',
        marker=dict(
            color=color_barra,
            line=dict(color="#008080", width=2),
            opacity=0.9
        ),
        text=textos,
        textposition="inside",  
        textfont=dict(size=16, color="white", family="Arial Black"),
        hovertemplate="<b>%{y}</b><br>Valor: %{text}<extra></extra>",
        width=0.6
    ))
    fig.update_layout(
        barmode='group',
        title=dict(
            text=f"<b>{titulo}</b>" if titulo else None,
            font=dict(size=20, color="#2C3E50", family="Arial"),
            x=0.3
        ),
        xaxis=dict(
            title=dict(text=f"<b>{etiquetas[y]}</b>" if etiquetas and y in etiquetas else "<b>Dinero</b>", font=dict(size=14, color="#2C3E50")),
            tickfont=dict(size=14, color="#2C3E50"),
            gridcolor="rgba(0, 176, 178, 0.1)",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="rgba(0, 176, 178, 0.3)",
            zerolinewidth=2
        ),
        yaxis=dict(
            title=dict(text=f"<b>{etiquetas[x]}</b>" if etiquetas and x in etiquetas else "<b>Categoría</b>", font=dict(size=16, color="#2C3E50")),
            tickfont=dict(size=14, color="#2C3E50"),
            gridcolor="rgba(0, 176, 178, 0.1)"
        ),
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.4,
        bargroupgap=0.1,
        font=dict(size=14, color="#2C3E50", family="Arial"),
        margin=dict(l=30, r=30, t=60, b=30),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#00B0B2",
            font_size=12,
            font_family="Arial"
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=key)



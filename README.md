# 🛒 Dashboard de KPIs - Área Comercial

Este proyecto presenta un dashboard interactivo desarrollado en **Streamlit** que permite visualizar de forma clara y dinámica los **Principales Indicadores de Desempeño (KPIs)** del Área Comercial de la compañía.

---

## 📌 ¿Qué son los KPIs?

Los **KPIs** (Key Performance Indicators) son métricas clave que nos permiten **evaluar el rendimiento** de procesos estratégicos en tiempo real. En el contexto comercial, los KPIs permiten:

- Monitorear la **efectividad en la gestión de cartera**.
- Identificar **zonas geográficas con mejor o peor comportamiento comercial**.
- Tomar decisiones basadas en datos confiables y actualizados.
- Establecer **metas claras y medibles** para los equipos de ventas y cartera.

---

## 📊 ¿Qué muestra este dashboard?

El sistema integra un análisis automatizado de Excel con visualizaciones modernas para presentar:

- **Indicador general de cartera** en formato de gráfico circular (avance vs restante).
- **Totales financieros**:
  - Total Vencido
  - Total Corriente
  - Total Cartera
- **Visualización geográfica** de zonas (Armenia, Bogotá, Antioquia, Costa, Pacífico), con:
  - Nombre del supervisor
  - Porcentaje de cumplimiento del KPI
  - Valores asociados a cartera
- Puntos del mapa **codificados por color y tamaño**:
  - Verde (#4CAF50): representa cumplimiento
  - Tamaño proporcional al desempeño

---

## 🌎 Beneficios de esta herramienta

✅ Información centralizada  
✅ Fácil interpretación para no expertos  
✅ Visual atractivo con mapas interactivos  
✅ Acceso con login personalizado  
✅ Escalable: permite añadir nuevas zonas, métricas o filtros

---

## 🚀 Tecnologías usadas

- `Python`
- `Streamlit`
- `Plotly`
- `Pandas`
- `Excel` como fuente de datos

---

## 👩‍💼 Para quién está hecho

Este dashboard está diseñado para:

- Gerentes comerciales
- Supervisores de zona
- Analistas de cartera
- Dirección general

Permite tener una **visión estratégica** del desempeño comercial y anticiparse a problemas financieros o de gestión.

---

## 🔐 Acceso seguro

El sistema incluye un **módulo de login** que restringe el acceso solo a usuarios autorizados mediante la librería `st.session_state`.

---

## ✨ Próximas mejoras

- Filtros por fechas o rango de tiempo
- Exportación automática de reportes en PDF
- Integración directa con sistemas ERP o bases de datos en la nube

---

## 📥 Requisitos para ejecución local

pip install streamlit pandas plotly openpyxl


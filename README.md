# Data Visualization & Dashboards Hub 📊

This repository is a collection of automated dashboard scripts developed with **Dash** and **Plotly**. It demonstrates a progression from static data visualization to dynamic, SQL-integrated applications.

### Projects Included
1.  **Basic Pipeline:** Demonstrates how to clean data and create multi-trace scatter plots programmatically.
2.  **SQL Integration:** Features a pipeline that creates a local SQLite database and serves data directly to a Dash interface.
3.  **Interactive Dashboards:** Implementation of React-based callbacks for real-time data filtering.

### How to Run
To run any of these dashboards, ensure you have Python installed and follow these steps:

1.  **Install dependencies:**
    ```bash
    pip install pandas dash sqlalchemy plotly
    ```
2.  **Initialize Database (for SQL projects):**
    ```bash
    python create_database.py
    ```
3.  **Launch the Dashboard:**
    ```bash
    python dashboard_sqlite.py
    ```
4.  **Access:** Open `http://127.0.0.1:8050/` in your browser.

### **🚀 Live Deployment:** [Visualize Interactive Dashboard here](https://web-production-7c4b6.up.railway.app/)

<br>
<br>

# Hub de Visualización de Datos y Dashboards 📊

Este repositorio es una colección de scripts para la creación de tableros (dashboards) automatizados desarrollados con **Dash** y **Plotly**. El proyecto demuestra una progresión técnica desde la visualización estática de datos hasta aplicaciones dinámicas integradas con bases de datos SQL.

### Proyectos Incluidos
1.  **Pipeline Básico:** Demuestra cómo limpiar datos y crear gráficos de dispersión de múltiples trazos de forma programática.
2.  **Integración SQL:** Incluye un pipeline que genera una base de datos local en **SQLite** y sirve los datos directamente a una interfaz de Dash.
3.  **Dashboards Interactivos:** Implementación de *callbacks* basados en React para el filtrado de datos en tiempo real por parte del usuario.

### Instrucciones de Ejecución
Para ejecutar cualquiera de estos tableros, asegúrate de tener Python instalado y sigue estos pasos:

1.  **Instalar dependencias:**
    ```bash
    pip install pandas dash sqlalchemy plotly
    ```
2.  **Inicializar la Base de Datos (para proyectos SQL):**
    Ejecuta el script para crear el archivo `.db` local:
    ```bash
    python create_database.py
    ```
3.  **Lanzar el Dashboard:**
    ```bash
    python dashboard_sqlite.py
    ```
4.  **Acceso:** Abre `http://127.0.0.1:8050/` en tu navegador para interactuar con la aplicación.

### **🚀 Demo en Vivo:** [Visualiza el Dashboard Interactivo aquí](https://web-production-7c4b6.up.railway.app/)

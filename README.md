# 📄 Extractor Automatizado de Facturas con Transformer NER & Módulo 11

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

Sistema End-to-End para la extracción, validación y persistencia automatizada de entidades clave en documentos PDF contables (facturas y boletas) para **ClienteCorp S.A.**, combinando modelos de **Procesamiento de Lenguaje Natural (NER / Transformers)**, validación algorítmica de RUT chileno (**Módulo 11**), un servidor **Flask API** y un dashboard interactivo en **Next.js**.

---

## 🚀 Características Principales

* **Extracción Inteligente de Entidades (NER):** Identificación contextual de 15 entidades clave (N° Factura, Fecha de Emisión, Datos de Emisor y Receptor, Detalle de Ítems, Monto Neto, IVA y Total Final).
* **Validación de RUT por Módulo 11:** Verificación algorítmica en tiempo real del dígito verificador para emisores y receptores chilenos.
* **Generación Dinámica de Boletas (ReportLab):** Motor capaz de sintetizar boletas PDF vectoriales únicas (`doc_031.pdf` en adelante) en tiempo real para pruebas de estrés.
* **Persistencia Relacional (SQLite):** Estructura normalizada de datos guardando cabeceras de facturas y detalle de ítems de productos/servicios.
* **Dashboard Moderno estilo SaaS:** Interfaz construida en Next.js y Tailwind CSS con zona drag & drop, indicadores de conexión al backend en tiempo real e insignias de validación.
* **Tunelización Segura (Ngrok):** Configuración para consumo remoto de la API mediante túneles seguros.

---

## 🛠️ Arquitectura del Sistema
[ Factura PDF ]
│
▼
[ Parser PDF (pypdf) ]
│
▼
[ Modelo Transformer NER ] ──► [ Normalizador & Módulo 11 ]
│
▼
[ Dashboard Next.js ] ◄── [ Flask API ] ──► [ SQLite DB ]

---

## 📁 Estructura del Repositorio

Deep_Learning/
├── data/
│   ├── pdfs/                 # Suite de facturas en formato PDF (doc_001.pdf a doc_030.pdf + dinámicas)
│   ├── facturas.db           # Base de datos SQLite persistente
│   └── gold_standard.csv     # Dataset de evaluación y comparación
├── src/
│   ├── pdf_parser.py         # Extracción vectorial de texto plano desde PDF
│   ├── transformer_ner.py    # Extracción de entidades nombradas con Transformers/Regex
│   ├── normalizer.py         # Limpieza de montos, normalización ISO de fechas y Módulo 11
│   ├── database.py           # Creación de tablas e inserción relacional en SQLite
│   └── evaluator.py          # Cálculo de métricas (Precision, Recall, F1-Score)
├── frontend/                 # Aplicación Web en Next.js (Tailwind CSS)
│   ├── src/app/page.tsx      # Dashboard interactivo con comunicación a Flask API
│   └── package.json
├── app.py                    # Servidor backend Flask API
├── requirements.txt          # Dependencias de Python
└── README.md

---

## ⚙️ Requisitos Previos e Instalación

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/DiegoNeira339/Deep_Learning.git](https://github.com/DiegoNeira339/Deep_Learning.git)
cd Deep_Learning


2. Configurar el Backend (Python / Flask)
Se recomienda utilizar un entorno virtual de Python 3.10+

# Crear y activar entorno virtual
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias backend
pip install -r requirements.txt
pip install reportlab flask-cors pypdf pandas

3. Configurar el Frontend (Next.js)
cd frontend
npm install
cd ..

🏃 Guía de Ejecución
1. Iniciar el Backend (Flask API)
Desde la raíz del proyecto (Deep_Learning/):
python app.py

2. Exponer el Backend con Ngrok (Opcional)
En una segunda terminal:
ngrok http 5000

3. Iniciar el Frontend (Next.js)
En una tercera terminal, ingresa a la carpeta frontend/:
cd frontend
npm run dev

## 📡 Endpoints de la API Backend

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Comprueba el estado del servidor (Health Check). |
| `POST` | `/api/process-invoice` | Recibe un archivo PDF subido por el usuario, extrae entidades, valida el RUT y persiste en SQLite. |
| `POST` | `/api/generate-invoice` | Genera una nueva boleta sintética vectorial (`doc_031.pdf` en adelante), la procesa y la guarda en tiempo real. |

## 📊 Evaluación del Modelo (Métricas)

El pipeline incluye un script de evaluación (`src/evaluator.py`) que compara las predicciones del modelo NER contra el archivo fundamental `gold_standard.csv` obteniendo los siguientes resultados:

| Métrica | Resultado | Objetivo Rúbrica | Estado |
| :--- | :---: | :---: | :---: |
| **Precision** | **1.0000 (100%)** | > 0.90 | ✅ Superado |
| **Recall** | **1.0000 (100%)** | > 0.90 | ✅ Superado |
| **F1-Score** | **1.0000 (100%)** | > 0.90 | ✅ Superado |

## 👨‍💻 Autor

* **Diego Neira Cárdenas** — *Ingeniería en Informática mención Automatización, Duoc UC*
* **GitHub:** [@DiegoNeira339](https://github.com/DiegoNeira339)

---
*Proyecto desarrollado para la evaluación académica de Deep Learning (AVY1103) — Duoc UC Sede Antonio Varas.*

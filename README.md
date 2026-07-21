# Finance Copilot

Aplicación de consulta inteligente sobre documentación financiera basada en **RAG** (Retrieval-Augmented Generation).

Permite subir documentos PDF, indexarlos automáticamente y responder preguntas en lenguaje natural utilizando exclusivamente la información contenida en los documentos, mostrando siempre las fuentes utilizadas.

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Backend | Python, FastAPI |
| IA | LangChain, LangGraph, OpenAI |
| Vector DB | ChromaDB |
| Embeddings | OpenAI Embeddings |
| Frontend | React (Vite) |

---

## Estructura del proyecto

```
Finance Copilot/
├── backend/
│   └── app/
│       ├── api/          # Endpoints REST
│       ├── config/       # Configuración y variables de entorno
│       ├── core/         # Utilidades transversales
│       ├── models/       # Schemas Pydantic
│       ├── rag/          # Pipeline RAG (ingestión, embeddings, vectorstore, chains)
│       └── services/     # Lógica de negocio
├── frontend/
│   └── src/
│       ├── api/          # Cliente HTTP hacia el backend
│       ├── components/   # Componentes reutilizables
│       ├── hooks/        # Custom hooks
│       └── pages/        # Vistas principales
├── requirements.txt
└── .env.example
```

---

## Requisitos previos

- Python 3.11+
- Node.js 18+
- Cuenta de OpenAI con API key

---

## Configuración

1. Clonar el repositorio y entrar al directorio del proyecto.

2. Copiar variables de entorno:

   ```bash
   cp .env.example .env
   ```

3. Completar `OPENAI_API_KEY` en el archivo `.env`.

---

## Backend

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación interactiva disponible en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación estará disponible en http://localhost:5173


---

## Licencia

Proyecto de portfolio — uso educativo y demostrativo.

# 🤖 Chatbot Inteligente - Browser Travel Solution

## Descripción del Proyecto
Este proyecto implementa un **chatbot inteligente** para una empresa de servicios tecnológicos.  
El objetivo es mejorar la atención al cliente 24/7, reducir la carga del equipo de soporte y ofrecer respuestas rápidas y contextuales a preguntas frecuentes.

El sistema:
- Responde consultas frecuentes sobre productos y servicios.
- Clasifica consultas en categorías como **ventas, soporte e información general**.
- Deriva conversaciones complejas a agentes humanos.
- Mantiene el **historial de conversación** y el **contexto**.
- Puede integrarse en una web o plataforma de terceros a través de una API REST.

---

#  Instrucciones de Instalación

### 1. Clonar el repositorio

git clone https://github.com/MiguelNaranjo02/PruebaTecnicaChatbot
cd chatbot_project

### 2. Crear y activar entorno virtual (recomendado con conda o venv)
conda create -n chatbot_env python=3.10 -y
conda activate chatbot_env

### 3. pip install -r requirements.txt
Dependencias principales:

- fastapi
- uvicorn
- pandas
- langchain-community
- langchain-huggingface.
- faiss-cpu
### 4. Crear estructura de datos
Dentro del directorio data/ coloca:
- faq.csv con preguntas frecuentes.
- knowledge.md con documentación extendida.
  
#GUIA DE USO
###1. Levantar el backend:
- En la terminal ejecutar:
- uvicorn src.api.server:app --reload --host 127.0.0.1 --port 8000

###2. Ejecutar LM Studio
- (descargar un modelo ej:Meta-Llama-3-8B-Instruct y correrlo en http://127.0.0.1:1234)

###3. Abrir la interfaz de chat: En la terminal ejecutar:
- streamlit run "path al archivo app.py"
- Esto abrirá una interfaz web simple para interactuar con el chatbot.

###4. Ejemplo de uso
- Usuario: "¿Qué servicios ofrecen?"
- A lo que el Chatbot respondera: "Ofrecemos desarrollo de software, consultoría en datos e implementación de IA."

##Explicacion de Arquitectura:
El proyecto está organizado en módulos:

- config.py → carga la configuración desde config.yaml.
- logger.py → logging centralizado para depuración y monitoreo.
- knowledge_base.py → gestiona la base de conocimientos, carga CSV/Markdown, indexa datos con FAISS + HuggingFaceEmbeddings.
- retriever.py → recupera información relevante de la base de conocimientos.
- chatbot.py → lógica principal del chatbot, integra el LLM y el contexto.
- server.py → expone API REST con FastAPI para integraciones externas.
- app.py → interfaz de usuario (chat web simple).

###Flujo:

- Usuario envía consulta → app.py.
- API recibe mensaje → server.py.
- Chatbot procesa → chatbot.py.
- Recupera contexto → retriever.py + knowledge_base.py.
- Respuesta generada por LLM.
- Respuesta devuelta al usuario.

##Tecnologías Utilizadas

- Python 3.10 → lenguaje principal.
- FastAPI → framework backend, expone API REST.
- Uvicorn → servidor ASGI rápido para producción.
- LangChain → manejo de embeddings y retrieval.
- HuggingFace Embeddings → modelo all-MiniLM-L6-v2 para vectorización de textos.
- FAISS → motor de búsqueda vectorial para indexación rápida.
- Logging → trazabilidad y depuración.

##Justificación:

- FastAPI y Uvicorn por su rapidez y compatibilidad con microservicios.
- LangChain y HuggingFace para procesamiento de lenguaje natural.
- FAISS por ser eficiente en búsquedas semánticas.

##Dificultades Encontradas y Soluciones

- Problemas con dependencias de embeddings (sentence-transformers): 
Solución: instalar con pip install sentence-transformers.

- Error al inicializar FAISS:
Solución: instalar versión adecuada según el entorno (faiss-cpu o faiss-gpu).

- Confusión entre Chroma y FAISS en LangChain:
Solución: mantener FAISS como vectorstore principal, ajustando knowledge_base.py.

- Error retriever.retrieve:
El VectorStoreRetriever no tiene .retrieve, solo .get_relevant_documents.

- Manejo de rutas relativas (config.yaml, data/faq.csv):
Ajustar rutas absolutas o asegurar ejecución desde raíz del proyecto.



# Instalación

El curso funciona completo **sin ningún modelo de IA**: el proyecto trae un proveedor falso
(`FakeLLM`) y embeddings que no necesitan red. Los modelos locales y las llaves comerciales se
usan para probar con IA de verdad, a partir de la sesión 6. Instale cada cosa antes de la sesión
en la que se usa.

| Para la sesión | Qué se necesita |
|---|---|
| 1 (5 oct) | Git, [uv](https://docs.astral.sh/uv/) y un editor (VS Code o PyCharm) |
| 6 (26 oct) | Ollama y el modelo de su tamaño (ver tabla); conviene instalarlo antes de la sesión 5 |
| 7 (28 oct) | Docker |
| 10 (11 nov) | Modelo de embeddings: `ollama pull qwen3-embedding:0.6b` |
| 11 (18 nov) | Tesseract con el idioma español, y el modelo de visión de su tamaño |

## Una regla: Ollama va nativo, no dentro de Docker

Ollama usa la tarjeta gráfica para que los modelos respondan rápido. En Mac, Docker no tiene
acceso a la GPU, y en Windows y Linux solo con configuración adicional: un modelo dentro de un
contenedor correría con el procesador y sería muy lento. Por eso Ollama se instala como
aplicación normal, y lo que corre en Docker (la API del asistente) se conecta a él por
`http://host.docker.internal:11434/v1`.

## macOS

```bash
brew install uv git
brew install --cask ollama docker-desktop  # o la app OrbStack
brew install tesseract tesseract-lang      # OCR, con el paquete de idiomas
```

Abra la aplicación Ollama una vez para que quede corriendo.

## Windows

```powershell
winget install --id astral-sh.uv
winget install --id Git.Git
winget install --id Ollama.Ollama
winget install --id Docker.DockerDesktop     # requiere WSL 2
winget install --id UB-Mannheim.TesseractOCR
```

- Tesseract: en el instalador marque el idioma **Spanish**, y agregue la carpeta de instalación
  (por ejemplo `C:\Program Files\Tesseract-OCR`) a la variable `PATH`.
- Ollama usa la GPU NVIDIA automáticamente; sin GPU, funciona con el procesador, más lento.

## Linux (Ubuntu)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://ollama.com/install.sh | sh
sudo apt install git docker.io tesseract-ocr tesseract-ocr-spa
```

En Linux, `host.docker.internal` no existe por defecto: al correr un contenedor que use Ollama,
agregue `--add-host=host.docker.internal:host-gateway` (en `docker-compose.yml`:
`extra_hosts: ["host.docker.internal:host-gateway"]`).

## Qué modelo descargar según la memoria de su equipo

| Memoria (RAM, o unificada en Mac) | Modelo de chat | Visión (sesión 11) |
|---|---|---|
| 8 GB | `qwen3:1.7b` | Proveedor comercial, o solo Tesseract |
| 16 GB | `qwen3:4b-instruct` | `qwen2.5vl:3b` |
| 24 GB o más | `qwen3:14b` | `qwen2.5vl:7b` |

Todos usan el mismo modelo de embeddings: `qwen3-embedding:0.6b`. Con poca memoria, cierre Docker
y el navegador mientras prueba el modelo: el modelo, el sistema y sus programas comparten la misma
memoria.

```bash
ollama pull qwen3:4b-instruct              # el de su tamaño
ollama run qwen3:4b-instruct "Hola, responde en una frase"
```

En su `.env` (copia de `.env.example`), ponga el modelo que descargó:

```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:4b-instruct
```

Los modelos Qwen3 y gpt-oss pueden "pensar" antes de responder, lo que multiplica el tiempo de
respuesta. El kit lo desactiva por defecto (`OLLAMA_REASONING=none` en `.env`). Por eso el modelo
de 16 GB es `qwen3:4b-instruct` y no `qwen3:4b`: este último siempre razona y tarda unas diez veces
más.

Y ejecute cargando ese archivo: `uv run --env-file .env uvicorn asistente.api.main:app --reload`.

## Sin equipo para modelos locales

- Siga con `LLM_PROVIDER=fake`: todos los talleres y pruebas funcionan.
- O use un proveedor comercial con su llave (`LLM_PROVIDER=openai` o `anthropic` en `.env`).
  Ponga un **límite de gasto** en el panel del proveedor y nunca suba el `.env` a Git.

## Dev Container y Codespaces

El repositorio trae un Dev Container (`.devcontainer/`) con Python, uv, Docker y Tesseract.
Ollama **no** va adentro: instálelo en su equipo como se explica arriba; el contenedor ya está
configurado para encontrarlo en `host.docker.internal`.

GitHub Codespaces corre en la nube y no puede ver el Ollama de su equipo: ahí use
`LLM_PROVIDER=fake` o un proveedor comercial.

## Verificar todo

```bash
uv --version
git --version
curl http://localhost:11434/v1/models     # lista los modelos de Ollama
tesseract --list-langs                    # debe incluir spa
docker run --rm hello-world               # desde la sesión 7
```

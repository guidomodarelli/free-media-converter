#!/bin/bash
# Quick start script for Free Media Converter Web Interface

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🎵🎬 Free Media Converter - Web Interface"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "💡 Instala Python 3 y vuelve a intentar"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    echo "💡 Instala Node.js (https://nodejs.org) y vuelve a intentar"
    exit 1
fi

echo "📦 Instalando dependencias de Node.js (MediaBunny)..."
(cd "$ROOT_DIR" && npm install)

# Check if virtual environment exists
if [ ! -d "$ROOT_DIR/.venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv "$ROOT_DIR/.venv"
fi

# Activate virtual environment and install dependencies
echo "📦 Instalando dependencias de Python..."
source "$ROOT_DIR/.venv/bin/activate"
pip install -r "$ROOT_DIR/requirements.txt"

echo ""
echo "🌐 Iniciando servidor web..."
echo "📍 La aplicación estará disponible en: http://localhost:5001"
echo "🛑 Presiona Ctrl+C para detener el servidor"
echo ""

cd "$ROOT_DIR/web"
python app.py

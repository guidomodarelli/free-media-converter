#!/usr/bin/env python3
"""
Free Media Converter - Web Interface
Interfaz web para convertir archivos de audio y video usando MediaBunny.
"""

import os
import sys
import json
import uuid
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for

# Importar funciones del CLI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import (
    check_mediabunny,
    get_supported_audio_formats,
    get_supported_video_formats,
    convert_media,
    detect_media_type
)

app = Flask(__name__)
app.secret_key = 'free_media_converter_secret_key_2025'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Configuración de directorios
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Formatos permitidos
ALLOWED_AUDIO_EXTENSIONS = get_supported_audio_formats() + ['mp2', 'au', 'aiff', 'ra']
ALLOWED_VIDEO_EXTENSIONS = get_supported_video_formats() + ['3gp', 'mpg', 'mpeg', 'ogv', 'divx']
ALLOWED_EXTENSIONS = ALLOWED_AUDIO_EXTENSIONS + ALLOWED_VIDEO_EXTENSIONS


def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_info(filepath):
    """Obtiene información del archivo."""
    if not os.path.exists(filepath):
        return None

    stat = os.stat(filepath)
    return {
        'size': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'type': detect_media_type(filepath)
    }


@app.route('/')
def index():
    """Página principal."""
    # Verificar MediaBunny/Node
    mediabunny_available = check_mediabunny()

    formats = {
        'audio': get_supported_audio_formats(),
        'video': get_supported_video_formats()
    }

    return render_template('index.html',
                         mediabunny_available=mediabunny_available,
                         formats=formats)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Maneja la subida de archivos."""
    if 'file' not in request.files:
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    if file and allowed_file(file.filename):
        # Generar nombre único
        file_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{file_id}.{file_extension}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Obtener información del archivo
        file_info = get_file_info(filepath)

        return jsonify({
            'success': True,
            'file_id': file_id,
            'original_name': original_filename,
            'filename': filename,
            'file_info': file_info
        })

    return jsonify({'error': 'Tipo de archivo no permitido'}), 400


@app.route('/convert', methods=['POST'])
def convert_file():
    """Convierte el archivo al formato especificado."""
    data = request.get_json()

    file_id = data.get('file_id')
    output_format = data.get('format')
    quality = data.get('quality', '192k')

    if not file_id or not output_format:
        return jsonify({'error': 'Parámetros faltantes'}), 400

    # Buscar el archivo de entrada
    input_file = None
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith(file_id):
            input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            break

    if not input_file or not os.path.exists(input_file):
        return jsonify({'error': 'Archivo no encontrado'}), 404

    # Generar nombre del archivo de salida
    output_filename = f"{file_id}_converted.{output_format}"
    output_file = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)

    try:
        # Realizar la conversión
        success = convert_media(input_file, output_file, output_format, quality)

        if success:
            # Obtener información del archivo convertido
            output_info = get_file_info(output_file)

            return jsonify({
                'success': True,
                'output_file': output_filename,
                'output_info': output_info,
                'download_url': url_for('download_file', filename=output_filename)
            })
        else:
            return jsonify({'error': 'Error durante la conversión'}), 500

    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Permite descargar el archivo convertido."""
    filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'Archivo no encontrado'}), 404

    # Obtener el nombre original sin el prefijo del ID
    display_name = filename.split('_converted.', 1)
    if len(display_name) == 2:
        display_name = f"converted.{display_name[1]}"
    else:
        display_name = filename

    return send_file(filepath, as_attachment=True, download_name=display_name)


@app.route('/status')
def status():
    """Verifica el estado del sistema."""
    return jsonify({
        'mediabunny_available': check_mediabunny(),
        'supported_formats': {
            'audio': get_supported_audio_formats(),
            'video': get_supported_video_formats()
        }
    })


@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    """Limpia archivos temporales."""
    try:
        # Limpiar uploads
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                os.remove(filepath)

        # Limpiar downloads más antiguos (opcional)
        # Por ahora solo reportamos éxito

        return jsonify({'success': True, 'message': 'Archivos temporales limpiados'})
    except Exception as e:
        return jsonify({'error': f'Error al limpiar: {str(e)}'}), 500


if __name__ == '__main__':
    if not check_mediabunny():
        print("⚠️  Advertencia: Node.js o MediaBunny no están instalados. La aplicación web no funcionará correctamente.")
        print("💡 Ejecuta npm install desde la raíz del proyecto.")

    print("🌐 Iniciando Free Media Converter Web Interface...")
    print("📍 Accede a: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)

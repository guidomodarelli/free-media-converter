#!/usr/bin/env python3
"""
Free Media Converter CLI
Convierte archivos de audio y video entre diferentes formatos usando MediaBunny.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONVERTER_SCRIPT = BASE_DIR / 'mediabunny_convert.mjs'


def check_mediabunny():
    """Verifica si Node.js y MediaBunny están disponibles en el entorno."""
    try:
        subprocess.run(['node', '-e', "require('mediabunny');"],
                       capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_supported_audio_formats():
    """Retorna los formatos de audio soportados."""
    return ['mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg']


def get_supported_video_formats():
    """Retorna los formatos de video soportados."""
    return ['mp4', 'mov', 'mkv', 'webm', 'm4v']


def get_all_supported_formats():
    """Retorna todos los formatos soportados (audio + video)."""
    return get_supported_audio_formats() + get_supported_video_formats()


def is_video_format(file_path):
    """Determina si un archivo es de video basándose en su extensión."""
    video_extensions = get_supported_video_formats() + ['3gp', 'asf', 'divx', 'f4v', 'm2v', 'mpg', 'mpeg', 'ogv', 'rmvb']
    extension = Path(file_path).suffix.lower().lstrip('.')
    return extension in video_extensions


def detect_media_type(file_path):
    """Determina si un archivo es de audio o video basándose en la extensión."""
    return 'video' if is_video_format(file_path) else 'audio'


def convert_media(input_file, output_file, output_format, quality='192k'):
    """
    Convierte un archivo de audio o video al formato especificado usando MediaBunny.

    Args:
        input_file (str): Ruta del archivo de entrada
        output_file (str): Ruta del archivo de salida
        output_format (str): Formato de salida
        quality (str): Calidad del audio/video
    """
    if not os.path.exists(input_file):
        print(f"❌ Error: El archivo '{input_file}' no existe.")
        return False

    media_type = detect_media_type(input_file)
    output_is_video = output_format.lower() in get_supported_video_formats()

    print(f"🔍 Detectado: {media_type}")
    print(f"🎯 Convirtiendo a: {'video' if output_is_video else 'audio'}")

    cmd = [
        'node',
        str(CONVERTER_SCRIPT),
        '--input',
        input_file,
        '--output',
        output_file,
        '--format',
        output_format.lower(),
        '--quality',
        quality,
    ]

    try:
        print(f"🔄 Convirtiendo '{input_file}' a '{output_file}' con MediaBunny...")
        subprocess.run(cmd, check=True)
        print("✅ Conversión completada exitosamente!")
        print(f"📁 Archivo guardado en: {output_file}")
        return True
    except FileNotFoundError:
        print("❌ Error: Node.js no está instalado o no se encuentra en el PATH.")
        return False
    except subprocess.CalledProcessError:
        print("❌ Error durante la conversión con MediaBunny. Revisa la salida anterior para más detalles.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="🎵🎬 Free Media Converter - Convierte archivos de audio y video usando MediaBunny",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Audio
  python run.py -i audio.wav -o audio.mp3
  python run.py -i song.flac -o song.mp3 -q 320k
  python run.py -i music.m4a -f wav

  # Video
  python run.py -i video.avi -f mp4
  python run.py -i movie.mkv -o movie.mp4 -q 720p
  python run.py -i clip.mov -f webm
        """
    )

    parser.add_argument('-i', '--input',
                       help='Archivo de audio o video de entrada')

    parser.add_argument('-o', '--output',
                       help='Archivo de salida (opcional)')

    parser.add_argument('-f', '--format',
                       choices=get_all_supported_formats(),
                       default='mp3',
                       help='Formato de salida (default: mp3)')

    parser.add_argument('-q', '--quality',
                       default='192k',
                       help='Calidad - bitrate para audio (192k) o resolución para video (720p)')

    parser.add_argument('--list-formats', action='store_true',
                       help='Mostrar formatos soportados')

    args = parser.parse_args()

    # Mostrar formatos soportados
    if args.list_formats:
        print("🎵 Formatos de audio soportados:")
        for fmt in get_supported_audio_formats():
            print(f"   • {fmt.upper()}")
        print("\n🎥 Formatos de video soportados:")
        for fmt in get_supported_video_formats():
            print(f"   • {fmt.upper()}")
        return

    # Verificar que se especifique archivo de entrada
    if not args.input:
        parser.error("Se requiere especificar un archivo de entrada (-i/--input)")
        return

    # Verificar que MediaBunny esté disponible
    if not check_mediabunny():
        print("❌ Error: Node.js o MediaBunny no están disponibles en el entorno.")
        print("💡 Instala Node.js (>=18) y ejecuta desde la raíz del proyecto:")
        print("   npm install")
        sys.exit(1)

    input_file = args.input
    output_format = args.format.lower()

    # Generar nombre de archivo de salida si no se especifica
    if args.output:
        output_file = args.output
    else:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix(f'.{output_format}'))

    # Realizar la conversión
    success = convert_media(input_file, output_file, output_format, args.quality)

    if success:
        # Mostrar información del archivo resultante
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            size_mb = size / (1024 * 1024)
            print(f"📊 Tamaño del archivo: {size_mb:.2f} MB")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

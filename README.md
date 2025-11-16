# 🎵🎬 Free Media Converter

**Free Media Converter** es una herramienta de línea de comandos ligera y fácil de usar que te permite convertir archivos de **audio y video** entre distintos formatos aprovechando el motor moderno de [MediaBunny](https://mediabunny.dev/guide/introduction), basado en WebCodecs y compatible con Node.js.

Diseñado para usuarios que buscan una solución rápida y flexible, este script en Python ofrece:

* 🎧 Conversión entre formatos de audio populares (MP3, WAV, FLAC, AAC, M4A, OGG)
* 🎥 Soporte para formatos de video comunes (MP4, MOV, MKV, WebM, M4V)
* ⚙️ Control de calidad mediante bitrate
* 🚫 Manejo de errores automático y verificación de dependencias
* 🖥️ Interfaz CLI intuitiva para flujos de trabajo rápidos y eficientes

Ideal para creadores de contenido, desarrolladores, podcasters y cualquier persona que necesite convertir medios sin complicaciones.

## 📋 Requisitos

- Python 3.6+
- Node.js 18+ (incluye npm)
- Ejecuta `npm install` en la raíz del repositorio para instalar MediaBunny

### Instalación de Node.js y dependencias

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# Fedora/Red Hat
sudo dnf install nodejs npm

# Arch Linux
sudo pacman -S nodejs npm

# macOS (con Homebrew)
brew install node

# Instalar dependencias de Node (MediaBunny)
npm install
```

### Instalación de dependencias Python

```bash
# Para uso de CLI únicamente (sin dependencias adicionales)
python run.py --help

# Para usar la interfaz web
pip install -r requirements.txt
```

## 🚀 Uso

> **Nota:** Ejecuta `npm install` desde la raíz del repositorio antes de usar la CLI o la interfaz web para que MediaBunny esté disponible.

### 🖥️ Línea de comandos (CLI)

#### Ejemplos básicos

##### 🎵 Conversión de Audio
```bash
# Convertir WAV a MP3 (calidad predeterminada 192k)
python run.py -i audio.wav -o audio.mp3

# Convertir FLAC a MP3 con alta calidad
python run.py -i song.flac -o song.mp3 -q 320k

# Convertir M4A a WAV (sin especificar archivo de salida)
python run.py -i music.m4a -f wav

# Convertir con calidad específica
python run.py -i audio.wav -f mp3 -q 128k
```

##### 🎥 Conversión de Video
```bash
# Convertir AVI a MP4
python run.py -i video.avi -f mp4

# Convertir MKV a MP4 con resolución específica
python run.py -i movie.mkv -o movie.mp4 -q 720p

# Convertir MOV a WebM para web
python run.py -i presentation.mov -f webm
```

### 🌐 Interfaz Web

> Antes de iniciar la interfaz web, asegúrate de haber ejecutado `npm install` en la raíz del proyecto para instalar MediaBunny.

Para usuarios que prefieren una interfaz gráfica, también incluimos una aplicación web moderna y fácil de usar:

#### Inicio rápido
```bash
# Opción 1: Script automático (Linux/macOS)
cd web
./start.sh

# Opción 2: Manual
pip install -r requirements.txt
cd web
python app.py
```

Luego abre tu navegador en: **http://localhost:5001**

#### Características de la interfaz web:
- 🎨 **Diseño moderno** con Bootstrap y animaciones suaves
- 📱 **Totalmente responsive** - funciona en móviles y tablets
- 🖱️ **Drag & drop** - arrastra archivos directamente
- 📊 **Información en tiempo real** del archivo y progreso
- 🎯 **Selección visual** de formatos de audio y video
- ⚙️ **Control de calidad** con opciones predefinidas
- 📥 **Descarga directa** del archivo convertido
- 🚫 **Manejo de errores** con mensajes claros

### 📋 Opciones de CLI

```
-i, --input       Archivo de audio o video de entrada (requerido)
-o, --output      Archivo de salida (opcional)
-f, --format      Formato de salida (default: mp3)
-q, --quality     Calidad - bitrate para audio (192k) o resolución para video (720p)
--list-formats    Mostrar formatos soportados
-h, --help        Mostrar ayuda
```

### Formatos soportados

#### 🎵 Audio
- **MP3** - MPEG Audio Layer III
- **WAV** - Waveform Audio File Format
- **FLAC** - Free Lossless Audio Codec
- **AAC** - Advanced Audio Coding
- **M4A** - MPEG-4 Audio
- **OGG** - Ogg Vorbis
#### 🎥 Video
- **MP4** - MPEG-4 Video
- **MKV** - Matroska Video
- **MOV** - QuickTime Movie
- **WebM** - Web Media Format
- **M4V** - iTunes Video

### Calidades recomendadas

#### 🎵 Audio (Bitrate)
- **128k** - Calidad básica (archivos pequeños)
- **192k** - Calidad estándar (predeterminado)
- **256k** - Calidad alta
- **320k** - Calidad muy alta (MP3 máxima)

#### 🎥 Video (Resolución)
- **480p** - Calidad básica (SD)
- **720p** - Calidad HD (predeterminado)
- **1080p** - Calidad Full HD
- **1440p** - Calidad 2K
- **2160p** - Calidad 4K Ultra HD

## 📁 Ejemplos de conversión

```bash
# Convertir toda una carpeta (requiere script adicional)
for file in *.wav; do
    python run.py -i "$file" -f mp3 -q 320k
done

# Convertir con nombre automático
python run.py -i cancion.flac -f mp3  # Resultado: cancion.mp3

# Especificar archivo de salida
python run.py -i entrada.wav -o salida_custom.mp3
```

## 🔍 Verificación

El script verificará automáticamente:
- ✅ Si Node.js y las dependencias de MediaBunny están instaladas
- ✅ Si el archivo de entrada existe
- ✅ Si la conversión fue exitosa
- 📊 Tamaño del archivo resultante

## 🐛 Solución de problemas

### Node.js o MediaBunny no disponibles
```
❌ Error: Node.js o MediaBunny no están disponibles en el entorno.
```
**Solución:** Instala Node.js (>=18) y vuelve a ejecutar `npm install` en la raíz del repositorio antes de lanzar la CLI o la interfaz web.

### Archivo no encontrado
```
❌ Error: El archivo 'archivo.wav' no existe.
```
**Solución:** Verifica la ruta del archivo de entrada.

### Error de conversión
Si hay errores durante la conversión, revisa la salida que genera MediaBunny (aparece en la terminal o en los logs del servidor web) para identificar el codec o la opción que requiere ajuste.

## 🎯 Características

- ✨ **Doble interfaz**: CLI para usuarios avanzados y Web para facilidad de uso
- 🎵 Conversión completa entre formatos de audio (6 formatos)
- 🎥 Conversión completa entre formatos de video (5 formatos)
- 🔍 Detección automática del tipo de media (audio/video)
- ⚙️ Control de calidad/bitrate para audio y resolución para video
- 📊 Información del archivo resultante con tamaño
- ❌ Manejo de errores robusto y verificación automática
- 🔧 Impulsado por MediaBunny (WebCodecs + Node) para conversiones modernas y multiplataforma
- 🌐 Interfaz web moderna con drag & drop
- 📱 Diseño responsive que funciona en todos los dispositivos
- 🚀 Perfecto para creadores de contenido, desarrolladores y podcasters

## 🗺️ Roadmap

### ✅ Versión 1.0 (Actual)
- [x] Conversión de formatos de audio
- [x] Conversión de formatos de video
- [x] Control de calidad/bitrate para audio
- [x] Control de resolución para video
- [x] Detección automática de tipo de media
- [x] Interfaz CLI completa
- [x] Manejo de errores robusto
- [x] Interfaz web moderna y responsive
- [x] Drag & drop para subida de archivos
- [x] Descarga directa de archivos convertidos

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

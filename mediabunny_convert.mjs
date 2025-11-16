#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {
    ALL_FORMATS,
    AdtsOutputFormat,
    Conversion,
    FilePathSource,
    FilePathTarget,
    FlacOutputFormat,
    Input,
    MkvOutputFormat,
    Mp3OutputFormat,
    Mp4OutputFormat,
    MovOutputFormat,
    OggOutputFormat,
    Output,
    WebMOutputFormat,
    WaveOutputFormat,
} from 'mediabunny';

const AUDIO_FORMATS = new Set(['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a']);
const VIDEO_FORMATS = new Set(['mp4', 'mov', 'mkv', 'webm', 'm4v']);

const FORMAT_BUILDERS = {
    mp4: () => new Mp4OutputFormat(),
    mov: () => new MovOutputFormat(),
    mkv: () => new MkvOutputFormat(),
    webm: () => new WebMOutputFormat(),
    m4v: () => new Mp4OutputFormat(),
    mp3: () => new Mp3OutputFormat(),
    wav: () => new WaveOutputFormat(),
    flac: () => new FlacOutputFormat(),
    ogg: () => new OggOutputFormat(),
    aac: () => new AdtsOutputFormat(),
    m4a: () => new Mp4OutputFormat(),
};

const AUDIO_CODECS = {
    mp3: 'mp3',
    wav: 'pcm-s16',
    flac: 'flac',
    ogg: 'vorbis',
    aac: 'aac',
    m4a: 'aac',
};

const VIDEO_AUDIO_CODEC = {
    mp4: 'aac',
    mov: 'aac',
    mkv: 'aac',
    webm: 'opus',
    m4v: 'aac',
};

function parseArgs(argv) {
    const params = {};

    for (let i = 2; i < argv.length; i += 1) {
        const token = argv[i];
        if (!token.startsWith('--')) {
            continue;
        }

        const key = token.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
            params[key] = true;
        } else {
            params[key] = next;
            i += 1;
        }
    }

    return params;
}

function parseBitrate(value) {
    if (!value || typeof value !== 'string') {
        return undefined;
    }

    const normalized = value.trim().toLowerCase();
    const match = normalized.match(/^(\d+)(k(?:bps)?)?$/i);
    if (!match) {
        return undefined;
    }

    const base = Number(match[1]);
    if (Number.isNaN(base)) {
        return undefined;
    }

    return match[2] ? base * 1000 : base;
}

function parseVideoHeight(value) {
    if (!value || typeof value !== 'string') {
        return undefined;
    }

    const normalized = value.trim().toLowerCase();
    const match = normalized.match(/^(\d+)p$/i);
    if (!match) {
        return undefined;
    }

    return Number(match[1]);
}

function printUsage() {
    console.log('Usage: node mediabunny_convert.mjs --input <path> --output <path> --format <format> [--quality <quality>]');
    console.log('Supported formats:', Object.keys(FORMAT_BUILDERS).join(', '));
}

function ensureFileExists(filepath) {
    if (!fs.existsSync(filepath)) {
        throw new Error(`El archivo de entrada no existe: ${filepath}`);
    }
}

function buildAudioOptions(format, quality, isVideo) {
    const options = {};
    const codec = isVideo ? VIDEO_AUDIO_CODEC[format] ?? 'aac' : AUDIO_CODECS[format] ?? 'aac';
    if (codec) {
        options.codec = codec;
    }

    const bitrate = parseBitrate(quality);
    if (bitrate) {
        options.bitrate = bitrate;
    }

    return options;
}

function buildVideoOptions(format, quality) {
    const options = {
        fit: 'contain',
    };

    const height = parseVideoHeight(quality);
    if (height) {
        options.height = height;
    }

    return options;
}

async function main() {
    const params = parseArgs(process.argv);

    const input = params.input;
    const output = params.output;
    const format = params.format?.toLowerCase();
    const quality = params.quality || '192k';

    if (!input || !output || !format) {
        printUsage();
        process.exit(1);
    }

    const builder = FORMAT_BUILDERS[format];
    if (!builder) {
        console.error(`Formato no soportado: ${format}`);
        printUsage();
        process.exit(1);
    }

    ensureFileExists(input);

    const absoluteInput = path.resolve(input);
    const absoluteOutput = path.resolve(output);

    const source = new FilePathSource(absoluteInput);
    const inputHandle = new Input({
        source,
        formats: ALL_FORMATS,
    });

    if (fs.existsSync(absoluteOutput)) {
        fs.unlinkSync(absoluteOutput);
    }

    const outputHandle = new Output({
        format: builder(),
        target: new FilePathTarget(absoluteOutput),
    });

    const isVideoFormat = VIDEO_FORMATS.has(format);

    const conversionOptions = {
        input: inputHandle,
        output: outputHandle,
        video: isVideoFormat ? buildVideoOptions(format, quality) : { discard: true },
        audio: buildAudioOptions(format, quality, isVideoFormat),
    };

    const conversion = await Conversion.init(conversionOptions);

    if (!conversion.isValid) {
        console.error('La conversión no es válida para el archivo y formato solicitados.');
        await inputHandle.dispose();
        process.exit(1);
    }

    let lastProgress = -1;
    conversion.onProgress = (progress) => {
        const percent = Math.round(progress * 100);
        if (percent !== lastProgress) {
            lastProgress = percent;
            console.log(`🔁 Progreso: ${percent}%`);
        }
    };

    await conversion.execute();
    await outputHandle.finalize();
    await inputHandle.dispose();

    console.log('✅ Conversión completada.');
}

main().catch((error) => {
    console.error('❌ Error:', error);
    process.exit(1);
});

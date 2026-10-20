---
title: Generación manual de canciones con ElevenLabs Music
created: 2026-10-20
updated: 2026-10-20
type: runbook
tags: [sistema, runbook, pipeline]
status: active
confidence: high
related: [ttchop-video-generation, ttchop-automatizaciones, ttchop-webapps]
---

# Generación manual de canciones con ElevenLabs Music

Esta guía documenta la prueba de canción enviada manualmente a ElevenLabs Music
por un proceso Node ejecutado en el directorio `ttchop-server` del VPS; no es una
función ni un endpoint del servidor. Es una generación de audio independiente:
no modifica el servidor, no incorpora audio a un video y no publica nada. Para
voz hablada/narración, el pipeline usa Text-to-Speech (`/v1/text-to-speech/{voiceId}`
con `eleven_v3`); eso no es canto. La prueba de canto usó el endpoint Music
`/v1/music`. El código vivo de `ttchop-server` no tiene endpoint Music ni uso de
`music_v2_5`.

## Procedimiento reutilizable

1. Aclara la idea, audiencia, idioma, tono y uso previsto. Pulir una letra
   original y obtener aprobación explícita de su contenido antes de generar.
2. Indica cuántas tomas se proponen y confirma autorización explícita de Arturo
   para ese número y el gasto de créditos. No generes tomas adicionales sin
   nueva autorización.
3. Para controlar letra y secciones, usa `composition_plan`; no lo combines con
   `prompt`. Incluye la letra y etiquetas de sección como `[Chorus]` en `text`.
   Escribe instrucciones de estilo descriptivas en inglés y la letra en el idioma
   elegido (en el ejemplo de prueba, japonés).
4. Define `duration_ms` por chunk y usa `context_adherence: 'high'`. La duración
   permitida por chunk es 3–120 s y el plan completo admite hasta 10 min. Haz una
   solicitud por toma. Para comparar tomas, conserva letra, duración y tempo y
   cambia solo detalles de arreglo.
5. Recibe la respuesta como bytes de audio, no como JSON. Guarda cada MP3
   temporalmente fuera de carpetas versionadas; registra solo status,
   content-type, song ID y cantidad de bytes.
6. Haz QA de cada archivo (ver abajo), escucha y entrega cada MP3 individual,
   claramente etiquetado. No montes el audio en video ni lo publiques sin
   solicitud y OK explícitos.

El siguiente ejemplo ilustra la forma de la petición; los valores estilísticos
son editables. Ejecutarlo solo después del gate de autorización de créditos.
Desde el repo del servidor, `import 'dotenv/config'` carga el entorno local. No
muestres, imprimas ni copies el valor de la clave. Pasa el bloque como stdin a
Node ESM desde `/root/projects/ttchop/ttchop-server`, con una ruta de salida única
como argumento (por ejemplo, `node --input-type=module - /root/.cache/ttchop-robot/take-01.mp3`).

```js
import 'dotenv/config';
import { writeFileSync } from 'node:fs';

const outputPath = process.argv[2]; // usa una ruta única fuera del repo
if (!process.env.ELEVENLABS_API_KEY || !outputPath) {
  throw new Error('Falta ELEVENLABS_API_KEY del entorno o ruta de salida');
}

const response = await fetch('https://api.elevenlabs.io/v1/music', {
  method: 'POST',
  headers: {
    'xi-api-key': process.env.ELEVENLABS_API_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model_id: 'music_v2_5',
    composition_plan: {
      chunks: [{
        positive_styles: [
          'high-energy electropop, dance-pop, and funk',
          'bright luminous synths with a catchy hook',
          'steady dance beat at 126 BPM',
          'bouncy bass and crisp funk guitar',
          'confident uplifting female lead singing in Japanese',
          'rhythmic phrasing and layered backing harmonies',
        ],
        negative_styles: ['slow ballad', 'dark mood', 'acoustic-only', 'spoken narration'],
        text: '[Chorus]\nブレない私、もう止まらない\n新しいピアス、光るサイン\n声を上げれば、広がる未来\n私の一歩で、明日を変えたい',
        duration_ms: 16000,
        context_adherence: 'high',
      }],
    },
  }),
});

if (!response.ok) throw new Error(`ElevenLabs Music HTTP ${response.status}`);
const bytes = Buffer.from(await response.arrayBuffer());
if (!bytes.length) throw new Error('ElevenLabs devolvió audio vacío');
writeFileSync(outputPath, bytes);
console.log({
  status: response.status,
  contentType: response.headers.get('content-type'),
  songId: response.headers.get('song-id'),
  bytes: bytes.length,
});
```

## QA y resguardo

- Confirma que la respuesta HTTP fue exitosa y el `content-type` corresponde a
  audio; comprueba que los bytes no sean vacíos ni triviales.
- Ejecuta `ffprobe` en cada archivo y registra container/codec, duración, sample
  rate, canales y bitrate. La duración y metadata varían; no prometas un largo
  exacto. En la prueba documentada el MP3 fue 16.032 s, 48 kHz, estéreo y cerca
  de 192 kb/s, pero son datos de esa salida, no defaults garantizados.
- Para varios takes, compara hashes para confirmar archivos distintos. No afirmes
  que letra o pronunciación son correctas sin escuchar o contar con transcripción
  fiable.
- Mantén MP3 y temporales fuera del repo y carpetas versionadas. Nunca incluyas
  claves en argumentos, logs, chat o documentación.
- Usa letra original y entradas con derechos suficientes. Antes de cualquier uso
  comercial/promocional, revisa los términos vigentes de ElevenLabs aplicables al
  plan de Arturo y las reglas vigentes de TikTok Shop. Una suscripción pagada no
  concede por sí sola permiso universal. Este runbook documenta generación, no
  autorización para publicar o licenciar.

## Límite de integración con collage

`POST /collage/create` acepta `audioBase64` opcional para omitir su llamada TTS,
pero sigue requiriendo `voiceId`, `dialogue`, `sessions` y `renderId`; diálogo y
duración participan en la receta de edición. Esto es solo un hook, no una
integración Music probada. Antes de usarlo para canción hace falta validar el
flujo end-to-end, edición y continuidad; no hay alineación de sílabas como en
TTS. Consulta [[ttchop-video-generation]].

## Prueba de referencia

Se generó manualmente desde el servidor con la clave existente en el entorno, sin
añadir endpoint ni cambiar código. La toma inicial usó `music_v2_5`, un chunk
`[Chorus]` de 16 000 ms, `context_adherence: 'high'` y la letra japonesa de
cuatro líneas incluida en el ejemplo; esa letra era específica de una prueba
sobre aretes, no una letra genérica. Dos variaciones posteriores mantuvieron
letra, duración y tempo, cambiando detalles de arreglo (arpegios +
call-and-response frente a synth-brass + armonías por capas). Cada solicitud
respondió 200 con `audio/mpeg` y un song ID; las salidas se recibieron como bytes,
se validaron y tuvieron hashes distintos. Los MP3 se guardaron temporalmente
fuera del repo, se copiaron al scratch del perfil para verificación y se borraron
del VPS. No se conservaron assets en el repositorio.

## Fuentes oficiales consultadas el 2026-10-20

- [Music compose API](https://elevenlabs.io/docs/api-reference/music/compose)
- [Composition plans](https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans)
- [ElevenLabs Music Terms](https://elevenlabs.io/music-terms)

Vuelve a comprobar documentación, esquema y términos antes de futuras
solicitudes si pueden haber cambiado.

## Enlaces relacionados

- [[ttchop-video-generation]] — collage/render y separación de generación frente a publicación.
- [[ttchop-automatizaciones]] — pipeline y TTS hablado de TTChop.
- [[ttchop-webapps]] — contexto de las aplicaciones TTChop.

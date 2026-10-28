---
title: Traducir un video con PumaVoice y alinear inicio y fin de voz
created: 2026-10-29
updated: 2026-10-29
type: runbook
tags: [runbook, pipeline, cli]
status: active
confidence: high
related: [ttchop-video-generation, ttchop-raw-asset-manual-edit, transcripcion-curso-gerardo-santiago]
---

# Video traducido con PumaVoice, sin ElevenLabs Dubbing

Flujo aprobado por Arturo: **transcripción local → traducción del asistente → TTS con su voz existente → ajuste local del intervalo de habla → audio nuevo sobre el video original**. No intenta mover labios ni sincronizar cada fonema. No usa ElevenLabs Dubbing, Producer, Firestore ni publicación en TikTok. Para otros montajes consultar [[ttchop-raw-asset-manual-edit]] y [[ttchop-video-generation]]; el reconocimiento local compatible se documenta también en [[transcripcion-curso-gerardo-santiago]].

## Cuándo elegirlo y qué autorizar

Es una alternativa para un narrador cuya voz ya está disponible en ElevenLabs. Para varias personas, música mezclada o voces simultáneas hay que diseñar separación/segmentación; la prueba corta de esta página no valida esos casos. Sustituir la pista completa elimina también ambiente y música del audio original: conservarlos requiere otra operación.

Arturo aprobó la prueba de voz japonesa y después pidió alinear aproximadamente cuándo empieza y termina. Cada generación paga requiere alcance/presupuesto autorizados, cuota incluida suficiente y comprobación de cuenta/voz. Documentar o ajustar un audio ya generado **no autoriza otro POST pagado**. No habilitar recargas, extras o cambios de suscripción.

## 1. Transcribir y traducir el contenido real

1. Medir audio/video con ffprobe. Extraer audio y reconocerlo localmente con faster-whisper usando el entorno/modelo ya disponible, sin instalar STT en el Python global de Hermes.
2. Revisar que el reconocimiento corresponde al audio; traducir el significado al japonés sin añadir frases, ofertas o afirmaciones. Guardar los textos ES/JA y vincularlos al archivo fuente.
3. Ajustar la traducción para que sea natural y de extensión razonable. No es obligatorio igualar caracteres o sílabas entre idiomas. Revisar sentido antes de gastar en TTS; ASR automático posterior no reemplaza revisión humana.

Prueba del 2026-10-28:

- ES confirmado: «Esta es una prueba de audio para ver si podemos traducir el vídeo a otro idioma».
- Traducción propia JA: `これは、この動画を別の言語に翻訳できるか確認するための音声テストです。`
- Solo se envió ese texto a TTS; la traducción no se solicitó a Dubbing. Archivo fuente: `video_94afb2a10a9a.mp4`, aproximadamente 9.176 s, H.264 720×1280 y AAC.

## 2. Generar una vez con la voz existente

- Voz comprobada en la configuración de TTChop y con GET de ElevenLabs: **PumaVoice01**, voice ID `ve7BOdejheJbgrBriBx4`. Puma'sVoice/PumaVoice son nombres usados para referirse a esa voz; validar ID, acceso y nombre real antes de una tarea nueva, no crear otra voz ni clonarla.
- Modelo usado: `eleven_v3`; endpoint TTS de la prueba: `POST /v1/text-to-speech/{voice_id}`. Revisar documentación oficial vigente y compatibilidad de idioma/modelo antes de nuevas generaciones.
- La receta reutilizó settings de `ttchop-server/pipeline/elevenlabs.js`. Solo `stability: 0` quedó confirmado en historial; no afirmar que controles como `speed: 0.5` hayan sido aplicados por v3. **La velocidad final se ajustó con FFmpeg**, no con una nueva generación.
- Una única petición protegida por marcador exclusivo. Ante timeout de POST, investigar historial/request ID antes de repetir: una respuesta perdida no prueba que no se cobró.
- Cargar la clave únicamente en memoria mediante configuración existente; no escribirla en argumentos, comandos de ejemplo, archivos versionados o logs. Las consultas de cuenta se filtran para no publicar previews de claves.
- Registrar contadores antes/después, `character-cost`, request ID e historial individual. No presentar un delta de cuenta compartida como cargo exclusivo si otros agentes pueden generar a la vez.

## 3. Medir el intervalo de voz, no solo la duración del archivo

El primer mux puso voz japonesa desde 0 s con silencio al final. No coincidía con el hablante original: el video original tenía silencio inicial. Arturo pidió corregirlo sin volver a generar voz.

```bash
ffmpeg -hide_banner -i ORIGINAL.mp4 \
  -af silencedetect=noise=-32dB:d=0.12 -vn -f null -
ffmpeg -hide_banner -i VOZ_JA.mp3 \
  -af silencedetect=noise=-32dB:d=0.12 -f null -
```

Leer `silence_end` del silencio inicial y `silence_start` del silencio final para estimar inicio/fin de voz. Contrastar más de un umbral y revisar el audio: una respiración, ruido, consonante suave o música pueden falsear los límites. Las cifras son **estimaciones por umbral de amplitud**, no fronteras lingüísticas exactas. En material con ruido/música o varios segmentos usar revisión/VAD y alineación por tramos; no comprimir indiscriminadamente una narración larga.

Para el caso probado, umbral −32 dB:

| Pista | Inicio de voz | Fin de voz |
|---|---:|---:|
| Español original | 1.58048 s | 7.28501 s |
| Japonés final entregado | 1.58447 s | 7.34109 s |

Desviación medida: aproximadamente **4 ms al inicio y 56 ms al final**. Se conservó la cola suave de la voz japonesa; no cortar consonantes para que el detector marque exactamente el mismo tiempo. Arturo aprobó el resultado como «está perfecto».

## 4. Ajustar localmente y comprobar de nuevo

Guía de cálculo inicial: si el habla japonesa útil ocupa `D_ja` y el intervalo objetivo ocupa `D_original`, probar `atempo = D_ja / D_original`. Más de 1 acelera; menos de 1 ralentiza manteniendo aproximadamente el tono. Reposicionar con silencio inicial (`adelay`), completar silencio final (`apad`) y limitar el **contenedor completo**, no la voz antes de terminar. Si el ajuste es excesivo, revisar el guion o segmentar antes de aprobar una regeneración; no afirmar naturalidad con cualquier factor.

El codificador/filtro puede desplazar los límites observados. Se hizo una primera aproximación, se midió el MP4 exportado y se refinó reutilizando la misma voz. El primer factor `1.0237477934203167` NO es el aprobado final. En el resultado final:

- Se quitaron `0.04005514038842802 s` de entrada de la pista japonesa, margen anterior al inicio detectado, preservando el habla.
- Se limitó su tramo a `5.84 s` del archivo de audio con padding; esto elimina silencio sobrante, no contenido hablado.
- Factor local final `atempo=1.0048475497832565` (aproximadamente **0.485% más rápido**).
- `adelay=69479S` a 44100 Hz sitúa el audio en el intervalo del original. `S` significa **muestras**, no milisegundos; cambiar sample rate exige recalcularlo.
- Después se añadió silencio hasta la duración completa del video. No se usó `-shortest` para recortar voz.

### Receta exacta del montaje aprobado (solo este caso)

Los tiempos/factor/rate siguientes son los medidos de esta prueba; **no copiarlos como defaults para otros videos**. Volver a medir cada fuente. `VOZ_JA.mp3` es la pista de 44100 Hz guardada en esta prueba; `ORIGINAL.mp4` es el adjunto intacto.

```bash
ffmpeg -v error -n -i ORIGINAL.mp4 -i VOZ_JA.mp3 \
  -filter_complex '[1:a]atrim=start=0.040055140:end=5.84,asetpts=PTS-STARTPTS,atempo=1.004847549783,adelay=69479S:all=1,apad,atrim=duration=9.175556[a]' \
  -map 0:v:0 -map '[a]' -c:v copy -c:a aac -b:a 192k \
  -metadata:s:a:0 language=jpn -movflags +faststart VIDEO_JA_SINCRONIZADO.mp4
```

Solo se conserva el stream de imagen del original y el audio japonés nuevo. `-c:v copy` no recodifica ni acelera el video. `atempo` modifica únicamente el audio. El audio original permanece dentro del archivo fuente intacto.

## 5. Verificación y evidencia

```bash
ffmpeg -v error -xerror -i VIDEO_JA_SINCRONIZADO.mp4 -f null -
ffprobe -v error -show_streams -show_format -of json VIDEO_JA_SINCRONIZADO.mp4
ffmpeg -v error -i ORIGINAL.mp4 -map 0:v:0 -c:v copy \
  -f streamhash -hash sha256 -
ffmpeg -v error -i VIDEO_JA_SINCRONIZADO.mp4 -map 0:v:0 -c:v copy \
  -f streamhash -hash sha256 -
```

Repetir silencedetect en la **salida final** y comparar con la fuente. Verificar duración, presencia del audio japonés, que no queda el español mezclado y decodificación íntegra. Comparar bitstream de video, no hash del MP4 entero (el contenedor y el audio cambiaron).

- Bitstream H.264 original/final: SHA-256 `4013bfd079d1d8afe1bc4b2cf25257899f9cec21d3c891159e012dbce7418b59`.
- Final `video_ja_sincronizado.mp4`: 4 977 530 bytes, SHA-256 `a780fda4eefdcd0661ad13f0fc28c58399c83543fc8d500f06081fbc21278ebf`; duración aproximada 9.177 s; H.264 720×1280 + AAC japonés, full decode correcto.
- ASR japonés de la generación inicial fue coherente con el texto traducido; no se presenta como certificación humana. La alineación posterior solo reutilizó ese audio y fue aprobada por Arturo.

## Créditos: medición de esta prueba, no tarifa universal

Una generación TTS cobró **14 créditos incluidos**, confirmados por `character-cost: 14` e historial individual 4250→4264. Request ID `3TBsYrrrQfOJvyaOnWTU`, history ID `qplRy1hKcIYC7STDKmEI`. Overage reportado US$0; extras no habilitados. El ajuste local de tiempos no hizo otra llamada pagada.

La prueba anterior con Dubbing v2 registró aumento de cuenta de **1682 créditos**. La comparación con 14 créditos sirve para **estas dos pruebas del mismo clip**, no demuestra un precio fijo por minuto ni ahorro universal. No confundir consumo incluido, cambio de contador y factura en dólares.

## Rutas y alcance operativo

Workspace temporal: `/root/.hermes/cache/scratch/elevenlabs-pumasvoice-ja-test/`, con `text_es.txt`, `text_ja.txt`, `tts_ja_original.mp3`, `audio_ja.mp3`, `video_ja_sincronizado.mp4`, `timing_alignment.json`, `RESULTADO.md` y evidencias de consumo. Scratch puede limpiarse; la receta y resultados esenciales quedan conservados en esta página. `timing_alignment.json` conserva también valores de una iteración anterior; usar `final_path` y `final_atempo` para la versión aprobada.

`verify_tts_get_only.py` consulta historial/suscripción sin generar; no volver a ejecutar `generate_once.py` para una verificación. La documentación del 2026-10-29 no generó voces ni movió archivos al NAS. Se entregó MP4 por Telegram, sin publicación, cambios de pipeline o integración automática. La sincronización lograda es **del inicio/fin del habla**, no de labios o palabras individuales.

/**
 * Divide un texto en chunks para respetar el límite de caracteres de Telegram (4096)
 * Limpia caracteres problemáticos y comillas especiales
 * @param {string} texto - Texto a dividir
 * @param {number} maxChars - Máximo de caracteres por mensaje (default: 4096)
 * @returns {array} Array de strings, cada uno <= maxChars y limpio
 */
function splitForTelegram(texto, maxChars = 4096) {
  // Limpia caracteres problemáticos
  texto = texto
    .replace(/"/g, '"')  // Comillas dobles curvas → rectas
    .replace(/'/g, "'")  // Comillas simples curvas → rectas
    .replace(/[""'']/g, '') // Quita comillas especiales
    .replace(/[^\w\s\n\.\,\:\;\!\?\-\(\)]/g, '') // Quita caracteres ASCII especiales
    .replace(/\s+/g, ' ') // Espacios múltiples → 1 espacio
    .trim();

  if (texto.length <= maxChars) {
    return [texto];
  }

  const chunks = [];
  const lineas = texto.split('\n');
  let chunk = '';

  for (const linea of lineas) {
    if ((chunk + linea + '\n').length > maxChars) {
      if (chunk) chunks.push(chunk.trim());
      chunk = linea + '\n';
    } else {
      chunk += linea + '\n';
    }
  }

  if (chunk) chunks.push(chunk.trim());
  return chunks;
}

module.exports = { splitForTelegram };

/**
 * USAGE EN N8N:
 *
 * 1. Function Node (después de Claude API):
 * ────────────────────────────────────────
 * const { splitForTelegram } = require('./utils/splitForTelegram.js');
 * const respuestaClaudeCompleta = items[0].json.response.content[0].text;
 * const mensajes = splitForTelegram(respuestaClaudeCompleta, 4096);
 * return [{ json: { mensajes: mensajes } }];
 *
 * 2. Loop Node:
 * ────────────────────────────────────────
 * Loop over: {{ $node['Function'].json.mensajes }}
 *
 * 3. Dentro del Loop - Telegram Send Message:
 * ────────────────────────────────────────
 * Message: {{ $item().json }}
 */

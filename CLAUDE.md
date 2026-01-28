# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Cacho** is a personal assistant system built around an N8N workflow. It tracks and manages multiple activity categories: Gym training, Meditation practice, Nutrition, and Options trading. The system integrates with Telegram and Claude AI to provide intelligent command parsing and message handling.

## Architecture

### Core Structure

The project uses a simple, file-based data storage approach:

- **`utils/`**: Shared utility functions used in N8N workflows
  - `parseNota.js`: Parses `/not{category} note` commands to extract category and note content
  - `splitForTelegram.js`: Chunks text for Telegram's 4096-character message limit
- **`data/`**: JSON-based persistent storage organized by activity category
  - `gym/`: Gym training sessions (historial.json for records, notas.json for notes)
  - `meditacion/`: Meditation sessions (same structure)
  - `nutricion/`: Nutrition tracking (same structure)
  - `options/`: Options trading trades (historial.json for records, notas.json for notes)

### Data Model

Each category follows the same pattern:

- **historial.json**: Array of timestamped records with activity details
  - Gym: includes fecha, dia_semana, tipo_entrenamiento, duracion_minutos, ejercicios array with sets and reps
  - Meditation: includes fecha, hora, tipo, duracion_minutos, tecnicas array, sensaciones, profundidad, notas
  - Nutrition: follows similar timestamped record structure
  - Options: includes fecha_apertura, simbolo, tipo_contrato, strike, expiration_date, premium_recibido, margen_requerido, pl_bruto, pl_porcentaje, estado
- **notas.json**: Array of timestamped notes associated with that category

### N8N Integration

The utilities are designed to be used as Function Nodes in N8N workflows:

1. **parseNota**: Triggered by Telegram messages starting with `/not` to route notes to correct category folder
   - Maps abbreviations: `gym`, `med`→meditacion, `nut`→nutricion, `opt`→options, `tra`→trading, `inv`→inversiones
   - Returns parsed object with error handling

2. **splitForTelegram**: Post-processes Claude AI responses before sending to Telegram
   - Cleans problematic characters (smart quotes, special characters)
   - Chunks text by character position to preserve word boundaries when possible
   - Returns array of messages, each ≤4096 characters

## Common Commands

This is a data + utilities project without build/test infrastructure. Work primarily involves:

- **Adding new utilities**: Create new .js files in `utils/` with module.exports
- **Extending data schema**: Modify notas.json or historial.json structure in specific category folders
- **Adding new categories**: Create `data/{categoria}/historial.json` and `data/{categoria}/notas.json`
- **Git commits**: Follow conventional commit format (examples: "Add parseNota utility", "Fix splitForTelegram character handling")

## Key Implementation Details

### parseNota Behavior

- Uses regex `/^\/not(\w+)\s+(.*)/i` to extract category abbreviation and note text
- Category abbreviations are case-insensitive
- Returns error object if format doesn't match or category not found
- Always returns `carpetaGit` field pointing to the correct notas.json file for that category

### splitForTelegram Behavior

- Character cleaning happens before length check (removes curly quotes, other problematic chars)
- Splits by character position, not line breaks
- Attempts to break at spaces for readability but requires space to be >50% of max length into chunk
- Returns trimmed chunks to avoid leading/trailing whitespace in messages

### Data Format Conventions

- Dates use ISO format: `"fecha": "2024-01-26"`
- Time uses 24-hour format: `"hora": "21:30"`
- Spanish is used for field names and UI-facing content
- JSON files are always arrays, even if single records
- Numeric fields (peso_kg, reps, duracion_minutos) are stored as numbers not strings

## Future Category Support

The codebase is structured to support additional categories beyond the initial three:
- `trading`: Already mapped in parseNota abbreviation `tra`
- `inversiones`: Already mapped in parseNota abbreviation `inv`
- Custom categories can be added by extending the categorias object in parseNota and creating corresponding data directories

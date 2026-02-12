# 📊 Contexto de Trading de Opciones

## Objetivos y Estrategia

| Parámetro | Valor |
|-----------|-------|
| **Objetivo** | Generar ingresos semanales vendiendo puts, y ganancias adicionales con covered calls |
| **Estrategia** | Sell Puts Semanales + Covered Call (si asignan) |
| **Presupuesto** | 3,000 USD |
| **Broker** | Webull |
| **Meta** | $300-500/mes (5-8% mensual) |

---

## 🎡 Estrategia: Sell Puts Semanales + Covered Call

La estrategia tiene **2 fases**:

### FASE 1: VENTA DE PUTS SEMANALES

- Vendes puts OTM (fuera del dinero) cada semana
  - Estructura: **1 put cerrándose cada semana** = flujo consistente
  - Pueden ser 1, 2 o más contratos según el precio del stock y margen disponible
  - Vende nuevo put cada semana para mantener el flujo
- Recibes premium cada semana
- Dejas que expiren naturalmente (sin take profit de 50%)
- Si no te asignan → Ganancias limpias

### FASE 2: VENTA DE CALL CUBIERTO (SOLO si asignan)

- Si fuiste asignado: ahora tienes 100 acciones
- Vendes 1 call cubierto de 4-6 semanas
- Strike: **50% sobre tu precio de entrada**
- **Take Profit de 50%**: Cierras la posición cuando ganes 50% en el call

**Ciclo normal**: 4-8 semanas (si hay asignación)
**Ganancia esperada**: ~1.5% semanal de tu capital en Fase 1 + prima adicional de Fase 2 si asignan

---

## ⚙️ Parámetros de Entrada

### Venta de PUT Semanal (FASE 1)

| Parámetro | Valor |
|-----------|-------|
| **Stock price** | $15-60 USD |
| **DTE** | 7 días a expiración |
| **Delta** | -0.25 a -0.15 (2-3 delta, conservador) |
| **IV Rank** | > 30% (más alto = mejores premios) |
| **Open Interest** | > 500 |
| **Bid-Ask spread** | < $0.15 |
| **Prima mínima** | 1.5% de tu capital por contrato |

### Gestión FASE 1

- **Salida**: Dejas que expire naturalmente en 7 días
- **Sin take profit de 50%** en puts semanales
- Si precio baja peligrosamente → considera cerrar antes

### Venta de CALL Cubierto (FASE 2 - solo si asignan)

| Parámetro | Valor |
|-----------|-------|
| **DTE** | 4-6 semanas |
| **Strike** | 50% sobre precio de entrada |
| **Take Profit** | 50% de ganancia (cierre automático) |
| **Herramienta** | Usar Limit Order para automatizar |

---

## 🔍 Búsqueda de Stocks

### En Webull: Market → Options → Screener

**Filtros principales**:
- Symbols: Whole Market
- Days to Expire: 7 to 7 (solo opciones semanales)
- Volume: 50+ (menos restrictivo para semanales)
- Open Interest: 500 to 525,654
- Delta: -0.25 to -0.15

**Después de resultados, filtra manualmente**:
- Stock price: $15-60
- IV Rank > 30% (cuanto más alto = mejores premios)
- Bid-Ask spread < $0.15
- Prima de put ≥ 1.5% de tu capital por contrato
- **Que entiendas la empresa** (posibilidad de asignación)

**Frecuencia**: Revisa **cada semana** para identificar puttos semanales a vender
- Después de tu put actual, identifica el siguiente para la siguiente semana
- Esto crea el flujo continuo de ingresos

---

## 📈 Indicador Técnico: RSI para Entrada

### RSI Settings

| Parámetro | Valor |
|-----------|-------|
| **Indicator** | RSI (Relative Strength Index) |
| **Length** | 14 |
| **Upper Band** | 70 (sobrecompra) |
| **Lower Band** | 30 (sobreventa) |

### Regla de Entrada Semanal

- **RSI < 30** → ✅ VENDER PUT (sobrevendido, mejor entrada)
- **RSI 30-70** → ⚠️ Evaluar con soporte/resistencia
- **RSI > 70** → ❌ NO vender put (sobrecomprado, riesgo alto)

**Objetivo**: Entrar cuando el stock está débil (RSI bajo) = mejor precio y menos riesgo

---

## 📋 Checklist Pre-Trade

Antes de vender PUT:
- [ ] ¿Cumple todos los parámetros? (IV > 30%, precio, spread, prima)
- [ ] ¿Entiendo el negocio?
- [ ] ¿Estaría cómodo asignado?

Si NO → Buscar otro stock

---

## 🎯 Empresa Objetivo

| Parámetro | Valor |
|-----------|-------|
| **Ticker** | UEC |
| **Empresa** | Uranium Energy Corp |
| **Precio actual** | $16.10 |
| **Target 12M** | $27 (+67%) |
| **Volatilidad** | 7.96% |
| **Rating** | 🟢 Buy |
| **Sector** | Energía Nuclear / Uranium |
| **Catalizador** | Demanda uranium nuclear en tendencia alcista |
| **Fecha selección** | Feb 10, 2026 |

**Por qué UEC**: Empresa real operacional, target alcista, sector en momentum, volatilidad decent para premios semanales. Fácil de entender el negocio.

---

## 📝 Registro y Seguimiento

- **Último registro**: [Actualizar con fecha]

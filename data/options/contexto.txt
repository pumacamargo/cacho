OBJETIVO: Generar ingresos vendiendo opciones (puts y calls)
ESTRATEGIA: Wheel (repetible, genera premium)
PRESUPUESTO: 3,000 USD
BROKER: Webull
META: 20-40% anual (~$600-1,200/año)

═══════════════════════════════════════════════════════════
WHEEL STRATEGY
═══════════════════════════════════════════════════════════

La estrategia wheel tiene 3 fases:

FASE 1: VENTA DE PUT
└─ Vendes put OTM (fuera del dinero)
└─ Recibes premium
└─ Si el precio baja y es asignado, compras 100 acciones

FASE 2: POSESIÓN DE STOCK (opcional)
└─ Si fuiste asignado, ahora tienes 100 acciones

FASE 3: VENTA DE CALL CUBIERTO
└─ Vendes call sobre las acciones que posees
└─ Recibes más premium
└─ Si es asignado, vendes las acciones con ganancia

CICLO: 4-8 semanas
GANANCIA ESPERADA: 4-8% por ciclo

═══════════════════════════════════════════════════════════
PARÁMETROS DE ENTRADA
═══════════════════════════════════════════════════════════

VENTA DE PUT:
- Stock price: < $30 USD
- DTE: 30-45 días a expiración
- Delta: -0.35 a -0.25 (30-35% out of the money)
- IV Rank: > 60% (volatilidad alta = más premium)
- Open Interest: > 500
- Bid-Ask spread: < $0.15

SALIDA:
- Take Profit: 50% de ganancia (cierre rápido, menos riesgo)
- Usar Limit Order para automatizar

═══════════════════════════════════════════════════════════
BÚSQUEDA DE STOCKS
═══════════════════════════════════════════════════════════

En Webull: Market → Options → Screener

Filtros:
- Symbols: Whole Market
- Days to Expire: 30 to 45
- Volume: 500 to 136,340
- Open Interest: 500 to 525,654
- Delta: -0.35 to -0.25

Después de resultados, filtra manualmente:
- Stock price < $30
- IV Rank > 60%
- Bid-Ask spread < $0.15

Revisa cada 2-3 días para nuevas oportunidades.

═══════════════════════════════════════════════════════════

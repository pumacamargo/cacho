# 📋 INSTRUCCIONES PASO A PASO - Setup Google Sheets

## 🚀 OPCIÓN 1: Rápida (15 minutos)

### Paso 1: Crear el Sheet base
1. Ve a [sheets.google.com](https://sheets.google.com)
2. Crea un nuevo Spreadsheet: **"Portfolio 2026"**
3. Renombra "Sheet1" a **"PORTAFOLIO ACTUAL"**

### Paso 2: Importar datos de ejemplo
1. Descarga el archivo `ejemplo_portafolio.csv`
2. En PORTAFOLIO ACTUAL, Archivo → Importar espacios de trabajo
3. Selecciona "Insertar nuevas hojas"
4. Se importará con todos los tickers

### Paso 3: Crear la hoja DASHBOARD
1. Crea una nueva hoja: **"DASHBOARD"**
2. Copia las fórmulas desde `formulas_google_sheets.txt`
3. Pega en la ubicación correcta

### Paso 4: Crear hojas adicionales
1. Crea: HISTORIAL, CUENTAS, SEÑALES, CONFIGURACIÓN
2. Añade encabezados según `portfolio_template.md`

### Paso 5: Agregar validaciones
1. Selecciona PORTAFOLIO ACTUAL, columna C (Cuenta)
2. Datos → Validación
3. Elige "Lista de elementos": `RRSP,Cash CAD,TFSA,Japón,Opciones,NISA`

**Listo**: Ya tienes un sheet funcional

---

## 🛠️ OPCIÓN 2: Detallada (45 minutos - recomendada)

### FASE 1: ESTRUCTURA (5 minutos)

```
1. Abre sheets.google.com
2. Crea: "Portfolio 2026"
3. Renombra Sheet1 → "PORTAFOLIO ACTUAL"
4. Crea 5 hojas más:
   - DASHBOARD
   - HISTORIAL TRANSACCIONES
   - CUENTAS
   - SEÑALES ALERTA
   - CONFIGURACIÓN
```

### FASE 2: HOJA CONFIGURACIÓN (10 minutos)

**Propósito**: Centralizar todos los parámetros base para referencias

**Setup**:
```
Fila 1: TÍTULOS
A1: Parámetro | B1: Valor | C1: Nota

Fila 2: Fecha
A2: Fecha Actualización | B2: [=TODAY()] | C2: Cambiar según necesario

Fila 3: Tipos de Cambio
A3: USD/CAD | B3: 1.38 | C3: Actualizar diariamente
A4: MXN/CAD | B4: 0.0192 | C4: Para CETES
A5: JPY/CAD | B5: 0.00864 | C5: Para cuenta Japón

Fila 6: Parámetros Operacionales
A6: CAD Líquido Mínimo | B6: 5000 | C6: No bajar de esto
A7: Cash Ready Deploy | B7: 15000 | C7: Pólvora seca

Fila 8: Targets de Distribución
| Categoría | Target % | Target CAD |
A8: Activos Productivos | B8: 40% | C8: [=229000*B8]
A9: REITs/Infraestructura | B9: 15% | C9: [=229000*B9]
A10: Metales & Commodities | B10: 20% | C10: [=229000*B10]
A11: Cash + CETES | B11: 20% | C11: [=229000*B11]
A12: Crypto | B12: 5% | C12: [=229000*B12]
```

**Formatting**:
- B2: Formato fecha
- B3:B5: Número (4 decimales)
- B6:B7: Moneda CAD
- B8:B12: Porcentaje / Moneda

### FASE 3: HOJA PORTAFOLIO ACTUAL (15 minutos)

**Paso 1: Crear Encabezados**

```
A: Ticker
B: Nombre
C: Cuenta
D: Categoría
E: Tipo Posición
F: Shares
G: Precio CAD
H: Valor CAD
I: % Portfolio
J: Notas
K: Vencimiento (Opciones)
L: Strike (Opciones)
```

**Paso 2: Agregar datos iniciales**

Opción A (Manual):
- Fila 3 en adelante: Tus posiciones actuales

Opción B (Importar CSV):
1. Selecciona A3
2. Archivo → Importar espacios de trabajo
3. Carga `ejemplo_portafolio.csv`
4. Elige "Insertar en esta hoja"

**Paso 3: Agregar Fórmulas**

Celda H3 (Valor CAD):
```
=F3*G3
```
- Copia hacia abajo hasta H100

Celda I3 (% Portfolio):
```
=IF(SUM($H$3:$H$100)=0,0,H3/SUM($H$3:$H$100))
```
- Copia hacia abajo hasta I100

**Paso 4: Agregar Validación**

Columna C (Cuenta):
1. Selecciona C3:C100
2. Datos → Validación
3. Criteria: "Lista de elementos"
4. Items: `RRSP,Cash CAD,TFSA,Japón,Opciones,NISA`
5. Mostrar alerta: ✓

Columna D (Categoría):
1. Selecciona D3:D100
2. Datos → Validación
3. Criteria: "Lista de elementos"
4. Items:
```
Activos Productivos,
REITs/Infraestructura,
Semiconductores,
Biotech,
Ciberseguridad,
Energía,
Mercados Emergentes,
Metales & Commodities,
Oro,
Cobre,
Plata,
Gas Natural,
Cash + CETES,
Crypto
```

Columna E (Tipo Posición):
1. Selecciona E3:E100
2. Datos → Validación
3. Criteria: "Lista de elementos"
4. Items: `Stock,Call,Put`

### FASE 4: HOJA DASHBOARD (15 minutos)

**Sección A: Resumen de Cuentas**

```
       A                    B              C
1      Cuenta               Saldo CAD      % Total
2      RRSP                 [fórmula]      [fórmula]
3      Cash CAD             [fórmula]      [fórmula]
4      TFSA                 [fórmula]      [fórmula]
5      Japón                [fórmula]      [fórmula]
6      Opciones             [fórmula]      [fórmula]
7      NISA                 [fórmula]      [fórmula]
8      TOTAL                [fórmula]      100%
```

**Celda A2 (RRSP)**:
```
=SUMIF('PORTAFOLIO ACTUAL'!C:C,"RRSP",'PORTAFOLIO ACTUAL'!H:H)
```

**Celda B2 (%)**:
```
=IF($A$8=0,0,A2/$A$8)
```

(Repetir para A3:A7 y B3:B7 con cambios en el nombre de la cuenta)

**Sección B: Distribución Actual vs Target**

```
       A                      B          C          D             E
10     Categoría              Actual %   Target %   Desviación    Status
11     Activos Productivos    [fórmula]  [ref]      [fórmula]     [fórmula]
12     REITs/Infraestructura  [fórmula]  [ref]      [fórmula]     [fórmula]
13     Metales & Commodities [fórmula]  [ref]      [fórmula]     [fórmula]
14     Cash + CETES           [fórmula]  [ref]      [fórmula]     [fórmula]
15     Crypto                 [fórmula]  [ref]      [fórmula]     [fórmula]
```

**Celda A11 (Activos Productivos - %)**:
```
=IF(SUM('PORTAFOLIO ACTUAL'!H:H)=0,0,SUMIF('PORTAFOLIO ACTUAL'!D:D,"Activos Productivos",'PORTAFOLIO ACTUAL'!H:H)/SUM('PORTAFOLIO ACTUAL'!H:H))
```

**Celda B11 (Target %)**:
```
=CONFIGURACIÓN!B8
```

**Celda C11 (Desviación)**:
```
=A11-B11
```

**Celda D11 (Status)**:
```
=IF(ABS(C11)<=0.05,"✅","⚠️")
```

(Repetir para filas 12-15 con cambios en el nombre de categoría)

### FASE 5: HOJA HISTORIAL TRANSACCIONES (5 minutos)

```
       A        B      C        D        E       F       G      H         I
       Fecha    Tipo   Ticker   Nombre   Cuenta  Shares  Precio Comisión  Valor Total
1      [header] [header] ...
2      2026-02-01 BUY EQIX Equinix RRSP 50 520.00 10 26010
3      2026-02-03 BUY NVDA Nvidia TFSA 25 840.00 5 21005
```

**Celda I2 (Valor Total)**:
```
=IF(B2="BUY",(F2*G2)+H2,(F2*G2)-H2)
```

**Validación en columna B (Tipo)**:
1. Selecciona B:B
2. Datos → Validación
3. Criteria: "Lista de elementos"
4. Items: `BUY,SELL`

### FASE 6: HOJA CUENTAS (5 minutos)

```
       A        B      C           D       E      F        G        H
       Cuenta   Tipo   Saldo Total Equity  Cash   Crypto   Target % Actual %
1      [header]
2      RRSP     Inv.   [fórmula]   [....]  [...]  [...]    43.7%    [fórmula]
3      Cash CAD Liq.   [fórmula]   ...     ...    ...      43.7%    [fórmula]
```

**Celda C2 (Saldo RRSP)**:
```
=SUMIF('PORTAFOLIO ACTUAL'!C:C,"RRSP",'PORTAFOLIO ACTUAL'!H:H)
```

**Celda H2 (Actual %)**:
```
=IF(SUM($C$2:$C$7)=0,0,C2/SUM($C$2:$C$7))
```

### FASE 7: HOJA SEÑALES ALERTA (5 minutos)

```
       A                  B              C         D       E
       Indicador          Actual         Threshold Status  Acción
1      [header]
2      ASML Guidance      [Manual]       -5%       [fórmula] [Manual]
3      HBM Prices YoY     [Manual]       -20%      [fórmula] [Manual]
4      Gas Natural        [Manual]       <2.00     [fórmula] [Manual]
5      High Yield Spreads [Manual]       >600      [fórmula] [Manual]
```

**Celda D2 (Status)**:
```
=IF(B2<C2,"🔴 ALERTA","🟢 OK")
```

---

## 🎨 FASE 8: FORMATEO Y VISUALIZACIÓN (10 minutos)

### Colores de Fondo

**DASHBOARD - Celda E11:E15 (Status)**:
1. Selecciona E11:E15
2. Formato → Formateo condicional
3. Escala de colores:
   - Si es "✅" → Fondo Verde (#00FF00)
   - Si es "⚠️" → Fondo Naranja (#FFA500)

### Formato de Números

- Columna G (PORTAFOLIO ACTUAL - Precio): Moneda CAD, 2 decimales
- Columna H (Valor CAD): Moneda CAD, 0 decimales
- Columna I (% Portfolio): Porcentaje, 1 decimal
- Columna B (DASHBOARD - % Total): Porcentaje, 1 decimal

### Gráficos

**Gráfico 1: Distribución Actual (DASHBOARD)**
1. Selecciona PORTAFOLIO ACTUAL: A3:A (Tickers) + H3:H (Valores)
2. Insertar → Gráfico
3. Tipo: Gráfico de torta
4. Título: "Distribución Actual (CAD)"
5. Ubicar en: DASHBOARD, posición B20

**Gráfico 2: Actual vs Target (DASHBOARD)**
1. Selecciona DASHBOARD: A11:B15
2. Insertar → Gráfico
3. Tipo: Gráfico de barras (columnas)
4. Título: "Distribución Actual vs Target"
5. Ubicar en: DASHBOARD, posición E20

---

## ✅ CHECKLIST FINAL

- [ ] 6 hojas creadas (PORTAFOLIO, DASHBOARD, HISTORIAL, CUENTAS, SEÑALES, CONFIG)
- [ ] PORTAFOLIO ACTUAL lleno con tus posiciones reales
- [ ] Validaciones de datos en Cuenta, Categoría, Tipo Posición
- [ ] Fórmulas en DASHBOARD para resumen de cuentas
- [ ] Fórmulas en DASHBOARD para distribución vs target
- [ ] Gráficos de torta y barras creados
- [ ] Formateo condicional en status
- [ ] Colores aplicados
- [ ] Números formateados correctamente
- [ ] Compartir sheet con tu email de respaldo

---

## 🎯 CÓMO USAR DESDE HOY

### Cada vez que compras/vendes:

1. Abre HISTORIAL TRANSACCIONES
2. Nueva fila: Fecha, Tipo (BUY/SELL), Ticker, Cuenta, Shares, Precio, Comisión
3. El valor se calcula automáticamente
4. En PORTAFOLIO ACTUAL, actualiza Shares de ese ticker

### Cada mes:

1. Abre CONFIGURACIÓN
2. Actualiza USD/CAD, MXN/CAD, JPY/CAD con tipos actuales
3. En PORTAFOLIO ACTUAL, actualiza "Precio CAD" de cada posición
4. DASHBOARD se actualiza automáticamente

### Cada trimestre:

1. Ve a DASHBOARD
2. Revisa "Desviación" en distribución
3. Si algo está > +5% o < -5%, es hora de rebalancear
4. En REBALANCEO (nueva hoja), calcula qué vender/comprar

---

## 🔗 REFERENCIAS RÁPIDAS

- Tipos de cambio: [XE.com](https://xe.com)
- Precios: [Google Finance](https://www.google.com/finance/)
- CETES yield: [Cetesdirecto.com.mx](https://www.cetesdirecto.com.mx)
- Tickers Japón: [Tokyo Stock Exchange](https://www.jpx.co.jp)

---

## 📱 COMPARTIR Y SINCRONIZAR

Para tener acceso desde celular:

1. Haz clic en "Compartir" (esquina superior derecha)
2. Comparte con tu email de respaldo
3. Descarga la app Google Sheets
4. El sheet se sincronizará automáticamente

---

**¡Listo! Tienes un portfolio tracker profesional.**


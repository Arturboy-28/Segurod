# Segurod — Borrador de proyecto

**Estado:** borrador / discovery  
**Alcance de este documento:** definición del producto, canales, integración con aseguradoras y plan de implementación.  
**Fuera de alcance ahora:** código, infraestructura en producción, contratos con aseguradoras.

---

## 1. Objetivo

Construir un **sistema cotizador de seguros** que permita al cliente:

1. **Cotizar por WhatsApp** (conversación guiada), o  
2. **Recibir un enlace web** y completar la cotización desde el celular (flujo responsive).

La cotización debe ser **completa**: datos del riesgo/asegurado → comparación multi-aseguradora → oferta clara → captura de lead / solicitud de emisión → seguimiento.

**Hipótesis de mercado inicial:** México, ramo **auto** (mayor madurez de APIs y demanda). Expansión posterior a moto, hogar, GMM y vida.

---

## 2. Propuesta de valor

| Para el cliente | Para el agente / broker |
|-----------------|-------------------------|
| Cotiza en minutos sin llamada ni apps | Un solo flujo WhatsApp + web |
| Compara varias aseguradoras | Lead estructurado y trazable |
| Enlace móvil si prefiere “llenar” | Menos fricción, más cierre |
| Transparencia de coberturas y precio | Base para emisión y postventa |

**Nombre de producto de trabajo:** Segurod (ajustable).

---

## 3. Canales de cotización

### 3.1 WhatsApp (canal primario de captación)

```
Cliente escribe / hace clic en wa.me
        ↓
Bot / flujo conversacional
  - Detecta ramo (auto, etc.)
  - Pregunta datos mínimos
  - Opción A: cotiza dentro del chat (resumen + botones)
  - Opción B: envía enlace web personalizado (/c/{token})
        ↓
Motor de cotización (API interna)
        ↓
Respuesta con 2–5 ofertas + CTA (asesor / emitir / guardar)
```

**Tecnología recomendada (borrador):**

- **Meta WhatsApp Cloud API** (oficial).
- Webhook en backend propio para mensajes entrantes.
- Plantillas aprobadas para: enlace de cotización, recordatorio, “tu cotización vence”, seguimiento postventa.
- Ventana de 24 h: respuestas del bot sin cargo de plantilla (modelo de precios Meta actual; validar al implementar).

**Alternativa operativa:** BSP (Twilio, 360dialog, etc.) si se quiere panel y menos operación Meta directa.

### 3.2 Web móvil (cotización completa en el celular)

Flujo de una sola sesión, pensado para móvil primero:

1. **Inicio** — tipo de seguro  
2. **Vehículo** — marca, modelo, año, versión (catalago AMIS / VIN si aplica)  
3. **Conductor / asegurado** — CP, fecha nacimiento, género, uso del vehículo  
4. **Paquete deseado** — RC / limitado / amplio (o “muéstrame todos”)  
5. **Resultados** — comparador (precio, deducible, coberturas clave)  
6. **Detalle** — desglose + PDF/share  
7. **Siguiente paso** — “Quiero contratar” / “Hablar con asesor” / “Guardar y enviar a WhatsApp”

El enlace puede venir de WhatsApp con **token de sesión** para prellenar lo ya capturado.

---

## 4. Cotización “completa” — qué incluye

### 4.1 Datos de entrada (auto — MVP)

- Código postal  
- Fecha de nacimiento del conductor principal  
- Género (según requerimiento de tarifas)  
- Marca / modelo / año / versión  
- Uso: publica / particular  
- Tipo de paquete o coberturas deseadas  
- (Opcional) NCI / historial, descuentos, placas, VIN  

### 4.2 Datos de salida

- Aseguradora + producto  
- Prima (anual / mensual / MSI si aplica)  
- Paquete y coberturas principales  
- Deducibles  
- Vigencia de la cotización  
- ID interno de cotización  
- Distinción: **tarifa orientativa** vs **tarifas negociadas del broker** (si hay conexión real)

### 4.3 Post-cotización (fase 2)

- Solicitud de emisión / carga de documentos  
- Pago  
- Entrega de póliza  
- Renovación y siniestros (fuera del MVP)

---

## 5. Investigación: APIs con aseguradoras

### 5.1 Conclusión corta

**Sí existen APIs**, pero en la práctica (México / LATAM) casi no se conecta “directo a Quálitas/GNP/etc.” desde el día uno. El camino realista es:

1. **Agregadores / Open Insurance / brokers con API** (cotizar y a veces emitir vía una sola integración), o  
2. **Conexión directa con cada aseguradora** (contratos comerciales + credenciales B2B; largo y costoso), o  
3. **Modo demo / motor propio** mientras se cierran alianzas (tarifas simuladas o “lead + asesor”).

Las APIs públicas gratuitas y abiertas de las grandes aseguradoras **no son la norma**. Se requiere convenio, clave de agente/broker, y a menudo certificación CNSF / figura legal adecuada.

### 5.2 Opciones de integración (México — referencias de mercado)

| Enfoque | Ejemplos | Ventaja | Consideración |
|---------|----------|---------|---------------|
| Agregador / plataforma API | Dora, Inter Connect (Interprotección), Bruno, Surexs, bolttech | Una API → varias aseguradoras; time-to-market | Comisión / fee; términos del partner |
| API de aseguradora / bancaseguros | p. ej. APIs de socios (BBVA Seguros y similares B2B) | Marca y tarifa “oficial” | Una compañía a la vez; proceso comercial |
| Core propio + scrapers / micrositios | No recomendado | — | Riesgo legal, frágil, no apto para emisión |
| Cotización manual asistida | Asesor recibe lead web/WA | Sin API al inicio | Escala limitada; útil en fase 0 |

**Recomendación de borrador:**

- **Fase 0:** motor mock + captura completa de lead (WhatsApp + web).  
- **Fase 1:** integrar **un agregador** con API REST documentada (OpenAPI).  
- **Fase 2:** sumar conexiones directas solo donde el gancho comercial y el volumen lo justifiquen.

### 5.3 Criterios para elegir partner de API

- Ramos soportados (auto primero)  
- Cotización **y** emisión, o solo cotización  
- SLA y tiempo de respuesta  
- ¿Se usan **tus** tarifas/comisiones o las del marketplace?  
- Ambiente sandbox  
- Cumplimiento LFPDPPP / retención de datos  
- Precio: fee fijo, % comisión, o ambos  
- Disponibilidad de webhook / id de cotización / PDF

### 5.4 WhatsApp como canal (no es API de seguros)

WhatsApp **no cotiza** seguros. Solo transporta la conversación y el enlace. El motor de seguros es independiente (agregador o APIs propias).

---

## 6. Arquitectura lógica (borrador)

```
┌─────────────┐     ┌─────────────┐
│  WhatsApp   │     │  Web móvil  │
│  Cloud API  │     │  /cotizar   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └─────────┬─────────┘
                 ▼
        ┌────────────────┐
        │  API Segurod   │  sesiones, leads, cotizaciones
        └────────┬───────┘
                 ▼
        ┌────────────────┐
        │ Quote Engine   │  orquesta providers
        └────────┬───────┘
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 Provider A   Provider B   Mock (dev)
 (agregador)  (aseguradora) 
                 │
                 ▼
        ┌────────────────┐
        │  CRM / Panel   │  agentes, seguimiento
        └────────────────┘
```

**Componentes conceptuales (sin implementación aún):**

| Módulo | Responsabilidad |
|--------|-----------------|
| Canal WhatsApp | Webhook, menús, envío de enlace, resumen de ofertas |
| Cotizador web | Wizard móvil, comparador, detalle |
| Quote Engine | Normaliza request/response entre providers |
| Adapters | Un adapter por agregador/aseguradora |
| Leads & cotizaciones | Persistencia, vigencia, token de enlace |
| Panel agente | Ver leads, retomar chat, asignación |
| Auth / roles | Admin, agente, (futuro) cliente |

---

## 7. Flujos de producto detallados

### Flujo A — 100 % en WhatsApp

1. Cliente: “Quiero cotizar mi auto”  
2. Bot: pide CP, año, marca/modelo (lista o texto), edad  
3. Cotiza vía Quote Engine  
4. Envía top 3 ofertas en mensajes/listas  
5. Cliente elige una → “Te contacta un asesor” o “Continúa emisión” (si hay API de emisión)

### Flujo B — WhatsApp → enlace web

1. Bot captura lo mínimo (o nada)  
2. Envía: `https://app.segurod.mx/c/abc123`  
3. Cliente completa en el celular  
4. Al terminar, bot puede avisar por WA: “Tu cotización está lista” + resumen

### Flujo C — Solo web (ads, sitio, QR)

1. Landing corta → entra al wizard  
2. Al guardar/contratar, opción “Recibir en WhatsApp”

---

## 8. Alcance por fases

### Fase 0 — Validación (este borrador)

- [x] Definir canales y cotización completa  
- [x] Investigar APIs  
- [ ] Validar país, ramos y figura legal (agente / broker / aliado)  
- [ ] Elegir 1–2 partners de API para demos comerciales  
- [ ] Prototipo de flujo (Figma / mapa de conversación) — **sin código**

### Fase 1 — MVP usable

- WhatsApp: menú + captura + enlace web  
- Web: cotizador auto completo (puede ser mock)  
- Panel mínimo de leads  
- Preparar adapter hacia un agregador real

### Fase 2 — Cotización real multi-aseguradora

- Integración productiva con partner API  
- Comparador con precios reales  
- Notificaciones y vencimiento de cotización  
- Asignación a agentes

### Fase 3 — Emisión y operación

- Emisión / pago / documentos  
- Renovaciones  
- Más ramos

---

## 9. Decisiones abiertas (para siguiente reunión)

1. **País y regulación:** ¿México u otro? ¿Ya hay cédula / oficina de agente o broker?  
2. **Ramo inicial:** ¿Solo auto o también GMM / hogar?  
3. **Modelo de negocio:** comisión por póliza, fee SaaS a agentes, white-label  
4. **Emisión:** ¿solo cotizar + lead, o cotizar y emitir en línea?  
5. **WhatsApp:** ¿Cloud API directa o BSP?  
6. **Provider preferido para cotizar:** Dora / Inter Connect / Bruno / Surexs / otro ya negociado  
7. **Marca visual y dominio**  
8. **Quién atiende los leads** (bot → humano)

---

## 10. Riesgos y supuestos

| Riesgo | Mitigación |
|--------|------------|
| Sin convenio API al lanzar | Empezar con lead completo + mock; no vender “póliza emitida” sin partner |
| Tarifas distintas a las del agente | Usar BYOR (“trae tus tarifas”) si el partner lo permite |
| Abandono en WhatsApp (muchas preguntas) | Ofrecer enlace web temprano |
| Cumplimiento de datos personales | Aviso de privacidad, consentimiento en WA y web |
| Expectativa de precio “oficial” | Etiquetar claramente si es estimado |

---

## 11. Entregables del borrador (esta etapa)

1. Este documento de proyecto  
2. Matriz de APIs / partners (sección 5)  
3. Mapa de flujos WhatsApp + web (secciones 3 y 7)  
4. Lista de decisiones abiertas (sección 9)

**Próximo paso sugerido (sin programar):**  
Responder las decisiones de la sección 9 → boceto UX del wizard y del chat → contacto comercial con 1 agregador para sandbox.

---

## 12. Referencias rápidas (investigación)

- Agregadores / Open Insurance (MX): Dora, Inter Connect, Bruno, Surexs, bolttech  
- Canal WhatsApp: Meta WhatsApp Cloud API (+ BSP opcionales)  
- Modelos de producto similares: comparadores web + chatbots de agencias de seguros  

*Las APIs concretas, precios y listados de aseguradoras se confirman con cada proveedor; no hay un “API pública universal” de todas las aseguradoras.*

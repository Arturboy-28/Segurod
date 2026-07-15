# Segurod — Borrador de proyecto

**Estado:** borrador / discovery  
**Alcance de este documento:** definición del producto (cotización + operaciones del agente + portal del cliente), canales, integración con aseguradoras y plan de implementación.  
**Fuera de alcance ahora:** código, infraestructura en producción, contratos con aseguradoras.

---

## 1. Objetivo

Construir **Segurod** como producto **SaaS multi-tenant** (cada oficina/agencia es un cliente que paga suscripción) con dos caras de producto:

### A) Cotización (adquisición)

1. **Cotizar por WhatsApp** (conversación guiada), o  
2. **Recibir un enlace web** y completar la cotización desde el celular.

Cotización **completa**: datos del riesgo → comparación multi-aseguradora → oferta → lead / emisión → seguimiento.

**Modos de cotización (requerimiento):** cada oficina/agente puede operar en **manual**, **API**, o **mixto**, y **activar/desactivar** la API por aseguradora o en global mientras obtiene credenciales, sandbox y homologación.

### B) Operación del agente (retención y administración)

Herramientas diarias del intermediario en un solo sistema:

- Agenda  
- Facturación de comisiones a aseguradoras  
- Comisiones pendientes por facturar  
- Comisiones pendientes de pago  
- Cartera de clientes  
- Recordatorios automáticos de vencimiento  
- Portal del cliente (pólizas y vencimientos)

**Hipótesis de mercado inicial:** México, ramo **auto** (mayor madurez de APIs). Expansión a moto, hogar, GMM y vida.

**Nombre de producto de trabajo:** Segurod (ajustable).

---

## 2. Propuesta de valor

| Para el cliente | Para el agente / broker |
|-----------------|-------------------------|
| Cotiza en minutos (WA o web móvil) | Cotiza y cierra desde un solo panel |
| Ve sus pólizas y vencimientos en portal | Cartera ordenada, no en Excel |
| Recibe recordatorios a tiempo | Menos pólizas que se van por olvido |
| Habla con su agente sin perder historial | Agenda + seguimiento de leads |
| Transparencia de coberturas y precio | Control de comisiones: por facturar / por cobrar |

En una frase: **SaaS para oficinas de seguros: cotizar + cartera + comisiones + portal, con su marca y sus usuarios.**

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

### 4.4 Modos de cotización: manual / API / mixto

El sistema **no depende** de tener API el día 1. El agente (o admin de oficina) configura el modo:

| Modo | Qué hace |
|------|----------|
| **Manual** | Captura datos del riesgo; el agente carga prima/coberturas a mano o marca “pendiente de cotizar”; puede adjuntar PDF de la aseguradora |
| **API** | Cotiza en automático contra el provider (agregador o aseguradora) |
| **Mixto** | Unas compañías por API y otras manuales (lo más realista al ir activando credenciales) |

**Interruptor (toggle) en configuración:**

- Activar / desactivar **API global** (mientras no haya sandbox/credenciales → queda solo manual)  
- Activar / desactivar **por aseguradora / provider** (ej. Quálitas ON vía API, GNP OFF → solo manual)  
- Ambiente: `sandbox` | `producción` (cuando aplique)  
- Si la API falla o está apagada → el flujo **no se rompe**: cae a manual o “enviar a agente”

**Flujo típico mientras se consiguen accesos:**

1. Arranque: todo en **manual** (WhatsApp/web capturan lead completo).  
2. Llega sandbox de un partner → se prueba con toggle en **sandbox** (solo admin).  
3. Homologación OK → se enciende esa compañía en **producción**.  
4. El resto sigue manual hasta tener clave/API.

**Datos mínimos en cotización manual:**

- Mismos datos de entrada del asegurado/riesgo  
- Aseguradora, paquete, prima, deducible, vigencia de la oferta  
- Origen: “capturada por agente” / “PDF importado”  
- Estatus: borrador · enviada al cliente · ganada · perdida · vencida

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

- **Día 1:** cotización **manual** + captura completa (WhatsApp + web); API apagada por toggle.  
- **Cuando haya sandbox:** encender un provider en modo prueba sin afectar producción.  
- **Después:** modo mixto (API ON por compañía) y sumar conexiones según credenciales reales.

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

## 6. Arquitectura por módulos (requerimiento de diseño)

**Principio:** el producto se maneja por **tipos de módulo**. Cada función nueva o cambio de característica debe vivir dentro de **un solo módulo**. Los demás solo se enteran por contratos estables (eventos / APIs internas), no por lógica mezclada.

### 6.1 Tipos de módulo

| Tipo | Rol | Ejemplo |
|------|-----|---------|
| **Core / plataforma** | Tenant, auth, permisos, auditoría — base de todos | `mod-tenancy`, `mod-identity` |
| **Canal** | Entrada/salida con el mundo exterior | `mod-whatsapp`, `mod-web-quote`, `mod-pwa` |
| **Dominio** | Negocio de seguros (una capacidad clara) | `mod-cotizacion`, `mod-cartera`, `mod-comisiones` |
| **Experiencia** | UI/portal para un actor | `mod-portal-agente`, `mod-portal-cliente`, `mod-portal-ceo` |
| **Integración** | Adapters externos enchufables | `mod-providers-api` |
| **Comunicaciones** | Envíos y alertas (sin dueñarse del negocio) | `mod-notificaciones` |

### 6.2 Catálogo de módulos (límites)

| ID | Módulo | Tipo | Responsabilidad (solo esto) | Qué NO debe meterse aquí |
|----|--------|------|-----------------------------|---------------------------|
| `mod-tenancy` | Tenancy SaaS | Core | Alta de oficina, aislamiento de datos, plan | UI de cotizar |
| `mod-identity` | Usuarios y permisos | Core | Roles, vendedores, splits internos de comisión | Cálculo de prima |
| `mod-config` | Configuración tenant | Core | Logo, datos empresa, direcciones, SMTP, toggles API | Emisión de pólizas |
| `mod-audit` | Auditoría | Core | Bitácora quién/qué/cuándo | Reglas de negocio |
| `mod-cotizacion` | Cotización | Dominio | Cotizar manual/API/mixto, leads, vigencia, tokens | Agenda o portal |
| `mod-providers-api` | APIs aseguradoras | Integración | Adapters, sandbox/prod, tablas % comisión cia. | Split interno agente |
| `mod-cartera` | Cartera | Dominio | Clientes, pólizas, ramos, estatus, docs | Facturar comisiones |
| `mod-agenda` | Agenda | Dominio | Citas, tareas, seguimientos | WhatsApp transport |
| `mod-comisiones` | Comisiones | Dominio | Por facturar / por pagar / pagadas, facturas a cias. | Login/PWA |
| `mod-renovaciones` | Renovaciones / vencimientos | Dominio | Reglas de vencimiento, cola de renovación | Diseño del portal |
| `mod-notificaciones` | Notificaciones | Comunicaciones | Email, push, plantillas, reglas de alerta | Datos de póliza (solo recibe eventos) |
| `mod-pwa` | PWA | Canal | Instalar en inicio, service worker, Web Push wiring | Contenido de negocio |
| `mod-whatsapp` | WhatsApp | Canal | Webhook, menús, envío de enlaces/mensajes | Motor de tarifas |
| `mod-web-quote` | Cotizador web | Canal / experiencia | Wizard móvil público | Panel CEO |
| `mod-portal-agente` | Portal administrativo | Experiencia | UI agentes: hoy, leads, atajos a módulos | Lógica de primas |
| `mod-portal-cliente` | Portal cliente | Experiencia | UI asegurado: pólizas, vencimientos, docs | Tablas de comisión |
| `mod-portal-ceo` | Panel CEO | Experiencia | Resúmenes y cortes por ramo/agente | Persistencia de pólizas (consume datos) |
| `mod-billing-saas` | Billing Segurod | Core (fase 2+) | Suscripción, límites de plan | Comisiones de aseguradoras |

### 6.3 Reglas para editar sin romper otros módulos

1. **Un cambio = un módulo.** Feature nueva → se asigna a un ID del catálogo (o se crea un módulo nuevo con límite claro).
2. **Prohibido acoplar lógica interna** de otro módulo (ej. `mod-whatsapp` no calcula primas; llama a `mod-cotizacion`).
3. **Contratos entre módulos:**
   - Pedidos: API interna / casos de uso (`Cotizar`, `RegistrarPoliza`)
   - Avisos: eventos (`CotizacionCreada`, `PolizaPorVencer`, `ComisionGenerada`)
4. **`mod-notificaciones` solo reacciona a eventos** — no decide vencimientos; eso es `mod-renovaciones`.
5. **Adapters de aseguradora** solo viven en `mod-providers-api`; apagar uno no toca cartera ni agenda.
6. **Portales (`mod-portal-*`) son capas finas de UI** — orquestan, no duplican reglas.
7. **Features por plan SaaS:** se habilitan/deshabilitan por módulo (`mod-tenancy` / plan), no con `if` dispersos.
8. Al documentar un cambio: indicar **módulo afectado** + eventos públicos tocados (si aplica).

### 6.4 Diagrama lógico (módulos)

```
                    ┌─────────────┐  ┌──────────────┐
                    │ mod-whatsapp│  │ mod-web-quote│
                    └──────┬──────┘  └──────┬───────┘
                           │                │
                           ▼                ▼
                    ┌─────────────────────────┐
                    │     mod-cotizacion      │──► mod-providers-api
                    └────────────┬────────────┘
                                 │ eventos
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
  mod-cartera              mod-agenda            mod-comisiones
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
           mod-renovaciones          mod-notificaciones
                    │                         │
                    │                         ├── push/email/WA
                    │                         └── mod-pwa
                    ▼
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 portal-agente  portal-cliente  portal-ceo
     │
     └── Core: tenancy · identity · config · audit · billing-saas
```

### 6.5 Cómo se usa esto al crecer el producto

| Pedido de negocio | Módulo a tocar | Evitar tocar |
|-------------------|----------------|--------------|
| Nueva alerta push de “cotización lista” | `mod-notificaciones` (+ evento desde cotización) | Portales enteros |
| Soporte ramo hogar | `mod-cotizacion` + `mod-cartera` (categoría) | WhatsApp transport |
| Nuevo % comisión Quálitas | `mod-providers-api` | Usuarios |
| Nuevo split de un vendedor | `mod-identity` | Providers |
| Widget nuevo en panel CEO | `mod-portal-ceo` | Cartera (salvo lectura) |
| Factura CFDI de comisión | `mod-comisiones` | Cotización |

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

### Flujo D — Vencimiento / renovación (cartera)

1. Sistema detecta póliza por vencer (ej. 45 / 30 / 15 / 7 días)  
2. Aviso automático al cliente (WhatsApp / email / portal)  
3. Tarea en agenda del agente  
4. Cliente o agente inicia recotización / renovación  
5. Se actualiza cartera y comisiones al emitir

### Flujo E — Comisión del agente

1. Póliza emitida / pagada → calcula comisión con **tabla de la aseguradora**  
2. Aplica **split interno** del vendedor vs oficina  
3. Genera **comisión por facturar** (oficina → aseguradora)  
4. Factura a la aseguradora / promotoría  
5. Pasa a **facturada / pendiente de pago** → al conciliar → **pagada**  
6. Comisión interna del vendedor queda pendiente/pagada según reglas de la oficina  
7. Todo alimenta reportes y **panel CEO** (por ramo, agente, compañía)

---

## 8. Modelo SaaS y configuración del tenant

Segurod se vende por **suscripción** (SaaS). Cada cliente (oficina, broker o agente independiente) es un **tenant** con su propia configuración, usuarios y datos.

### 8.0 Pantalla / área de Configuración (requerido)

#### Identidad y marca
- Logo de la empresa (cotizador, portal cliente, PDFs, correos)
- Nombre comercial / razón social
- Colores básicos (opcional, white-label ligero)
- Datos del agente o de la empresa de seguros (RFC, cédula, clave de agente global si aplica)

#### Datos de contacto y direcciones
- Teléfonos, WhatsApp de la oficina, sitio web
- Correo de contacto visible al cliente
- Direcciones (matriz, sucursales) — una o varias
- Horarios de atención (opcional)

#### Correo para envíos
- Configurar remitente (SMTP propio o proveedor: Resend, SendGrid, SES, etc.)
- From name / from email / reply-to
- Plantillas: cotización, vencimiento, bienvenida al portal, factura de comisión
- Prueba de envío (“enviar correo de test”)
- Fallbacks si falla el SMTP del tenant (cola + reintento)

#### Cotización / APIs (ligado a §4.4)
- Toggle manual / API / mixto
- Credenciales por provider (sandbox/prod)
- Quién puede editar estas llaves (solo admin/dueño)

#### Comisiones otorgadas por aseguradora (en config de APIs / compañías)
Por cada empresa de seguros (haya API o sea manual) se define lo que **paga la aseguradora a la oficina**:

- % o monto fijo por ramo / producto / paquete (ej. auto amplio 12 %, GMM 18 %)
- Vigencia de la tabla (desde / hasta)
- Notas (bonos, escalones, excepciones)
- Usado para calcular “comisión por facturar” al cerrar/emitir

Sin esto, las comisiones se capturan a mano; con esto, se proponen solas y se pueden ajustar.

#### Usuarios (vendedores) y permisos
Roles mínimos sugeridos:

| Rol | Puede |
|-----|--------|
| **CEO / Dueño** | Todo + **panel ejecutivo** + billing SaaS |
| **Admin** | Configuración, usuarios, reportes, comisiones, APIs |
| **Vendedor / agente** | Cotizar, cartera asignada, agenda, leads |
| **Asistente** | Carga docs, agenda, seguimiento (sin ver comisiones si se restringe) |
| **Cliente** | Solo portal del asegurado |

#### Comisiones internas por usuario / agente
Además de lo que paga la aseguradora, la oficina reparte hacia adentro:

| Concepto | Ejemplo |
|----------|---------|
| Comisión de la aseguradora (oficina) | 12 % de la prima |
| % o monto del **vendedor** | 60 % de esa comisión (o 7.2 % de prima) |
| % **oficina / CEO** | El resto |
| Overrides | Bono por meta, trato especial por agente |

Configurable en la ficha del usuario (y/o por ramo). Al cerrar una venta se calcula:
1) comisión bruta según tabla de la aseguradora →  
2) split interno según reglas del agente →  
3) queda en pendientes por facturar / pagar según el flujo de comisiones.

Permisos granulares (ejemplos): ver comisiones propias, ver comisiones del equipo, facturar, editar tablas de comisión, editar config, exportar cartera, activar API, ver auditoría, ver **panel CEO**.

#### Auditoría de usuarios
Bitácora inmutable (o difícil de alterar) con:
- Login / logout / intentos fallidos
- Altas, bajas y cambios de permisos
- Cambios en configuración (logo, correo, APIs)
- Altas/ediciones sensibles: pólizas, comisiones, facturas
- Exportaciones de datos
- Quién, qué, cuándo, IP/dispositivo (si disponible)

Vista filtrable para admin/dueño; retención configurable (ej. 90 días / 1 año).

#### Respaldos
- Política de backup del tenant (automático diario/semanal)
- Listado de respaldos disponibles
- Solicitar restauración (self-service o vía soporte, según plan)
- Exportación de cartera / comisiones (CSV) como “respaldo operativo” del usuario
- Nota SaaS: el backup técnico lo corre la plataforma; el tenant ve estado y puede pedir restore/export

#### Billing SaaS (config lateral, fase posterior)
- Plan activo, límites (usuarios, cotizaciones, WhatsApp)
- Facturación de la suscripción Segurod (separada de comisiones a aseguradoras)

#### Alertas push (cliente y administrativo)
El tenant puede **definir y encender** alertas push hacia:

| Destino | Ejemplos de alerta |
|---------|-------------------|
| **Portal del cliente** | Póliza por vencer, cotización lista, documento disponible, renovación, mensaje del agente |
| **Portal administrativo** (agente / admin / CEO) | Lead nuevo, cita próxima, vencimientos del día, comisión pagada, cotización ganada/perdida, meta |

Configurables:
- Activar/desactivar por tipo de alerta  
- Destinatarios (rol, agente asignado, cliente de la póliza)  
- Antelación (ej. 30 / 15 / 7 días antes del vencimiento)  
- Canal: **push** (y opcionalmente WhatsApp / email en paralelo)

#### PWA — “Agregar a inicio” (iPhone / Android)
Para que las alertas push funcionen bien en móvil sin app de tienda:

- Portales (**cliente** y **administrativo**) como **PWA** instalable  
- Flujo guiado: “Agregar a pantalla de inicio” (iOS Safari / Android Chrome)  
- Service worker + Web Push (y lo que requiera iOS para notificaciones en PWA instalada)  
- Permiso de notificaciones solo después de instalar / interacción del usuario  
- Icono = logo del tenant (o Segurod)  
- Si no hay push (permiso negado): fallback a email / WhatsApp / badge in-app

---

### 8.0b Panel CEO / dirección (requerido)

Vista ejecutiva de **toda la oficina** (no solo la cartera de un vendedor). Pensado para el dueño/CEO.

**Resúmenes en un vistazo**
- Cotizaciones creadas (hoy / semana / mes / rango)
- Ventas cerradas (pólizas emitidas / ganadas)
- % conversión cotización → venta
- Primas cotizadas vs primas cerradas
- Comisiones generadas / por facturar / cobradas
- Movimientos recientes (alta lead, cotización, cierre, factura, pago)

**Filtros y cortes**
- Por periodo
- Por agente / vendedor
- Por aseguradora
- Por canal (WhatsApp, web, manual)

**Por categorías / ramos** (drill-down)
- Autos  
- Casa / hogar  
- Vida  
- Gastos médicos  
- Moto, flotillas, otros (según se activen)

En cada categoría: cotizaciones, cerradas, prima, comisión, ranking de agentes.

**Permiso:** solo CEO / Dueño (y Admin si se delega). Los vendedores no ven totales de toda la oficina salvo que se autorice.

---

## 8A. Módulo agente — alcance confirmado

Funciones operativas que **sí entran** (además de la configuración SaaS):

### 8.1 Agenda

- Citas con prospectos y clientes  
- Seguimientos (“llamar mañana”, “enviar cotización”)  
- Vista día / semana  
- Ligada a lead, cliente o póliza  
- Recordatorio interno al agente (y opcional WhatsApp)

### 8.2 Cartera de clientes

- Ficha del cliente (datos, contactos, documentos)  
- Pólizas: aseguradora, ramo, número, vigencia, prima, estatus  
- Historial de cotizaciones y renovaciones  
- Búsqueda y filtros (por vencer, cancelada, ramo, compañía)  
- Asignación a agente (oficinas con varios asesores)

### 8.3 Recordatorios automáticos de vencimiento

- Reglas configurables (ej. 45-30-15-7 días)  
- Canales: WhatsApp, email, notificación en portal  
- Cola de renovaciones del día para el agente  
- Evitar spam: una secuencia por póliza + opt-out

### 8.4 Comisiones

**Dos capas (requerido):**

1. **Aseguradora → oficina** — % definidos en config de compañías/APIs  
2. **Oficina → usuario/agente** — split interno en ficha de usuario  

Estados mínimos (capa oficina vs aseguradora):

| Estado | Significado |
|--------|-------------|
| Pendiente por facturar | Lista para facturar a la aseguradora |
| Facturada / pendiente de pago | Factura enviada; se espera depósito |
| Pagada | Conciliada con la aseguradora |
| En disputa / ajuste | Diferencia con estado de cuenta |

Interno (vendedor): comisión del agente pendiente / liberada / pagada (cuando la oficina paga a su fuerza de ventas).

Vistas:

- Por aseguradora  
- Por periodo  
- Por agente  
- Por ramo/categoría  
- Totales: por facturar / por cobrar / cobrado  
- Panel CEO: rollup de todo lo anterior

### 8.5 Facturación de comisiones a aseguradoras

- Alta de aseguradoras / promotorías como “clientes a facturar”  
- Generar o registrar factura (factura + folio CFDI si el negocio lo requiere)  
- Adjuntar soporte (estado de cuenta, producción del mes)  
- Marcar envío y seguimiento de pago  
- Nota: la timbrado CFDI puede ser nativo o vía proveedor (Facturama, etc.) — decidir en implementación

### 8.6 Portal del cliente

Login del asegurado para:

- Ver pólizas vigentes  
- Ver fechas de vencimiento  
- Descargar documentos (póliza, recibo) cuando existan  
- Solicitar renovación / “quiero que me cotice”  
- Actualizar datos de contacto  
- **Instalar en inicio** (PWA) y activar **alertas push**  
- Centro de notificaciones in-app  
- (Opcional) ver historial de siniestros / estatus de reporte

---

## 9. Ideas adicionales (software típico de agentes)

Basado en portales de agentes, CRM insurtech y prácticas de oficinas. Priorizar después del núcleo (secciones 8 y 8A).  
*Nota: logo, usuarios/permisos, auditoría y white-label básico ya están en Configuración SaaS (§8).*

### Alta prioridad (casi estándar en el mercado)

| Idea | Para qué sirve |
|------|----------------|
| **Pipeline de ventas / embudo** | Lead → contactado → cotizado → negociación → ganado/perdido |
| **Bandeja unificada WhatsApp** | Varios agentes, asignación, historial en la ficha del cliente |
| **Alertas de cobranza (recibo)** | No solo vence la póliza: también el pago fraccionado |
| **Renovaciones en un tablero** | “Esta semana hay 23 por renovar” con % retenido |
| **Documentos del cliente** | INE, comprobante, factura auto, fotos, solicitudes |
| **Reportes y tablero** | Primas, emisiones, retención, comisiones del mes |
| **Plantillas de mensajes** | WA/email: cotización lista, faltan datos, feliz cumpleaños, vencimiento |
| **Sucursales** | Varias direcciones/equipos bajo el mismo tenant |

### Media prioridad (diferenciadores)

| Idea | Para qué sirve |
|------|----------------|
| **Comparativo PDF / propuesta formal** | Enviar 3 opciones con logo de la oficina |
| **Recotización en 1 clic** | Renovar con mismos datos del año pasado |
| **Endosos y movimientos** | Cambio de auto, alta de conductor, domicilio |
| **Siniestros (mesa ligera)** | Alta de reporte, folios, seguimiento, documentos |
| **Metas y bonos** | Escalones sobre el split interno ya definido en usuarios |
| **App móvil del agente** | Agenda + cartera + cotizar en campo |
| **Importar cartera** | Excel / CSV desde otras oficinas o portales |
| **Estados de cuenta vs aseguradora** | Conciliación automática o semi (cargar Excel de la cia.) |
| **Firma digital / checklist de emisión** | Documentos listos antes de emitir |
| **NPS / encuesta post-emisión** | Calidad de atención |

### Más adelante (escala / oficina grande)

| Idea | Para qué sirve |
|------|----------------|
| **Cotizador flotillas** | Empresas / varios vehículos |
| **Gastos médicos (familia)** | Padecimientos, suma asegurada, parentescos |
| **Vida y beneficiarios** | Gestión de designaciones |
| **Contabilidad ligera** | Ingresos, egresos, utilidad por agente |
| **Marketing**: landing + QR + tracking UTM | Origen del lead |
| **Capacitación / library** | Materiales de aseguradoras, guías |
| **API propia Segurod** | Que otras apps lean cartera / creen leads |
| **White-label avanzado** | Dominio propio (cotiza.tuagencia.com), CSS completo |
| **Integración Google Calendar / Outlook** | Sincronizar agenda |
| **Pagos en línea al cliente** | Link de pago de prima (si hay pasarela + convenio) |

### Ideas de UX que suelen marcar diferencia

- **Hoy en un vistazo:** agenda del día + vencimientos + comisiones por facturar + leads nuevos  
- **Ficha 360 del cliente:** chat, pólizas, docs, comisiones, tareas  
- **Modo “solo móvil”** para agentes en calle  
- **Botón “compartir portal”** al cliente por WhatsApp  

---

## 10. Alcance por fases (actualizado)

### Fase 0 — Validación (borrador)

- [x] Definir canales y cotización completa  
- [x] Investigar APIs  
- [x] Modos manual / API / mixto con toggles (activar al tener sandbox)  
- [x] Definir módulo agente: agenda, comisiones, cartera, recordatorios, portal  
- [x] Modelo SaaS: config (logo, datos, correo, usuarios, permisos, auditoría, respaldos)  
- [x] Comisiones por aseguradora + split interno por agente + panel CEO  
- [x] Arquitectura por tipos de módulo (cambios aislados por módulo)  
- [ ] Validar país, ramos y figura legal  
- [ ] Elegir partners de API  
- [ ] Boceto UX: config + panel agente + panel CEO + portal cliente — **sin código**

### Fase 1 — MVP SaaS + cotización + leads

- Alta de tenant (oficina) + login  
- **Configuración:** logo, datos empresa/agente, direcciones, correo de envíos  
- Usuarios vendedor + roles/permisos básicos + auditoría de login/cambios clave  
- Tablas simples de **% comisión por aseguradora** (aunque sea alta manual)  
- **% comisión interna** por usuario  
- WhatsApp + web: captura completa  
- Cotización **manual** operativa desde el día 1  
- Toggles API OFF (listos para encender después)  
- Panel: leads y asignación básica  
- Ficha mínima de cliente  
- **Panel CEO** básico: cotizaciones creadas, cerradas, por ramo (aunque solo auto al inicio)

### Fase 2 — Cartera y agenda

- Cartera de pólizas (alta manual o import CSV)  
- Agenda y tareas  
- Recordatorios de vencimiento (email y/o WhatsApp)  
- Portal cliente básico (pólizas + vencimientos)  
- PWA “agregar a inicio” (cliente + admin) + opt-in de **push**  
- Config de tipos de alerta (vencimiento, lead nuevo, etc.)

### Fase 3 — API opcional + comisiones

- Adapter(s) detrás de toggle (sandbox → producción)  
- Modo **mixto**: compañías con API ON + resto manual  
- Fallback a manual si API off o error  
- Módulo comisiones (por facturar / por pagar / pagadas)  
- Facturación a aseguradoras (registro + adjuntos; CFDI según decisión)  
- Tablero renovaciones

### Fase 4 — Operación avanzada + plataforma SaaS

- Emisión / documentos  
- Siniestros ligeros  
- Conciliación de estados de cuenta  
- Respaldos self-service / restore  
- Billing de suscripción Segurod (planes y límites)  
- Reportes / app  
- Más ramos

---

## 11. Decisiones abiertas (para siguiente reunión)

1. **País y regulación:** ¿México? ¿Cédula / oficina agente o broker?  
2. **Ramo inicial:** ¿Solo auto o también GMM / hogar?  
3. **Planes SaaS:** precios, límites (usuarios, cotizaciones, WA), trial  
4. **Emisión:** ¿solo cotizar + lead, o cotizar y emitir?  
5. **WhatsApp:** Cloud API directa o BSP; ¿un número por tenant?  
6. **Provider API:** Dora / Inter Connect / Bruno / Surexs / directo  
6b. **Cotización:** arrancar 100 % manual; ¿quién activa toggles API? (dueño/admin)  
7. **Comisiones:** ¿solo registro interno o también **timbrado CFDI** desde día 1?  
8. **Correo de envíos:** ¿SMTP del cliente o correo gestionado por Segurod?  
9. **Respaldos:** ¿restore self-service o solo vía soporte?  
10. **Cartera inicial:** ¿alta manual, import Excel, o sync con aseguradoras?  
11. **Dominio:** app.segurod.mx vs subdominio por oficina (acme.segurod.mx)  
12. **Marca visual Segurod** (la plataforma) vs marca de cada tenant

---

## 12. Riesgos y supuestos

| Riesgo | Mitigación |
|--------|------------|
| Sin convenio API al lanzar | Cotización manual + toggles OFF; cartera/agenda sí aportan valor |
| Tarifas distintas a las del agente | BYOR si el partner lo permite |
| Abandono en WhatsApp | Enlace web temprano |
| Datos personales | Aviso de privacidad, consentimiento WA/web/portal |
| Expectativa de precio “oficial” | Etiquetar estimado vs tarifa real |
| CFDI / factura mal diseñada | Empezar con “registro de factura” y enlazar PAC después |
| Recordatorios molestos | Reglas claras + opt-out + tope por póliza |
| Portal sin adopción | Activarlo al emitir / renovar y mandar link por WA |
| Push en iPhone sin instalar | Guiar a “Agregar a inicio”; sin PWA instalada el push es limitado |
| Usuario niega notificaciones | Fallback email/WhatsApp + centro in-app |
| Mezcla de datos entre oficinas | Multi-tenant estricto; nunca compartir tablas sin `tenant_id` |
| Vendedor ve comisiones ajenas | Permisos por rol + cartera asignada |
| SMTP mal configurado | Test de envío + logs + fallback de plataforma |

---

## 13. Entregables del borrador (esta etapa)

1. Documento de proyecto (SaaS + cotización + ops agente + portal)  
2. Matriz de APIs / partners (sección 5)  
3. Mapa de flujos WhatsApp, web, renovación y comisiones  
4. Configuración SaaS + módulo agente + backlog (secciones 8, 8A y 9)  
5. Decisiones abiertas (sección 11)

**Próximo paso sugerido (sin programar):**  
Boceto de **Configuración del tenant** (logo, usuarios, correo) → MVP panel → portal cliente → contacto API.

---

## 14. Referencias rápidas (investigación)

- Agregadores / Open Insurance (MX): Dora, Inter Connect, Bruno, Surexs, bolttech  
- Canal WhatsApp: Meta WhatsApp Cloud API (+ BSP opcionales)  
- Software de referencia (categoría): CRM/agencias de seguros, portales Q 360 / IDEAS GNP (como referencia de funciones, no como competencia a clonar)  
- Modelos vecinos: comparador + chatbot + cartera + cobranza de comisiones  

*Las APIs concretas se confirman con cada proveedor; no hay un API pública universal de todas las aseguradoras.*

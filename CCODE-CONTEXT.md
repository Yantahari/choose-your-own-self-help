# CCODE-CONTEXT — Choose Your Own Self-Help

Documento de traspaso para Claude Code. Actualizar al final de cada sesión relevante.

**Última actualización:** 2026-04-25

---

## Qué es esto

Web y automatización para promocionar el libro "Choose Your Own Self-Help" de Luna Bolt. El libro está publicado en Amazon KDP. Este repo es el GitHub Pages del quiz + blog SEO + autoposter de Bluesky.

- **Live:** https://yantahari.github.io/choose-your-own-self-help/
- **Repo:** https://github.com/Yantahari/choose-your-own-self-help

---

## Producción — qué está vivo

| Componente | URL | Estado |
|---|---|---|
| Quiz interactivo EN | `/index.html` | Live |
| Quiz interactivo ES | `/es.html` | Live |
| Blog SEO EN | `/blog/` | 4 artículos publicados |
| Buy page EN | `/buy-en.html` | Live |
| Buy page ES | `/buy-es.html` | Live |
| Autoposter Bluesky | `autoposter.py` | Operativo (ver abajo) |
| Open Graph (EN + ES) | `/images/og-share*.png` | Configurado |
| Google Analytics | G-ZZNGFH5D7N (property 530845489) | Conectado |

---

## Amazon KDP — publicado

| Versión | Formato | ASIN | Link Amazon |
|---|---|---|---|
| Español ebook | Kindle | B0GFFPWKDS | amazon.es/dp/B0GFFPWKDS |
| Español papel | Tapa blanda | B0GVWD1L5D | amazon.es/dp/B0GVWD1L5D |
| Inglés ebook | Kindle | B0DWPJC6C6 | amazon.com/dp/B0DWPJC6C6 |
| Inglés papel | Tapa blanda | B0GVXQWMCN | amazon.com/dp/B0GVXQWMCN |

---

## Canales de redes

| Canal | Handle / URL | Ritmo |
|---|---|---|
| Bluesky | @lunabolt.bsky.social | 1/día automático |
| Medium | @lunabolt | 1 cada 3 días (manual) |
| Facebook | Página Luna Bolt | 2/semana (manual) |

---

## Autoposter Bluesky — detalle operativo

- **Script:** `autoposter.py` (publica POSTS[next_index] y actualiza estado)
- **Estado:** `bluesky_state.json` — `next_index` apunta al próximo post a publicar
- **Cola de posts:** 30 posts hardcoded en `autoposter.py` (alterna EN/ES)
- **Trigger remoto (Anthropic):** `trig_01VPAN2FsTtPfW5TLhmHprWf` — "Luna Bolt Bluesky Daily Post", cron `0 8 * * *` (10:00 CEST)

### Problemas conocidos (19 abr 2026)
- El trigger remoto `Run now` falla con `github_repo_access_denied` a pesar de tener la GitHub App "Claude" instalada con acceso al repo. Pendiente verificar si los runs automáticos (cron) funcionan o comparten el problema.
- Si el automático falla, ejecutar manualmente: `cd choose-your-own-self-help && python3 autoposter.py && git add bluesky_state.json && git commit -m "..." && git push`.

### Credenciales
- `.env` (en el padre del repo, no commiteado): `BLUESKY_HANDLE=lunabolt.bsky.social`, `BLUESKY_APP_PASSWORD=...`

---

## Reglas del proyecto

1. **Coste cero hasta ingresos.** No proponer herramientas de pago. Solo invertir cuando el libro genere dinero.
2. **Autonomía máxima.** El usuario tiene poco tiempo, delega con confianza. Actuar, no preguntar si el paso es claro.
3. **Links a Amazon** (no "coming soon"): usar los ASINs arriba. Por defecto, link al Kindle EN (`B0DWPJC6C6`) para contenido en inglés.
4. **Medium:** escribir artículo localmente, el usuario copia-pega manualmente. Ojo al pegar links: pegarlos limpios (sin markdown del editor) porque si no Medium los deja rotos.
5. **Canales SEO + Medium:** tráfico orgánico, tarda 2-4 semanas en notarse.

---

## Calendario Medium

Archivo con calendario completo: `../promocion/medium_calendario.md` (en el proyecto padre, no en este repo).

Publicados al 19 abr: 3 (Homeopathy, Mercury Retrograde, Reiki). Siguiente pendiente según calendario: "Which Alternative Therapy Is Right for Me?" (programado 10 abr, con retraso).

---

## Scripts disponibles

| Script | Ubicación | Para qué |
|---|---|---|
| `autoposter.py` | raíz repo | Publica 1 post de Bluesky y actualiza `bluesky_state.json` |

Consulta de métricas GA (ejecutar desde el proyecto padre):
```bash
GOOGLE_APPLICATION_CREDENTIALS="../luna-bolt-analytics-206cef37f414.json" python3 <<EOF
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
client = BetaAnalyticsDataClient()
r = client.run_report(RunReportRequest(
    property="properties/530845489",
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    metrics=[Metric(name="activeUsers"), Metric(name="sessions")],
))
print(r.rows[0].metric_values[0].value, "users /", r.rows[0].metric_values[1].value, "sessions")
EOF
```

---

## Paths importantes (en el proyecto padre)

Ruta base: `/home/yantahari/Documents/Projectes/Elije tu propia.../`

| Path | Contenido |
|---|---|
| `PROYECTO_COO.md` | Documento resumen del proyecto para el COO |
| `promocion/medium_calendario.md` | Calendario editorial Medium (19 artículos) |
| `promocion/medium_articulos*.md` | Artículos preparados para Medium |
| `promocion/contenido_redes_EN.md` / `_ES.md` | 30 posts por idioma |
| `promocion/reddit_posts.md` | Posts preparados (sin publicar) |
| `promocion/fb_cover_woowoo.png` | Cover de Facebook |
| `promocion/lunabolt_avatar_2.png` | Avatar usado en redes |
| `libro/ilustraciones/terapias/` | Ilustraciones .png por terapia |
| `libro_en/output/cover_front_en.png` | Portada inglesa |
| `libro/output/portada_solo_imagen.png` | Portada española |
| `.env` | Credenciales Bluesky (NO commiteado) |
| `luna-bolt-analytics-206cef37f414.json` | Service account GA (NO commiteado) |

---

## Estrategia actual (giro 25 abr 2026)

Después de 6 semanas el crecimiento orgánico es **cero**: 0 interacciones en FB, 0 visitas GA en 7 días, 3 seguidores Bluesky. Cambio de táctica:

1. **Reducir FB propio a 1/semana** (antes 2/semana). Publicar al vacío no merece el esfuerzo.
2. **Foco en intervenciones de Luna en posts ajenos** — comentar en publicaciones de las cuentas seguidas (Goop, Chopra, Dispenza, Bryan Johnson, Mushies, IFLScience, Brian Cox, etc.). Ahí está la audiencia.
3. **Flujo:** el usuario detecta post jugoso, lo comparte (link/screenshot/texto), Claude redacta comentario en voz Luna, usuario aprueba/publica.
4. Medium y Bluesky se mantienen como están.

## En curso / pendiente

- Esperar primera oportunidad de comentario reactivo desde el feed renovado de FB.
- Verificar si el trigger remoto Bluesky funciona automáticamente. Si falla, ejecución manual durante sesiones.
- Seguir publicando Medium según calendario (retraso acumulado de ~2 semanas).
- Primera reseña verificada en Amazon (acelera algoritmo KDP).

---

## Métricas a 25 abr 2026

- **Bluesky:** 3 seguidores, 5 posts publicados, 2 likes (sin cambios desde 19 abr; trigger remoto sigue roto, último post manual del 19 abr)
- **GA últimos 7 días:** 0 usuarios / 0 sesiones — **estancamiento total**
- **GA últimos 30 días:** 15 usuarios / 15 sesiones / 16 vistas (todo del periodo previo al 19 abr)
- **FB Feb-Abr (12 posts en 6 semanas):** 31 impresiones totales, 55 vistas, **0 interacciones, 0 reacciones, 0 shares, 0 comentarios, 0 net follows**. Cada post tiene ~1 viewer (probablemente el usuario verificando).
- **Medium:** 4 artículos publicados, último el 25 abr (Crystal Therapy)
- **Cuentas FB seguidas:** ~16 (David Sedaris, Mark Manson, IFLScience, Goop, Committee for Skeptical Inquiry, Sarah Knight, + 6 nuevas el 25 abr: Deepak Chopra, Joe Dispenza, Bryan Johnson, Science-Based Medicine, Brian Cox, Caitlin Doughty)
- **Amazon:** sin datos confirmados de ventas

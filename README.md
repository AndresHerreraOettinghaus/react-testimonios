# Testimonios — Práctica inicial de React

Ingeniería de Software · Unidad 3 · TecNM Celaya · AGO–DIC 2026

Interfaz que muestra testimonios de uno en uno con navegación Anterior, Siguiente y Aleatorio, y una ampliación con reproducción automática cada cinco segundos. Los testimonios y retratos son datos ficticios de demostración.

## Integrantes

| Integrante | No. de control | GitHub |
|---|---|---|
| Diego | 21031300 | |
| Andrés Herrera Oettinghaus | 23030694 | AndresHerreraOettinghaus |

Trabajo en pareja con roles de conductor y observador; Andrés creó el repositorio, la configuración y los primeros datos. El tablero, la estimación y el registro de roles están en [docs/TABLERO-Y-ROLES.md](docs/TABLERO-Y-ROLES.md).

## Etapa terminada

- **Etapa básica: terminada.** Cumple los criterios de aceptación y pasa P01 a P10. Conservada en la etiqueta `etapa-basica`.
- **Ampliación con reproducción automática: terminada.** Pasa A01 a A07. Es la versión actual de `main`.
- **Experimento de reutilización (sección 12): realizado** en la rama `experimento-reutilizacion`; `main` conserva la navegación.

## Versiones

| Herramienta | Versión |
|---|---|
| Node.js | v22.23.4 (LTS) |
| npm | 10.9.9 |
| Vite | 8.3.6 |
| React / React DOM | 19.3.1 |

Cada integrante registra aquí la salida de `node -v` y `npm -v` de su equipo si es distinta.

## Instalación y ejecución

```bash
git clone https://github.com/AndresHerreraOettinghaus/react-testimonios.git
cd react-testimonios
npm install
npm run dev        # servidor de desarrollo; abrir la dirección Local que muestra la terminal
npm run build      # versión de producción en dist/
npm run preview    # revisar localmente la compilación
```

Para ver la etapa básica sin la ampliación: `git checkout etapa-basica`. Para volver: `git checkout main`.

## Estructura

```
testimonios/
├── index.html              # contiene <div id="root">; carga src/main.jsx
├── public/fotos/           # retratos ilustrativos locales (SVG)
├── src/
│   ├── main.jsx            # crea la raíz de React, monta App e importa styles.css
│   ├── App.jsx             # conserva el estado (index, reproduciendo) y coordina
│   ├── data.js             # arreglo de 8 testimonios (módulo JS, no JSON)
│   ├── styles.css          # estilos únicos de la aplicación
│   └── components/
│       ├── Testimonial.jsx # presenta un registro recibido en la prop item
│       └── Controls.jsx    # botones que comunican acciones con callbacks
├── docs/                   # pruebas, tablero, explicaciones y capturas
└── pruebas/                # scripts que repiten las pruebas en el navegador
```

Recorrido: `index.html` → `main.jsx` → `App` → `Testimonial` y `Controls`.

## Decisiones principales

1. **Responsabilidades separadas.** `App` es el único dueño del estado; `Testimonial` solo presenta lo que recibe en `item`; `Controls` no sabe qué testimonio se muestra, solo avisa la intención mediante `onPrev`, `onNext` y `onRandom`.
2. **Retratos locales en lugar de URLs remotas.** Los tres primeros registros usaban `i.pravatar.cc`, que depende de conexión y muestra fotografías de personas reales. Se reemplazaron por ilustraciones SVG con iniciales en `public/fotos` (rutas `/fotos/ana.svg`, etc.). Funcionan sin internet y no usan la imagen de nadie. Se conservaron los nombres, cargos y textos de esos tres registros.
3. **Posición segura con `index % total`.** Durante las pruebas, editar `data.js` con la app abierta dejaba la página en blanco: la recarga en caliente de Vite conserva `index` y podía quedar fuera del nuevo rango. Se calcula `posicion = index % total` antes de renderizar. Es coherente con `next`, `prev` y `random`, que parten del mismo residuo. Detalle y capturas en [docs/PRUEBAS.md](docs/PRUEBAS.md#corrección-realizada).
4. **Navegación modular.** `%` envuelve los extremos; en `prev` se suma `total` para no obtener negativos; Aleatorio elige un salto entre 1 y `total − 1` para nunca repetir el actual.
5. **Ampliación.** El intervalo vive en un `useEffect` con limpieza (`clearInterval`) y dependencias `[reproduciendo, total]`. Inicia pausado para permitir leer; cualquier acción manual pausa y solo Reanudar lo reactiva. Se retiró `aria-live` del contador para evitar anuncios cada cinco segundos. El botón Pausar/Reanudar lleva la clase `autoplay-toggle` solo para separarlo 10 px de los controles.
6. **Imports de CSS eliminados.** Al borrar `App.css` e `index.css` (commit `e053d2d`), `App.jsx` y `main.jsx` todavía los importaban y la compilación fallaba. El commit de la tarjeta (`5e3067b`) reescribe ambos archivos y `main.jsx` importa solo `styles.css`.
7. **`index.html` en español.** Se cambió `lang="en"` por `lang="es"` para que los lectores de pantalla pronuncien bien el contenido, y el título a «Testimonios». Se conservó `<div id="root">`.
8. **`StrictMode` se conserva.** El efecto se monta, limpia y vuelve a montar en desarrollo; la prueba A07 confirma que nunca queda más de un intervalo activo.

## Pruebas

Registro completo con resultados, evidencia y la corrección realizada: [docs/PRUEBAS.md](docs/PRUEBAS.md).

| Etapa | Casos | Resultado |
|---|---|---|
| Básica | P01–P10 | 10 de 10 aprobadas |
| Ampliación | A01–A07 | 7 de 7 aprobadas |

Los casos se ejecutaron en Chromium con los scripts de `pruebas/` (Python + Playwright), que hacen los mismos clics y pulsaciones de teclado que la prueba manual y reemplazan temporalmente `data.js` para los casos de 3, 1 y 0 registros. Para repetirlos: `pip install playwright && playwright install chromium`, luego `python pruebas/pruebas_basicas.py . docs/capturas resultados.json`.

Capturas en tres anchos: [320 px](docs/capturas/ancho-320.png) · [768 px](docs/capturas/ancho-768.png) · [1280 px](docs/capturas/ancho-1280.png).

## Explicaciones individuales

- [docs/EXPLICACION-DIEGO.md](docs/EXPLICACION-DIEGO.md)
- [docs/EXPLICACION-ANDRES.md](docs/EXPLICACION-ANDRES.md)

## Referencias

- React, Inicio rápido: https://es.react.dev/learn
- Pensar en React: https://es.react.dev/learn/thinking-in-react
- El estado, la memoria de un componente: https://es.react.dev/learn/state-a-components-memory
- Renderizado y confirmación: https://es.react.dev/learn/render-and-commit
- Sincronizar con efectos: https://es.react.dev/learn/synchronizing-with-effects
- Guía de Vite: https://vite.dev/guide/

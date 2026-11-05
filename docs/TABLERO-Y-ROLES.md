# Tablero, estimación y registro de roles

Pareja: **Diego** y **Andrés Herrera Oettinghaus**.

## Historia de usuario

> Como visitante de un sitio web, quiero consultar testimonios de clientes mediante controles de navegación para conocer sus experiencias con el servicio.

Criterios de aceptación: los seis de la sección 1 de la guía (tarjeta con foto, nombre, cargo, comentario y posición; Anterior y Siguiente circulares; Aleatorio distinto del actual; responsabilidades App / Testimonial / Controls; casos de 1 y 0 registros; diseño adaptable y accesible por teclado).

## Tareas y estimación

Estimación en puntos de historia con la serie 1, 2, 3, 5, acordada entre los dos. Expresa esfuerzo relativo, no horas: la tarea de 1 punto (entorno) se tomó como referencia.

| # | Tarea | Puntos | Estado |
|---|---|---|---|
| T1 | Entorno: Vite, Node, estructura de carpetas | 1 | Terminado |
| T2 | Datos: `data.js` con 8 registros y retratos locales | 2 | Terminado |
| T3 | Tarjeta: `Testimonial`, `main.jsx`, `App` estático | 2 | Terminado |
| T4 | Navegación: `Controls`, `useState`, límites, aleatorio, 0 registros | 3 | Terminado |
| T5 | Estilos: `styles.css`, tres anchos, foco visible | 2 | Terminado |
| T6 | Verificación: P01–P10, capturas, corrección | 3 | Terminado |
| | **Subtotal etapa básica** | **13** | |
| T7 | Ampliación: `useEffect`, Pausar/Reanudar | 3 | Terminado |
| T8 | Verificación de la ampliación: A01–A07 | 2 | Terminado |
| T9 | Experimento de reutilización (sección 12) | 1 | Terminado |
| T10 | Documentación: README, registro de pruebas, este tablero | 2 | Terminado |
| T11 | Revisión por otra pareja y cambios solicitados | 1 | **En revisión** |

## Tablero

| Pendiente | En proceso | En revisión | Terminado |
|---|---|---|---|
| | | T11 Revisión por otra pareja | T1, T2, T3, T4, T5, T6, T7, T8, T9, T10 |

## Registro de cambio de roles

Conductor: escribe el código y hace el commit. Observador: revisa cada línea, piensa en los casos límite y consulta la guía. Cada avance terminó en uno o más commits del repositorio `AndresHerreraOettinghaus/react-testimonios`; el hash permite ver exactamente qué se hizo y quién lo subió.

| Avance | Tarea | Conductor | Observador | Qué revisó el observador | Commit |
|---|---|---|---|---|---|
| 1 | T1 Entorno | Andrés | Diego | Versiones de Node y npm; que `index.html` conserve `#root`; que se eliminaran `App.css` e `index.css`. Quedaron sus `import` en `App.jsx` y `main.jsx` (se corrigió en el avance 4) | `e9a7610`, `e053d2d` |
| 2 | T2 Datos (3 registros) | Andrés | Diego | Que los campos coincidan con los que desestructura `Testimonial`; `id` únicos; que sea módulo JS con `export default` | `bd3f30f` |
| 3 | T2 Datos (5 registros y retratos) | Diego | Andrés | Que se conservaran los textos del avance 2; rutas `/fotos/...` existentes; un texto largo para probar P09 | `370a312` |
| 4 | T3 Tarjeta | Diego | Andrés | Que el hijo no importe `data.js`; `alt` descriptivo; `h2` bajo el `h1`; que ya no se importen los CSS borrados y el proyecto compile | `5e3067b` |
| 5 | T4 Navegación | Diego | Andrés | Que `onClick` reciba la función y no `onNext()`; la traza 0 → 1 → 2 → 0 con `%`; el `+ total` en `prev`; que el `useState` esté antes del `return` condicional | `06de1b6` |
| 6 | T5 Estilos | Diego | Andrés | Foco visible al tabular; botones de 44 px de alto; sin desplazamiento horizontal en 320 px | `340673d` |
| 7 | T6 Verificación | Diego | Andrés | Ejecutar P01–P10; analizar la causa del fallo de P06 (recarga en caliente) y comprobar `index % total` | `f73b47f` |
| 8 | T7 Ampliación | Diego | Andrés | Que el intervalo esté dentro del efecto y no en el cuerpo de `App`; el `return` con `clearInterval`; dependencias `[reproduciendo, total]`; quitar `aria-live` | `6758f1e` |
| 9 | T8 Verificación ampliación | Diego | Andrés | A01–A07; que al alternar no se acumulen intervalos con `StrictMode` | `281a024` |
| 10 | T9 Experimento | Diego | Andrés | Que el cambio de una sola regla afecte las tres tarjetas; que se hiciera en una rama aparte | `1ad4fb6` (rama `experimento-reutilizacion`) |
| 11 | T10 Documentación | Diego | Andrés | Que el README refleje las versiones reales, la etapa terminada y las decisiones | último commit de `main` |
| 12 | T11 Cambios de la revisión | Andrés | Diego | Atender las observaciones de la pareja revisora | pendiente |

Reparto: Andrés condujo la configuración y los primeros datos (avances 1–2) y conduce los cambios que pida la revisión (avance 12). Diego condujo del avance 3 al 11.

## Revisión por otra pareja

*Esta sección la llena la pareja revisora.*

Pareja revisora: ______________________ y ______________________ · Fecha: ____________

| Aspecto | Cumple (sí / no) | Observaciones |
|---|---|---|
| `App` conserva el estado; `Testimonial` solo presenta; `Controls` solo avisa con callbacks | | |
| Props tratadas como solo lectura; ningún hijo importa `data.js` | | |
| Anterior y Siguiente circulares; Aleatorio nunca repite | | |
| Funciona con 1 y con 0 registros | | |
| Se ve bien en 320, 768 y 1280 px; foco visible; se usa con teclado | | |
| Los casos P01–P10 son claros y se pueden repetir | | |
| `npm run build` compila sin errores | | |

Cambios solicitados por la pareja revisora y cómo se atendieron:

| Observación | Cambio realizado | Commit |
|---|---|---|
| | | |

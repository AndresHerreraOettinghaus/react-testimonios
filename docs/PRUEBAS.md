# Registro de pruebas

Fecha de ejecución: 05/11/2026 · Navegador: Chromium 153 · Servidor: `npm run dev` (Vite 8.3.6, con `StrictMode`).

P01 a P07 se ejecutaron con los tres registros iniciales de la guía; P06 y P07 con `data.js` reducido temporalmente a uno y a cero registros; P08 a P10 con los ocho registros finales. Las pruebas básicas se registran separadas de las de autoplay.

## Etapa básica (etiqueta `etapa-basica`)

| Prueba | Acción | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| P01 Inicio | Abrir la página | Ana y 1 de 3 | Ana Pérez · Testimonio 1 de 3 | Aprobado |
| P02 Siguiente | Desde Ana, Siguiente | Luis y 2 de 3 | Luis García · Testimonio 2 de 3 | Aprobado |
| P03 Límite superior | Desde María, Siguiente | Ana | Ana Pérez · Testimonio 1 de 3 | Aprobado |
| P04 Límite inferior | Desde Ana, Anterior | María | María López · Testimonio 3 de 3 | Aprobado |
| P05 Aleatorio | 10 clics seguidos | Cada clic cambia a otra posición válida | Desde María (3 de 3): 1, 2, 3, 2, 1, 3, 1, 2, 3, 1; ninguna repite la anterior | Aprobado |
| P06 Un registro | `data.js` con un objeto; Anterior, Siguiente, Aleatorio, Siguiente, Anterior | Se mantiene el registro, sin errores | Ana Pérez · 1 de 1 tras los 5 clics; 0 errores en consola | Aprobado (tras corrección) |
| P07 Sin registros | `data.js` con `[]` | Mensaje y sin controles | Mensaje visible; 0 tarjetas; 0 botones; 0 errores | Aprobado (tras corrección) |
| P08 Ampliación de datos | Restaurar y recorrer con Siguiente 8 veces | Navegación completa, contador de 8 | 8 nombres distintos y regresa a 1 de 8; las 8 fotos locales cargan | Aprobado |
| P09 Presentación | Anchos 320, 768 y 1280; texto largo; Tab, Enter, Espacio | Sin desplazamiento horizontal; foco visible; teclado funcional | `scrollWidth` = `clientWidth` en los tres anchos, también con el texto largo de Valeria Torres. Tab recorre Anterior → Siguiente → Aleatorio con contorno de 3 px; Enter y Espacio activan el botón enfocado | Aprobado |
| P10 Compilación | `npm run build` y revisar consola | Sin errores | Build correcto; 0 errores de aplicación en consola durante P01–P09 | Aprobado (tras corrección) |

### Inspección de la lógica de Aleatorio (P05)

El muestreo de 10 clics no demuestra la propiedad por sí solo, así que también se revisó la fórmula:

```js
const salto = 1 + Math.floor(Math.random() * (total - 1));
setIndex(actual => (actual + salto) % total);
```

`Math.random()` devuelve un valor en [0, 1), por lo que `salto` está entre 1 y `total − 1`. Sumar un salto que no es 0 ni múltiplo de `total` nunca deja el residuo igual al actual. Se comprobó en Node para `total` de 2 a 20, todas las posiciones y valores extremos de `Math.random` (0, 0.999999999): 1254 casos, 0 repeticiones o posiciones fuera de rango. Con `total < 2` la función sale antes de llamar a `setIndex`.

### Capturas

| Ancho | Primer registro | Texto largo |
|---|---|---|
| 320 px | [ancho-320.png](capturas/ancho-320.png) | [texto-largo-320.png](capturas/texto-largo-320.png) |
| 768 px | [ancho-768.png](capturas/ancho-768.png) | [texto-largo-768.png](capturas/texto-largo-768.png) |
| 1280 px | [ancho-1280.png](capturas/ancho-1280.png) | [texto-largo-1280.png](capturas/texto-largo-1280.png) |

Otras: [foco con teclado](capturas/foco-teclado.png) · [tres registros](capturas/p01-p05-tres-registros.png) · [sin registros](capturas/p07-sin-registros.png).

## Corrección realizada

**Síntoma.** En una ejecución de las pruebas falló P06: la consola mostró `Cannot destructure property 'nombre' of 'item' as it is undefined.` y la página quedó en blanco. P07 y P10 también se marcaron como fallidos porque verifican que la consola no tenga errores acumulados. En otra ejecución las tres pasaron: el fallo depende de en qué testimonio termine P05, que es aleatorio.

**Causa.** Para P06 se editó `data.js` (de 3 a 1 registro) con la aplicación abierta en Luis (`index = 1`), donde había quedado tras P05. Cuando P05 terminaba en Ana (`index = 0`), la posición seguía existiendo y no fallaba. La recarga en caliente de Vite reemplaza el módulo pero conserva el estado de `App`, así que `index` seguía en 1 y `testimonios[1]` ya no existía. `Testimonial` recibió `undefined` en `item` y falló al desestructurar.

**Reproducción aislada.** Como la suite no lo detecta siempre, se escribió `pruebas/reproducir_hmr.py`, que no depende del azar: con la app en «Testimonio 8 de 8», cambia `data.js` a un registro sin recargar. Sobre el commit de estilos (`340673d`), antes de la corrección, la tarjeta y el contador desaparecen siempre ([antes](capturas/correccion-antes.png)).

**Solución.** En `App.jsx`, después de la validación de cero registros:

```js
const posicion = index % total;
// <Testimonial item={testimonios[posicion]} /> y "Testimonio {posicion + 1} de {total}"
```

Se eligió `%` y no «volver a 0» porque `next`, `prev` y `random` también calculan desde `actual % total`; así lo que se ve y el siguiente paso coinciden.

**Comprobación.** Se repitió la reproducción: muestra Ana Pérez · Testimonio 1 de 1 y 0 errores ([después](capturas/correccion-despues.png)). Se volvieron a ejecutar P01–P10: 10 de 10 aprobadas.

## Ampliación con reproducción automática (`main`)

Se usó el reloj simulado de Playwright para avanzar el tiempo exacto y se contaron los intervalos de 5000 ms activos envolviendo `setInterval` y `clearInterval`.

| Prueba | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|
| A01 Activación | Reanudar inicia avances separados ~5 s | Sin reanudar, 6 s después sigue en 1 de 8. Tras Reanudar: a 4.9 s sigue 1 de 8, a 5 s pasa a 2 de 8, a 10 s a 3 de 8. 1 intervalo activo | Aprobado |
| A02 Pausa | Pausar mantiene el testimonio más de 5 s | 3 de 8 antes y 12 s después; 0 intervalos | Aprobado |
| A03 Acción manual | Anterior, Siguiente o Aleatorio cambian la tarjeta y dejan pausado | Siguiente 3→4, Anterior 4→3, Aleatorio 3→8; en los tres casos no hubo avance en 11 s y el botón volvió a «Reanudar» | Aprobado |
| A04 Reanudación | Reanudar varias veces sin aceleración | Tras alternar 5 veces, avanzó 8→1→2→3, uno por cada 5 s; 1 intervalo activo | Aprobado |
| A05 Límites | El último vuelve al primero | 8 de 8 → 1 de 8 | Aprobado |
| A06 Pocos datos | Con 0 o 1 registro no se crea intervalo | 1 registro: sin botón Pausar/Reanudar, 0 intervalos en 11 s. 0 registros: mensaje y 0 intervalos | Aprobado |
| A07 Limpieza | Sin intervalos acumulados al alternar | 10 alternancias: máximo 1 simultáneo; 0 al pausar; 0 errores. El `return () => clearInterval(intervalo)` del efecto se revisó en el código | Aprobado |

Captura: [reproduciendo](capturas/autoplay-reproduciendo.png).

También se volvieron a ejecutar P01–P10 sobre la versión con autoplay: 10 de 10 aprobadas.

## Revisión visual

En la captura con el botón de reproducción, «Pausar» quedaba pegado a la fila de controles. Se agregó `.autoplay-toggle { margin-top: 10px; }`, igual al `gap` de `.controls`, y se repitieron A01–A07 y P01–P10.

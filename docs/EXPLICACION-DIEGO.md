# Explicación individual — Diego

## Sección 3 · Comprobación previa

**Diferencia entre un objeto y un arreglo de objetos.** Un objeto agrupa los datos de una sola cosa con nombre de campo: `{ id: 1, nombre: 'Ana Pérez', cargo: 'CEO - EmpresaX', ... }` es un testimonio. Un arreglo es una lista ordenada que se recorre por posición: `testimonios` contiene ocho de esos objetos y `testimonios[0]` es el primero.

**Qué exporta `data.js` y qué recibe el `import`.** `data.js` exporta por defecto el arreglo `testimonios` (`export default testimonios`). En `App.jsx`, `import testimonios from './data.js'` recibe ese mismo arreglo; el nombre del lado del import lo elige quien importa, porque es una exportación por defecto.

**Por qué `nombre` está entre llaves en el JSX.** Las llaves indican que lo de adentro es una expresión de JavaScript y no texto literal. Sin llaves se mostraría la palabra «nombre»; con llaves se muestra el valor, por ejemplo «Ana Pérez».

**Qué pasa al pasar otro nombre al mismo componente.** `<Saludo nombre="Luis" />` muestra «Hola, Luis». Es la misma función con otra entrada: el componente no cambia, cambia la prop que recibe.

## Sección 7 · Detente y explica

**Qué archivo contiene la tarjeta y cuál el objeto mostrado.** La tarjeta está en `src/components/Testimonial.jsx`. El objeto mostrado viene de `src/data.js`; `App` elige cuál con `testimonios[posicion]`.

**Qué recibe `item` y por qué el hijo no importa `data.js`.** `item` recibe un solo objeto testimonio. `Testimonial` no necesita saber que existe una lista ni en qué posición va: solo presenta lo que le dan. Si importara `data.js`, quedaría atado a esos datos y no se podría reutilizar con otros.

**Diferencia entre `main.jsx` y `App.jsx`.** `main.jsx` es el punto de entrada: busca `#root` en `index.html`, crea la raíz de React con `createRoot`, monta `<App />` dentro de `StrictMode` e importa `styles.css` una sola vez. `App.jsx` es el componente principal de la interfaz: guarda el estado y decide qué mostrar.

**Qué copiaría si no existiera `Testimonial`.** Todo el `<article>` con la imagen, el `h2`, el cargo y el `blockquote`, cada vez que quisiera mostrar un testimonio. En el experimento de la sección 12 habría tenido que copiarlo tres veces.

## Sección 10 · Evidencias de comprensión

**Qué información baja de App a cada hijo.**

```
App  (estado: index, reproduciendo · datos: testimonios)
 ├── Testimonial  ← item = testimonios[posicion]        (un objeto, solo lectura)
 └── Controls     ← onPrev, onNext, onRandom            (funciones)
                     └── al hacer clic las invoca → el cambio sube a App
```

Hacia abajo bajan datos (`item`) y funciones (los callbacks). Hacia arriba no sube ningún valor directamente: `Controls` solo ejecuta la función que recibió y es `App` quien cambia su propio estado.

**Recorrido clic → callback → setIndex → renderizado → DOM.**
1. El usuario hace clic en «Siguiente».
2. React llama a la función que `Controls` recibió en `onNext`, que es `next` de `App` (en la ampliación, `() => navegar(next)`).
3. `next` llama a `setIndex(actual => (actual + 1) % total)`. No cambia `index` en ese instante; programa un nuevo valor.
4. React vuelve a ejecutar `App` con el nuevo `index`, calcula `posicion` y pasa otro objeto a `Testimonial`.
5. React compara el resultado con lo anterior y confirma en el DOM solo lo que cambió: la imagen, el nombre, el cargo, el texto y el contador.

**Por qué no se escribe `testimonios[index + 1]` sin controlar el límite.** En el último registro `index + 1` vale `total` y esa posición no existe: `testimonios[8]` es `undefined` y `Testimonial` falla al desestructurarlo. Por eso uso `% total`, que convierte 8 en 0 y vuelve al primero.

**Un error que encontré y cómo comprobé la solución.** En P06 cambié `data.js` a un solo registro con la app abierta en el segundo testimonio. La página quedó en blanco con `Cannot destructure property 'nombre' of 'item' as it is undefined`. La recarga en caliente de Vite reemplazó los datos pero conservó `index = 1`, y `testimonios[1]` ya no existía. Lo reproduje aparte, desde el testimonio 8 de 8, para confirmar la causa. La solución fue calcular `const posicion = index % total` antes de renderizar. Repetí la reproducción (mostró 1 de 1 sin errores) y volví a correr P01–P10: todas aprobadas.

## Sección 11 · Preguntas individuales

**Por qué el temporizador se maneja con un efecto y el clic con un evento.** El clic es algo que hace el usuario en un momento concreto: se responde en el manejador. El temporizador no lo causa ninguna interacción; es un sistema externo que debe existir mientras se cumpla una condición (`reproduciendo` y al menos dos registros). `useEffect` sirve para mantener la app sincronizada con algo externo: lo crea cuando la condición se cumple y lo elimina cuando deja de cumplirse.

**Qué problema evita `clearInterval`.** Que se acumulen intervalos. Sin la limpieza, cada vez que paso de Pausar a Reanudar se crearía un intervalo nuevo sin quitar el anterior, y el carrusel avanzaría cada vez más rápido. También seguiría corriendo aunque el componente se desmontara. En A07 alterné diez veces y nunca hubo más de un intervalo activo.

**Por qué no existe un Hook llamado `render`.** Renderizar no es algo que el componente pida; es lo que React hace al llamar a la función del componente. El componente solo describe la interfaz con JSX y React decide cuándo ejecutarlo, normalmente después de un cambio de estado. `createRoot(...).render(<App />)` en `main.jsx` es un método de la raíz que monta la aplicación una vez, no un Hook.

**Qué cambiaría si el arreglo llegara de una API.** Los testimonios dejarían de ser una constante importada y pasarían a ser estado de `App` (por ejemplo `const [testimonios, setTestimonios] = useState([])`). Haría falta un efecto que pida los datos al montar el componente, y estados para «cargando» y «error». Como el arreglo podría cambiar de tamaño, `index` podría quedar fuera de rango: justo el problema que ya vi con la recarga en caliente, así que `index % total` o reiniciar el índice al recibir datos nuevos seguiría siendo necesario.

## Sección 12 · Reflexión individual breve

**Qué reutilicé y qué duplicación evité.** Reutilicé `Testimonial`. En la rama `experimento-reutilizacion` lo usé tres veces (la tarjeta principal y dos de ejemplo) y agregué una sola línea a `.testimonial-card`: `border-top: 6px solid #125ca3;`. Las tres tarjetas cambiaron. Sin el componente habría tenido tres copias del `<article>` y tres lugares donde corregir cualquier cambio.

**Comparación con actualizar varios nodos del DOM a mano.** Sin React, en cada clic tendría que buscar la imagen, el nombre, el cargo, el texto y el contador con `querySelector` y cambiar cada uno (`src`, `alt`, `textContent`). Si olvido uno, la pantalla queda inconsistente, por ejemplo con la foto de Ana y el nombre de Luis. Con React solo cambio `index` y la interfaz se recalcula completa a partir de ese valor.

**Qué organización depende de mi diseño y qué aporta React.** Decidir que `App` sea el dueño del estado, que `Testimonial` solo presente y que `Controls` solo avise fue una decisión nuestra; React no obliga a separarlo así. React aporta el mecanismo: el estado con `useState`, volver a ejecutar el componente cuando cambia y confirmar en el DOM solo las diferencias.

**Una dificultad o costo de React en una aplicación pequeña.** Para tres botones y una tarjeta hay que instalar Node, npm, Vite y más de 200 KB de JavaScript en la compilación (`dist/assets/index-*.js` ≈ 222 KB, unos 70 KB comprimido). Con HTML, CSS y unas líneas de JavaScript se resolvería sin herramientas. Además hay que entender conceptos como el renderizado o la recarga en caliente, que fue justo lo que causó el error de P06.

**Una parte que todavía no comprendo.** ¿Cómo decide React Fast Refresh qué estado conservar cuando edito un archivo que no es un componente, como `data.js`? Vi que conservó `index` y reemplazó los datos, pero no sé en qué casos reinicia el estado y en cuáles lo mantiene.

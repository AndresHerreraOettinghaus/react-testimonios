import { useEffect, useState } from 'react';
import testimonios from './data.js';
import Testimonial from './components/Testimonial.jsx';
import Controls from './components/Controls.jsx';

export default function App() {
  const [index, setIndex] = useState(0);
  const total = testimonios.length;
  const [reproduciendo, setReproduciendo] = useState(false);

  useEffect(() => {
    if (!reproduciendo || total < 2) return;
    const intervalo = setInterval(() => {
      setIndex(actual => (actual + 1) % total);
    }, 5000);
    return () => clearInterval(intervalo);
  }, [reproduciendo, total]);

  function next() {
    setIndex(actual => (actual + 1) % total);
  }
  function prev() {
    setIndex(actual => (actual - 1 + total) % total);
  }
  function random() {
    if (total < 2) return;
    const salto = 1 + Math.floor(Math.random() * (total - 1));
    setIndex(actual => (actual + salto) % total);
  }
  function navegar(accion) {
    setReproduciendo(false);
    accion();
  }

  if (total === 0) {
    return (
      <main className="app">
        <h1>Experiencias de nuestros usuarios</h1>
        <p>No hay testimonios disponibles.</p>
      </main>
    );
  }

  // Si data.js se edita con la app abierta, Vite conserva index y puede quedar
  // fuera del nuevo rango. index % total lo mantiene válido y es la misma
  // posición de la que parten next, prev y random.
  const posicion = index % total;

  return (
    <main className="app">
      <h1>Experiencias de nuestros usuarios</h1>
      <Testimonial item={testimonios[posicion]} />
      <Controls
        onPrev={() => navegar(prev)}
        onNext={() => navegar(next)}
        onRandom={() => navegar(random)}
      />
      {total > 1 && (
        <button type="button" className="autoplay-toggle"
          onClick={() => setReproduciendo(actual => !actual)}>
          {reproduciendo ? 'Pausar' : 'Reanudar'}
        </button>
      )}
      <p className="counter">
        Testimonio {posicion + 1} de {total}
      </p>
    </main>
  );
}

import testimonios from './data.js';
import Testimonial from './components/Testimonial.jsx';

export default function App() {
  return (
    <main className="app">
      <h1>Experiencias de nuestros usuarios</h1>
      <Testimonial item={testimonios[0]} />
    </main>
  );
}

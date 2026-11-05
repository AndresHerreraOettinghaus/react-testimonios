export default function Controls({ onPrev, onNext, onRandom }) {
  return (
    <div className="controls">
      <button type="button" onClick={onPrev}>Anterior</button>
      <button type="button" onClick={onNext}>Siguiente</button>
      <button type="button" onClick={onRandom}>Aleatorio</button>
    </div>
  );
}

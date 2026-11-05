export default function Testimonial({ item }) {
  const { nombre, cargo, texto, foto } = item;
  return (
    <article className="testimonial-card">
      <img className="testimonial-photo"
        src={foto} alt={`Retrato ilustrativo de ${nombre}`}
        width="90" height="90" />
      <h2>{nombre}</h2>
      <p className="testimonial-role">{cargo}</p>
      <blockquote>{texto}</blockquote>
    </article>
  );
}

"""Ejecuta A01-A07 de la ampliación con reloj simulado de Playwright.

Uso: python3 pruebas_autoplay.py <ruta_proyecto> <carpeta_capturas> <salida_json>
Cuenta los intervalos de 5000 ms activos envolviendo setInterval/clearInterval.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

proyecto = Path(sys.argv[1]).resolve()
capturas = Path(sys.argv[2]).resolve()
salida = Path(sys.argv[3]).resolve()
capturas.mkdir(parents=True, exist_ok=True)
data_path = proyecto / "src" / "data.js"
data_original = data_path.read_text(encoding="utf-8")
UNO = """const testimonios = [
  { id: 1, nombre: 'Ana Pérez', cargo: 'CEO - EmpresaX',
    texto: 'Este servicio cambió la forma en que trabajamos. ¡Altamente recomendado!',
    foto: '/fotos/ana.svg' }
];
export default testimonios;
"""
VACIO = "const testimonios = [];\nexport default testimonios;\n"
URL = "http://localhost:5175/"
CONTADOR = """(() => {
  const activos = new Set();
  const si = window.setInterval.bind(window);
  const ci = window.clearInterval.bind(window);
  window.setInterval = (fn, ms, ...a) => {
    const id = si(fn, ms, ...a);
    if (ms === 5000) activos.add(id);
    return id;
  };
  window.clearInterval = id => { activos.delete(id); return ci(id); };
  window.__intervalos = () => activos.size;
})();"""

resultados, errores = [], []


def registrar(id_, nombre, esperado, obtenido, ok):
    resultados.append({"id": id_, "prueba": nombre, "esperado": esperado, "obtenido": obtenido,
                       "resultado": "Aprobado" if ok else "Fallido"})
    print(f"{id_} {'OK ' if ok else 'FALLA'} {obtenido}")


srv = subprocess.Popen(["npx", "vite", "--port", "5175", "--strictPort"], cwd=proyecto,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(3)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 768, "height": 800})
        page = ctx.new_page()
        page.clock.install()
        page.add_init_script(CONTADOR)
        page.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errores.append(str(e)))

        def abrir():
            page.goto(URL)
            page.wait_for_selector("h1")

        def pos():
            return page.locator(".counter").inner_text()

        def boton(nombre):
            return page.get_by_role("button", name=nombre, exact=True)

        def activos():
            return page.evaluate("window.__intervalos()")

        abrir()
        inicial = pos()
        page.clock.run_for(6000)
        sigue_pausado = pos() == inicial and boton("Reanudar").count() == 1

        # A01
        boton("Reanudar").click()
        page.clock.run_for(4900)
        a_4900 = pos()
        page.clock.run_for(100)
        a_5000 = pos()
        page.clock.run_for(5000)
        a_10000 = pos()
        page.screenshot(path=str(capturas / "autoplay-reproduciendo.png"))
        registrar("A01", "Activación",
                  "Inicia pausado; tras Reanudar avanza cada ~5 s",
                  f"6 s sin reanudar: {inicial} (pausado={sigue_pausado}); 4.9 s: {a_4900}; 5 s: {a_5000}; 10 s: {a_10000}; intervalos activos: {activos()}",
                  sigue_pausado and a_4900 == "Testimonio 1 de 8" and a_5000 == "Testimonio 2 de 8"
                  and a_10000 == "Testimonio 3 de 8" and activos() == 1)

        # A02
        boton("Pausar").click()
        antes = pos()
        page.clock.run_for(12000)
        registrar("A02", "Pausa", "Pausar mantiene el testimonio más de 5 s",
                  f"antes: {antes}; tras 12 s: {pos()}; intervalos activos: {activos()}",
                  pos() == antes and activos() == 0)

        # A03
        detalle, ok3 = [], True
        for accion in ("Siguiente", "Anterior", "Aleatorio"):
            boton("Reanudar").click()
            antes = pos()
            boton(accion).click()
            despues = pos()
            page.clock.run_for(11000)
            quieto = pos() == despues
            pausado = boton("Reanudar").count() == 1
            ok3 = ok3 and despues != antes and quieto and pausado and activos() == 0
            detalle.append(f"{accion}: {antes} → {despues}, 11 s después {pos()}, botón={'Reanudar' if pausado else 'Pausar'}")
        registrar("A03", "Acción manual", "Cambia la tarjeta y deja la reproducción pausada",
                  " | ".join(detalle), ok3)

        # A04
        for _ in range(5):
            boton("Reanudar").click()
            boton("Pausar").click()
        boton("Reanudar").click()
        base = int(pos().split()[1])
        pasos = []
        for _ in range(3):
            page.clock.run_for(5000)
            pasos.append(int(pos().split()[1]))
        esperado = [((base - 1 + k) % 8) + 1 for k in (1, 2, 3)]
        registrar("A04", "Reanudación", "Tras alternar 5 veces, un avance por cada 5 s (sin aceleración)",
                  f"desde {base}: {pasos} (esperado {esperado}); intervalos activos: {activos()}",
                  pasos == esperado and activos() == 1)
        boton("Pausar").click()

        # A05
        abrir()
        boton("Anterior").click()  # 8 de 8, queda pausado
        boton("Reanudar").click()
        page.clock.run_for(5000)
        registrar("A05", "Límites", "Durante autoplay, del último pasa al primero",
                  f"Testimonio 8 de 8 → {pos()}", pos() == "Testimonio 1 de 8")

        # A06
        data_path.write_text(UNO, encoding="utf-8")
        time.sleep(1)
        abrir()
        uno_botones = boton("Reanudar").count() + boton("Pausar").count()
        page.clock.run_for(11000)
        uno = (pos(), uno_botones, activos())
        data_path.write_text(VACIO, encoding="utf-8")
        time.sleep(1)
        abrir()
        page.clock.run_for(11000)
        cero = (page.get_by_text("No hay testimonios disponibles.").count(), activos())
        data_path.write_text(data_original, encoding="utf-8")
        time.sleep(1)
        registrar("A06", "Pocos datos", "Con 1 o 0 registros no hay botón de reproducción ni intervalo",
                  f"1 registro: {uno[0]}, botón Pausar/Reanudar={uno[1]}, intervalos={uno[2]} | 0 registros: mensaje={cero[0]}, intervalos={cero[1]}",
                  uno == ("Testimonio 1 de 1", 0, 0) and cero == (1, 0))

        # A07
        abrir()
        maximo = 0
        for _ in range(10):
            boton("Reanudar").click()
            maximo = max(maximo, activos())
            boton("Pausar").click()
        final_pausado = activos()
        boton("Reanudar").click()
        final_activo = activos()
        boton("Pausar").click()
        registrar("A07", "Limpieza",
                  "Al alternar 10 veces nunca hay más de un intervalo; pausado hay cero",
                  f"máximo simultáneo: {maximo}; pausado: {final_pausado}; reproduciendo: {final_activo}; errores en consola: {len(errores)}",
                  maximo == 1 and final_pausado == 0 and final_activo == 1 and not errores)
        b.close()
finally:
    data_path.write_text(data_original, encoding="utf-8")
    srv.terminate()
    srv.wait()

salida.write_text(json.dumps({"resultados": resultados, "errores_consola": errores},
                             ensure_ascii=False, indent=2), encoding="utf-8")

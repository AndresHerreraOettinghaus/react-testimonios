"""Ejecuta P01-P10 de la práctica contra el servidor de desarrollo de Vite.

Uso: python3 pruebas_basicas.py <ruta_proyecto> <carpeta_capturas> <salida_json>
Reemplaza temporalmente src/data.js para los casos de 3, 1 y 0 registros
y lo restaura al terminar.
"""
import json
import re
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

TRES = """const testimonios = [
  { id: 1, nombre: 'Ana Pérez', cargo: 'CEO - EmpresaX',
    texto: 'Este servicio cambió la forma en que trabajamos. ¡Altamente recomendado!',
    foto: '/fotos/ana.svg' },
  { id: 2, nombre: 'Luis García', cargo: 'Freelancer',
    texto: 'Me ayudó a duplicar mis clientes. Fácil de usar y fiable.',
    foto: '/fotos/luis.svg' },
  { id: 3, nombre: 'María López', cargo: 'Marketing Lead',
    texto: 'Resultados visibles en pocas semanas. Excelente soporte.',
    foto: '/fotos/maria.svg' }
];
export default testimonios;
"""
UNO = """const testimonios = [
  { id: 1, nombre: 'Ana Pérez', cargo: 'CEO - EmpresaX',
    texto: 'Este servicio cambió la forma en que trabajamos. ¡Altamente recomendado!',
    foto: '/fotos/ana.svg' }
];
export default testimonios;
"""
VACIO = "const testimonios = [];\nexport default testimonios;\n"

URL = "http://localhost:5173/"
resultados = []
errores_consola = []


def registrar(id_, nombre, esperado, obtenido, ok, notas=""):
    resultados.append({"id": id_, "prueba": nombre, "esperado": esperado,
                       "obtenido": obtenido, "resultado": "Aprobado" if ok else "Fallido",
                       "notas": notas})
    print(f"{id_} {'OK ' if ok else 'FALLA'} {obtenido}")


def usar_datos(contenido, page):
    data_path.write_text(contenido, encoding="utf-8")
    time.sleep(0.8)
    page.goto(URL)
    page.wait_for_selector("h1")


def estado(page):
    nombre = page.locator(".testimonial-card h2")
    contador = page.locator(".counter")
    return (nombre.inner_text() if nombre.count() else None,
            contador.inner_text() if contador.count() else None)


def clic(page, texto):
    page.get_by_role("button", name=texto, exact=True).click()


servidor = subprocess.Popen(["npx", "vite", "--port", "5173", "--strictPort"],
                            cwd=proyecto, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
try:
    time.sleep(3)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        page = nav.new_page(viewport={"width": 1280, "height": 900})
        page.on("console", lambda m: errores_consola.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errores_consola.append(str(e)))

        # ---- Tres registros ----
        usar_datos(TRES, page)
        n, c = estado(page)
        registrar("P01", "Inicio", "Ana Pérez · Testimonio 1 de 3", f"{n} · {c}",
                  n == "Ana Pérez" and c == "Testimonio 1 de 3")

        clic(page, "Siguiente")
        n, c = estado(page)
        registrar("P02", "Siguiente", "Luis García · Testimonio 2 de 3", f"{n} · {c}",
                  n == "Luis García" and c == "Testimonio 2 de 3")

        clic(page, "Siguiente")  # María
        clic(page, "Siguiente")  # vuelve a Ana
        n, c = estado(page)
        registrar("P03", "Límite superior", "Desde María, Siguiente muestra Ana Pérez · 1 de 3",
                  f"{n} · {c}", n == "Ana Pérez" and c == "Testimonio 1 de 3")

        clic(page, "Anterior")
        n, c = estado(page)
        registrar("P04", "Límite inferior", "Desde Ana, Anterior muestra María López · 3 de 3",
                  f"{n} · {c}", n == "María López" and c == "Testimonio 3 de 3")

        secuencia, ok5 = [], True
        for _ in range(10):
            antes = estado(page)[1]
            clic(page, "Aleatorio")
            despues = estado(page)[1]
            pos = int(re.search(r"Testimonio (\d+)", despues).group(1))
            secuencia.append(pos)
            ok5 = ok5 and antes != despues and 1 <= pos <= 3
        registrar("P05", "Aleatorio (10 clics)", "Cada clic cambia a otra posición válida",
                  "Posiciones: " + ", ".join(map(str, secuencia)), ok5)
        page.screenshot(path=str(capturas / "p01-p05-tres-registros.png"))

        # ---- Un registro ----
        usar_datos(UNO, page)
        ok6, vistos = True, []
        for b in ["Anterior", "Siguiente", "Aleatorio", "Siguiente", "Anterior"]:
            clic(page, b)
            n, c = estado(page)
            vistos.append(c)
            ok6 = ok6 and n == "Ana Pérez" and c == "Testimonio 1 de 1"
        errs6 = len(errores_consola)
        registrar("P06", "Un registro", "Los controles mantienen a Ana Pérez · 1 de 1, sin errores",
                  f"{vistos[-1]} tras 5 clics; errores en consola: {errs6}", ok6 and errs6 == 0)

        # ---- Sin registros ----
        usar_datos(VACIO, page)
        mensaje = page.get_by_text("No hay testimonios disponibles.").count()
        botones = page.get_by_role("button").count()
        tarjetas = page.locator(".testimonial-card").count()
        page.screenshot(path=str(capturas / "p07-sin-registros.png"))
        registrar("P07", "Sin registros", "Mensaje visible, sin tarjeta ni controles",
                  f"mensaje={mensaje}, tarjetas={tarjetas}, botones={botones}, errores={len(errores_consola)}",
                  mensaje == 1 and botones == 0 and tarjetas == 0 and len(errores_consola) == 0)

        # ---- Ocho registros (data.js real) ----
        usar_datos(data_original, page)
        nombres = []
        for _ in range(8):
            nombres.append(estado(page)[0])
            clic(page, "Siguiente")
        n, c = estado(page)
        imgs_ok = page.evaluate("""async () => {
            const urls = ['ana','luis','maria','jorge','sofia','carlos','valeria','fernando'];
            const r = await Promise.all(urls.map(u => fetch('/fotos/' + u + '.svg').then(x => x.ok)));
            return r.every(Boolean);
        }""")
        registrar("P08", "Ampliación de datos",
                  "Recorre 8 testimonios distintos y regresa a 1 de 8",
                  f"{len(set(nombres))} nombres distintos; tras 8 clics: {c}; fotos locales disponibles: {imgs_ok}",
                  len(set(nombres)) == 8 and c == "Testimonio 1 de 8" and imgs_ok)

        # ---- Presentación: tres anchos, texto largo, teclado ----
        detalles, ok9 = [], True
        for ancho in (320, 768, 1280):
            page.set_viewport_size({"width": ancho, "height": 800})
            page.goto(URL)
            page.wait_for_selector(".testimonial-card")
            foto_ok = page.evaluate("document.querySelector('.testimonial-photo').naturalWidth > 0")
            page.screenshot(path=str(capturas / f"ancho-{ancho}.png"), full_page=True)
            # Valeria (índice 6) tiene el texto largo
            for _ in range(6):
                clic(page, "Siguiente")
            sw, cw = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            page.screenshot(path=str(capturas / f"texto-largo-{ancho}.png"), full_page=True)
            sin_scroll = sw <= cw
            ok9 = ok9 and sin_scroll and foto_ok
            detalles.append(f"{ancho}px: scrollWidth {sw} / clientWidth {cw}, foto={'sí' if foto_ok else 'no'}")

        page.set_viewport_size({"width": 768, "height": 800})
        page.goto(URL)
        page.wait_for_selector(".testimonial-card")
        orden = []
        for _ in range(3):
            page.keyboard.press("Tab")
            orden.append(page.evaluate("document.activeElement.textContent"))
        outline = page.evaluate("getComputedStyle(document.activeElement).outlineStyle + ' ' + getComputedStyle(document.activeElement).outlineWidth")
        page.screenshot(path=str(capturas / "foco-teclado.png"))
        page.keyboard.press("Shift+Tab")  # Siguiente
        page.keyboard.press("Enter")
        tras_enter = estado(page)[1]
        page.keyboard.press("Space")
        tras_espacio = estado(page)[1]
        ok_tecl = (orden == ["Anterior", "Siguiente", "Aleatorio"] and outline.startswith("solid")
                   and tras_enter == "Testimonio 2 de 8" and tras_espacio == "Testimonio 3 de 8")
        detalles.append(f"Tab: {' → '.join(orden)}; foco {outline}; Enter → {tras_enter}; Espacio → {tras_espacio}")
        registrar("P09", "Presentación",
                  "Sin desplazamiento horizontal en 320/768/1280, texto largo ajustado, teclado y foco visibles",
                  " | ".join(detalles), ok9 and ok_tecl)

        nav.close()
finally:
    data_path.write_text(data_original, encoding="utf-8")
    servidor.terminate()
    servidor.wait()

# ---- Compilación ----
build = subprocess.run(["npm", "run", "build"], cwd=proyecto, capture_output=True, text=True)
linea = next((l for l in build.stdout.splitlines() if "built in" in l), build.stdout[-200:])
registrar("P10", "Compilación y consola",
          "npm run build sin errores y sin errores de aplicación en consola",
          f"build código {build.returncode} ({linea.strip()}); errores en consola durante P01-P09: {len(errores_consola)}",
          build.returncode == 0 and not errores_consola)

salida.write_text(json.dumps({"resultados": resultados, "errores_consola": errores_consola},
                             ensure_ascii=False, indent=2), encoding="utf-8")

"""Reproduce el fallo: editar data.js con la app abierta en un índice mayor al nuevo total.

Uso: python3 reproducir_hmr.py <ruta_proyecto> <captura.png>
"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

proyecto = Path(sys.argv[1]).resolve()
captura = Path(sys.argv[2]).resolve()
data_path = proyecto / "src" / "data.js"
original = data_path.read_text(encoding="utf-8")
UNO = """const testimonios = [
  { id: 1, nombre: 'Ana Pérez', cargo: 'CEO - EmpresaX',
    texto: 'Este servicio cambió la forma en que trabajamos. ¡Altamente recomendado!',
    foto: '/fotos/ana.svg' }
];
export default testimonios;
"""
errores = []
srv = subprocess.Popen(["npx", "vite", "--port", "5174", "--strictPort"], cwd=proyecto,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(3)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 768, "height": 700})
        page.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errores.append(str(e)))
        page.goto("http://localhost:5174/")
        page.wait_for_selector(".counter")
        page.get_by_role("button", name="Anterior").click()  # índice 7 (Fernando)
        print("Antes de editar:", page.locator(".counter").inner_text())
        data_path.write_text(UNO, encoding="utf-8")  # se edita sin recargar
        time.sleep(2)
        tarjeta = page.locator(".testimonial-card h2")
        print("Tarjeta tras editar:", tarjeta.inner_text() if tarjeta.count() else "(no se muestra)")
        contador = page.locator(".counter")
        print("Contador tras editar:", contador.inner_text() if contador.count() else "(no se muestra)")
        page.screenshot(path=str(captura))
        b.close()
finally:
    data_path.write_text(original, encoding="utf-8")
    srv.terminate()
    srv.wait()
print("Errores:", errores[:3])

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ------------------------------
# Configuración del driver
# ------------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# ------------------------------
# Funciones para Productos
# ------------------------------
BASE_URL = "http://localhost:8000/vistas/productos/"

def listar_productos():
    driver.get(BASE_URL + "index.php")
    time.sleep(1)
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    productos = []
    for r in rows:
        columnas = r.find_elements(By.TAG_NAME, "td")
        if len(columnas) >= 5:  # id, nombre, precio, inventario, proveedor
            productos.append({
                "id": columnas[0].text,
                "nombre": columnas[1].text,
                "precio": columnas[2].text,
                "inventario": columnas[3].text,
                "proveedor": columnas[4].text
            })
    return productos

def crear_producto(nombre, precio, inventario, id_proveedor=1):
    driver.get(BASE_URL + "add.php")
    wait.until(EC.presence_of_element_located((By.ID, "nombre"))).send_keys(nombre)
    driver.find_element(By.ID, "precio_prod").send_keys(precio)
    driver.find_element(By.ID, "inventario_prod").send_keys(inventario)

    # Seleccionar proveedor (id_prove del select)
    select = driver.find_element(By.ID, "id_prove")
    opciones = select.find_elements(By.TAG_NAME, "option")
    if len(opciones) > 1:
        opciones[1].click()  # tomar el primero válido
    driver.find_element(By.XPATH, "//button[text()='Guardar']").click()
    time.sleep(2)

def editar_producto(id_prod, nuevo_nombre, nuevo_precio, nuevo_inventario):
    driver.get(BASE_URL + f"editar.php?id={id_prod}")
    wait.until(EC.presence_of_element_located((By.NAME, "nombre"))).clear()
    driver.find_element(By.NAME, "nombre").send_keys(nuevo_nombre)

    precio_input = driver.find_element(By.NAME, "precio")
    precio_input.clear()
    precio_input.send_keys(nuevo_precio)

    inventario_input = driver.find_element(By.NAME, "cantidad")
    inventario_input.clear()
    inventario_input.send_keys(nuevo_inventario)

    # seleccionar primer proveedor válido
    select = driver.find_element(By.NAME, "id_prov")
    opciones = select.find_elements(By.TAG_NAME, "option")
    if len(opciones) > 1:
        opciones[1].click()

    driver.find_element(By.NAME, "guardar").click()
    time.sleep(2)

def eliminar_producto(id_prod):
    driver.get(BASE_URL + f"eliminar.php?id={id_prod}")
    time.sleep(2)

# ------------------------------
# Ejecución de pruebas
# ------------------------------

# Crear producto
crear_producto("Producto Test", "150", "5")
print("Lista después de crear:", listar_productos())

# Editar producto (usando el primer ID de la lista)
primer_producto = listar_productos()[0]["id"]
editar_producto(primer_producto, "Producto Editado", "200", "10")
print("Lista después de editar:", listar_productos())

# Eliminar producto (el último id de la lista)
ultimo_producto = listar_productos()[-1]["id"]
eliminar_producto(6)
print("Lista después de eliminar:", listar_productos())

# ------------------------------
# Cierre
# ------------------------------
driver.quit()

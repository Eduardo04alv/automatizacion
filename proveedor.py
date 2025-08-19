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
# Funciones para Proveedores
# ------------------------------
BASE_URL = "http://localhost:8000/vistas/proveedor/"

def listar_proveedores():
    driver.get(BASE_URL + "index.php")
    time.sleep(1)
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    proveedores = []
    for r in rows:
        columnas = r.find_elements(By.TAG_NAME, "td")
        if len(columnas) >= 4:
            proveedores.append({
                "id": columnas[0].text,
                "nombre": columnas[1].text,
                "apellido": columnas[2].text,
                "telefono": columnas[3].text
            })
    return proveedores

def crear_proveedor(nombre, apellido, telefono):
    driver.get(BASE_URL + "add.php")
    wait.until(EC.presence_of_element_located((By.ID, "nombre"))).send_keys(nombre)
    driver.find_element(By.ID, "apellido").send_keys(apellido)
    driver.find_element(By.ID, "telefono").send_keys(telefono)
    driver.find_element(By.XPATH, "//button[text()='Guardar']").click()
    time.sleep(2)  # espera la redirección y alerta

def editar_proveedor(id_prov, nuevo_nombre, nuevo_apellido, nuevo_telefono):
    driver.get(BASE_URL + f"editar.php?id={id_prov}")
    wait.until(EC.presence_of_element_located((By.NAME, "nombre"))).clear()
    driver.find_element(By.NAME, "nombre").send_keys(nuevo_nombre)
    driver.find_element(By.NAME, "apellido").clear()
    driver.find_element(By.NAME, "apellido").send_keys(nuevo_apellido)
    driver.find_element(By.NAME, "telefono").clear()
    driver.find_element(By.NAME, "telefono").send_keys(nuevo_telefono)
    driver.find_element(By.NAME, "guardar").click()
    time.sleep(2)

def eliminar_proveedor(id_prov):
    driver.get(BASE_URL + f"eliminar.php?id={id_prov}")
    time.sleep(2)  # espera la alerta de confirmación y redirección

# ------------------------------
# Ejecución de pruebas
# ------------------------------

# Crear proveedor
crear_proveedor("Juan", "Pérez", "8091234567")
print("Lista después de crear:", listar_proveedores())

# Editar proveedor (usando el primer ID de la lista)
primer_proveedor = listar_proveedores()[0]["id"]
editar_proveedor(primer_proveedor, "Juan Editado", "Pérez Editado", "8097654321")
print("Lista después de editar:", listar_proveedores())

# Eliminar proveedor
eliminar_proveedor(11)
print("Lista después de eliminar:", listar_proveedores())

# ------------------------------
# Cierre
# ------------------------------
driver.quit()

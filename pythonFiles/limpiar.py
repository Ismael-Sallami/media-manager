import os
import sys
import hashlib

# ============================
# FUNCIONES
# ============================

def calcular_hash(path, algoritmo='md5'):
    """Calcula el hash MD5 del archivo"""
    hash_func = hashlib.new(algoritmo)
    try:
        with open(path, 'rb') as f:
            for bloque in iter(lambda: f.read(4096), b''):
                hash_func.update(bloque)
        return hash_func.hexdigest()
    except:
        return None

def obtener_hashes(ruta):
    """Devuelve un diccionario {hash: [ruta1, ruta2, ...]}"""
    hashes = {}
    for dirpath, _, filenames in os.walk(ruta):
        for f in filenames:
            path = os.path.join(dirpath, f)
            if not os.path.isfile(path):
                continue
            h = calcular_hash(path)
            if h:
                hashes.setdefault(h, []).append(path)
    return hashes

def formato_bytes(bytes):
    mb = bytes / (1024 ** 2)
    gb = bytes / (1024 ** 3)
    if bytes < 1024:  # Si el tamaño es menor a 1 KB
        return f"{bytes} bytes"
    elif mb < 0.01:  # Si el tamaño es menor a 0.01 MB
        return f"{bytes} bytes / {mb:.4f} MB / {gb:.4f} GB"
    else:
        return f"{bytes} bytes / {mb:.2f} MB / {gb:.2f} GB"

# ============================
# PARÁMETROS
# ============================

if len(sys.argv) < 3:
    print("Uso: python limpiar.py <ruta_origen> <ruta_destino>")
    exit(1)

ruta_origen = sys.argv[1]
ruta_destino = sys.argv[2]

# ============================
# HASH DE DESTINO (referencia)
# ============================

# Preguntar al usuario si desea comparar por hashes o solo por nombre y tamaño
respuesta_comparar_hash = input("¿Deseas comparar usando hashes? (s/n): ").strip().lower()

if respuesta_comparar_hash == 's':
    print("🔍 Calculando hashes de destino...")
    hashes_destino = obtener_hashes(ruta_destino)
    hashes_set_destino = set(hashes_destino.keys())
    comparar_por_hash = True
else:
    print("🔍 Obteniendo nombres y tamaños de destino...")
    archivos_destino = set()
    for dirpath, _, filenames in os.walk(ruta_destino):
        for f in filenames:
            path = os.path.join(dirpath, f)
            if not os.path.isfile(path):
                continue
            tam = os.path.getsize(path)
            archivos_destino.add((f, tam))
    comparar_por_hash = False

# ============================
# ARCHIVOS CANDIDATOS A BORRAR
# ============================

# ============================
# ARCHIVOS CANDIDATOS A BORRAR
# ============================

archivos_a_borrar = []

print("🧹 Buscando archivos duplicados en origen...")

for dirpath, _, filenames in os.walk(ruta_origen):
    for f in filenames:
        path = os.path.join(dirpath, f)
        if not os.path.isfile(path):
            continue
        if comparar_por_hash:
            h = calcular_hash(path)
            if h and h in hashes_set_destino:
                archivos_a_borrar.append((path, os.path.getsize(path)))
        else:
            tam = os.path.getsize(path)
            if (f, tam) in archivos_destino:
                archivos_a_borrar.append((path, tam))

def filtrar_archivos_por_criterio(archivos, criterio):
    """Filtra los archivos según el criterio especificado."""
    total_tamano = sum(tam for _, tam in archivos)
    
    # Convertir el criterio a minúsculas para evitar problemas con mayúsculas/minúsculas
    criterio = criterio.lower()
    
    if criterio == "all":
        return archivos
    elif criterio.endswith("mb"):
        limite = float(criterio[:-2]) * 1024 ** 2  # Convertir a bytes (elimina 'mb')
    elif criterio.endswith("gb"):
        limite = float(criterio[:-2]) * 1024 ** 3  # Convertir a bytes (elimina 'gb')
    elif criterio.endswith("%"):
        porcentaje = float(criterio[:-1]) / 100  # Elimina '%' y calcula porcentaje
        limite = total_tamano * porcentaje
    else:
        raise ValueError("Criterio inválido. Usa 'ALL', '5MB', '5GB' o '50%'.")
    
    # Si el límite especificado supera el tamaño total, se procede a borrar todo
    if limite >= total_tamano:
        print(f"⚠️ El criterio especificado ({criterio}) supera el tamaño total de los archivos ({formato_bytes(total_tamano)}). Procediendo a borrar todo.")
        return archivos
    
    archivos_filtrados = []
    acumulado = 0
    for path, tam in sorted(archivos, key=lambda x: x[1], reverse=True):  # Ordenar por tamaño
        if acumulado + tam > limite:
            break
        acumulado += tam
        archivos_filtrados.append((path, tam))
    
    return archivos_filtrados

# ============================
# CONFIRMAR Y BORRAR
# ============================

total_a_liberar = sum(tam for _, tam in archivos_a_borrar)
print(f"\n📋 Se pueden eliminar {len(archivos_a_borrar)} archivos duplicados.")
print(f"💾 Espacio que se puede liberar: {formato_bytes(total_a_liberar)}")

criterio = input("¿Cuánto espacio deseas liberar? (ALL, 5MB, 5GB, 50%): ").strip().lower()
try:
    archivos_a_borrar = filtrar_archivos_por_criterio(archivos_a_borrar, criterio)
except ValueError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

if not archivos_a_borrar:
    print("❌ No hay suficientes archivos para cumplir con el criterio especificado.")
    sys.exit(0)

respuesta = input(f"¿Deseas continuar y borrar estos {len(archivos_a_borrar)} archivos? (s/n): ").strip().lower()
if respuesta != 's':
    print("❌ Operación cancelada por el usuario.")
    sys.exit(0)

liberado = 0
borrados = []

for path, tam in archivos_a_borrar:
    try:
        os.remove(path)
        liberado += tam
        borrados.append(path)
        print(f"🗑️ Borrado: {path} ({tam / 1024 ** 2:.2f} MB)")
    except Exception as e:
        print(f"❌ No se pudo borrar {path}: {e}")

# ============================
# RESUMEN FINAL
# ============================

print(f"\n✅ Espacio liberado: {formato_bytes(liberado)}")
print(f"📦 Total archivos borrados: {len(borrados)}")
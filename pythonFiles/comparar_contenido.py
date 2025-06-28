import os
import sys
import hashlib

# ========================
# FUNCIONES AUXILIARES
# ========================

# Calcula el hash (MD5 por defecto) de un archivo
def calcular_hash(archivo, algoritmo='md5'):
    hash_func = hashlib.new(algoritmo)
    with open(archivo, 'rb') as f:
        for bloque in iter(lambda: f.read(4096), b''):
            hash_func.update(bloque)
    return hash_func.hexdigest()

# Devuelve un diccionario {nombre_archivo: tamaño_en_bytes}
def obtener_info_archivos(ruta):
    info = {}
    for dirpath, _, archivos_en_dir in os.walk(ruta):
        for f in archivos_en_dir:
            ruta_abs = os.path.join(dirpath, f)
            try:
                tam = os.path.getsize(ruta_abs)
                info[f] = tam  # último tamaño encontrado para ese nombre
            except OSError:
                continue
    return info

# Devuelve un diccionario {nombre_archivo: hash_md5}
def obtener_hashes_por_nombre(ruta):
    hashes = {}
    for dirpath, _, archivos_en_dir in os.walk(ruta):
        for nombre in archivos_en_dir:
            ruta_abs = os.path.join(dirpath, nombre)
            try:
                hash_valor = calcular_hash(ruta_abs)
                hashes[nombre] = hash_valor
            except OSError:
                continue
    return hashes

# ========================
# LECTURA DE PARÁMETROS
# ========================

if len(sys.argv) != 3:
    print("Uso: python comparar_contenido.py <ruta_1> <ruta_2>")
    sys.exit(1)

ruta_1 = sys.argv[1]
ruta_2 = sys.argv[2]

# ========================
# COMPARACIÓN DE NOMBRES Y TAMAÑOS
# ========================

archivos_1 = obtener_info_archivos(ruta_1)
archivos_2 = obtener_info_archivos(ruta_2)

nombres_1 = set(archivos_1.keys())
nombres_2 = set(archivos_2.keys())

if nombres_1 == nombres_2:
    print("✅ COINCIDEN LOS NOMBRES DE ARCHIVOS")
else:
    print("❌ NO COINCIDEN LOS NOMBRES DE ARCHIVOS")
    diferencia_1 = nombres_1 - nombres_2
    diferencia_2 = nombres_2 - nombres_1
    if diferencia_1:
        print(f"🟥 Archivos en {ruta_1} pero no en {ruta_2}:")
        for e in sorted(diferencia_1):
            print(f"  - {e}")
    if diferencia_2:
        print(f"🟦 Archivos en {ruta_2} pero no en {ruta_1}:")
        for e in sorted(diferencia_2):
            print(f"  - {e}")

# Comparar tamaños si los nombres coinciden
if nombres_1 & nombres_2:
    print("\n📏 Comparando tamaños de archivos coincidentes...")
    for nombre in sorted(nombres_1 & nombres_2):
        t1 = archivos_1[nombre]
        t2 = archivos_2[nombre]
        if t1 != t2:
            print(f"⚠️  Diferencia de tamaño en {nombre}: {t1} bytes en origen vs {t2} bytes en destino")

# ========================
# DETECCIÓN DE ARCHIVOS DUPLICADOS AL 100%
# ========================

respuesta = input("\n¿Desea verificar duplicados reales por contenido (uso de hash, tarda bastante tiempo si son bastantes archivos) ? (s/n): ").strip().lower()
duplicados_reales = []
if respuesta == 's':
    print("\n🔍 Verificando duplicados reales por contenido (hash)...")
    hashes_1 = obtener_hashes_por_nombre(ruta_1)
    hashes_2 = obtener_hashes_por_nombre(ruta_2)
    for nombre in hashes_1:
        if nombre in hashes_2 and hashes_1[nombre] == hashes_2[nombre]:
            duplicados_reales.append(nombre)
else:
    print("\n⏩ Saltando verificación de duplicados por contenido.")

print(f"\n🔁 Archivos duplicados exactos (nombre y contenido): {len(duplicados_reales)}")
for nombre in sorted(duplicados_reales):
    print(f"  ✅ {nombre}")

# ========================
# TOTALES E INFORMACIÓN FINAL
# ========================

print("\n📂 Resumen final:")
print(f"  Total en {ruta_1}: {len(archivos_1)} archivos")
print(f"  Total en {ruta_2}: {len(archivos_2)} archivos")
print(f"  Coincidencias por nombre: {len(nombres_1 & nombres_2)}")
print(f"  Coincidencias exactas (duplicados): {len(duplicados_reales)}")

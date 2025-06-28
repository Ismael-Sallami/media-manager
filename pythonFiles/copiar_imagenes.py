#!/usr/bin/env python3

import os
import shutil
import hashlib
from pathlib import Path
import sys

# ===============================
# CONFIGURACIÓN Y PARÁMETROS
# ===============================

if len(sys.argv) != 3:
    print(f"Uso: {sys.argv[0]} <ruta_origen> <ruta_destino>")
    sys.exit(1)

ruta_origen = sys.argv[1]
ruta_destino = sys.argv[2]

extensiones = {'.jpg', '.jpeg', '.png', '.gif', '.heic', '.mov', '.mp4', '.webp', '.aae', '.avif'}

Path(ruta_destino).mkdir(parents=True, exist_ok=True)

contador_copiados = 0
contador_duplicados = 0
errores = []
total = 0

mantener_estructura = input("¿Desea mantener la estructura de subdirectorios? (s/n): ").strip().lower()
if mantener_estructura not in ['s', 'n']:
    print("❌ Respuesta inválida. Abortando.")
    sys.exit(1)
mantener_estructura = (mantener_estructura == 's')

# ===============================
# FUNCIONES
# ===============================

def calcular_hash(path, algoritmo='md5'):
    """Calcula el hash MD5 de un archivo"""
    hash_func = hashlib.new(algoritmo)
    try:
        with open(path, 'rb') as f:
            for bloque in iter(lambda: f.read(4096), b''):
                hash_func.update(bloque)
        return hash_func.hexdigest()
    except Exception:
        return None

def mostrar_barra_progreso(actual, total, longitud=30):
    """Muestra una barra de progreso ASCII"""
    porcentaje = actual / total
    completado = int(longitud * porcentaje)
    barra = '█' * completado + '-' * (longitud - completado)
    return f"[{barra}]"

# ===============================
# RECOPILACIÓN DE ARCHIVOS A COPIAR
# ===============================

archivos_a_copiar = []

# for raiz, _, archivos in os.walk(ruta_origen):
#     for archivo in archivos:
#         ext = os.path.splitext(archivo)[1].lower()
#         if ext in extensiones:
#             origen = os.path.join(raiz, archivo)
#             relativo = os.path.relpath(origen, ruta_origen)
#             destino = os.path.join(ruta_destino, relativo)

#             if not os.path.exists(destino):
#                 archivos_a_copiar.append((origen, destino, archivo))
#             else:
#                 hash_origen = calcular_hash(origen)
#                 hash_destino = calcular_hash(destino)

#                 if hash_origen == hash_destino:
#                     print(f"YA COPIADO (idéntico): {archivo}")
#                     contador_duplicados += 1
#                 else:
#                     print(f"⚠️ Mismo nombre pero distinto contenido: {archivo}")
#                     # Renombrar archivo destino para evitar sobrescritura
#                     base, ext = os.path.splitext(destino)
#                     nuevo_destino = base + "_copy" + ext
#                     archivos_a_copiar.append((origen, nuevo_destino, archivo + " (renombrado)"))

# total = len(archivos_a_copiar)

for raiz, _, archivos in os.walk(ruta_origen):
    for archivo in archivos:
        ext = os.path.splitext(archivo)[1].lower()
        if ext in extensiones:
            origen = os.path.join(raiz, archivo)
            if mantener_estructura:
                relativo = os.path.relpath(origen, ruta_origen)
                destino = os.path.join(ruta_destino, relativo)
            else:
                destino = os.path.join(ruta_destino, archivo)

            if not os.path.exists(destino):
                archivos_a_copiar.append((origen, destino, archivo))
            else:
                hash_origen = calcular_hash(origen)
                hash_destino = calcular_hash(destino)

                if hash_origen == hash_destino:
                    print(f"YA COPIADO (idéntico): {archivo}")
                    contador_duplicados += 1
                else:
                    print(f"⚠️ Mismo nombre pero distinto contenido: {archivo}")
                    # Renombrar archivo destino para evitar sobrescritura
                    base, ext = os.path.splitext(destino)
                    nuevo_destino = base + "_copy" + ext
                    archivos_a_copiar.append((origen, nuevo_destino, archivo + " (renombrado)"))
                    
# Total de archivos a copiar
total = len(archivos_a_copiar)

# ===============================
# COPIA DE ARCHIVOS
# ===============================

for i, (origen, destino, nombre_mostrar) in enumerate(archivos_a_copiar, 1):
    try:
        Path(os.path.dirname(destino)).mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)
        contador_copiados += 1
        barra = mostrar_barra_progreso(i, total)
        print(f"{barra} Copiado: {nombre_mostrar} ({contador_copiados}/{total})")
    except Exception as e:
        errores.append((origen, str(e)))
        print(f"Error al copiar {nombre_mostrar}: {e}")

# ===============================
# RESUMEN FINAL
# ===============================

print("\n📋 RESUMEN FINAL")
print(f"✅ {contador_copiados} archivos copiados.")
print(f"🔁 {contador_duplicados} archivos ya estaban copiados (idénticos).")
if errores:
    print(f"❌ {len(errores)} errores encontrados:")
    for origen, err in errores:
        print(f"- {origen}: {err}")

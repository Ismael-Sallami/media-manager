#!/bin/sh

# ========== FUNCIONES ==========

leer_parametro() {
  sed -e '/^\s*#/d' -e '/^\s*$/d' parametros.txt | sed -n "${1}p"
}

mostrar_separador() {
  echo
  echo "==========================="
  echo "$1"
  echo "==========================="
  echo
}

mostrar_uso() {
  echo "Uso: ./GESTIONAR_IMAGENES [--limpiar] [--zip] [--comparar] [--encriptar]"
  echo "Si no se especifican argumentos, se ejecuta todo el flujo completo interactivo."
}

crear_zip() {
  archivo_zip="backup_$(date +%Y%m%d_%H%M%S).zip"
  zip -r "$archivo_zip" "$param2" >/dev/null
  echo "📦 ZIP creado: $archivo_zip"
}

encriptar_zip() {
  archivo="$1"
  echo "🔐 Introduce contraseña para encriptar el ZIP:"
  read -r -s pass1
  echo
  echo "🔐 Repite la contraseña:"
  read -r -s pass2
  echo

  if [ "$pass1" != "$pass2" ]; then
    echo "❌ Las contraseñas no coinciden. Abortando."
    exit 5
  fi

  zip -P "$pass1" "${archivo%.zip}_enc.zip" "$archivo" >/dev/null
  echo "🔒 ZIP encriptado creado: ${archivo%.zip}_enc.zip"
  rm -f "$archivo"
}

# ========== LECTURA DE PARÁMETROS ==========
param1=$(leer_parametro 1)
param2=$(leer_parametro 2)

if [ -z "$param1" ] || [ -z "$param2" ]; then
  echo "Error: No se pudieron leer ambos parámetros de parametros.txt"
  exit 1
fi

# ========== FLAGS ==========
hacer_copia=true
hacer_comparacion=true
hacer_limpieza=false
hacer_zip=false
hacer_encriptado=false
solo_comparar=false
solo_zip=false
solo_limpiar=false
solo_copiar=false
solo_encriptar=false

for arg in "$@"; do
  case "$arg" in
    --limpiar) hacer_limpieza=true ;;
    --zip) hacer_zip=true ;;
    --encriptar) hacer_encriptado=true ;;
    --comparar)
      hacer_copia=false
      hacer_comparacion=true
      solo_comparar=true
      ;;
    --only-zip)
      solo_zip=true
      hacer_zip=true
      hacer_copia=false
      hacer_comparacion=false
      hacer_limpieza=false
      hacer_encriptado=false
      ;;
    --only-limpiar)
      solo_limpiar=true
      hacer_limpieza=true
      hacer_copia=false
      hacer_comparacion=false
      hacer_zip=false
      hacer_encriptado=false
      ;;
    --only-copiar)
      solo_copiar=true
      hacer_copia=true
      hacer_comparacion=false
      hacer_limpieza=false
      hacer_zip=false
      hacer_encriptado=false
      ;;
    --only-encriptar)
      solo_encriptar=true
      hacer_encriptado=true
      hacer_copia=false
      hacer_comparacion=false
      hacer_limpieza=false
      hacer_zip=false
      ;;
    --help|-h)
      mostrar_uso
      exit 0
      ;;
    *)
      echo "❌ Opción no reconocida: $arg"
      mostrar_uso
      exit 1
      ;;
  esac
done

# ========== EJECUCIÓN ==========
echo
echo "📁 Origen: $param1"
echo "📂 Destino: $param2"
echo

if [ "$hacer_copia" = true ]; then
  mostrar_separador "COPIANDO IMAGENES"
  if ! python3 pythonFiles/copiar_imagenes.py "$param1" "$param2"; then
    echo "❌ Error al copiar imágenes. Abortando."
    exit 2
  fi
  mostrar_separador "IMAGENES COPIADAS"
fi

if [ "$hacer_comparacion" = true ]; then
  echo "🔍 Comparando contenido..."
  if ! python3 pythonFiles/comparar_contenido.py "$param1" "$param2"; then
    echo "❌ Error durante la comparación. Abortando."
    exit 3
  fi
  mostrar_separador "COMPARACIÓN FINALIZADA"
fi

if [ "$solo_comparar" = true ]; then
  exit 0
fi

if [ "$hacer_limpieza" = true ]; then
  mostrar_separador "LIMPIEZA DE ARCHIVOS ORIGINALES"
  if ! python3 pythonFiles/limpiar.py "$param1" "$param2"; then
    echo "❌ Error durante la limpieza. Abortando."
    exit 4
  fi
fi

if [ "$hacer_zip" = true ]; then
  mostrar_separador "CREANDO ARCHIVO ZIP"
  crear_zip
fi

if [ "$hacer_encriptado" = true ]; then
  if [ "$hacer_zip" = false ]; then
    echo "❌ No se puede encriptar si no se ha generado un ZIP. Usa --zip junto con --encriptar."
    exit 6
  fi
  mostrar_separador "ENCRIPTANDO ARCHIVO ZIP"
  encriptar_zip "$archivo_zip"
fi

echo
echo "🎉 Todo el proceso ha finalizado correctamente."
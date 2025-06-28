
<p align="center">
    <img src="readmeFiles/icons-1151_256.gif" alt="Imagen 1" width="150" style="display:inline-block; margin-right:20px;"/>
    <img src="readmeFiles/envio.gif" alt="Imagen 2" width="150" style="display:inline-block;"/>
</p>

# ¿Qué hacer cuando se llena la memoria del iPhone (o Android)?

Cuando la memoria del teléfono se llena, se nos presentan varias opciones: pagar por almacenamiento en la nube (como iCloud en Apple), borrar archivos a mano, o buscar soluciones prácticas cuando ya no queda espacio.
Muchos, como yo, dejamos que la situación llegue al límite, y nos encontramos con que tanto el móvil como iCloud están saturados.

Por eso creé esta herramienta: **un script que transfiere automáticamente tus imágenes al PC**, las **comprime** e incluso **encripta**, todo ello de forma sencilla y segura. Así ahorras espacio y dinero sin complicaciones.

---

# ¿Cómo funciona?

### 1. Clona el repositorio:

```bash
git clone https://github.com/Ismael-Sallami/media-manager.git
```

### 2. Estructura del proyecto

* **`GESTIONAR_IMAGENES.sh`**: Script principal. Se encarga de copiar, comparar, comprimir y encriptar imágenes entre tu teléfono y tu ordenador, según las opciones elegidas.
* **`parametros.txt`**: Archivo de configuración con dos líneas:

  * Línea 1: ruta de origen (donde están las imágenes).
  * Línea 2: ruta de destino (donde se guardarán).
* **`pythonFiles/`**: Scripts auxiliares en Python para compresión, encriptado y tareas adicionales.
* **`readmeFiles/`**: Contiene recursos visuales como imágenes y gifs usados en este README.
* **`LICENSE`**: Licencia MIT del proyecto.

### 3. Configura tus rutas

Edita `parametros.txt` y coloca:

```
/ruta/de/origen
/ruta/de/destino
```

> 💡 Si estás en Linux y no sabes la ruta exacta, entra en el directorio y usa `pwd`.

---

# ⚙️ Modos de uso

Ejecuta el script según lo que necesites:

```bash
./GESTIONAR_IMAGENES           # Modo interactivo (pregunta paso a paso)
./GESTIONAR_IMAGENES --limpiar # Elimina imágenes del origen sin preguntar
./GESTIONAR_IMAGENES --comparar # Solo compara origen y destino
./GESTIONAR_IMAGENES --zip     # Copia, compara y comprime en ZIP
./GESTIONAR_IMAGENES --zip --encriptar  # Igual que el anterior, pero también encripta
./GESTIONAR_IMAGENES --limpiar --zip --encriptar # Todo el proceso sin preguntas
```

---

## ⚙️ Opciones avanzadas (`only`)

Permiten realizar una única acción concreta:

* `--only-zip`: Solo comprime.
* `--only-limpiar`: Solo elimina.
* `--only-comparar`: Solo compara archivos.
* `--only-copiar`: Solo copia.
* `--only-encriptar`: Solo encripta un ZIP existente.

Estas opciones ofrecen flexibilidad para flujos personalizados.

---

# 🧹 Opciones de eliminación

Puedes especificar cómo y cuánto eliminar:

* `ALL`: elimina **todos** los archivos duplicados.
* `n%`: elimina un **porcentaje** (entre 0 y 100) del total duplicado.
* `5GB`: elimina hasta liberar 5 gigabytes.
* `5MB`: elimina hasta liberar 5 megabytes.

> 📌 La eliminación **solo afecta a imágenes duplicadas** (presentes en origen y destino), para no perder datos importantes.

> 📌 Por rendimiento, la comparación puede hacerse por nombre/tamaño o por hash. El uso de hash es más seguro pero más lento si hay muchos archivos (>7000).

---

## ¿Por qué eliminar menos con ciertos criterios?

### Comportamiento de los filtros:

* **ALL**: elimina todos los duplicados sin restricción.
* **Tamaño o porcentaje (`5GB`, `50%`, etc.)**: elimina **solo lo necesario** hasta alcanzar el límite indicado.

### Ejemplo:

* Duplicados totales: `5.79 GB` (\~5955 archivos)
* `ALL`: elimina los 5.79 GB completos.
* `5GB`: elimina archivos hasta alcanzar 5GB.
* `50%`: elimina hasta alcanzar el 50% del total (\~2.89GB).

> No hay problema en usar `ALL` si previamente copiaste todo correctamente. Se recomienda verificar el borrado y hacer una nueva comparación como precaución.

---

# 🖥️ Compatibilidad con Windows

Aunque está pensado para Linux, también puedes usar esta herramienta en Windows mediante:

### 1. Instala un entorno de terminal:

* [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/windows/wsl/) ✅ Recomendado
* [Git Bash](https://gitforwindows.org/)
* [Cygwin](https://www.cygwin.com/)

### 2. Instala Python (si se requiere)

* Descárgalo desde [python.org](https://www.python.org/downloads/windows/)

### 3. Ejecuta el script:

```bash
./GESTIONAR_IMAGENES --zip --encriptar
```

o si es Python:

```bash
python GESTIONAR_IMAGENES.py --zip --encriptar
```

### 4. Rutas en Windows:

* En WSL: `C:\Users\TuUsuario\Imágenes` es `/mnt/c/Users/TuUsuario/Imágenes`
* En Git Bash: `/c/Users/TuUsuario/Imágenes`

> ⚠️ WSL permite usar herramientas Linux nativamente y es la opción más robusta.

---

# Cómo conectar tu iPhone en Arch Linux

Si al conectar tu iPhone ves el error `ERROR: No device found!`, sigue estos pasos:

### 1. Instala los paquetes necesarios:

```bash
sudo pacman -S ifuse usbmuxd libimobiledevice gvfs-afc
sudo pacman -S libplist libusbmuxd  # Opcionales
```

### 2. Activa el servicio:

```bash
sudo systemctl start usbmuxd
sudo systemctl enable usbmuxd
```

### 3. Desbloquea y confía en el ordenador

* Desbloquea tu iPhone.
* Conéctalo **directamente** (sin hub).
* Acepta el mensaje de **"Confiar en este ordenador"**.

### 4. Verifica la conexión USB:

```bash
lsusb
```

Debe aparecer algo como:

```
Bus 001 Device 008: ID 05ac:12a8 Apple, Inc. iPhone
```

### 5. Empareja el dispositivo:

```bash
idevicepair pair
```

Si falla:

```bash
idevicepair unpair
idevicepair pair
```

### 6. Revisa que está conectado:

```bash
ideviceinfo
```

### 7. Monta el dispositivo:

```bash
mkdir ~/iphone
ifuse ~/iphone
ls ~/iphone/DCIM
```

---

## ¿Sigue sin funcionar?

Ejecuta estos comandos y revisa la salida:

* `lsusb`
* `idevicepair pair`
* `sudo journalctl -f` (luego conecta el iPhone)

> 📌 Se recomienda ejecutar una comparación adicional para asegurar que todo ha sido copiado correctamente.
> Si faltan archivos, puedes usar `cp <origen> <destino>` o buscar con `find <ruta> -name "archivo"`.

---

# 🙋‍♂️ Autor

**Ismael Sallami Moreno**

# 🪪 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---


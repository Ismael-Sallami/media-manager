<p align="center">
  <img src="readmeFiles/icons-1151_256.gif" alt="Imagen 1" width="150" style="display:inline-block; margin-right:20px;"/>
  <img src="readmeFiles/envio.gif" alt="Imagen 2" width="150" style="display:inline-block;"/>
</p>

## ¿Qué hacer cuando se llena la memoria del iPhone (o Android)?

Cuando la memoria del teléfono se llena, surgen varias alternativas: pagar por servicios en la nube, adquirir espacio en iCloud (si eres usuario de Apple), o buscar soluciones cuando ya no queda espacio. Muchos, como yo, esperamos hasta el último momento y nos encontramos con que tanto iCloud como el teléfono están al límite.

Por eso, presento una herramienta práctica que transfiere automáticamente tus imágenes al PC, guardándolas comprimidas e incluso encriptadas en un disco duro externo o pendrive. Así, puedes ahorrar dinero y espacio de forma sencilla.

---

## ¿Cómo funciona?

Primero, debemos de clonar el repositorio:
```bash
git clone https://github.com/Ismael-Sallami/media-manager.git
```

Aquí encontramos los siguientes ficheros:

- **GESTIONAR_IMAGENES.sh**: Script principal que gestiona el flujo completo de copia, comparación, compresión y encriptado de imágenes entre el teléfono y el PC, según las opciones seleccionadas.
- **parametros.txt**: Archivo de configuración donde se indican la ruta de origen (primer línea) y la ruta de destino (segunda línea) para las imágenes. Debemos de suistituir la linea de `ruta1` por el origen y `ruta2` por el destino.
- **readmeFiles/**: Carpeta que contiene imágenes y recursos gráficos utilizados en este README, como iconos y gifs ilustrativos.
- **LICENSE**: Archivo que especifica la licencia MIT bajo la que se distribuye el proyecto.
- **pythonFiles/**: Carpeta que contiene scripts auxiliares en Python utilizados por el proyecto para tareas específicas como compresión, encriptado o gestión avanzada de archivos.

La explicación técnica puede ser compleja, así que iré directo al uso. Si te interesa el detalle, puedes revisar el código fuente.

No necesitas conocimientos previos en informática, Linux, Bash o Python. Aquí te explico cómo usarlo paso a paso.

1. **Configura las rutas**  
    En el archivo `parametros.txt`, escribe en la primera línea la ruta de origen de las imágenes y en la segunda línea la ruta de destino donde quieres guardarlas.  
    Si no sabes la ruta y usas Linux, sitúate en el directorio deseado y ejecuta el comando `pwd`. Copia la ruta que aparece (por ejemplo, `/home/usuario/...`).

---

## Modos de uso

Ejecuta la herramienta con las siguientes opciones según lo que necesites:

- `./GESTIONAR_IMAGENES`  
  Ejecuta el flujo completo con preguntas interactivas.

- `./GESTIONAR_IMAGENES --limpiar`  
  Elimina imágenes del origen sin preguntas.

- `./GESTIONAR_IMAGENES --comparar`  
  Solo compara imágenes entre origen y destino, sin copiar ni comprimir.

- `./GESTIONAR_IMAGENES --zip`  
  Copia, compara y comprime las imágenes en un archivo zip.

- `./GESTIONAR_IMAGENES --zip --encriptar`  
  Copia, compara, comprime y encripta las imágenes resultantes.

- `./GESTIONAR_IMAGENES --limpiar --zip --encriptar`  
  Realiza limpieza, copia, comparación, compresión y encriptado, todo sin preguntas interactivas.

  ## Opciones avanzadas (`only`)

  Puedes ejecutar acciones específicas usando las siguientes opciones:

  - `--only-zip`: Solo crea el archivo ZIP de las imágenes, sin copiar ni limpiar.
  - `--only-limpiar`: Solo realiza la limpieza de imágenes en el origen, sin copiar ni comprimir.
  - `--only-comparar`: Solo compara imágenes entre origen y destino, sin copiar, limpiar ni comprimir.
  - `--only-copiar`: Solo copia las imágenes del origen al destino, sin comprimir ni limpiar.
  - `--only-encriptar`: Solo encripta el archivo ZIP generado previamente, sin copiar, limpiar ni comprimir.

  Estas opciones permiten ejecutar únicamente la acción indicada, facilitando flujos personalizados según tus necesidades.

Elige la opción que mejor se adapte a tus necesidades.

---

## Opciones de eliminación

Se implementaron opciones para eliminar, comprimir y encriptar porque resultan útiles. Para eliminar imágenes del origen (dejando solo la copia), puedes especificar:

- `ALL`: elimina todas las imágenes.
- `n%`: elimina un porcentaje (`n`) de imágenes (0 a 100).
- `5GB`: elimina hasta liberar 5 gigabytes.
- `5MB`: elimina hasta liberar 5 megabytes.

> **Nota:**  
> Si hay menos espacio del solicitado (por ejemplo, 2MB y pides 5MB), se eliminarán todas las imágenes. Sirve tanto para usuarios IOS como para Android. Todo esto se realiza de manera iterativa por terminal, de manera que si queremos guardar la salida podemos ejecutar el comando y seguido de este `> salida.txt`.

> **Cabe destacar que cuando se refiere a `duplicados` es a los que están en origen y destino, ya que solo podemos eliminar los que estén en ambos para no perder nada.**

> En cuanto a la eliminación, cuando comparamos de nuevo el hacerlo mediante hash tarda más tiempo (en el caso de que se tenga bastantes archivos en origen (>7000) ) que mediante tamaño y nombre.


### Aclaración sobre los criterios de eliminación

El comportamiento que describes ocurre porque el criterio `ALL` selecciona todos los archivos duplicados para ser eliminados, mientras que otros criterios como `5MB`, `5GB` o `50%` filtran los archivos según el límite especificado. Esto significa que con `ALL` no hay restricciones, pero con otros criterios se aplica un filtro basado en el tamaño total o porcentaje.

**Explicación del comportamiento:**

- **Criterio `ALL`:**
  - Selecciona todos los archivos duplicados encontrados en la lista `archivos_a_borrar`.
  - No aplica ningún filtro basado en tamaño o porcentaje.

- **Criterios como `5MB`, `5GB` o `50%`:**
  - Calculan un límite basado en el tamaño total de los archivos duplicados.
  - Solo se seleccionan los archivos que cumplen con el límite especificado.
  - Si el límite es menor que el tamaño total de los archivos duplicados, se selecciona un subconjunto de archivos.

**Ejemplo:**

- Espacio total duplicado: `6222324956` bytes (~5.79 GB).
- Criterio `ALL`: Selecciona los 5955 archivos duplicados (5.79 GB).
- Criterio `5GB`: Filtra los archivos hasta alcanzar un límite de 5GB, lo que puede resultar en menos archivos seleccionados.
- Criterio `50%`: Calcula el 50% del tamaño total (5.79 GB * 0.5 ≈ 2.89 GB) y selecciona archivos hasta alcanzar ese límite.

> No debemos de tener miedo a usar la opción `ALL`, si sabemos que previamente lo hemos copiado todo. Se aconseja revisar que se ha borrado todo correctamente en el teléfono.

---

*Lo explicado anteriormente es para usuario de Linux, así que vamos a ver para los usuario de `Windows`*.

> Si se desea abortar en algún caso debemos de presionar `ctrl+c` y saltarán errores pero es normal, no hay que preocuparse.


## Instalación y solución de errores comunes en Linux

Si al conectar tu iPhone ves el error `ERROR: No device found!`, significa que Arch Linux no lo está detectando correctamente. Aquí tienes una guía paso a paso para solucionarlo y montar tu iPhone:

---

### Pasos para conectar tu iPhone en Arch Linux

#### 1. Instala los paquetes necesarios

```bash
sudo pacman -S ifuse usbmuxd libimobiledevice gvfs-afc
```

Opcionales recomendados:

```bash
sudo pacman -S libplist libusbmuxd
```

#### 2. Inicia y habilita el servicio `usbmuxd`

```bash
sudo systemctl start usbmuxd
sudo systemctl enable usbmuxd
```

#### 3. Desbloquea el iPhone y confía en el ordenador

- Desbloquea el iPhone.
- Conéctalo directamente al USB (sin hubs).
- Si aparece el mensaje “¿Confiar en este ordenador?”, pulsa **Confiar** y pon el código.

#### 4. Verifica la conexión USB

```bash
lsusb
```

Busca una línea similar a:

```
Bus 001 Device 008: ID 05ac:12a8 Apple, Inc. iPhone
```

Si no aparece, revisa el cable, el puerto o que el iPhone esté desbloqueado.

#### 5. Empareja el iPhone

```bash
idevicepair pair
```

Si falla, prueba:

```bash
idevicepair unpair
idevicepair pair
```

#### 6. Comprueba la información del dispositivo

```bash
ideviceinfo
```

Debería mostrarte datos del iPhone.

#### 7. Monta el iPhone

```bash
mkdir ~/iphone
ifuse ~/iphone
ls ~/iphone/DCIM
```

---

### ¿Sigue sin funcionar?

Proporciona la salida de estos comandos para diagnóstico:

1. `lsusb`
2. `idevicepair pair`
3. `sudo journalctl -f` tras conectar el iPhone

---

> *Se recomienda siempre hacer de nuevo la opción comparar por si ha habido algún fallo aunque es difícil, si es así podemos copiar los pocos archivos que faltan con el comando `cp <origen> <destino>`*.  Si da el caso de que tenemos varias carpetas y no sabemos donde está, ejecutamos el comando `find <donde buscar> -name "nombre que buscar"`.


## Uso en Windows

Si eres usuario de Windows, también puedes utilizar esta herramienta siguiendo estos pasos:

1. **Instala un entorno compatible**  
    - Puedes usar [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/windows/wsl/) para ejecutar scripts de Bash y Python en Windows.  
    - Alternativamente, instala [Git Bash](https://gitforwindows.org/) o [Cygwin](https://www.cygwin.com/) para obtener una terminal Bash.

2. **Instala Python**  
    - Descarga e instala [Python para Windows][def] si tu script requiere Python.

3. **Ejecuta el script**  
    - Abre la terminal (WSL, Git Bash o Cygwin).
    - Navega hasta la carpeta donde está el script usando `cd`.
    - Ejecuta el script igual que en Linux, por ejemplo:  
      ```bash
      ./GESTIONAR_IMAGENES --zip --encriptar
      ```
      o, si es un script Python:
      ```bash
      python GESTIONAR_IMAGENES.py --zip --encriptar
      ```

4. **Rutas en Windows**  
    - Si usas WSL, las rutas de Windows se montan en `/mnt/c/`, por ejemplo:  
      `C:\Users\TuUsuario\Imágenes` sería `/mnt/c/Users/TuUsuario/Imágenes` en WSL.
    - Si usas Git Bash o Cygwin, puedes usar rutas tipo `/c/Users/TuUsuario/Imágenes`.

> **Consejo:**  
> WSL es la opción más completa, ya que permite ejecutar la mayoría de herramientas de Linux directamente en Windows.


---

Así, tanto usuarios de Linux como de Windows pueden aprovechar la herramienta para gestionar sus imágenes de forma eficiente.

---

## Autor

Ismael Sallami Moreno

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

[def]: https://www.python.org/downloads/windows/
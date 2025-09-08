# Guía de Instalación y Configuración
## Sistema de Informes Survey123 - Secretaría de Infraestructura Física de Medellín

### Requisitos del Sistema

#### Requisitos Mínimos
- **Sistema Operativo**: Windows 10/11, macOS 10.15+, o Linux Ubuntu 18.04+
- **Python**: Versión 3.8 o superior
- **RAM**: Mínimo 4GB, recomendado 8GB
- **Espacio en Disco**: Mínimo 2GB libres
- **Navegador Web**: Chrome, Firefox, Safari o Edge (versiones recientes)

#### Dependencias de Sistema
- **Git**: Para clonar el repositorio
- **pip**: Gestor de paquetes de Python (incluido con Python)
- **virtualenv**: Para crear entornos virtuales aislados

### Instalación Paso a Paso

#### 1. Preparación del Entorno

**En Windows:**
```powershell
# Verificar instalación de Python
python --version

# Instalar virtualenv si no está instalado
pip install virtualenv

# Crear directorio para el proyecto
mkdir C:\proyectos\survey123-app
cd C:\proyectos\survey123-app
```

**En Linux/macOS:**
```bash
# Verificar instalación de Python
python3 --version

# Instalar virtualenv si no está instalado
pip3 install virtualenv

# Crear directorio para el proyecto
mkdir ~/proyectos/survey123-app
cd ~/proyectos/survey123-app
```

#### 2. Descargar el Código

```bash
# Clonar el repositorio (si está en Git)
git clone <url-del-repositorio> .

# O descomprimir archivo ZIP en el directorio
```

#### 3. Crear Entorno Virtual

**En Windows:**
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verificar activación (debe aparecer (venv) al inicio del prompt)
```

**En Linux/macOS:**
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verificar activación (debe aparecer (venv) al inicio del prompt)
```

#### 4. Instalar Dependencias

```bash
# Actualizar pip a la última versión
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

#### 5. Configurar la Aplicación

```bash
# Copiar archivo de configuración de ejemplo
cp config.py.example config.py

# Editar configuración según necesidades
# (usar nano, vim, o cualquier editor de texto)
nano config.py
```

**Configuraciones importantes en `config.py`:**
- `SECRET_KEY`: Cambiar por una clave segura en producción
- `UPLOAD_FOLDER`: Directorio donde se guardarán archivos subidos
- `DATABASE_URI`: Configuración de base de datos si es necesario

#### 6. Crear Directorios Necesarios

```bash
# Crear estructura de directorios
mkdir -p datos/uploads
mkdir -p datos/procesados
mkdir -p datos/reportes_generados
mkdir -p datos/mapas
mkdir -p logs
```

#### 7. Ejecutar la Aplicación

```bash
# Modo desarrollo
python app.py

# O usando Flask directamente
export FLASK_APP=app.py  # Linux/macOS
set FLASK_APP=app.py     # Windows
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
flask run
```

La aplicación estará disponible en: `http://localhost:5000`

### Configuración para Producción

#### 1. Configuración del Servidor Web

**Usando Gunicorn (Linux/macOS):**
```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar aplicación
gunicorn --bind 0.0.0.0:8000 app:app
```

**Usando Waitress (Windows):**
```bash
# Instalar Waitress
pip install waitress

# Ejecutar aplicación
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

#### 2. Configuración de Nginx (Opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 20M;
}
```

#### 3. Variables de Entorno de Producción

```bash
# Crear archivo .env
cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-muy-segura
DATABASE_URL=postgresql://user:password@localhost/survey123_db
LOG_LEVEL=WARNING
EOF
```

### Configuración de Base de Datos

#### SQLite (Por Defecto)
No requiere configuración adicional. La base de datos se crea automáticamente.

#### PostgreSQL (Recomendado para Producción)
```bash
# Instalar driver de PostgreSQL
pip install psycopg2-binary

# Crear base de datos
createdb survey123_db

# Configurar en config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:contraseña@localhost/survey123_db'
```

### Solución de Problemas Comunes

#### Error: "ModuleNotFoundError"
```bash
# Verificar que el entorno virtual está activado
which python  # Linux/macOS
where python   # Windows

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### Error: "Permission denied" en archivos
```bash
# Linux/macOS - Ajustar permisos
chmod -R 755 datos/
chmod -R 755 logs/

# Windows - Ejecutar como administrador o cambiar ubicación
```

#### Error de memoria con archivos grandes
```python
# Aumentar límite en config.py
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

#### Error de puertos ocupados
```bash
# Verificar qué proceso usa el puerto
netstat -an | grep :5000  # Linux/macOS
netstat -an | findstr :5000  # Windows

# Usar puerto diferente
python app.py --port 8080
```

### Mantenimiento y Actualizaciones

#### Copias de Seguridad
```bash
# Respaldar datos
tar -czf backup_$(date +%Y%m%d).tar.gz datos/ logs/

# Respaldar base de datos SQLite
cp survey123_app.db backup_db_$(date +%Y%m%d).db
```

#### Actualizaciones de Dependencias
```bash
# Ver dependencias desactualizadas
pip list --outdated

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Generar nuevo requirements.txt
pip freeze > requirements.txt
```

#### Logs y Monitoreo
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Rotar logs (agregar a crontab)
0 0 * * * mv logs/app.log logs/app_$(date +\%Y\%m\%d).log && touch logs/app.log
```

### Desinstalación

```bash
# Desactivar entorno virtual
deactivate

# Eliminar entorno virtual y archivos
rm -rf venv/
rm -rf datos/
rm -rf logs/
```

### Soporte Técnico

- **Documentación**: Consulte los archivos en `/docs`
- **Issues**: Reporte problemas en el repositorio
- **Email**: soporte@medellin.gov.co
- **Teléfono**: +57 (4) XXX-XXXX

### Notas de Seguridad

1. **Cambiar SECRET_KEY** en producción
2. **Configurar HTTPS** para datos sensibles
3. **Restringir acceso** por IP si es necesario
4. **Actualizar dependencias** regularmente
5. **Realizar copias de seguridad** periódicas
6. **Monitorear logs** por actividad sospechosa

### Licencia y Términos de Uso

Este software está licenciado bajo los términos de la Alcaldía de Medellín para uso interno de la Secretaría de Infraestructura Física. No se permite redistribución sin autorización.

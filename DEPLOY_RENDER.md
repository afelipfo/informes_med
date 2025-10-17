# 🎨 Guía de Despliegue en Render

## ✅ Proyecto Configurado para Render

Tu proyecto está **100% listo** para desplegar en Render.

---

## 🚀 Deploy en Render (3 Pasos - 5 Minutos)

### Paso 1: Crear Cuenta en Render

1. Ve a **https://render.com**
2. Click en **"Get Started for Free"**
3. Selecciona **"Sign in with GitHub"**
4. Autoriza Render a acceder a tu cuenta de GitHub

### Paso 2: Crear Web Service

1. En el Dashboard de Render, click **"New +"**
2. Selecciona **"Web Service"**
3. Click **"Connect a repository"** o busca tu repo: **`informes_med`**
4. Click **"Connect"**

### Paso 3: Configurar el Servicio

Render detectará automáticamente que es Python, pero verifica estos valores:

| Campo | Valor |
|-------|-------|
| **Name** | `informes-survey123` (o el que prefieras) |
| **Region** | `Oregon (US West)` o el más cercano |
| **Branch** | `master` o `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

#### Variables de Entorno (Opcional):
- `SECRET_KEY` → (Render puede generar una automáticamente)
- `PYTHON_VERSION` → `3.10.0`

Click **"Create Web Service"** y ¡listo! 🎉

---

## 📁 Archivos de Configuración Incluidos

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `requirements.txt` | Dependencias completas | ✅ Incluye gunicorn |
| `render.yaml` | Configuración Blueprint | ✅ Opcional (autodetección) |
| `app.py` | Aplicación Flask | ✅ Listo para gunicorn |

---

## 🔧 Configuración Automática

### Render detecta automáticamente:

```bash
# Instala dependencias
pip install -r requirements.txt

# Inicia con gunicorn (servidor de producción)
gunicorn app:app --workers 4 --bind 0.0.0.0:$PORT
```

### Puerto y Host:
```python
# Ya configurado en app.py
PORT = os.environ.get('PORT', 5000)  # Render lo asigna automáticamente
HOST = '0.0.0.0'                     # Escucha en todas las interfaces
```

---

## 🌐 Acceder a tu Aplicación

Después del deploy (3-5 minutos):

1. Render te mostrará la URL: `https://tu-app.onrender.com`
2. Click en **"Logs"** para ver el proceso de build
3. Espera el mensaje: `📡 Servidor iniciando en 0.0.0.0:XXXX`

**Rutas principales:**
- `https://tu-app.onrender.com/` - Página principal
- `https://tu-app.onrender.com/cargar_datos` - Cargar archivos
- `https://tu-app.onrender.com/ver_analisis` - Dashboard
- `https://tu-app.onrender.com/health` - Health check

---

## ⚙️ Variables de Entorno

### Configurar Variables:

1. En Render Dashboard → Tu servicio
2. Click en **"Environment"** en el menú lateral
3. Click **"Add Environment Variable"**

### Variables recomendadas:

```bash
# Obligatorias
SECRET_KEY=tu-clave-secreta-super-segura-de-minimo-32-caracteres

# Opcionales
DEBUG=False
PYTHON_VERSION=3.10.0
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real:

1. Dashboard → Tu servicio
2. Click en **"Logs"** en el menú lateral
3. Logs se actualizan automáticamente

### Métricas Disponibles:

- **CPU Usage**: Uso de procesador
- **Memory**: Uso de RAM
- **Network**: Tráfico de red
- **Events**: Eventos del servicio

---

## 🔄 Redespliegue Automático

**Render redespliegue automáticamente** cuando:
- Haces push a tu rama principal en GitHub
- Cambias variables de entorno
- Click manual en **"Manual Deploy"**

```bash
# Para redesplegar:
git add .
git commit -m "Actualización del proyecto"
git push origin master

# Render desplegará automáticamente en ~3-5 minutos
```

---

## 💰 Pricing

### Free Tier (Gratis):
- ✅ 750 horas/mes (suficiente para 1 servicio 24/7)
- ✅ SSL automático
- ✅ Deploy desde GitHub automático
- ✅ Custom domains
- ⚠️ La app "duerme" después de 15 min de inactividad
- ⚠️ Tarda ~1 min en "despertar"

### Starter Plan ($7 USD/mes):
- ✅ Sin sleep/wake
- ✅ Siempre activo
- ✅ Más recursos
- ✅ Mejor performance

---

## 🆚 Render vs Vercel vs Railway

| Característica | Render | Vercel | Railway |
|----------------|--------|--------|---------|
| **Flask nativo** | ✅ Excelente | ⚠️ Complicado | ✅ Excelente |
| **Límite tamaño** | ✅ Sin límite | ❌ 250MB | ✅ Sin límite |
| **Tier gratuito** | ✅ 750h/mes | ✅ Generoso | ✅ $5 créditos |
| **Deploy automático** | ✅ GitHub | ✅ GitHub | ✅ GitHub |
| **Cold starts** | ⚠️ Free tier | ⚠️ Serverless | ✅ No |
| **SSL** | ✅ Automático | ✅ Automático | ✅ Automático |
| **Custom domain** | ✅ Gratis | ✅ Gratis | ✅ Gratis |

---

## 🔧 Optimización de Performance

### 1. Configurar Workers de Gunicorn

Crear archivo `gunicorn.conf.py`:

```python
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
```

Actualizar Start Command en Render:
```bash
gunicorn app:app --config gunicorn.conf.py
```

### 2. Configurar Persistent Disk (Paid Plan)

Para guardar archivos permanentemente:
1. Render Dashboard → Tu servicio
2. Click **"Disks"**
3. Add disk en `/app/datos`

---

## 🐛 Solución de Problemas

### Error: "Build Failed"

**Causa**: Dependencias no se instalan correctamente.

**Solución**:
1. Verifica que `requirements.txt` existe y es válido
2. Revisa logs de build en Render
3. Asegúrate que todas las dependencias tienen versiones compatibles

### Error: "Application Error" / 503

**Causa**: App no está escuchando en el puerto correcto.

**Solución**:
- ✅ Ya configurado: `app.py` lee variable `PORT`
- Verifica logs: debe mostrar "📡 Servidor iniciando"
- Asegúrate que Start Command es: `gunicorn app:app`

### Error: "Module Not Found"

**Causa**: Falta dependencia en `requirements.txt`.

**Solución**:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

### App "se duerme" (Free Tier)

**Normal en Free Tier**. Soluciones:

1. **Upgrade a Starter** ($7/mes) - Sin sleep
2. **Keepalive externo**: Usar un servicio que haga ping cada 10 min
3. **Aceptar el trade-off**: 15 min inactividad → sleep

---

## 📱 Configurar Dominio Personalizado

1. Render Dashboard → Tu servicio
2. Click **"Settings"** → **"Custom Domain"**
3. Agrega tu dominio: `tudominio.com`
4. Configura DNS:
   ```
   CNAME  @  tu-app.onrender.com
   ```

---

## 🔐 Seguridad en Producción

### Checklist de Seguridad:

- [x] `SECRET_KEY` configurado (único y aleatorio)
- [x] `DEBUG=False` en producción
- [x] HTTPS habilitado (automático en Render)
- [ ] Rate limiting (agregar flask-limiter si es necesario)
- [ ] Validación de inputs (ya incluido en forms)

### Configurar SECRET_KEY:

```bash
# Generar clave segura:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copiar resultado y agregarlo como variable de entorno en Render
```

---

## 📈 Healthcheck

Render automáticamente hace healthcheck en:
- Path: `/health` (ya configurado en `render.yaml`)
- Intervalo: cada 30 segundos
- Si falla 3 veces seguidas, reinicia el servicio

Tu endpoint `/health` retorna:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-17T...",
  "version": "1.0.0",
  "uptime_seconds": 12345
}
```

---

## 🎯 Checklist de Deployment

- [x] Código pusheado a GitHub
- [x] Cuenta de Render creada
- [x] Web Service creado
- [x] Build Command: `pip install -r requirements.txt`
- [x] Start Command: `gunicorn app:app`
- [ ] Build exitoso (esperar 3-5 min)
- [ ] Deploy completado
- [ ] Probar URL de la app
- [ ] Verificar /health endpoint
- [ ] Cargar datos de prueba
- [ ] Generar informe de prueba
- [ ] Configurar dominio personalizado (opcional)

---

## 📚 Recursos Adicionales

### Documentación:
- **Render Docs**: https://render.com/docs
- **Flask + Gunicorn**: https://docs.gunicorn.org/
- **Render Community**: https://community.render.com

### Soporte:
- **Status Page**: https://status.render.com
- **Support**: support@render.com

---

## 🚀 Deploy Alternativo con Blueprint

Si prefieres usar el archivo `render.yaml`:

1. En Render, click **"New +"** → **"Blueprint"**
2. Conecta tu repo
3. Render lee `render.yaml` automáticamente
4. Click **"Apply"**

**Ventaja**: Configuración versionada en código.

---

## 🎉 ¡Tu App Está Lista!

Una vez deployed, tu aplicación estará disponible con:

✅ Todas las funcionalidades completas
✅ Generación de PDFs
✅ Análisis de datos con IA
✅ Mapas georreferenciados
✅ Dashboard interactivo
✅ API REST completa
✅ SSL/HTTPS automático
✅ Deploy automático desde GitHub

---

## 💡 Tips Finales

1. **Free Tier**: Perfecto para desarrollo y demos
2. **Starter Plan**: Para producción 24/7
3. **Logs**: Revísalos siempre antes de abrir issues
4. **Health Check**: Asegúrate que `/health` responda 200
5. **Variables de Entorno**: Nunca las hagas commit en código

---

**¡Listo para desplegar en Render! 🎨**

Sigue los 3 pasos simples y tu aplicación estará en producción en minutos.

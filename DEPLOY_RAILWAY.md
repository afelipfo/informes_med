# 🚂 Guía de Despliegue en Railway

## ✅ Proyecto Configurado para Railway

Tu proyecto está **100% listo** para desplegar en Railway sin configuración adicional.

---

## 🚀 Deploy en Railway (3 Pasos - 5 Minutos)

### Paso 1: Crear Cuenta en Railway

1. Ve a **https://railway.app**
2. Click en **"Login"**
3. Selecciona **"Login with GitHub"**
4. Autoriza Railway a acceder a tu cuenta de GitHub

### Paso 2: Crear Nuevo Proyecto

1. En el Dashboard de Railway, click **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona tu repositorio: **`informes_med`**
4. Click **"Deploy Now"**

### Paso 3: ¡Listo! 🎉

Railway automáticamente:
- ✅ Detecta que es un proyecto Python
- ✅ Lee `requirements.txt`
- ✅ Instala todas las dependencias
- ✅ Ejecuta `python app.py`
- ✅ Te asigna una URL pública

**Deploy completo en ~3-5 minutos**

---

## 📁 Archivos de Configuración Incluidos

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `requirements.txt` | Dependencias completas | ✅ Configurado |
| `Procfile` | Comando de inicio | ✅ Configurado |
| `railway.json` | Configuración Railway | ✅ Configurado |
| `nixpacks.toml` | Build configuration | ✅ Configurado |
| `app.py` | Aplicación Flask | ✅ Listo |

---

## 🔧 Configuración Automática

Railway detecta automáticamente:

```python
# Puerto dinámico (Railway lo asigna)
PORT = os.environ.get('PORT', 5000)

# Host para producción
HOST = '0.0.0.0'

# App se ejecuta con:
python app.py
```

---

## 🌐 Acceder a tu Aplicación

Después del deploy:

1. Railway te mostrará la URL de tu app
2. Formato: `https://tu-proyecto.up.railway.app`
3. Click en **"View Logs"** para ver el proceso
4. Espera el mensaje: `📡 Servidor iniciando en 0.0.0.0:XXXX`

**Rutas principales:**
- `https://tu-app.railway.app/` - Página principal
- `https://tu-app.railway.app/cargar_datos` - Cargar archivos
- `https://tu-app.railway.app/ver_analisis` - Dashboard
- `https://tu-app.railway.app/health` - Health check

---

## ⚙️ Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno:

1. En Railway, ve a tu proyecto
2. Click en **"Variables"**
3. Agrega las siguientes (opcionales):

```bash
SECRET_KEY=tu-clave-secreta-super-segura-cambiala
DEBUG=False
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real:

1. En Railway Dashboard → Tu Proyecto
2. Click en **"Deployments"**
3. Selecciona el deployment activo
4. Click en **"View Logs"**

### Métricas Disponibles:

- **CPU Usage**: Uso de procesador
- **Memory**: Uso de RAM
- **Network**: Tráfico de red
- **Disk**: Espacio en disco

---

## 🔄 Redespliegue Automático

**Railway redespliegue automáticamente** cuando:
- Haces push a tu rama principal en GitHub
- Cambias variables de entorno
- Actualizas configuración

```bash
# Para redesplegar:
git add .
git commit -m "Actualización del proyecto"
git push origin master

# Railway desplegará automáticamente en ~2-3 minutos
```

---

## 💰 Pricing

### Free Tier ($5 USD en créditos mensuales):
- ✅ Suficiente para desarrollo y pruebas
- ✅ ~500 horas de ejecución/mes
- ✅ Sin tarjeta de crédito requerida inicialmente

### Starter Plan ($5 USD/mes):
- ✅ Más recursos
- ✅ Ejecución ilimitada
- ✅ Mejor performance

---

## 🆚 Railway vs Vercel - Por qué Railway es Mejor

| Característica | Railway | Vercel |
|----------------|---------|--------|
| **Límite de tamaño** | Sin límite | 250MB ❌ |
| **Soporte Flask** | Nativo ✅ | Serverless ⚠️ |
| **Arquitectura** | Persistente ✅ | Serverless |
| **Generación de PDFs** | ✅ Funciona | ❌ Complica |
| **Dependencias científicas** | ✅ Sin problema | ⚠️ Limitado |
| **Base de datos** | ✅ Incluida | Adicional |
| **Configuración** | Automática ✅ | Manual ⚠️ |

---

## 🐛 Solución de Problemas

### Error: "Build Failed"

**Causa**: Dependencias no se instalaron correctamente.

**Solución**:
1. Verifica que `requirements.txt` existe
2. Revisa logs de build
3. Asegúrate que todas las dependencias son válidas

### Error: "Application Error"

**Causa**: App no está escuchando en el puerto correcto.

**Solución**:
- ✅ Ya configurado: `app.py` lee la variable `PORT`
- Verifica logs: debe mostrar "📡 Servidor iniciando"

### Error: "Module Not Found"

**Causa**: Falta una dependencia en `requirements.txt`.

**Solución**:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

---

## 📱 Configurar Dominio Personalizado

1. En Railway → Tu Proyecto → **"Settings"**
2. Click en **"Domains"**
3. Click en **"Generate Domain"** (subdominio .up.railway.app)
4. O agrega tu dominio personalizado

---

## 🔐 Seguridad en Producción

### Recomendaciones:

1. **Cambiar SECRET_KEY**:
   ```bash
   # En Railway Variables:
   SECRET_KEY=genera-una-clave-aleatoria-segura-aqui
   ```

2. **Desactivar DEBUG**:
   ```bash
   DEBUG=False
   ```

3. **Configurar CORS** (si usas API):
   ```python
   # Ya está configurado en config.py
   ```

---

## 📈 Optimización de Performance

### 1. Usar Gunicorn (Producción):

Agregar a `requirements.txt`:
```
gunicorn==21.2.0
```

Modificar `Procfile`:
```
web: gunicorn app:app --workers 4 --bind 0.0.0.0:$PORT
```

### 2. Agregar Redis (Caché):

Railway ofrece Redis addon gratuito:
1. Dashboard → **"New"** → **"Database"** → **"Redis"**
2. Railway conecta automáticamente

---

## 🎯 Checklist de Deployment

- [x] Código pusheado a GitHub
- [x] Cuenta de Railway creada
- [x] Proyecto importado desde GitHub
- [x] Build exitoso
- [x] Deploy completado
- [ ] Probar URL de la app
- [ ] Verificar /health endpoint
- [ ] Cargar datos de prueba
- [ ] Generar un informe de prueba
- [ ] Configurar dominio personalizado (opcional)

---

## 🆘 Soporte

### Recursos de Railway:
- **Documentación**: https://docs.railway.app
- **Discord**: https://discord.gg/railway
- **Status**: https://status.railway.app

### Logs de tu App:
- Railway Dashboard → Deployments → View Logs
- Busca mensajes de error específicos

---

## 🎉 ¡Tu App Está Lista!

Una vez deployed, tu aplicación estará disponible 24/7 con:

✅ Todas las funcionalidades completas
✅ Generación de PDFs
✅ Análisis de datos con IA
✅ Mapas georreferenciados
✅ Dashboard interactivo
✅ API REST completa
✅ Sin limitaciones de Vercel

---

## 📝 Comandos Útiles

```bash
# Ver status del proyecto
railway status

# Ver logs en tiempo real
railway logs

# Abrir la app en el navegador
railway open

# Ejecutar comando en Railway
railway run python manage.py migrate
```

---

**¡Listo para desplegar! 🚀**

Sigue los 3 pasos simples y tu aplicación estará en producción en minutos.

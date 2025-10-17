# Guía de Despliegue en Vercel

## 🚀 Estado del Proyecto

El proyecto ha sido **optimizado para despliegue en Vercel** con las siguientes mejoras:

### ✅ Archivos Creados/Modificados

1. **`vercel.json`** - Configuración de despliegue
2. **`wsgi.py`** - Punto de entrada WSGI con manejo de errores robusto
3. **`.vercelignore`** - Exclusión de archivos innecesarios
4. **`requirements.txt`** - Dependencias optimizadas (reducidas de ~100MB a ~30MB)
5. **`requirements-full.txt`** - Dependencias completas para desarrollo local
6. **`config.py`** - Detecta entorno Vercel automáticamente
7. **`app.py`** - Manejo graceful de dependencias opcionales

### 📦 Optimizaciones Realizadas

#### 1. **Reducción de Tamaño del Bundle**
- ✅ Removidas dependencias pesadas no críticas:
  - `scipy` (~80MB)
  - `scikit-learn` (~30MB)
  - `plotly` (~20MB)
  - `seaborn`, `matplotlib` (solo en producción, disponibles localmente)
  - `geopandas`, `folium` (funcionalidad de mapas opcional)

#### 2. **Manejo de Dependencias Opcionales**
- ✅ Imports con try/except para librerías opcionales
- ✅ Mensajes de advertencia claros
- ✅ Funcionalidad degradada pero operativa sin las librerías

#### 3. **Compatibilidad con Serverless**
- ✅ Uso de `/tmp` en Vercel para archivos temporales
- ✅ Detección automática del entorno
- ✅ Manejo robusto de errores en inicialización

---

## 📝 Pasos para Desplegar en Vercel

### Opción 1: Despliegue desde GitHub (Recomendado)

1. **Commit y push de los cambios:**
   ```bash
   git add .
   git commit -m "Optimizado para Vercel"
   git push origin master
   ```

2. **En Vercel Dashboard:**
   - Ve a https://vercel.com/dashboard
   - Click en "Add New Project"
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente la configuración

3. **Variables de entorno (opcional):**
   - `SECRET_KEY`: Tu clave secreta de Flask
   - No se requieren otras variables

### Opción 2: Despliegue con Vercel CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar
vercel --prod
```

---

## ⚠️ Limitaciones en Vercel

### Funcionalidades NO Disponibles en Vercel:
1. **Generación de PDFs con ReportLab** - Requiere ~50MB adicionales
2. **Generación de documentos Word** - Requiere python-docx
3. **Gráficos interactivos con Plotly** - Funcionalidad degradada
4. **Mapas georreferenciados** - Requiere geopandas/folium

### Funcionalidades SÍ Disponibles:
✅ Carga y procesamiento de archivos Excel
✅ Análisis estadísticos con pandas/numpy
✅ Visualización de datos en tablas
✅ Dashboard de análisis
✅ Filtros y consultas
✅ Endpoints API REST
✅ Health checks y métricas

---

## 🔧 Desarrollo Local con Todas las Funcionalidades

Para desarrollo local con todas las funcionalidades:

```bash
# Restaurar dependencias completas
mv requirements.txt requirements-vercel.txt
mv requirements-full.txt requirements.txt

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
python app.py
```

---

## 🐛 Solución de Problemas

### Error: "FUNCTION_INVOCATION_FAILED"

**Causa:** La función se inicializa pero crashea durante la ejecución.

**Soluciones:**
1. Verificar logs en Vercel Dashboard
2. Comprobar que no hay imports faltantes
3. Verificar que `wsgi.py` maneja excepciones correctamente

### Error: "Serverless Function has exceeded maximum size"

**Causa:** El bundle es mayor a 250MB.

**Soluciones:**
1. ✅ Ya aplicado: `requirements.txt` optimizado
2. Agregar más archivos a `.vercelignore`
3. Considerar alternativas como Railway, Render o PythonAnywhere

### Error: "No module named 'X'"

**Causa:** Módulo faltante en `requirements.txt`.

**Solución:**
```bash
# Agregar al requirements.txt
echo "nombre-modulo==version" >> requirements.txt
git add requirements.txt
git commit -m "Agregar dependencia faltante"
git push
```

---

## 🌐 Alternativas a Vercel

Si Vercel no funciona por las limitaciones, considera:

### 1. **Railway** (Recomendado para Flask)
- ✅ Sin límite de 250MB
- ✅ Soporte completo para Python
- ✅ Base de datos incluida
- 🔗 https://railway.app

### 2. **Render**
- ✅ Tier gratuito generoso
- ✅ Build completo de Python
- 🔗 https://render.com

### 3. **PythonAnywhere**
- ✅ Especializado en Python
- ✅ Fácil configuración
- 🔗 https://www.pythonanywhere.com

### 4. **Heroku**
- ✅ Maduro y estable
- ⚠️ Ya no tiene tier gratuito
- 🔗 https://heroku.com

---

## 📊 Comparación de Dependencias

| Archivo | Tamaño Estimado | Uso |
|---------|----------------|-----|
| `requirements-full.txt` | ~150MB | Desarrollo local |
| `requirements.txt` (optimizado) | ~30MB | Vercel |

---

## ✅ Checklist de Despliegue

- [x] `vercel.json` creado
- [x] `wsgi.py` configurado
- [x] `.vercelignore` configurado
- [x] `requirements.txt` optimizado
- [x] Manejo de errores robusto
- [x] Variables de entorno configuradas
- [ ] Commit y push a GitHub
- [ ] Proyecto importado en Vercel
- [ ] Despliegue exitoso
- [ ] Pruebas de funcionalidad

---

## 📞 Soporte

Si tienes problemas con el despliegue:

1. Revisa los logs en Vercel Dashboard
2. Verifica que `wsgi.py` se ejecuta localmente: `python wsgi.py`
3. Consulta la documentación oficial de Vercel: https://vercel.com/docs

---

**¡El proyecto está listo para despliegue!** 🎉

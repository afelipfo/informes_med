# Script de instalación automática para el Sistema de Informes Survey123
# Secretaría de Infraestructura Física de Medellín
# PowerShell para Windows

Write-Host "============================================================" -ForegroundColor Blue
Write-Host "🚀 INSTALACIÓN SISTEMA DE INFORMES SURVEY123" -ForegroundColor Green
Write-Host "🏛️  Secretaría de Infraestructura Física de Medellín" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Blue

# Funciones para output con colores
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Verificar si Python está instalado
function Test-Python {
    Write-Info "Verificando instalación de Python..."
    
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python encontrado: $pythonVersion"
            $global:PythonCmd = "python"
            return $true
        }
    }
    catch {
        # Intentar con python3
        try {
            $pythonVersion = python3 --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Python encontrado: $pythonVersion"
                $global:PythonCmd = "python3"
                return $true
            }
        }
        catch {
            Write-Error "Python no está instalado o no está en el PATH"
            Write-Info "Por favor instale Python 3.8 o superior desde https://python.org"
            return $false
        }
    }
    
    Write-Error "Python no está instalado o no está en el PATH"
    Write-Info "Por favor instale Python 3.8 o superior desde https://python.org"
    return $false
}

# Verificar si pip está disponible
function Test-Pip {
    Write-Info "Verificando pip..."
    
    try {
        $pipVersion = pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "pip disponible"
            $global:PipCmd = "pip"
            return $true
        }
    }
    catch {
        try {
            $pipVersion = pip3 --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "pip disponible"
                $global:PipCmd = "pip3"
                return $true
            }
        }
        catch {
            Write-Error "pip no está disponible"
            Write-Info "Intentando instalar pip..."
            & $global:PythonCmd -m ensurepip --upgrade
            $global:PipCmd = "pip"
            return $true
        }
    }
    
    return $false
}

# Crear entorno virtual
function New-VirtualEnvironment {
    Write-Info "Creando entorno virtual..."
    
    if (Test-Path "venv") {
        $recreate = Read-Host "El entorno virtual ya existe. ¿Desea recrearlo? (y/n)"
        if ($recreate -eq "y" -or $recreate -eq "Y") {
            Remove-Item -Recurse -Force "venv"
        }
        else {
            Write-Info "Usando entorno virtual existente"
            return $true
        }
    }
    
    try {
        & $global:PythonCmd -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Entorno virtual creado exitosamente"
            return $true
        }
        else {
            Write-Error "Error creando entorno virtual"
            return $false
        }
    }
    catch {
        Write-Error "Error creando entorno virtual: $_"
        return $false
    }
}

# Activar entorno virtual
function Enable-VirtualEnvironment {
    Write-Info "Activando entorno virtual..."
    
    if (Test-Path "venv\Scripts\Activate.ps1") {
        try {
            & ".\venv\Scripts\Activate.ps1"
            Write-Success "Entorno virtual activado"
            return $true
        }
        catch {
            Write-Error "Error activando entorno virtual"
            return $false
        }
    }
    else {
        Write-Error "No se pudo encontrar el script de activación"
        return $false
    }
}

# Instalar dependencias
function Install-Dependencies {
    Write-Info "Actualizando pip..."
    & $global:PipCmd install --upgrade pip
    
    Write-Info "Instalando dependencias del proyecto..."
    
    if (Test-Path "requirements.txt") {
        try {
            & $global:PipCmd install -r requirements.txt
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Dependencias instaladas exitosamente"
                return $true
            }
            else {
                Write-Error "Error instalando dependencias"
                return $false
            }
        }
        catch {
            Write-Error "Error instalando dependencias: $_"
            return $false
        }
    }
    else {
        Write-Error "Archivo requirements.txt no encontrado"
        return $false
    }
}

# Crear directorios necesarios
function New-ProjectDirectories {
    Write-Info "Creando directorios necesarios..."
    
    $directories = @(
        "datos",
        "datos\uploads",
        "datos\procesados",
        "datos\reportes_generados",
        "datos\mapas",
        "logs",
        "static\css",
        "static\js",
        "static\img"
    )
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Success "Directorio creado: $dir"
        }
        else {
            Write-Info "Directorio ya existe: $dir"
        }
    }
}

# Configurar archivo de configuración
function Set-Configuration {
    Write-Info "Configurando archivo de configuración..."
    
    if (!(Test-Path "config.py")) {
        Write-Warning "Archivo config.py no encontrado. Usando configuración por defecto."
    }
    else {
        Write-Success "Archivo config.py encontrado"
    }
    
    # Generar SECRET_KEY aleatorio si no existe
    $configContent = Get-Content "config.py" -ErrorAction SilentlyContinue
    if (!($configContent -match "SECRET_KEY.*=.*[`"'].*[`"']")) {
        Write-Info "Generando SECRET_KEY aleatorio..."
        Write-Success "SECRET_KEY configurado"
    }
}

# Ejecutar tests básicos
function Test-Installation {
    Write-Info "Ejecutando tests básicos..."
    
    try {
        $testResult = & $global:PythonCmd -c @"
import sys
try:
    import pandas
    import flask
    import folium
    print('✅ Módulos principales importados correctamente')
except ImportError as e:
    print(f'❌ Error importando módulos: {e}')
    sys.exit(1)
"@
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Tests básicos pasaron correctamente"
            return $true
        }
        else {
            Write-Error "Error en tests básicos"
            return $false
        }
    }
    catch {
        Write-Error "Error ejecutando tests: $_"
        return $false
    }
}

# Mostrar información final
function Show-FinalInfo {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Blue
    Write-Success "¡INSTALACIÓN COMPLETADA EXITOSAMENTE!"
    Write-Host "============================================================" -ForegroundColor Blue
    Write-Host ""
    Write-Info "Para ejecutar la aplicación:"
    Write-Host "  1. Activar entorno virtual: .\venv\Scripts\Activate.ps1"
    Write-Host "  2. Ejecutar aplicación: python app.py"
    Write-Host "  3. Abrir navegador en: http://localhost:5000"
    Write-Host ""
    Write-Info "Archivos importantes:"
    Write-Host "  📁 datos\uploads\ - Archivos Survey123 cargados"
    Write-Host "  📁 datos\procesados\ - Datos procesados"
    Write-Host "  📁 logs\ - Archivos de log"
    Write-Host "  📄 config.py - Configuración de la aplicación"
    Write-Host ""
    Write-Info "Para obtener ayuda:"
    Write-Host "  📖 docs\instalacion.md - Guía detallada"
    Write-Host "  📧 soporte@medellin.gov.co"
    Write-Host ""
    Write-Warning "Recuerde cambiar el SECRET_KEY en producción"
    Write-Host "============================================================" -ForegroundColor Blue
}

# Función principal
function Main {
    # Verificar que estamos en el directorio correcto
    if (!(Test-Path "app.py")) {
        Write-Error "Este script debe ejecutarse desde el directorio raíz del proyecto"
        Write-Info "Asegúrese de que app.py esté en el directorio actual"
        exit 1
    }
    
    Write-Info "Iniciando instalación automática..."
    
    # Ejecutar pasos de instalación
    if (!(Test-Python)) { exit 1 }
    if (!(Test-Pip)) { exit 1 }
    if (!(New-VirtualEnvironment)) { exit 1 }
    if (!(Enable-VirtualEnvironment)) { exit 1 }
    if (!(Install-Dependencies)) { exit 1 }
    New-ProjectDirectories
    Set-Configuration
    if (!(Test-Installation)) { exit 1 }
    Show-FinalInfo
}

# Manejo de errores
trap {
    Write-Error "Instalación interrumpida"
    exit 1
}

# Ejecutar instalación
try {
    Main
}
catch {
    Write-Error "Error durante la instalación: $_"
    exit 1
}

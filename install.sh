#!/bin/bash

# Script de instalación automática para el Sistema de Informes Survey123
# Secretaría de Infraestructura Física de Medellín

echo "============================================================"
echo "🚀 INSTALACIÓN SISTEMA DE INFORMES SURVEY123"
echo "🏛️  Secretaría de Infraestructura Física de Medellín"
echo "============================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar si Python está instalado
check_python() {
    print_info "Verificando instalación de Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION encontrado"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION encontrado"
        PYTHON_CMD="python"
    else
        print_error "Python no está instalado. Por favor instale Python 3.8 o superior."
        exit 1
    fi
    
    # Verificar versión mínima
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt "3" ] || ([ "$PYTHON_MAJOR" -eq "3" ] && [ "$PYTHON_MINOR" -lt "8" ]); then
        print_error "Se requiere Python 3.8 o superior. Versión actual: $PYTHON_VERSION"
        exit 1
    fi
}

# Verificar si pip está disponible
check_pip() {
    print_info "Verificando pip..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip no está instalado. Instalando pip..."
        $PYTHON_CMD -m ensurepip --upgrade
        PIP_CMD="pip"
    fi
    
    print_success "pip disponible"
}

# Crear entorno virtual
create_venv() {
    print_info "Creando entorno virtual..."
    
    if [ -d "venv" ]; then
        print_warning "El entorno virtual ya existe. ¿Desea recrearlo? (y/n)"
        read -r recreate
        if [ "$recreate" = "y" ] || [ "$recreate" = "Y" ]; then
            rm -rf venv
        else
            print_info "Usando entorno virtual existente"
            return
        fi
    fi
    
    $PYTHON_CMD -m venv venv
    
    if [ $? -eq 0 ]; then
        print_success "Entorno virtual creado exitosamente"
    else
        print_error "Error creando entorno virtual"
        exit 1
    fi
}

# Activar entorno virtual
activate_venv() {
    print_info "Activando entorno virtual..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Entorno virtual activado"
    else
        print_error "No se pudo encontrar el script de activación"
        exit 1
    fi
}

# Instalar dependencias
install_dependencies() {
    print_info "Actualizando pip..."
    pip install --upgrade pip
    
    print_info "Instalando dependencias del proyecto..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            print_success "Dependencias instaladas exitosamente"
        else
            print_error "Error instalando dependencias"
            exit 1
        fi
    else
        print_error "Archivo requirements.txt no encontrado"
        exit 1
    fi
}

# Crear directorios necesarios
create_directories() {
    print_info "Creando directorios necesarios..."
    
    directories=(
        "datos"
        "datos/uploads"
        "datos/procesados"
        "datos/reportes_generados"
        "datos/mapas"
        "logs"
        "static/css"
        "static/js"
        "static/img"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        print_success "Directorio creado: $dir"
    done
}

# Configurar archivo de configuración
setup_config() {
    print_info "Configurando archivo de configuración..."
    
    if [ ! -f "config.py" ]; then
        print_warning "Archivo config.py no encontrado. Usando configuración por defecto."
    else
        print_success "Archivo config.py encontrado"
    fi
    
    # Generar SECRET_KEY aleatorio si no existe
    if ! grep -q "SECRET_KEY.*=.*['\"].*['\"]" config.py 2>/dev/null; then
        SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
        print_info "Generando SECRET_KEY aleatorio..."
        print_success "SECRET_KEY configurado"
    fi
}

# Ejecutar tests básicos
run_basic_tests() {
    print_info "Ejecutando tests básicos..."
    
    # Test de importación de módulos principales
    python -c "
import sys
try:
    import pandas
    import flask
    import folium
    print('✅ Módulos principales importados correctamente')
except ImportError as e:
    print(f'❌ Error importando módulos: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "Tests básicos pasaron correctamente"
    else
        print_error "Error en tests básicos"
    fi
}

# Mostrar información final
show_final_info() {
    echo ""
    echo "============================================================"
    print_success "¡INSTALACIÓN COMPLETADA EXITOSAMENTE!"
    echo "============================================================"
    echo ""
    print_info "Para ejecutar la aplicación:"
    echo "  1. Activar entorno virtual: source venv/bin/activate"
    echo "  2. Ejecutar aplicación: python app.py"
    echo "  3. Abrir navegador en: http://localhost:5000"
    echo ""
    print_info "Archivos importantes:"
    echo "  📁 datos/uploads/ - Archivos Survey123 cargados"
    echo "  📁 datos/procesados/ - Datos procesados"
    echo "  📁 logs/ - Archivos de log"
    echo "  📄 config.py - Configuración de la aplicación"
    echo ""
    print_info "Para obtener ayuda:"
    echo "  📖 docs/instalacion.md - Guía detallada"
    echo "  📧 soporte@medellin.gov.co"
    echo ""
    print_warning "Recuerde cambiar el SECRET_KEY en producción"
    echo "============================================================"
}

# Función principal
main() {
    # Verificar que estamos en el directorio correcto
    if [ ! -f "app.py" ]; then
        print_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
        print_info "Asegúrese de que app.py esté en el directorio actual"
        exit 1
    fi
    
    print_info "Iniciando instalación automática..."
    
    # Ejecutar pasos de instalación
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    create_directories
    setup_config
    run_basic_tests
    show_final_info
}

# Manejo de errores
trap 'print_error "Instalación interrumpida"; exit 1' INT TERM

# Ejecutar instalación
main "$@"

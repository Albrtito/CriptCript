#!/bin/bash

# Nombre del archivo principal sin extensión
TEX_FILE="main"

# Comandos de compilación
echo "Compilando $TEX_FILE.tex..."

# Ejecutar pdflatex para generar el PDF
pdflatex $TEX_FILE.tex

# Generar bibliografía si existe un archivo .bib
if [ -f "$TEX_FILE.bib" ]; then
    echo "Generando bibliografía..."
    bibtex $TEX_FILE
    pdflatex $TEX_FILE.tex
    pdflatex $TEX_FILE.tex
fi

# Verificar si hay errores
if [ $? -eq 0 ]; then
    echo "Compilación exitosa. El archivo PDF está listo."
else
    echo "Error durante la compilación. Revisa el archivo de log."
fi

# Eliminar archivos temporales
echo "Limpiando archivos temporales..."
rm -f $TEX_FILE.aux $TEX_FILE.bbl $TEX_FILE.blg $TEX_FILE.log $TEX_FILE.out

echo "Proceso completado."

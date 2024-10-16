cd ../../memoria

# Preaparar la ejecución del script
rm main.pdf

# Crear el pdf
pdflatex main.tex 
rm main.aux main.log main.toc main.out
open main.pdf


.PHONY: main clean FORCE

main: poster.pdf

poster.pdf: FORCE
	latexmk -pdflatex='xelatex -interaction nonstopmode' -pdf poster.tex

clean:
	latexmk -pdf -C

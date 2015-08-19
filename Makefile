# Makefile for Sphinx documentation
# Modified to include examples/* and tutorial/* files from rstdocs to build/html
#

# You can set these variables from the command line.
SPHINXOPTS    = -q
SPHINXBUILD   = sphinx-build

INDIR	      = rstdocs
HTMLDIR	      = .

# Internal variables.
ALLSPHINXOPTS   = -d build/doctrees $(SPHINXOPTS) $(INDIR)

.PHONY: help clean html web pickle htmlhelp latex changes linkcheck

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  latex     to make LaTeX files"
	@echo "  changes   to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"

rstdocs/conf.py.txt: rstdocs/conf.py
	python3 src/pylit.py rstdocs/conf.py

rstdocs/examples/setup.py.txt: src/setup.py
	python3 src/pylit.py src/setup.py rstdocs/examples/setup.py.txt

rstdocs/examples/pylit.py.txt: src/pylit.py
	python3 src/pylit.py src/pylit.py rstdocs/examples/pylit.py.txt

rstdocs/examples/pylit_test.py.txt: test/pylit_test.py
	python3 src/pylit.py --comment-string='## ' test/pylit_test.py rstdocs/examples/pylit_test.py.txt

rstdocs/tutorial/hello.py.txt: rstdocs/tutorial/hello.py
	python3 src/pylit.py rstdocs/tutorial/hello.py

rstdocs/tutorial/hello_2.py: rstdocs/tutorial/hello_2.py.txt
	python3 src/pylit.py rstdocs/tutorial/hello_2.py.txt

rstdocs/tutorial/hello_with_header.py: rstdocs/tutorial/hello_with_header.py.txt
	python3 src/pylit.py rstdocs/tutorial/hello_with_header.py.txt

rstdocs/tutorial/hello_with_doctest.py.txt: rstdocs/tutorial/hello_with_doctest.py
	python3 src/pylit.py --doctest rstdocs/tutorial/hello_with_doctest.py
	python3 src/pylit.py rstdocs/tutorial/hello_with_doctest.py

rstdocs/tutorial/hello_with_doctest_2.py.txt: rstdocs/tutorial/hello_with_doctest_2.py
	python3 src/pylit.py --doctest rstdocs/tutorial/hello_with_doctest_2.py
	python3 src/pylit.py rstdocs/tutorial/hello_with_doctest_2.py

rstdocs/tutorial/greeting.py.txt: rstdocs/tutorial/greeting.py
	python3 src/pylit.py rstdocs/tutorial/greeting.py

rstdocs/tutorial/hello_multifile.py.txt: rstdocs/tutorial/hello_multifile.py rstdocs/tutorial/greeting.py.txt
	python3 src/pylit.py rstdocs/tutorial/hello_multifile.py

rstdocs/examples/simplestates.py: rstdocs/examples/simplestates.py.txt
	python3 src/pylit.py rstdocs/examples/simplestates.py.txt

rstdocs/examples/simplestates_test.py: rstdocs/examples/simplestates_test.py.txt
	python3 src/pylit.py rstdocs/examples/simplestates_test.py.txt
	(cd rstdocs/examples; python3 simplestates_test.py)

rstdocs/examples/iterqueue.py: rstdocs/examples/iterqueue.py.txt
	python3 src/pylit.py rstdocs/examples/iterqueue.py.txt
	(cd rstdocs/examples; python3 ../../src/pylit.py --doctest iterqueue.py.txt)

rstdocs/examples/iterqueue_test.py: rstdocs/examples/iterqueue_test.py.txt
	python3 src/pylit.py rstdocs/examples/iterqueue_test.py.txt
	(cd rstdocs/examples; python3 iterqueue_test.py)

rstdocs/examples/iterqueue_speed_test.py: rstdocs/examples/iterqueue_speed_test.py.txt
	python3 src/pylit.py rstdocs/examples/iterqueue_speed_test.py.txt
	(cd rstdocs/examples; python3 iterqueue_speed_test.py)

rstdocs/examples/testfile_literate.py: rstdocs/examples/testfile_literate.py.txt
	python3 src/pylit.py rstdocs/examples/testfile_literate.py.txt
	(cd rstdocs/examples; python3 -m doctest -v testfile_literate.py.txt )

rstdocs/examples/testmod_literate.py: rstdocs/examples/testmod_literate.py.txt
	python3 src/pylit.py rstdocs/examples/testmod_literate.py.txt
	(cd rstdocs/examples; PYTHONPATH=../../src python3 testmod_literate.py )

OTHERS = rstdocs/conf.py.txt \
	rstdocs/examples/pylit.py.txt \
	rstdocs/examples/setup.py.txt \
	rstdocs/examples/pylit_test.py.txt \
	rstdocs/examples/simplestates.py \
	rstdocs/examples/simplestates_test.py \
	rstdocs/examples/iterqueue.py \
	rstdocs/examples/iterqueue_test.py \
	rstdocs/examples/iterqueue_speed_test.py \
	rstdocs/examples/testfile_literate.py \
	rstdocs/examples/testmod_literate.py \
	rstdocs/tutorial/hello.py.txt \
	rstdocs/tutorial/hello_2.py \
	rstdocs/tutorial/hello_with_header.py \
	rstdocs/tutorial/hello_with_doctest.py.txt \
	rstdocs/tutorial/hello_with_doctest_2.py.txt \
	rstdocs/tutorial/greeting.py.txt \
	rstdocs/tutorial/hello_multifile.py.txt

clean:
	-rm -rf build/*

html: $(OTHERS)
	mkdir -p $(HTMLDIR) build/doctrees
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(HTMLDIR)
	@echo
	@echo "Copying some source files"
	cp $(INDIR)/download/pylit $(HTMLDIR)/download/
	cp $(INDIR)/examples/*.txt $(HTMLDIR)/examples/
	cp $(INDIR)/tutorial/*.py  $(HTMLDIR)/tutorial/
	cp $(INDIR)/tutorial/*.py.txt $(HTMLDIR)/tutorial/
	# cp $(INDIR)/examples/*.py  $(HTMLDIR)/examples/
	# cp $(INDIR)/examples/*.sty $(HTMLDIR)/examples/
	# cp $(INDIR)/examples/*.css $(HTMLDIR)/examples/

	@echo
	@echo "Build finished: HTML pages are in $(HTMLDIR)"

pickle: $(OTHERS)
	mkdir -p build/pickle build/doctrees
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) build/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

web: pickle

json: $(OTHERS)
	mkdir -p build/json build/doctrees
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) build/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	mkdir -p build/htmlhelp build/doctrees
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) build/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in build/htmlhelp."

latex: $(OTHERS)
	mkdir -p build/latex build/doctrees
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) build/latex
	@echo
	@echo "Build finished; the LaTeX files are in build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes: $(OTHERS)
	mkdir -p build/changes build/doctrees
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) build/changes
	@echo
	@echo "The overview file is in build/changes."

linkcheck:
	mkdir -p build/linkcheck build/doctrees
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in build/linkcheck/output.txt."

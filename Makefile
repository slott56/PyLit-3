# Makefile for Sphinx documentation
# Modified to include examples/* and tutorial/* files from docs to _build/html
#

# You can set these variables from the command line.
SPHINXOPTS    = -q
SPHINXBUILD   = sphinx-build

INDIR	      = docs
HTMLDIR	      = _build/html

# Internal variables.
ALLSPHINXOPTS   = -d _build/doctrees $(SPHINXOPTS) $(INDIR)

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

docs/conf.py.txt: docs/conf.py
	python3 src/pylit.py docs/conf.py

docs/examples/setup.py.txt: setup.py
	python3 src/pylit.py setup.py docs/examples/setup.py.txt

docs/examples/pylit.py.txt: src/pylit.py
	python3 src/pylit.py src/pylit.py docs/examples/pylit.py.txt

docs/examples/pylit_test.py.txt: test/pylit_test.py
	python3 src/pylit.py --comment-string='## ' test/pylit_test.py docs/examples/pylit_test.py.txt

docs/tutorial/hello.py.txt: docs/tutorial/hello.py
	python3 src/pylit.py docs/tutorial/hello.py

docs/tutorial/hello_2.py: docs/tutorial/hello_2.py.txt
	python3 src/pylit.py docs/tutorial/hello_2.py.txt

docs/tutorial/hello_with_header.py: docs/tutorial/hello_with_header.py.txt
	python3 src/pylit.py docs/tutorial/hello_with_header.py.txt

docs/tutorial/hello_with_doctest.py.txt: docs/tutorial/hello_with_doctest.py
	python3 src/pylit.py --doctest docs/tutorial/hello_with_doctest.py
	python3 src/pylit.py docs/tutorial/hello_with_doctest.py

docs/tutorial/hello_with_doctest_2.py.txt: docs/tutorial/hello_with_doctest_2.py
	python3 src/pylit.py --doctest docs/tutorial/hello_with_doctest_2.py
	python3 src/pylit.py docs/tutorial/hello_with_doctest_2.py

docs/tutorial/greeting.py.txt: docs/tutorial/greeting.py
	python3 src/pylit.py docs/tutorial/greeting.py

docs/tutorial/hello_multifile.py.txt: docs/tutorial/hello_multifile.py docs/tutorial/greeting.py.txt
	python3 src/pylit.py docs/tutorial/hello_multifile.py

docs/examples/simplestates.py: docs/examples/simplestates.py.txt
	python3 src/pylit.py docs/examples/simplestates.py.txt

docs/examples/simplestates_test.py: docs/examples/simplestates_test.py.txt
	python3 src/pylit.py docs/examples/simplestates_test.py.txt
	(cd docs/examples; python3 simplestates_test.py)

docs/examples/iterqueue.py: docs/examples/iterqueue.py.txt
	python3 src/pylit.py docs/examples/iterqueue.py.txt
	(cd docs/examples; python3 ../../src/pylit.py --doctest iterqueue.py.txt)

docs/examples/iterqueue_test.py: docs/examples/iterqueue_test.py.txt
	python3 src/pylit.py docs/examples/iterqueue_test.py.txt
	(cd docs/examples; python3 iterqueue_test.py)

docs/examples/iterqueue_speed_test.py: docs/examples/iterqueue_speed_test.py.txt
	python3 src/pylit.py docs/examples/iterqueue_speed_test.py.txt
	(cd docs/examples; python3 iterqueue_speed_test.py)

docs/examples/testfile_literate.py: docs/examples/testfile_literate.py.txt
	python3 src/pylit.py docs/examples/testfile_literate.py.txt
	(cd docs/examples; python3 -m doctest -v testfile_literate.py.txt )

docs/examples/testmod_literate.py: docs/examples/testmod_literate.py.txt
	python3 src/pylit.py docs/examples/testmod_literate.py.txt
	(cd docs/examples; PYTHONPATH=../../src python3 testmod_literate.py )

OTHERS = docs/conf.py.txt \
	docs/examples/pylit.py.txt \
	docs/examples/setup.py.txt \
	docs/examples/pylit_test.py.txt \
	docs/examples/simplestates.py \
	docs/examples/simplestates_test.py \
	docs/examples/iterqueue.py \
	docs/examples/iterqueue_test.py \
	docs/examples/iterqueue_speed_test.py \
	docs/examples/testfile_literate.py \
	docs/examples/testmod_literate.py \
	docs/tutorial/hello.py.txt \
	docs/tutorial/hello_2.py \
	docs/tutorial/hello_with_header.py \
	docs/tutorial/hello_with_doctest.py.txt \
	docs/tutorial/hello_with_doctest_2.py.txt \
	docs/tutorial/greeting.py.txt \
	docs/tutorial/hello_multifile.py.txt

clean:
	-rm -rf _build/*

html: $(OTHERS)
	mkdir -p $(HTMLDIR) _build/doctrees
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
	mkdir -p _build/pickle _build/doctrees
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) _build/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

web: pickle

json: $(OTHERS)
	mkdir -p _build/json _build/doctrees
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) _build/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	mkdir -p _build/htmlhelp _build/doctrees
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) _build/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in _build/htmlhelp."

latex: $(OTHERS)
	mkdir -p _build/latex _build/doctrees
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) _build/latex
	@echo
	@echo "Build finished; the LaTeX files are in _build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes: $(OTHERS)
	mkdir -p _build/changes _build/doctrees
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) _build/changes
	@echo
	@echo "The overview file is in _build/changes."

linkcheck:
	mkdir -p _build/linkcheck _build/doctrees
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) _build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in _build/linkcheck/output.txt."

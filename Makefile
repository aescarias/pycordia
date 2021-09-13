generate_docs:
	echo "Generating Docs"
	cd pycordia && pdoc --html --force --config show_source_code=False --output-dir ../docs .

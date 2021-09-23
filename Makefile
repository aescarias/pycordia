generate_docs:
	echo "Generating Docs"
	cd docs && sphinx-apidoc -f -o source/ --module-first ../pycordia
	cd docs && make html

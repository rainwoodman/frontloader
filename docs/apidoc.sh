# bash

# Run this script to generate the automatic apidoc pages

if ! python -c 'import numpydoc'; then easy_install --user numpydoc; fi
if ! python -c 'import sphinx'; then easy_install --user sphinx; fi

sphinx-apidoc -H "API Reference" -M -e -f -o . ../frontloader 

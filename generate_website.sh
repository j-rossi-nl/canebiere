#!/bin/bash

poetry run jupyter nbconvert --execute --no-input --to html generate_page.ipynb --output index  
poetry run jupyter nbconvert --execute --no-input --to html generate_academies.ipynb --output academies  
poetry run jupyter nbconvert --execute --no-input --to html generate_notes.ipynb --output notes  
poetry run jupyter nbconvert --execute --no-input --to html generate_opponents.ipynb --output opponents  
poetry run jupyter nbconvert --execute --no-input --to html generate_words.ipynb --output words  

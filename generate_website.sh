#!/bin/bash

poetry run jupyter nbconvert --execute --no-input --to html generate_page.ipynb --output index  
poetry run jupyter nbconvert --execute --no-input --to html generate_academies.ipynb --output academies  
poetry run jupyter nbconvert --execute --no-input --to html generate_notes.ipynb --output notes  
poetry run jupyter nbconvert --execute --no-input --to html generate_opponents.ipynb --output opponents  
poetry run jupyter nbconvert --execute --no-input --to html generate_words.ipynb --output words  
poetry run jupyter nbconvert --execute --no-input --to html generate_2021_2022.ipynb --output 2021_2022  
poetry run jupyter nbconvert --execute --no-input --to html generate_2022_2023.ipynb --output 2022_2023  
poetry run jupyter nbconvert --execute --no-input --to html generate_2023_2024.ipynb --output 2023_2024  
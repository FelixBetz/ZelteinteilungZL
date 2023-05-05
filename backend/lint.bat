@echo off
::python -m pylint --recursive=y  main maps participant person tent_leader file_indices config helpers mailing
python -m   pylint --recursive=y app.py src/ file_indices pathes 
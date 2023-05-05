@echo off
::python -m pylint --recursive=y  main maps participant person tent_leader file_indices config helpers mailing
python -m   pylint --recursive=y main.py maps participants/ person tent_leaders/ file_indices config helpers mailing pathes
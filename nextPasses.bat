@echo off
set min_el=30
set num_passes=25
nextPasses.py -e %min_el% -n %num_passes% ISS nasabare.txt
nextPasses.py -e %min_el% -n %num_passes% "OSCAR 7 (AO-7)" amateur.txt
nextPasses.py -e %min_el% -n %num_passes% AO-27 nasabare.txt
nextPasses.py -e %min_el% -n %num_passes% AO-73 nasabare.txt
nextPasses.py -e %min_el% -n %num_passes% AO-91 nasabare.txt
nextPasses.py -e %min_el% -n %num_passes% AO-92  nasabare.txt

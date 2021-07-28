NVIS=100
ARCMIN=1.0
view:
	python3 view_casacore.py --ms test_data/1557347448_J1939_6342_XXscan1chan950to1050.ms --arcmin ${ARCMIN} --nvis ${NVIS}

view_dask:
	python3 view_data.py --ms test_data/1557347448_J1939_6342_XXscan1chan950to1050.ms

	
# Pip install disko
disko:
	disko --ms test_data/1557347448_J1939_6342_XXscan1chan950to1050.ms --tikhonov --SVG --display --fov 2.0 --arcmin 1
	
	
install:
	sudo pip3 install disko dask-ms --upgrade

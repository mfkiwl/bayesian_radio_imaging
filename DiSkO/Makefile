all: TART Cygnus

install:
	sudo pip3 install DiSkO --upgrade
	
TART:
	disko_bayes --fov 155 --ms ../test_data/test.ms  --mu --pcf --var --PNG --arcmin=90  --dir test_out --title 'bayes_tart' --sigma-v=0.15 --posterior post.h5

Cygnus:
	disko_bayes --fov 0.05 --ms ../test_data/cyg2052.ms --SVG --mu --pcf --var --dir test_out --arcmin 0.05 --nvis 500 --title 'cygnus'

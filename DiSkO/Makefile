all: TART cygnus

install:
	sudo pip3 install DiSkO --upgrade
	
TART:
	disko_bayes --ms ../test_data/test.ms  --mu --pcf --var --PNG \
		--fov 155 --arcmin=90  \
		--sigma-v=0.15 --posterior post.h5 \
		--dir test_out --title 'bayes_tart' 

cygnus:
	disko_bayes --ms ../test_data/cyg2052.ms \
		--SVG --mu --pcf --var --nsamples 3 \
		--sigma-v 10.0 \
		--fov 0.05  --arcmin 0.03 --nvis 1000 \
		--title 'cygnus' --dir test_out 

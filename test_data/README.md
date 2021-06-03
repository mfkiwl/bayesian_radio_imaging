# Test Data


## Meerkat Calibration Data

This is an observation targeting the ESO137 field. I split out scan 1 and 3 which are on the calibrator J1939-6342 (only one calibrator because the primary was close enough to the target). I don't have the source parameters for you right now but I'll look them up. If you want to get started, the MODEL_DATA column has been populated with what CASA thinks the model visibilities of the source should be. CORRECED_DATA has the inverse gain solutions applied to the raw data which resides in the DATA column. The WEIGHT_SPECTRUM column contains only ones at this stage. Initial flagging was done with tricolor so the FLAG column is populated but I used a fairly conservative flagging strategy so there will still be some low-level RFI in the data. I am busy trying to figure out how to also split the gain tables by scan. Once I have these I'll place the CASA solutions there for reference as well. I am also busy tidying up an old repo where I started implementing generic telescope and source models. 

wget -m ftp://elwood.ru.ac.za:/pub/bester/1557347448_J1939_6342_scan1and3.ms

    
## TART data

* field of view: Close to the full hemisphere. Typically 170 degrees should cover most of the flux
* The pixel size is 90 arcminutes over the full hemisphere. 
* The primary beam is 180 degrees of each antenna (in practice this is not true, and there is considerable structure in the beam pattern)
* The sources are mostly bright point sources corresponding to GPS and Galileo satellites, with the galactic plane present as a large diffuse source.
* The data are callibrated. The calibration is not great. I estimate 10 percent error in complex magnitude.
* All data are valid (flagging is not required)

## Cygnus Data

* The FoV is 0.05 degrees, with a pixel size of 0.03 arcmin


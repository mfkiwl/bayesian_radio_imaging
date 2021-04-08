# Test Data

There are two bits. One from the VLA [Rick Perley 2 GHz of the Cygnus A radio galaxy. The other is an all-sky image from the TART telescope.

To get the cygnus data type

    make
    
    
## TART data

* field of view: Close to the full hemisphere. Typically 170 degrees should cover most of the flux
* The pixel size is 90 arcminutes over the full hemisphere. 
* The primary beam is 180 degrees of each antenna (in practice this is not true, and there is considerable structure in the beam pattern)
* The sources are mostly bright point sources corresponding to GPS and Galileo satellites, with the galactic plane present as a large diffuse source.
* The data are callibrated. The calibration is not great. I estimate 10 percent error in complex magnitude.
* All data are valid (flagging is not required)

## Cygnus Data



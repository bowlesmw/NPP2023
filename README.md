# NPP2023
This repository contains a python script used to determine net primary productivity rates according to the VGPM model of Behrenfeld and Falkowski (1997). For all input parameters we used the monthly 4km resolution OB.DAAC level 3 data (https://oceancolor.gsfc.nasa.gov/l3/). For chlorophyll a and PAR the reprocessing version R2022.0 was used and R2019.0 for SST. The day length parameter is given in the zipped folder 'day_light_monthly.zip' and contains 12 '.nc' with day length in hours (United States Naval Observatory, 1990). The code was successfully ran on Python (3.9.18) wherein we first filtered values outside of the file-specific maximum and minimum values. 




Behrenfeld, M. J. & Falkowski, P. G. Photosynthetic rates derived from satellite‐based chlorophyll concentration. Limnol. Oceanogr. 42, 1–20 (1997).

United States Naval Observatory, Almanac for computers. HathiTrust https://hdl.handle.net/2027/uiug.30112059294311?urlappend=%3Bseq=3. (1990). 


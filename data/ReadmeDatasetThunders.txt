-------------------------READ THIS FIRST!-------------------------
The STARNET Lightning detection network is run by the University of São Paulo, Brazil,
at Laboratório de Sensoriamento Remoto de Tempestades STORM-T, Department of Atmospheric Sciences, IAG
 
For more information about the data and the network check http://www.zeus.iag.usp.br.
 
If you use this data, we ask that you acknowledge us in your use of the data and cite:
 
    MORALES, C.A.; NEVES. J.R; ANSELMO. E.M.; SFERICS TIMING AND RANGING NETWORK - STARNET: EVALUATION OVER SOUTH AMERICA 
    - In: XIV International Conference on Atmospheric Electricity, August 08-12, 2011, Rio de Janeiro, Brazil
 
Any question, e-mail: morales@model.iag.usp.br
------------------------------------------------------------------------
 
Bellow is the information of the data columns.
 
The STARNET data set gathers the following information by columns:
 
Collumn  1: Year
Collumn  2: Month
Collumn  3: Day
Collumn  4: Hour (UTC)
Collumn  5: Minute
Collumn  6: Second
Collumn  7: Millisecond
Collumn  8: Latitude
Collumn  9: Longitude
Collumn 10: Major ellipse error of the ATD solution (in meters)
Collumn 11: ATD error in microseconds
Collumn 12: Quality control (0,1,2). See bellow.
Collumn 13: Polarity (0,1,2,3) (+-). See bellow.
Collumn 14: Number of Rx employed in the Solution (4,5,6,7)
Collumn 15: Number of ATD pairs employed in the Solution (6-21)
Collumn 16: RX 1  - (Not employed)
Collumn 17: RX 2  - (Not employed)
Collumn 18: RX 3  - (Not employed)
Collumn 19: RX 4  - (Not employed)
Collumn 20: RX 5  - Universidade de São Paulo                   - São Paulo             , SP, Brasil         - latitude: -23.559352 , longitude: -46.73334  - Since 29/10/2010
Collumn 21: RX 6  - Sede INMET                                  - Brasilia              , DF, Brasil         - latitude: -15.78903  , longitude: -47.92334  - Since 24/09/2009
Collumn 22: RX 7  - UFAM, Setor de Avicultura                   - Manaus                , AM, Brasil         - latitude:  -3.10339  , longitude: -59.98055  - Since 27/05/2009
Collumn 23: RX 8  - SIPAM ,Centro Regional de Belém (CR/BE)     - Belém                 , PA, Brasil         - latitude:  -1.40945  , longitude: -48.46286  - Since 24/08/2012
Collumn 24: RX 9  - (Not employed)
Collumn 25: RX 10 - UFMS, Departamento de Veterinária           - Campo Grande          , MS, Brasil         - latitude:  -20.51021 , longitude: -54.61942 
Collumn 26: RX 11 - OES/CRS-INPE                                - São Martinho da Serra , RS, Brasil         - latitude:  -29.44213 , longitude: -53.82161
Collumn 27: RX 12 - CIRAD - Antilles-Guyane                     - Point-à-Pitre         , Guadaloupe, France - latitude:   16.18177 , longitude: -61.59016
Collumn 28: RX 13 - UECE, Campus do Itaperi                     - Fortaleza             , CE, Brasil         - latitude:   -3.79456 , longitude: -38.55699
Collumn 29: RX 14 - LIM, CPTEC/INPE                             - Cachoeira Paulista    , SP, Brasil         - latitude:  -22.68905 , longitude: -45.00597
 
 
Major ellipse error: It represent the major axis of the ellipse error that 
             circumscribes the ATDs. The lower the value, better the
             solution. (This error is still under analyses, so don't
             take too much in consideration, use the ATD error
             instead).
ATD error: It represents the Residual Error of the ATD solution. The values
       lower than 20 micro-seconds are considered acceptable, and it is
       expected to have low location errors according to the theoretical
       model.
Quality control: It a simplification of the ATD error/Major Axis that is 
       used to diagnose the location accuracy: 0-Good; 1-Questionable;
       2-Bad
Polariy: It is the retrieved ELF polarity (+ or -), where the values represent
           confidence level (1-low; 2-median; 3-high) and 0 no confidence. 
################################################################################
VERY IMPORTANT: The data from before 2007-11 does not contain Polarity information.
So adjust your program to not read this column in the 2006 and 2007 data.
################################################################################
 
Number of Rx: It tells how many receivers were employed in the solution
Number of ATDs: It tell how many ATDs were used in the solution. If we had
       4 rx, we have a maximum of 6 ATDs (combination of 4, 2 a 2); 5 rx
       have 10 ATDs, 6 rx have 15 ATDs and 7 rx have 21 ATDs. The ATDs
       employed in the solution passed a quality control, and if it does
       not pass, it is not used.  So, you might have some solutions that
       did not used the maximum number of ATDs according to the number of
       rx available
The Collumns (16-29) indicate which receivers were available (1) or not (o).
        
In the STARNET data example (the first 3 below) we have the following information:
 
    Sferics observed on October 12th 2008, at 23:00:02.649726 located at 
    latitude=-4.37723 and lontitude=-72.91611, with an estimated major axis error=7.112 km
    with an ATD error of 16.0 us, quality good, 4 rxs avaible and 6 ATDs were
    employed. The Rx Sao Martinho, Campo Grande, Guadloupe and Sao Paulo were available.
 
2008  10 12 23  0  2 649726   -4.37723  -72.91611     7112  16.0  0 -3  4  6 0 0 0 0 0 0 0 0 0 1 1 1 0 1
2008  10 12 23  0  4  23439   -4.18725  -72.13458     3642  15.6  0  3  5 10 0 0 0 0 0 0 0 0 0 1 1 1 1 1
2008  10 12 23  0  5 782687   -7.55228  -75.02688     7289  16.4  0  0  4  6 0 0 0 0 0 0 0 0 0 1 1 1 0 1
 
The FORTRAN format to read the data is:
 
    n_receiver_STARNET=14
 
    read(40,200)year,month,day,hour,minuto,second,milisecond,
     1           ,lat,lon,major_ellipse,
     1           userEr,qual,Pol,nRx,nPr,
     1           (id_rx(i),i=1,n_receiver_STARNET)
 
 
200 format(I4,1x,5I3,1x,I6,2f11.5,I9,f6.1,4i3,14i2)
 
For months before 2007-11 the data have the following format:
 
2007  10 31 23 59 34 891119   -4.96377  -65.34975     3949  14.9  0  4  6 0 0 0 0 0 0 0 0 0 1 0 1 1 1
2007  10 31 23 59 46 126149  -66.02706  156.07356    11196   7.8  0  4  6 0 0 0 0 0 0 0 0 1 1 0 0 1 1
2007  10 31 23 59 53 728414  -50.49265  -51.48805     5335   0.9  0  4  6 0 0 0 0 0 0 0 0 1 1 0 0 1 1
 
The FORTRAN format to read the data is:
 
    n_receiver_STARNET=14
 
    read(40,200)year,month,day,hour,minuto,second,milisecond,
     1           ,lat,lon,major_ellipse,
     1           userEr,qual,nRx,nPr,
     1           (id_rx(i),i=1,n_receiver_STARNET)
 
 
200 format(I4,1x,5I3,1x,I6,2f11.5,I9,f6.1,3i3,14i2)
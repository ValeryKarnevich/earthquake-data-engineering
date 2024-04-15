# Dataset Description

This is a brief overview of the contents of the columns in the [USGS Earthquake Catalog](https://earthquake.usgs.gov/fdsnws/event/1/) data in `.csv` format. Full detailed description can be found at:
https://earthquake.usgs.gov/data/comcat/index.php

#
An earthquake begins to rupture at a hypocenter which is defined by a position on the surface of the earth (epicenter) and a depth below this point (focal depth). The coordinates of the epicenter are provided in units of latitude and longitude. 

## 1. `time`
Time when the event occurred.

## 2. `latitude`
Decimal degrees latitude. Negative values for southern latitudes.

## 3. `longitude`
Decimal degrees longitude. Negative values for western longitudes.

## 4. `depth`
The depth where the earthquake begins to rupture in kilometers. 

## 5. `mag`
The magnitude for the event. 

Earthquake magnitude is a measure of the size of an earthquake at its source. It is a logarithmic measure. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake. The total amount of energy released by the earthquake usually goes up by a larger factor: for many commonly used magnitude types, the total energy of an average earthquake goes up by a factor of approximately 32 for each unit increase in magnitude.

## 6. `magType`
The method or algorithm used to calculate the preferred magnitude for the event. For more info, see:
https://www.usgs.gov/programs/earthquake-hazards/magnitude-types

## 7. `nst`
The total number of seismic stations used to determine earthquake location.

## 8. `gap`
The largest azimuthal gap between azimuthally adjacent stations (in degrees). In general, the smaller this number, the more reliable is the calculated horizontal position of the earthquake. Earthquake locations in which the azimuthal gap exceeds 180 degrees typically have large location and depth uncertainties.

## 9. `dmin`
Horizontal distance from the epicenter to the nearest station (in degrees). 1 degree is approximately 111.2 kilometers. In general, the smaller this number, the more reliable is the calculated depth of the earthquake.

## 10. `rms`
The root-mean-square (RMS) travel time residual, in sec, using all weights. This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location. Smaller numbers reflect a better fit of the data. The value is dependent on the accuracy of the velocity model used to compute the earthquake location, the quality weights assigned to the arrival time data, and the procedure used to locate the earthquake.

## 11. `net`
The ID of a data contributor. Identifies the network considered to be the preferred source of information for this event.

## 12. `id`
A unique identifier for the event.

## 13. `updated`
Time when the event was most recently updated. 

## 14. `place`
Textual description of named geographic region near to the event.

## 15. `type`
Type of seismic event: “earthquake” or “quarry”.

## 16. `locationSource`
The network that originally authored the reported location of this event.

## 17. `magSource`
Network that originally authored the reported magnitude for this event.

## 18. `horizontalError`
Uncertainty of reported location of the event in kilometers.

## 19. `depthError`
Uncertainty of reported depth of the event in kilometers.

## 20. `magError`
Uncertainty of reported magnitude of the event. The estimated standard error of the magnitude. The uncertainty corresponds to the specific magnitude type being reported and does not take into account magnitude variations and biases between different magnitude scales.

## 21. `magNst`
The total number of seismic stations used to calculate the magnitude for this earthquake.

## 22. `status`
Indicates whether the event has been reviewed by a human. Status is either automatic or reviewed. Automatic events are directly posted by automatic processing systems and have not been verified or altered by a human. Reviewed events have been looked at by a human. The level of review can range from a quick validity check to a careful reanalysis of the event.


import pandas as pd
import numpy as np
from astropy.visualization import astropy_mpl_style, quantity_support
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import matplotlib.pyplot as plt
from astropy.coordinates import get_moon
astropy_mpl_style['axes.grid'] = False
from astroplan import FixedTarget
plt.style.use(astropy_mpl_style)
quantity_support()
import datetimeselect
import matplotlib.pyplot as plt



def starmap(y, m, d, h, min, s):

    ystr = str(y)

    if (m < 10):
        mstr = str(m).zfill(2)
    else:
        mstr = str(m)

    if (d < 10):
        dstr = str(d).zfill(2)
    else:
        dstr = str(d)

    if (h < 10):
        hstr = str(h).zfill(2)
    else:
        hstr = str(h)

    if (min < 10):
        minstr = str(min).zfill(2)
    else:
        minstr = str(min)

    if (s < 10):
        sstr = str(s).zfill(2)
    else:
        sstr = str(s)



    #Displaying data
    data = pd.read_csv("landolt_north.csv", delimiter = "|")

    #Position of the Bath Physics Observatory - You can change this to wherever you are!
    #Units: Lat. (°), Long. (°), Elevation (m)

    latitude = 51.37283*u.deg
    longitude = -2.319209*u.deg
    elevation = 190.0*u.m


    # Set location
    bath = EarthLocation(lat = latitude, lon = longitude, height = elevation)

    # Input time year-month-day - whenever you are making (or plan on making) observations!
    time_str = str('{}-{}-{} {}:{}:{}'.format(ystr, mstr, dstr, hstr, minstr, sstr))
    time = Time('{}-{}-{} {}:{}:{}'.format(y, m, d, h, min, s))

    # Find information about the two variable stars - RZ Ceph and RV UMa
    #RZ Ceph first:
    v1 = SkyCoord('22h40m0.51s', '+64d58m45.0s', frame = 'icrs')
    #Transform coordinates
    caltaz = v1.transform_to(AltAz(obstime=time,location=bath))
    rzCepAlt = float(caltaz.altaz.alt.deg)
    rzCepAz = float(caltaz.altaz.az.deg)



    # RV UMa:
    v2 = SkyCoord('13h34m12.58s', '+53d52m7.9s') #From SIMBAD star catalogue
    # Transform coordinates
    daltaz = v2.transform_to(AltAz(obstime=time,location=bath))
    rvUMaAlt = daltaz.altaz.alt.deg
    rvUMaAz = daltaz.altaz.az.deg



    # RZ Cas:
    v3 = SkyCoord('02h48m55.5s', '+69d38m03.4s') #From SIMBAD star catalogue
    # Transform coordinates
    ealtaz = v3.transform_to(AltAz(obstime=time,location=bath))
    rzCasAlt = ealtaz.altaz.alt.deg
    rzCasAz = ealtaz.altaz.az.deg

    #Removing whitespace from column heads - was formatted weirdly
    data.columns = data.columns.str.strip()

    # Converting from ra and dec to alt and az at specific time and location
    AltAzdegrees = SkyCoord(data['ra'], data['dec'], frame='icrs', unit='deg')
    a = AltAzdegrees.transform_to(AltAz(obstime=time, location=bath))
    b = a.to_string('decimal')
    data['AltAz'] = b

    # Add Az and Alt to data table for each of the standard stars
    data[['Az','Alt']] = data.AltAz.str.split(expand=True)

    #Adjusting data types for further manipulation
    data["Az"] = pd.to_numeric(data["Az"])
    data["Alt"] = pd.to_numeric(data["Alt"])

    #The 4 variables controls which stars are considered "visible" i.e. near to the variable star in question
    #They are just constraints on Alt/Az angles

    AzMinCeph = 300
    AzMaxCeph = 360
    AltMinCeph = 15
    AltMaxCeph = 35

    if (AltMinCeph < 0 or AzMinCeph < 0 or AzMaxCeph > 360 or AltMaxCeph > 90):
        print("Invalid angles. Printing full set of stars")
        AzMinCeph = 0
        AzMaxCeph = 360
        AltMinCeph = 0
        AltMaxCeph = 90



    visibleStars_ceph = data.loc[(data['Az'] >= AzMinCeph) & (data['Az'] <= AzMaxCeph) & (data['Alt'] >= AltMinCeph) & (data['Alt'] <= AltMaxCeph)]


    AzMinLy = 300
    AzMaxLy = 360
    AltMinLy = 15
    AltMaxLy = 35

    if (AltMinCeph < 0 or AzMinCeph < 0 or AzMaxCeph > 360 or AltMaxCeph > 90):
        print("Invalid angles. Printing full set of stars")
        AzMinLy = 0
        AzMaxLy = 360
        AltMinLy = 0
        AltMaxLy = 90

    visibleStars_lyrae = data.loc[(data['Az'] >= AzMinLy) & (data['Az'] <= AzMaxLy) & (data['Alt'] >= AltMinLy) & (data['Alt'] <= AltMaxLy)]


    xstandard = data['Az']
    ystandard = data['Alt']

    plt.plot(rzCepAz, rzCepAlt, marker="o", markersize=10, markeredgecolor="blue", markerfacecolor="white", label = "RZ Cep", linestyle = "None")
    plt.plot(rvUMaAz, rvUMaAlt, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="white", label = "RV UMa", linestyle = "None")
    plt.plot(rzCasAz, rzCasAlt, marker="o", markersize=10, markeredgecolor="green", markerfacecolor="white", label = "RZ Cas", linestyle = "None")


    plt.plot(xstandard, ystandard, marker = 'x', markersize=8, linestyle = "None", color = "black", label = "Nearby Standards")
    plt.xlabel("Azimuth °")
    plt.ylabel("Altitude °")
    plt.legend()
    #plt.savefig('visStars@{}.png'.format(time_str))
    plt.title('Map of variable stars and nearby standard stars at the BPO at \n {}'.format(time_str))
    plt.grid(color = 'grey', linestyle = '--')

    plt.show()



datetime = datetimeselect.select_date_and_time()

y = datetime[0]
m = datetime[1]
d = datetime[2]
h = datetime[3]
min = datetime[4]
s = datetime[5]

starmap(y, m, d, h, min, s)











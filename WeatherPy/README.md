
## Unit 6 | Assignment - What's the Weather Like?

## Background

Whether financial, political, or social -- data's true power lies in its ability to answer questions definitively. So let's take what you've learned about Python requests, APIs, and JSON traversals to answer a fundamental question: "What's the weather like as we approach the equator?"

Now, we know what you may be thinking: _"Duh. It gets hotter..."_ 

But, if pressed, how would you **prove** it? 


## WeatherPy

In this example, you'll be creating a Python script to visualize the weather of 500+ cities across the world of varying distance from the equator. To accomplish this, you'll be utilizing a [simple Python library](https://pypi.python.org/pypi/citipy), the [OpenWeatherMap API](https://openweathermap.org/api), and a little common sense to create a representative model of weather across world cities.

Your objective is to build a series of scatter plots to showcase the following relationships:

* Temperature (F) vs. Latitude
* Humidity (%) vs. Latitude
* Cloudiness (%) vs. Latitude
* Wind Speed (mph) vs. Latitude

Your final notebook must:

* Randomly select **at least** 500 unique (non-repeat) cities based on latitude and longitude.
* Perform a weather check on each of the cities using a series of successive API calls. 
* Include a print log of each city as it's being processed with the city number, city name, and requested URL.
* Save both a CSV of all data retrieved and png images for each scatter plot.

As final considerations:

* You must use the Matplotlib and Seaborn libraries.
* You must include a written description of three observable trends based on the data. 
* You must use proper labeling of your plots, including aspects like: Plot Titles (with date of analysis) and Axes Labels.
* You must include an exported markdown version of your Notebook called  `README.md` in your GitHub repository.  
* See [Example Solution](WeatherPy_Example.pdf) for a reference on expected format. 


```python
#dependencies
import random
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from config import *
import requests
from pprint import pprint
from citipy import citipy
import matplotlib as mpl
from matplotlib import rcParams
```


```python
#generate cities list
#longitude (-180,180), latitude (-90,90)
def city_gen(cities, countries):
    '''
    Returns a list of randomly generated lat, lng coordinates and closest city
    '''
    lat, lng = random.uniform(-90, 90), random.uniform(-180, 180)
    city = citipy.nearest_city(lat, lng)
    
    city_name = city.city_name.title()
    country = city.country_code.upper()
    
    if city_name in cities and country in countries:
        #print(f'Found duplicate: {city_name},{country}')
        city_marker = city_gen(cities, countries)[2]
    else:
        city_marker = city_name+','+country
        #print(f'returning {city_marker}')
    return [lat, lng, city_marker]
```


```python
#request current weather
# Save config information.
url = "http://api.openweathermap.org/data/2.5/weather?"
units = "imperial"

# Build partial query URL
query_url = f"{url}appid={api_key}&units={units}&q="

#set up number of cities to query
iterator = 1
number_of_cities = 500

#set up lists for storing results
lat = []
lng = []
temp = []
cities = []
countries = []
humidity = []
cloudiness = []
windspeed =[]

#set up text formatting
bold = "\033[1m"
reset = "\033[0;0m"

while iterator <= number_of_cities:
    print(bold + f'Requesting weather for city # {iterator}' + reset)
    #generate random city
    city_g = city_gen(cities, countries)
    
    r = requests.get(query_url + city_g[2])
    print(f'   requested URL: {r.url}')
    
    if r.status_code == 200:
        response = r.json()
        #pprint(response)
        try:
            city = response['name']
            country = response['sys']['country']
            #make sure city is unique
            if  city in cities and country in countries:
                print(f'   {city}, {country} has already been added, retrying with different city...\n')
            else:
                print('   recording weather for ' + bold + f'{city}, {country}' + reset + '\n')
                temp.append(response['main']['temp'])
                lat.append(response['coord']['lat'])
                lng.append(response['coord']['lon'])
                humidity.append(response['main']['humidity'])
                cloudiness.append(response['wind']['speed'])
                windspeed.append(response['clouds']['all'])
                cities.append(city)
                countries.append(country)
                iterator += 1
        except KeyError:
            print('Key is not found')
    elif r.status_code == 404:
        print('   city not found, retrying with different city... \n')
        
print(bold + f'Recorded weather for {len(cities)} cities.' + reset)
```

    [1mRequesting weather for city # 1[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kapaa,US
       recording weather for [1mKapaa, US[0;0m
    
    [1mRequesting weather for city # 2[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hasaki,JP
       recording weather for [1mHasaki, JP[0;0m
    
    [1mRequesting weather for city # 3[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bengkulu,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 3[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Attawapiskat,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 3[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hilo,US
       recording weather for [1mHilo, US[0;0m
    
    [1mRequesting weather for city # 4[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cherskiy,RU
       recording weather for [1mCherskiy, RU[0;0m
    
    [1mRequesting weather for city # 5[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 5[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Punta%20Arenas,CL
       recording weather for [1mPunta Arenas, CL[0;0m
    
    [1mRequesting weather for city # 6[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 6[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Souillac,MU
       recording weather for [1mSouillac, MU[0;0m
    
    [1mRequesting weather for city # 7[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Alfred,ZA
       recording weather for [1mPort Alfred, ZA[0;0m
    
    [1mRequesting weather for city # 8[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Henties%20Bay,NA
       recording weather for [1mHenties Bay, NA[0;0m
    
    [1mRequesting weather for city # 9[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Coquimbo,CL
       recording weather for [1mCoquimbo, CL[0;0m
    
    [1mRequesting weather for city # 10[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Versalles,CO
       recording weather for [1mVersalles, CO[0;0m
    
    [1mRequesting weather for city # 11[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cardston,CA
       recording weather for [1mCardston, CA[0;0m
    
    [1mRequesting weather for city # 12[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bluff,NZ
       recording weather for [1mBluff, NZ[0;0m
    
    [1mRequesting weather for city # 13[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kavieng,PG
       recording weather for [1mKavieng, PG[0;0m
    
    [1mRequesting weather for city # 14[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chokurdakh,RU
       recording weather for [1mChokurdakh, RU[0;0m
    
    [1mRequesting weather for city # 15[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ancud,CL
       recording weather for [1mAncud, CL[0;0m
    
    [1mRequesting weather for city # 16[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Doha,QA
       recording weather for [1mDoha, QA[0;0m
    
    [1mRequesting weather for city # 17[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hobart,AU
       recording weather for [1mHobart, AU[0;0m
    
    [1mRequesting weather for city # 18[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rikitea,PF
       recording weather for [1mRikitea, PF[0;0m
    
    [1mRequesting weather for city # 19[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kenai,US
       recording weather for [1mKenai, US[0;0m
    
    [1mRequesting weather for city # 20[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 20[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kouroussa,GN
       recording weather for [1mKouroussa, GN[0;0m
    
    [1mRequesting weather for city # 21[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lebu,CL
       recording weather for [1mLebu, CL[0;0m
    
    [1mRequesting weather for city # 22[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Havre-Saint-Pierre,CA
       recording weather for [1mHavre-Saint-Pierre, CA[0;0m
    
    [1mRequesting weather for city # 23[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=East%20London,ZA
       recording weather for [1mEast London, ZA[0;0m
    
    [1mRequesting weather for city # 24[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hami,CN
       recording weather for [1mHami, CN[0;0m
    
    [1mRequesting weather for city # 25[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yar-Sale,RU
       recording weather for [1mYar-Sale, RU[0;0m
    
    [1mRequesting weather for city # 26[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Qaanaaq,GL
       recording weather for [1mQaanaaq, GL[0;0m
    
    [1mRequesting weather for city # 27[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Carnarvon,AU
       recording weather for [1mCarnarvon, AU[0;0m
    
    [1mRequesting weather for city # 28[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tuatapere,NZ
       recording weather for [1mTuatapere, NZ[0;0m
    
    [1mRequesting weather for city # 29[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luxor,EG
       recording weather for [1mLuxor, EG[0;0m
    
    [1mRequesting weather for city # 30[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Novoagansk,RU
       recording weather for [1mNovoagansk, RU[0;0m
    
    [1mRequesting weather for city # 31[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Listvyanka,RU
       recording weather for [1mListvyanka, RU[0;0m
    
    [1mRequesting weather for city # 32[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 32[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Busselton,AU
       recording weather for [1mBusselton, AU[0;0m
    
    [1mRequesting weather for city # 33[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tiksi,RU
       recording weather for [1mTiksi, RU[0;0m
    
    [1mRequesting weather for city # 34[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grootfontein,NA
       recording weather for [1mGrootfontein, NA[0;0m
    
    [1mRequesting weather for city # 35[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lorengau,PG
       recording weather for [1mLorengau, PG[0;0m
    
    [1mRequesting weather for city # 36[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santo%20Augusto,BR
       recording weather for [1mSanto Augusto, BR[0;0m
    
    [1mRequesting weather for city # 37[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dikson,RU
       recording weather for [1mDikson, RU[0;0m
    
    [1mRequesting weather for city # 38[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dancheng,CN
       recording weather for [1mDancheng, CN[0;0m
    
    [1mRequesting weather for city # 39[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Attawapiskat,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 39[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Maraba,BR
       recording weather for [1mMaraba, BR[0;0m
    
    [1mRequesting weather for city # 40[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Faanui,PF
       recording weather for [1mFaanui, PF[0;0m
    
    [1mRequesting weather for city # 41[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ushuaia,AR
       recording weather for [1mUshuaia, AR[0;0m
    
    [1mRequesting weather for city # 42[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wahiawa,US
       recording weather for [1mWahiawa, US[0;0m
    
    [1mRequesting weather for city # 43[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Walvis%20Bay,NA
       recording weather for [1mWalvis Bay, NA[0;0m
    
    [1mRequesting weather for city # 44[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Savannah%20Bight,HN
       recording weather for [1mSavannah Bight, HN[0;0m
    
    [1mRequesting weather for city # 45[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Torbay,CA
       recording weather for [1mTorbay, CA[0;0m
    
    [1mRequesting weather for city # 46[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jamestown,SH
       recording weather for [1mJamestown, SH[0;0m
    
    [1mRequesting weather for city # 47[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Burgeo,CA
       recording weather for [1mBurgeo, CA[0;0m
    
    [1mRequesting weather for city # 48[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Abu%20Samrah,QA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 48[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Lincoln,AU
       recording weather for [1mPort Lincoln, AU[0;0m
    
    [1mRequesting weather for city # 49[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Visnes,NO
       recording weather for [1mVisnes, NO[0;0m
    
    [1mRequesting weather for city # 50[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Celle,DE
       recording weather for [1mCelle, DE[0;0m
    
    [1mRequesting weather for city # 51[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Albany,AU
       recording weather for [1mAlbany, AU[0;0m
    
    [1mRequesting weather for city # 52[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Terney,RU
       recording weather for [1mTerney, RU[0;0m
    
    [1mRequesting weather for city # 53[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barrow,US
       recording weather for [1mBarrow, US[0;0m
    
    [1mRequesting weather for city # 54[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Riberalta,BO
       recording weather for [1mRiberalta, BO[0;0m
    
    [1mRequesting weather for city # 55[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tianpeng,CN
       recording weather for [1mTianpeng, CN[0;0m
    
    [1mRequesting weather for city # 56[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Palmerston,AU
       recording weather for [1mPalmerston, AU[0;0m
    
    [1mRequesting weather for city # 57[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Longyearbyen,SJ
       recording weather for [1mLongyearbyen, SJ[0;0m
    
    [1mRequesting weather for city # 58[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Skiathos,GR
       recording weather for [1mSkiathos, GR[0;0m
    
    [1mRequesting weather for city # 59[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Soto%20La%20Marina,MX
       recording weather for [1mSoto la Marina, MX[0;0m
    
    [1mRequesting weather for city # 60[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Ayora,EC
       recording weather for [1mPuerto Ayora, EC[0;0m
    
    [1mRequesting weather for city # 61[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Envira,BR
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 61[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chimoio,MZ
       recording weather for [1mChimoio, MZ[0;0m
    
    [1mRequesting weather for city # 62[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 62[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cape%20Town,ZA
       recording weather for [1mCape Town, ZA[0;0m
    
    [1mRequesting weather for city # 63[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vulcan,CA
       recording weather for [1mVulcan, CA[0;0m
    
    [1mRequesting weather for city # 64[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kalabo,ZM
       recording weather for [1mKalabo, ZM[0;0m
    
    [1mRequesting weather for city # 65[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Maniitsoq,GL
       recording weather for [1mManiitsoq, GL[0;0m
    
    [1mRequesting weather for city # 66[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rakaia,NZ
       recording weather for [1mRakaia, NZ[0;0m
    
    [1mRequesting weather for city # 67[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kaliua,TZ
       recording weather for [1mKaliua, TZ[0;0m
    
    [1mRequesting weather for city # 68[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Macquarie,AU
       recording weather for [1mPort Macquarie, AU[0;0m
    
    [1mRequesting weather for city # 69[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Freeport,US
       recording weather for [1mFreeport, US[0;0m
    
    [1mRequesting weather for city # 70[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nagarote,NI
       recording weather for [1mNagarote, NI[0;0m
    
    [1mRequesting weather for city # 71[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mogadishu,SO
       recording weather for [1mMogadishu, SO[0;0m
    
    [1mRequesting weather for city # 72[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nikolskoye,RU
       recording weather for [1mNikolskoye, RU[0;0m
    
    [1mRequesting weather for city # 73[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Leshukonskoye,RU
       recording weather for [1mLeshukonskoye, RU[0;0m
    
    [1mRequesting weather for city # 74[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kahului,US
       recording weather for [1mKahului, US[0;0m
    
    [1mRequesting weather for city # 75[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Portland,AU
       recording weather for [1mPortland, AU[0;0m
    
    [1mRequesting weather for city # 76[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Isangel,VU
       recording weather for [1mIsangel, VU[0;0m
    
    [1mRequesting weather for city # 77[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Caraballeda,VE
       recording weather for [1mCaraballeda, VE[0;0m
    
    [1mRequesting weather for city # 78[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cockburn%20Town,TC
       recording weather for [1mCockburn Town, TC[0;0m
    
    [1mRequesting weather for city # 79[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atuona,PF
       recording weather for [1mAtuona, PF[0;0m
    
    [1mRequesting weather for city # 80[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yellowknife,CA
       recording weather for [1mYellowknife, CA[0;0m
    
    [1mRequesting weather for city # 81[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dicabisagan,PH
       recording weather for [1mDicabisagan, PH[0;0m
    
    [1mRequesting weather for city # 82[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Moradabad,IN
       recording weather for [1mMoradabad, IN[0;0m
    
    [1mRequesting weather for city # 83[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sechura,PE
       recording weather for [1mSechura, PE[0;0m
    
    [1mRequesting weather for city # 84[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Broken%20Hill,AU
       recording weather for [1mBroken Hill, AU[0;0m
    
    [1mRequesting weather for city # 85[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lodja,CD
       recording weather for [1mLodja, CD[0;0m
    
    [1mRequesting weather for city # 86[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Emba,KZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 86[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kaitangata,NZ
       recording weather for [1mKaitangata, NZ[0;0m
    
    [1mRequesting weather for city # 87[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 87[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bow%20Island,CA
       recording weather for [1mBow Island, CA[0;0m
    
    [1mRequesting weather for city # 88[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tottori,JP
       recording weather for [1mTottori, JP[0;0m
    
    [1mRequesting weather for city # 89[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tecoanapa,MX
       recording weather for [1mTecoanapa, MX[0;0m
    
    [1mRequesting weather for city # 90[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Uwajima,JP
       recording weather for [1mUwajima, JP[0;0m
    
    [1mRequesting weather for city # 91[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tuktoyaktuk,CA
       recording weather for [1mTuktoyaktuk, CA[0;0m
    
    [1mRequesting weather for city # 92[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 92[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Oranjemund,NA
       recording weather for [1mOranjemund, NA[0;0m
    
    [1mRequesting weather for city # 93[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Thompson,CA
       recording weather for [1mThompson, CA[0;0m
    
    [1mRequesting weather for city # 94[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barroualie,VC
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 94[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hay%20River,CA
       recording weather for [1mHay River, CA[0;0m
    
    [1mRequesting weather for city # 95[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint%20Anthony,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 95[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kodiak,US
       recording weather for [1mKodiak, US[0;0m
    
    [1mRequesting weather for city # 96[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mendahara,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 96[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Severo-Kurilsk,RU
       recording weather for [1mSevero-Kurilsk, RU[0;0m
    
    [1mRequesting weather for city # 97[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lompoc,US
       recording weather for [1mLompoc, US[0;0m
    
    [1mRequesting weather for city # 98[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=New%20Norfolk,AU
       recording weather for [1mNew Norfolk, AU[0;0m
    
    [1mRequesting weather for city # 99[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pisco,PE
       recording weather for [1mPisco, PE[0;0m
    
    [1mRequesting weather for city # 100[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Thinadhoo,MV
       recording weather for [1mThinadhoo, MV[0;0m
    
    [1mRequesting weather for city # 101[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Castro,CL
       recording weather for [1mCastro, CL[0;0m
    
    [1mRequesting weather for city # 102[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 102[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 102[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Te%20Anau,NZ
       recording weather for [1mTe Anau, NZ[0;0m
    
    [1mRequesting weather for city # 103[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Georgetown,SH
       recording weather for [1mGeorgetown, SH[0;0m
    
    [1mRequesting weather for city # 104[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ilhabela,BR
       recording weather for [1mIlhabela, BR[0;0m
    
    [1mRequesting weather for city # 105[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Namtsy,RU
       recording weather for [1mNamtsy, RU[0;0m
    
    [1mRequesting weather for city # 106[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Victoria,SC
       recording weather for [1mVictoria, SC[0;0m
    
    [1mRequesting weather for city # 107[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ahumada,MX
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 107[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Manokwari,ID
       recording weather for [1mManokwari, ID[0;0m
    
    [1mRequesting weather for city # 108[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Biak,ID
       recording weather for [1mBiak, ID[0;0m
    
    [1mRequesting weather for city # 109[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Huilong,CN
       recording weather for [1mHuilong, CN[0;0m
    
    [1mRequesting weather for city # 110[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       recording weather for [1mMar del Plata, AR[0;0m
    
    [1mRequesting weather for city # 111[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bredasdorp,ZA
       recording weather for [1mBredasdorp, ZA[0;0m
    
    [1mRequesting weather for city # 112[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=College,US
       recording weather for [1mCollege, US[0;0m
    
    [1mRequesting weather for city # 113[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Narsaq,GL
       recording weather for [1mNarsaq, GL[0;0m
    
    [1mRequesting weather for city # 114[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Binga,CD
       recording weather for [1mBinga, CD[0;0m
    
    [1mRequesting weather for city # 115[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 115[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cidreira,BR
       recording weather for [1mCidreira, BR[0;0m
    
    [1mRequesting weather for city # 116[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 116[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Umm%20Kaddadah,SD
       recording weather for [1mUmm Kaddadah, SD[0;0m
    
    [1mRequesting weather for city # 117[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mount%20Isa,AU
       recording weather for [1mMount Isa, AU[0;0m
    
    [1mRequesting weather for city # 118[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tema,GH
       recording weather for [1mTema, GH[0;0m
    
    [1mRequesting weather for city # 119[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ustye,RU
       recording weather for [1mUstye, RU[0;0m
    
    [1mRequesting weather for city # 120[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Patricio,MX
       recording weather for [1mSan Patricio, MX[0;0m
    
    [1mRequesting weather for city # 121[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Terrace%20Bay,CA
       recording weather for [1mTerrace Bay, CA[0;0m
    
    [1mRequesting weather for city # 122[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sao%20Joao%20Da%20Barra,BR
       recording weather for [1mSao Joao da Barra, BR[0;0m
    
    [1mRequesting weather for city # 123[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belmopan,BZ
       recording weather for [1mBelmopan, BZ[0;0m
    
    [1mRequesting weather for city # 124[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vagamo,NO
       recording weather for [1mVagamo, NO[0;0m
    
    [1mRequesting weather for city # 125[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kuhdasht,IR
       recording weather for [1mKuhdasht, IR[0;0m
    
    [1mRequesting weather for city # 126[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chuy,UY
       recording weather for [1mChuy, UY[0;0m
    
    [1mRequesting weather for city # 127[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Isiro,CD
       recording weather for [1mIsiro, CD[0;0m
    
    [1mRequesting weather for city # 128[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint-Philippe,RE
       recording weather for [1mSaint-Philippe, RE[0;0m
    
    [1mRequesting weather for city # 129[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hithadhoo,MV
       recording weather for [1mHithadhoo, MV[0;0m
    
    [1mRequesting weather for city # 130[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vaini,TO
       recording weather for [1mVaini, TO[0;0m
    
    [1mRequesting weather for city # 131[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Don%20Sak,TH
       recording weather for [1mDon Sak, TH[0;0m
    
    [1mRequesting weather for city # 132[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Scottsburgh,ZA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 132[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mafinga,TZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 132[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kruisfontein,ZA
       recording weather for [1mKruisfontein, ZA[0;0m
    
    [1mRequesting weather for city # 133[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rungata,KI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 133[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Palabuhanratu,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 133[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tubruq,LY
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 133[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mangai,CD
       recording weather for [1mMangai, CD[0;0m
    
    [1mRequesting weather for city # 134[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vagay,RU
       recording weather for [1mVagay, RU[0;0m
    
    [1mRequesting weather for city # 135[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 135[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Esperance,AU
       recording weather for [1mEsperance, AU[0;0m
    
    [1mRequesting weather for city # 136[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ndouci,CI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 136[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mayumba,GA
       recording weather for [1mMayumba, GA[0;0m
    
    [1mRequesting weather for city # 137[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Klaksvik,FO
       recording weather for [1mKlaksvik, FO[0;0m
    
    [1mRequesting weather for city # 138[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Quintin,MX
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 138[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Payo,PH
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 138[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taoudenni,ML
       recording weather for [1mTaoudenni, ML[0;0m
    
    [1mRequesting weather for city # 139[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rio%20Grande,BR
       recording weather for [1mRio Grande, BR[0;0m
    
    [1mRequesting weather for city # 140[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Great%20Falls,US
       recording weather for [1mGreat Falls, US[0;0m
    
    [1mRequesting weather for city # 141[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Morant%20Bay,JM
       recording weather for [1mMorant Bay, JM[0;0m
    
    [1mRequesting weather for city # 142[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yulara,AU
       recording weather for [1mYulara, AU[0;0m
    
    [1mRequesting weather for city # 143[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Korla,CN
       recording weather for [1mKorla, CN[0;0m
    
    [1mRequesting weather for city # 144[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Estelle,US
       recording weather for [1mEstelle, US[0;0m
    
    [1mRequesting weather for city # 145[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jiaozuo,CN
       recording weather for [1mJiaozuo, CN[0;0m
    
    [1mRequesting weather for city # 146[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 146[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Hedland,AU
       recording weather for [1mPort Hedland, AU[0;0m
    
    [1mRequesting weather for city # 147[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bambous%20Virieux,MU
       recording weather for [1mBambous Virieux, MU[0;0m
    
    [1mRequesting weather for city # 148[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 148[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       recording weather for [1mPonta do Sol, CV[0;0m
    
    [1mRequesting weather for city # 149[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cabo%20San%20Lucas,MX
       recording weather for [1mCabo San Lucas, MX[0;0m
    
    [1mRequesting weather for city # 150[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jalu,LY
       recording weather for [1mJalu, LY[0;0m
    
    [1mRequesting weather for city # 151[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bhanpuri,IN
       recording weather for [1mBhanpuri, IN[0;0m
    
    [1mRequesting weather for city # 152[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yatou,CN
       recording weather for [1mYatou, CN[0;0m
    
    [1mRequesting weather for city # 153[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cacoal,BR
       recording weather for [1mCacoal, BR[0;0m
    
    [1mRequesting weather for city # 154[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tual,ID
       recording weather for [1mTual, ID[0;0m
    
    [1mRequesting weather for city # 155[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chumikan,RU
       recording weather for [1mChumikan, RU[0;0m
    
    [1mRequesting weather for city # 156[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Butaritari,KI
       recording weather for [1mButaritari, KI[0;0m
    
    [1mRequesting weather for city # 157[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Agadez,NE
       recording weather for [1mAgadez, NE[0;0m
    
    [1mRequesting weather for city # 158[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 158[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Malakwal,PK
       recording weather for [1mMalakwal, PK[0;0m
    
    [1mRequesting weather for city # 159[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Georgetown,GY
       recording weather for [1mGeorgetown, GY[0;0m
    
    [1mRequesting weather for city # 160[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luena,AO
       recording weather for [1mLuena, AO[0;0m
    
    [1mRequesting weather for city # 161[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Peniche,PT
       recording weather for [1mPeniche, PT[0;0m
    
    [1mRequesting weather for city # 162[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 162[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Charters%20Towers,AU
       recording weather for [1mCharters Towers, AU[0;0m
    
    [1mRequesting weather for city # 163[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Geraldton,AU
       recording weather for [1mGeraldton, AU[0;0m
    
    [1mRequesting weather for city # 164[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Touros,BR
       recording weather for [1mTouros, BR[0;0m
    
    [1mRequesting weather for city # 165[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dunedin,NZ
       recording weather for [1mDunedin, NZ[0;0m
    
    [1mRequesting weather for city # 166[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 166[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Harrisburg,US
       recording weather for [1mHarrisburg, US[0;0m
    
    [1mRequesting weather for city # 167[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Cristobal,EC
       recording weather for [1mSan Cristobal, EC[0;0m
    
    [1mRequesting weather for city # 168[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ngunguru,NZ
       recording weather for [1mNgunguru, NZ[0;0m
    
    [1mRequesting weather for city # 169[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Clyde%20River,CA
       recording weather for [1mClyde River, CA[0;0m
    
    [1mRequesting weather for city # 170[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sorvag,FO
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 170[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tabiauea,KI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 170[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Naze,JP
       recording weather for [1mNaze, JP[0;0m
    
    [1mRequesting weather for city # 171[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Half%20Moon%20Bay,US
       recording weather for [1mHalf Moon Bay, US[0;0m
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Umzimvubu,ZA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gwadar,PK
       recording weather for [1mGwadar, PK[0;0m
    
    [1mRequesting weather for city # 173[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Hardy,CA
       recording weather for [1mPort Hardy, CA[0;0m
    
    [1mRequesting weather for city # 174[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Auriflama,BR
       recording weather for [1mAuriflama, BR[0;0m
    
    [1mRequesting weather for city # 175[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Upernavik,GL
       recording weather for [1mUpernavik, GL[0;0m
    
    [1mRequesting weather for city # 176[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cam%20Ranh,VN
       recording weather for [1mCam Ranh, VN[0;0m
    
    [1mRequesting weather for city # 177[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Erdenet,MN
       recording weather for [1mErdenet, MN[0;0m
    
    [1mRequesting weather for city # 178[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nador,MA
       recording weather for [1mNador, MA[0;0m
    
    [1mRequesting weather for city # 179[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Itarsi,IN
       recording weather for [1mItarsi, IN[0;0m
    
    [1mRequesting weather for city # 180[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Airai,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 180[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tecolutla,MX
       recording weather for [1mTecolutla, MX[0;0m
    
    [1mRequesting weather for city # 181[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Xining,CN
       recording weather for [1mXining, CN[0;0m
    
    [1mRequesting weather for city # 182[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kununurra,AU
       recording weather for [1mKununurra, AU[0;0m
    
    [1mRequesting weather for city # 183[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sentyabrskiy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 183[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jingdezhen,CN
       recording weather for [1mJingdezhen, CN[0;0m
    
    [1mRequesting weather for city # 184[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pevek,RU
       recording weather for [1mPevek, RU[0;0m
    
    [1mRequesting weather for city # 185[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sumbawa,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 185[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 185[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mahebourg,MU
       recording weather for [1mMahebourg, MU[0;0m
    
    [1mRequesting weather for city # 186[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Quelimane,MZ
       recording weather for [1mQuelimane, MZ[0;0m
    
    [1mRequesting weather for city # 187[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hermanus,ZA
       recording weather for [1mHermanus, ZA[0;0m
    
    [1mRequesting weather for city # 188[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Provideniya,RU
       recording weather for [1mProvideniya, RU[0;0m
    
    [1mRequesting weather for city # 189[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vaitupu,WF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 189[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ketchikan,US
       recording weather for [1mKetchikan, US[0;0m
    
    [1mRequesting weather for city # 190[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saryshagan,KZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 190[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tonj,SD
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 190[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Masterton,NZ
       recording weather for [1mMasterton, NZ[0;0m
    
    [1mRequesting weather for city # 191[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Norman%20Wells,CA
       recording weather for [1mNorman Wells, CA[0;0m
    
    [1mRequesting weather for city # 192[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Avarua,CK
       recording weather for [1mAvarua, CK[0;0m
    
    [1mRequesting weather for city # 193[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tevriz,RU
       recording weather for [1mTevriz, RU[0;0m
    
    [1mRequesting weather for city # 194[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tasiilaq,GL
       recording weather for [1mTasiilaq, GL[0;0m
    
    [1mRequesting weather for city # 195[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cayenne,GF
       recording weather for [1mCayenne, GF[0;0m
    
    [1mRequesting weather for city # 196[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atlantic%20City,US
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 196[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Novopokrovka,RU
       recording weather for [1mNovopokrovka, RU[0;0m
    
    [1mRequesting weather for city # 197[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ribeira%20Grande,PT
       recording weather for [1mRibeira Grande, PT[0;0m
    
    [1mRequesting weather for city # 198[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Boa%20Vista,BR
       recording weather for [1mBoa Vista, BR[0;0m
    
    [1mRequesting weather for city # 199[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 199[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Elizabeth,ZA
       recording weather for [1mPort Elizabeth, ZA[0;0m
    
    [1mRequesting weather for city # 200[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 200[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nadym,RU
       recording weather for [1mNadym, RU[0;0m
    
    [1mRequesting weather for city # 201[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nanortalik,GL
       recording weather for [1mNanortalik, GL[0;0m
    
    [1mRequesting weather for city # 202[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ambon,ID
       recording weather for [1mAmbon, ID[0;0m
    
    [1mRequesting weather for city # 203[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bengkulu,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 203[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Salalah,OM
       recording weather for [1mSalalah, OM[0;0m
    
    [1mRequesting weather for city # 204[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hualmay,PE
       recording weather for [1mHualmay, PE[0;0m
    
    [1mRequesting weather for city # 205[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Muromtsevo,RU
       recording weather for [1mMuromtsevo, RU[0;0m
    
    [1mRequesting weather for city # 206[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chokwe,MZ
       recording weather for [1mChokwe, MZ[0;0m
    
    [1mRequesting weather for city # 207[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Clarence%20Town,BS
       recording weather for [1mClarence Town, BS[0;0m
    
    [1mRequesting weather for city # 208[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saskylakh,RU
       recording weather for [1mSaskylakh, RU[0;0m
    
    [1mRequesting weather for city # 209[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 209[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ugoofaaru,MV
       recording weather for [1mUgoofaaru, MV[0;0m
    
    [1mRequesting weather for city # 210[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Buala,SB
       recording weather for [1mBuala, SB[0;0m
    
    [1mRequesting weather for city # 211[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santa%20Cruz,CR
       recording weather for [1mSanta Cruz, CR[0;0m
    
    [1mRequesting weather for city # 212[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizwa,OM
       recording weather for [1mNizwa, OM[0;0m
    
    [1mRequesting weather for city # 213[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Erzin,RU
       recording weather for [1mErzin, RU[0;0m
    
    [1mRequesting weather for city # 214[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belaya%20Gora,RU
       recording weather for [1mBelaya Gora, RU[0;0m
    
    [1mRequesting weather for city # 215[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mopti,ML
       recording weather for [1mMopti, ML[0;0m
    
    [1mRequesting weather for city # 216[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lata,SB
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 216[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vila%20Velha,BR
       recording weather for [1mVila Velha, BR[0;0m
    
    [1mRequesting weather for city # 217[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Roald,NO
       recording weather for [1mRoald, NO[0;0m
    
    [1mRequesting weather for city # 218[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bethel,US
       recording weather for [1mBethel, US[0;0m
    
    [1mRequesting weather for city # 219[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 219[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ostrovnoy,RU
       recording weather for [1mOstrovnoy, RU[0;0m
    
    [1mRequesting weather for city # 220[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 220[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sinnamary,GF
       recording weather for [1mSinnamary, GF[0;0m
    
    [1mRequesting weather for city # 221[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Karratha,AU
       recording weather for [1mKarratha, AU[0;0m
    
    [1mRequesting weather for city # 222[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kaihua,CN
       recording weather for [1mKaihua, CN[0;0m
    
    [1mRequesting weather for city # 223[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint-Pierre,PM
       recording weather for [1mSaint-Pierre, PM[0;0m
    
    [1mRequesting weather for city # 224[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 224[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mittagong,AU
       recording weather for [1mMittagong, AU[0;0m
    
    [1mRequesting weather for city # 225[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nouakchott,MR
       recording weather for [1mNouakchott, MR[0;0m
    
    [1mRequesting weather for city # 226[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Adrar,DZ
       recording weather for [1mAdrar, DZ[0;0m
    
    [1mRequesting weather for city # 227[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pangnirtung,CA
       recording weather for [1mPangnirtung, CA[0;0m
    
    [1mRequesting weather for city # 228[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Malwan,IN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 228[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 228[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bathsheba,BB
       recording weather for [1mBathsheba, BB[0;0m
    
    [1mRequesting weather for city # 229[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 229[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belmonte,BR
       recording weather for [1mBelmonte, BR[0;0m
    
    [1mRequesting weather for city # 230[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 230[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Morondava,MG
       recording weather for [1mMorondava, MG[0;0m
    
    [1mRequesting weather for city # 231[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=West%20Bay,KY
       recording weather for [1mWest Bay, KY[0;0m
    
    [1mRequesting weather for city # 232[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Leiyang,CN
       recording weather for [1mLeiyang, CN[0;0m
    
    [1mRequesting weather for city # 233[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Katsuura,JP
       recording weather for [1mKatsuura, JP[0;0m
    
    [1mRequesting weather for city # 234[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Winslow,US
       recording weather for [1mWinslow, US[0;0m
    
    [1mRequesting weather for city # 235[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dombarovskiy,RU
       recording weather for [1mDombarovskiy, RU[0;0m
    
    [1mRequesting weather for city # 236[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mount%20Gambier,AU
       recording weather for [1mMount Gambier, AU[0;0m
    
    [1mRequesting weather for city # 237[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Asau,TV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 237[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Champasak,LA
       recording weather for [1mChampasak, LA[0;0m
    
    [1mRequesting weather for city # 238[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tsihombe,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 238[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Caravelas,BR
       recording weather for [1mCaravelas, BR[0;0m
    
    [1mRequesting weather for city # 239[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sola,VU
       recording weather for [1mSola, VU[0;0m
    
    [1mRequesting weather for city # 240[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arcata,US
       recording weather for [1mArcata, US[0;0m
    
    [1mRequesting weather for city # 241[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bajo%20Baudo,CO
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 241[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Muros,ES
       recording weather for [1mMuros, ES[0;0m
    
    [1mRequesting weather for city # 242[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Baghdad,IQ
       recording weather for [1mBaghdad, IQ[0;0m
    
    [1mRequesting weather for city # 243[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Changping,CN
       recording weather for [1mChangping, CN[0;0m
    
    [1mRequesting weather for city # 244[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yomitan,JP
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 244[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kostyantynivka,UA
       recording weather for [1mKostyantynivka, UA[0;0m
    
    [1mRequesting weather for city # 245[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Asau,TV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 245[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nishihara,JP
       recording weather for [1mNishihara, JP[0;0m
    
    [1mRequesting weather for city # 246[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tabou,CI
       recording weather for [1mTabou, CI[0;0m
    
    [1mRequesting weather for city # 247[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bagdarin,RU
       recording weather for [1mBagdarin, RU[0;0m
    
    [1mRequesting weather for city # 248[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Redlands,US
       recording weather for [1mRedlands, US[0;0m
    
    [1mRequesting weather for city # 249[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 249[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tsihombe,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 249[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sangar,RU
       recording weather for [1mSangar, RU[0;0m
    
    [1mRequesting weather for city # 250[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Denton,US
       recording weather for [1mDenton, US[0;0m
    
    [1mRequesting weather for city # 251[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sentyabrskiy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 251[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       recording weather for [1mArraial do Cabo, BR[0;0m
    
    [1mRequesting weather for city # 252[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wellington,AU
       recording weather for [1mWellington, AU[0;0m
    
    [1mRequesting weather for city # 253[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tazovskiy,RU
       recording weather for [1mTazovskiy, RU[0;0m
    
    [1mRequesting weather for city # 254[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Avera,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 254[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 254[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Airai,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 254[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alikalia,SL
       recording weather for [1mAlikalia, SL[0;0m
    
    [1mRequesting weather for city # 255[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Quintin,MX
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 255[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nome,US
       recording weather for [1mNome, US[0;0m
    
    [1mRequesting weather for city # 256[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sorong,ID
       recording weather for [1mSorong, ID[0;0m
    
    [1mRequesting weather for city # 257[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hamilton,BM
       recording weather for [1mHamilton, BM[0;0m
    
    [1mRequesting weather for city # 258[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ahipara,NZ
       recording weather for [1mAhipara, NZ[0;0m
    
    [1mRequesting weather for city # 259[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 259[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 259[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kangaatsiaq,GL
       recording weather for [1mKangaatsiaq, GL[0;0m
    
    [1mRequesting weather for city # 260[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bara,SD
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 260[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Polis,CY
       recording weather for [1mPolis, CY[0;0m
    
    [1mRequesting weather for city # 261[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Celestun,MX
       recording weather for [1mCelestun, MX[0;0m
    
    [1mRequesting weather for city # 262[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Namibe,AO
       recording weather for [1mNamibe, AO[0;0m
    
    [1mRequesting weather for city # 263[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sao%20Miguel%20Do%20Araguaia,BR
       recording weather for [1mSao Miguel do Araguaia, BR[0;0m
    
    [1mRequesting weather for city # 264[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Quang%20Ngai,VN
       recording weather for [1mQuang Ngai, VN[0;0m
    
    [1mRequesting weather for city # 265[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 265[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 265[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lagoa,PT
       recording weather for [1mLagoa, PT[0;0m
    
    [1mRequesting weather for city # 266[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Isla%20Mujeres,MX
       recording weather for [1mIsla Mujeres, MX[0;0m
    
    [1mRequesting weather for city # 267[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Meulaboh,ID
       recording weather for [1mMeulaboh, ID[0;0m
    
    [1mRequesting weather for city # 268[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Carutapera,BR
       recording weather for [1mCarutapera, BR[0;0m
    
    [1mRequesting weather for city # 269[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ixtapa,MX
       recording weather for [1mIxtapa, MX[0;0m
    
    [1mRequesting weather for city # 270[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nabire,ID
       recording weather for [1mNabire, ID[0;0m
    
    [1mRequesting weather for city # 271[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vardo,NO
       recording weather for [1mVardo, NO[0;0m
    
    [1mRequesting weather for city # 272[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Salta,AR
       recording weather for [1mSalta, AR[0;0m
    
    [1mRequesting weather for city # 273[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint%20George,BM
       recording weather for [1mSaint George, BM[0;0m
    
    [1mRequesting weather for city # 274[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ribeira%20Brava,PT
       recording weather for [1mRibeira Brava, PT[0;0m
    
    [1mRequesting weather for city # 275[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 275[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saldanha,ZA
       recording weather for [1mSaldanha, ZA[0;0m
    
    [1mRequesting weather for city # 276[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Skjervoy,NO
       recording weather for [1mSkjervoy, NO[0;0m
    
    [1mRequesting weather for city # 277[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pontal%20Do%20Parana,BR
       recording weather for [1mPontal do Parana, BR[0;0m
    
    [1mRequesting weather for city # 278[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20Gaube,MU
       recording weather for [1mGrand Gaube, MU[0;0m
    
    [1mRequesting weather for city # 279[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Falmouth,US
       recording weather for [1mFalmouth, US[0;0m
    
    [1mRequesting weather for city # 280[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Marapanim,BR
       recording weather for [1mMarapanim, BR[0;0m
    
    [1mRequesting weather for city # 281[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 281[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bac%20Lieu,VN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 281[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Oktyabrskoye,RU
       recording weather for [1mOktyabrskoye, RU[0;0m
    
    [1mRequesting weather for city # 282[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Diffa,NE
       recording weather for [1mDiffa, NE[0;0m
    
    [1mRequesting weather for city # 283[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Oktyabrskiy,RU
       recording weather for [1mOktyabrskiy, RU[0;0m
    
    [1mRequesting weather for city # 284[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alotau,PG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 284[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Viedma,AR
       recording weather for [1mViedma, AR[0;0m
    
    [1mRequesting weather for city # 285[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       Ponta do Sol, CV has already been added, retrying with different city...
    
    [1mRequesting weather for city # 285[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 285[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand-Lahou,CI
       recording weather for [1mGrand-Lahou, CI[0;0m
    
    [1mRequesting weather for city # 286[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Airai,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 286[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Araouane,ML
       recording weather for [1mAraouane, ML[0;0m
    
    [1mRequesting weather for city # 287[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rorvik,NO
       recording weather for [1mRorvik, NO[0;0m
    
    [1mRequesting weather for city # 288[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vostok,RU
       recording weather for [1mVostok, RU[0;0m
    
    [1mRequesting weather for city # 289[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Banda%20Aceh,ID
       recording weather for [1mBanda Aceh, ID[0;0m
    
    [1mRequesting weather for city # 290[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Solnechnyy,RU
       recording weather for [1mSolnechnyy, RU[0;0m
    
    [1mRequesting weather for city # 291[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Talnakh,RU
       recording weather for [1mTalnakh, RU[0;0m
    
    [1mRequesting weather for city # 292[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 292[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ravar,IR
       recording weather for [1mRavar, IR[0;0m
    
    [1mRequesting weather for city # 293[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 293[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kota%20Kinabalu,MY
       recording weather for [1mKota Kinabalu, MY[0;0m
    
    [1mRequesting weather for city # 294[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fortuna,US
       recording weather for [1mFortuna, US[0;0m
    
    [1mRequesting weather for city # 295[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rungata,KI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 295[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arona,ES
       recording weather for [1mArona, ES[0;0m
    
    [1mRequesting weather for city # 296[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Guane,CU
       recording weather for [1mGuane, CU[0;0m
    
    [1mRequesting weather for city # 297[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Coahuayana,MX
       recording weather for [1mCoahuayana, MX[0;0m
    
    [1mRequesting weather for city # 298[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=El%20Alto,PE
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 298[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Boyolangu,ID
       recording weather for [1mBoyolangu, ID[0;0m
    
    [1mRequesting weather for city # 299[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kirakira,SB
       recording weather for [1mKirakira, SB[0;0m
    
    [1mRequesting weather for city # 300[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Comonfort,MX
       recording weather for [1mComonfort, MX[0;0m
    
    [1mRequesting weather for city # 301[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nakatsu,JP
       recording weather for [1mNakatsu, JP[0;0m
    
    [1mRequesting weather for city # 302[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cabedelo,BR
       recording weather for [1mCabedelo, BR[0;0m
    
    [1mRequesting weather for city # 303[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ormond%20Beach,US
       recording weather for [1mOrmond Beach, US[0;0m
    
    [1mRequesting weather for city # 304[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Richards%20Bay,ZA
       recording weather for [1mRichards Bay, ZA[0;0m
    
    [1mRequesting weather for city # 305[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Attawapiskat,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 305[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 305[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 305[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Brae,GB
       recording weather for [1mBrae, GB[0;0m
    
    [1mRequesting weather for city # 306[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Oistins,BB
       recording weather for [1mOistins, BB[0;0m
    
    [1mRequesting weather for city # 307[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Red%20Wing,US
       recording weather for [1mRed Wing, US[0;0m
    
    [1mRequesting weather for city # 308[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 308[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 308[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Darhan,MN
       recording weather for [1mDarhan, MN[0;0m
    
    [1mRequesting weather for city # 309[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Schramberg,DE
       recording weather for [1mSchramberg, DE[0;0m
    
    [1mRequesting weather for city # 310[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fairlie,NZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 310[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gryazovets,RU
       recording weather for [1mGryazovets, RU[0;0m
    
    [1mRequesting weather for city # 311[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hambantota,LK
       recording weather for [1mHambantota, LK[0;0m
    
    [1mRequesting weather for city # 312[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Phan%20Rang,VN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 312[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dhadar,PK
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 312[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Seoul,KR
       recording weather for [1mSeoul, KR[0;0m
    
    [1mRequesting weather for city # 313[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zhezkazgan,KZ
       recording weather for [1mZhezkazgan, KZ[0;0m
    
    [1mRequesting weather for city # 314[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 314[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bismarck,US
       recording weather for [1mBismarck, US[0;0m
    
    [1mRequesting weather for city # 315[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dalvik,IS
       recording weather for [1mDalvik, IS[0;0m
    
    [1mRequesting weather for city # 316[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bridlington,GB
       recording weather for [1mBridlington, GB[0;0m
    
    [1mRequesting weather for city # 317[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kapoeta,SD
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 317[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Eirunepe,BR
       recording weather for [1mEirunepe, BR[0;0m
    
    [1mRequesting weather for city # 318[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Christchurch,NZ
       recording weather for [1mChristchurch, NZ[0;0m
    
    [1mRequesting weather for city # 319[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 319[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Eresos,GR
       recording weather for [1mEresos, GR[0;0m
    
    [1mRequesting weather for city # 320[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 320[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vao,NC
       recording weather for [1mVao, NC[0;0m
    
    [1mRequesting weather for city # 321[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       Arraial do Cabo, BR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 321[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 321[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chihuahua,MX
       recording weather for [1mChihuahua, MX[0;0m
    
    [1mRequesting weather for city # 322[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Preobrazheniye,RU
       recording weather for [1mPreobrazheniye, RU[0;0m
    
    [1mRequesting weather for city # 323[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Riverton,NZ
       recording weather for [1mRiverton, NZ[0;0m
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kuche,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rawannawi,KI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nichinan,JP
       recording weather for [1mNichinan, JP[0;0m
    
    [1mRequesting weather for city # 325[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tupik,RU
       recording weather for [1mTupik, RU[0;0m
    
    [1mRequesting weather for city # 326[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atar,MR
       recording weather for [1mAtar, MR[0;0m
    
    [1mRequesting weather for city # 327[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Linxia,CN
       recording weather for [1mLinxia, CN[0;0m
    
    [1mRequesting weather for city # 328[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Banaue,PH
       recording weather for [1mBanaue, PH[0;0m
    
    [1mRequesting weather for city # 329[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mardin,TR
       recording weather for [1mMardin, TR[0;0m
    
    [1mRequesting weather for city # 330[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pemba,MZ
       recording weather for [1mPemba, MZ[0;0m
    
    [1mRequesting weather for city # 331[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kutum,SD
       recording weather for [1mKutum, SD[0;0m
    
    [1mRequesting weather for city # 332[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Monrovia,LR
       recording weather for [1mMonrovia, LR[0;0m
    
    [1mRequesting weather for city # 333[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=The%20Pas,CA
       recording weather for [1mThe Pas, CA[0;0m
    
    [1mRequesting weather for city # 334[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Cabezas,NI
       recording weather for [1mPuerto Cabezas, NI[0;0m
    
    [1mRequesting weather for city # 335[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Viligili,MV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 335[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=El%20Calvario,CO
       recording weather for [1mEl Calvario, CO[0;0m
    
    [1mRequesting weather for city # 336[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hovd,MN
       recording weather for [1mHovd, MN[0;0m
    
    [1mRequesting weather for city # 337[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sur,OM
       recording weather for [1mSur, OM[0;0m
    
    [1mRequesting weather for city # 338[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Marcona,PE
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 338[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Constitucion,MX
       recording weather for [1mConstitucion, MX[0;0m
    
    [1mRequesting weather for city # 339[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Padang,ID
       recording weather for [1mPadang, ID[0;0m
    
    [1mRequesting weather for city # 340[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Camaguey,CU
       recording weather for [1mCamaguey, CU[0;0m
    
    [1mRequesting weather for city # 341[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 341[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Singarayakonda,IN
       recording weather for [1mSingarayakonda, IN[0;0m
    
    [1mRequesting weather for city # 342[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kiama,AU
       recording weather for [1mKiama, AU[0;0m
    
    [1mRequesting weather for city # 343[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 343[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barrhead,CA
       recording weather for [1mBarrhead, CA[0;0m
    
    [1mRequesting weather for city # 344[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kyzyl-Suu,KG
       recording weather for [1mKyzyl-Suu, KG[0;0m
    
    [1mRequesting weather for city # 345[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mondlo,ZA
       recording weather for [1mMondlo, ZA[0;0m
    
    [1mRequesting weather for city # 346[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Praia%20Da%20Vitoria,PT
       recording weather for [1mPraia da Vitoria, PT[0;0m
    
    [1mRequesting weather for city # 347[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saleaula,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 347[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Misratah,LY
       recording weather for [1mMisratah, LY[0;0m
    
    [1mRequesting weather for city # 348[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Broome,AU
       recording weather for [1mBroome, AU[0;0m
    
    [1mRequesting weather for city # 349[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Iqaluit,CA
       recording weather for [1mIqaluit, CA[0;0m
    
    [1mRequesting weather for city # 350[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Hueneme,US
       recording weather for [1mPort Hueneme, US[0;0m
    
    [1mRequesting weather for city # 351[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mitsamiouli,KM
       recording weather for [1mMitsamiouli, KM[0;0m
    
    [1mRequesting weather for city # 352[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Shar,KZ
       recording weather for [1mShar, KZ[0;0m
    
    [1mRequesting weather for city # 353[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Monaragala,LK
       recording weather for [1mMonaragala, LK[0;0m
    
    [1mRequesting weather for city # 354[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 354[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Attawapiskat,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 354[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mao,TD
       recording weather for [1mMao, TD[0;0m
    
    [1mRequesting weather for city # 355[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sabha,LY
       recording weather for [1mSabha, LY[0;0m
    
    [1mRequesting weather for city # 356[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alofi,NU
       recording weather for [1mAlofi, NU[0;0m
    
    [1mRequesting weather for city # 357[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mushie,CD
       recording weather for [1mMushie, CD[0;0m
    
    [1mRequesting weather for city # 358[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dudinka,RU
       recording weather for [1mDudinka, RU[0;0m
    
    [1mRequesting weather for city # 359[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rawlins,US
       recording weather for [1mRawlins, US[0;0m
    
    [1mRequesting weather for city # 360[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alice%20Springs,AU
       recording weather for [1mAlice Springs, AU[0;0m
    
    [1mRequesting weather for city # 361[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Phuket,TH
       recording weather for [1mPhuket, TH[0;0m
    
    [1mRequesting weather for city # 362[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Flinders,AU
       recording weather for [1mFlinders, AU[0;0m
    
    [1mRequesting weather for city # 363[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luderitz,NA
       recording weather for [1mLuderitz, NA[0;0m
    
    [1mRequesting weather for city # 364[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Laguna,BR
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 364[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 364[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aksarka,RU
       recording weather for [1mAksarka, RU[0;0m
    
    [1mRequesting weather for city # 365[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Birin,DZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 365[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       Arraial do Cabo, BR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 365[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Airai,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 365[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barbastro,ES
       recording weather for [1mBarbastro, ES[0;0m
    
    [1mRequesting weather for city # 366[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luorong,CN
       recording weather for [1mLuorong, CN[0;0m
    
    [1mRequesting weather for city # 367[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 367[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kandrian,PG
       recording weather for [1mKandrian, PG[0;0m
    
    [1mRequesting weather for city # 368[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Catumbela,AO
       recording weather for [1mCatumbela, AO[0;0m
    
    [1mRequesting weather for city # 369[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kalianget,ID
       recording weather for [1mKalianget, ID[0;0m
    
    [1mRequesting weather for city # 370[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lae,PG
       recording weather for [1mLae, PG[0;0m
    
    [1mRequesting weather for city # 371[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tautira,PF
       recording weather for [1mTautira, PF[0;0m
    
    [1mRequesting weather for city # 372[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wahran,DZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 372[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Defiance,US
       recording weather for [1mDefiance, US[0;0m
    
    [1mRequesting weather for city # 373[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Garowe,SO
       recording weather for [1mGarowe, SO[0;0m
    
    [1mRequesting weather for city # 374[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kisangani,CD
       recording weather for [1mKisangani, CD[0;0m
    
    [1mRequesting weather for city # 375[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atambua,ID
       recording weather for [1mAtambua, ID[0;0m
    
    [1mRequesting weather for city # 376[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 376[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bonthe,SL
       recording weather for [1mBonthe, SL[0;0m
    
    [1mRequesting weather for city # 377[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aswan,EG
       recording weather for [1mAswan, EG[0;0m
    
    [1mRequesting weather for city # 378[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ocala,US
       recording weather for [1mOcala, US[0;0m
    
    [1mRequesting weather for city # 379[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 379[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gizo,SB
       recording weather for [1mGizo, SB[0;0m
    
    [1mRequesting weather for city # 380[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Irbil,IQ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 380[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sabang,ID
       recording weather for [1mSabang, ID[0;0m
    
    [1mRequesting weather for city # 381[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Katobu,ID
       recording weather for [1mKatobu, ID[0;0m
    
    [1mRequesting weather for city # 382[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taltal,CL
       recording weather for [1mTaltal, CL[0;0m
    
    [1mRequesting weather for city # 383[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Acapulco,MX
       recording weather for [1mAcapulco, MX[0;0m
    
    [1mRequesting weather for city # 384[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Moresby,PG
       recording weather for [1mPort Moresby, PG[0;0m
    
    [1mRequesting weather for city # 385[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Galiwinku,AU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 385[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Iskateley,RU
       recording weather for [1mIskateley, RU[0;0m
    
    [1mRequesting weather for city # 386[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 386[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zhangye,CN
       recording weather for [1mZhangye, CN[0;0m
    
    [1mRequesting weather for city # 387[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 387[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Whyalla,AU
       recording weather for [1mWhyalla, AU[0;0m
    
    [1mRequesting weather for city # 388[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Havoysund,NO
       recording weather for [1mHavoysund, NO[0;0m
    
    [1mRequesting weather for city # 389[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gravdal,NO
       recording weather for [1mGravdal, NO[0;0m
    
    [1mRequesting weather for city # 390[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mrakovo,RU
       recording weather for [1mMrakovo, RU[0;0m
    
    [1mRequesting weather for city # 391[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Petropavlovsk-Kamchatskiy,RU
       recording weather for [1mPetropavlovsk-Kamchatskiy, RU[0;0m
    
    [1mRequesting weather for city # 392[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Termoli,IT
       recording weather for [1mTermoli, IT[0;0m
    
    [1mRequesting weather for city # 393[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 393[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Olafsvik,IS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 393[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Eureka,US
       recording weather for [1mEureka, US[0;0m
    
    [1mRequesting weather for city # 394[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Artyk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 394[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Champerico,GT
       recording weather for [1mChamperico, GT[0;0m
    
    [1mRequesting weather for city # 395[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fairbanks,US
       recording weather for [1mFairbanks, US[0;0m
    
    [1mRequesting weather for city # 396[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bardiyah,LY
       recording weather for [1mBardiyah, LY[0;0m
    
    [1mRequesting weather for city # 397[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Plettenberg%20Bay,ZA
       recording weather for [1mPlettenberg Bay, ZA[0;0m
    
    [1mRequesting weather for city # 398[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Corrente,BR
       recording weather for [1mCorrente, BR[0;0m
    
    [1mRequesting weather for city # 399[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aklavik,CA
       recording weather for [1mAklavik, CA[0;0m
    
    [1mRequesting weather for city # 400[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Qaqortoq,GL
       recording weather for [1mQaqortoq, GL[0;0m
    
    [1mRequesting weather for city # 401[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kashi,CN
       recording weather for [1mKashi, CN[0;0m
    
    [1mRequesting weather for city # 402[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Udachnyy,RU
       recording weather for [1mUdachnyy, RU[0;0m
    
    [1mRequesting weather for city # 403[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hofn,IS
       recording weather for [1mHofn, IS[0;0m
    
    [1mRequesting weather for city # 404[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Namatanai,PG
       recording weather for [1mNamatanai, PG[0;0m
    
    [1mRequesting weather for city # 405[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kedrovyy,RU
       recording weather for [1mKedrovyy, RU[0;0m
    
    [1mRequesting weather for city # 406[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 406[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       Ponta do Sol, CV has already been added, retrying with different city...
    
    [1mRequesting weather for city # 406[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luau,AO
       recording weather for [1mLuau, AO[0;0m
    
    [1mRequesting weather for city # 407[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Opuwo,NA
       recording weather for [1mOpuwo, NA[0;0m
    
    [1mRequesting weather for city # 408[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 408[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Khash,IR
       recording weather for [1mKhash, IR[0;0m
    
    [1mRequesting weather for city # 409[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Asau,TV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 409[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kousseri,CM
       recording weather for [1mKousseri, CM[0;0m
    
    [1mRequesting weather for city # 410[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Escondido,MX
       recording weather for [1mPuerto Escondido, MX[0;0m
    
    [1mRequesting weather for city # 411[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Revda,RU
       recording weather for [1mRevda, RU[0;0m
    
    [1mRequesting weather for city # 412[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 412[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lavrentiya,RU
       recording weather for [1mLavrentiya, RU[0;0m
    
    [1mRequesting weather for city # 413[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 413[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nuevo%20Progreso,MX
       recording weather for [1mNuevo Progreso, MX[0;0m
    
    [1mRequesting weather for city # 414[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amapa,BR
       recording weather for [1mAmapa, BR[0;0m
    
    [1mRequesting weather for city # 415[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint-Augustin,CA
       recording weather for [1mSaint-Augustin, CA[0;0m
    
    [1mRequesting weather for city # 416[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Minturno,IT
       recording weather for [1mMinturno, IT[0;0m
    
    [1mRequesting weather for city # 417[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Koslan,RU
       recording weather for [1mKoslan, RU[0;0m
    
    [1mRequesting weather for city # 418[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Warragul,AU
       recording weather for [1mWarragul, AU[0;0m
    
    [1mRequesting weather for city # 419[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Algiers,DZ
       recording weather for [1mAlgiers, DZ[0;0m
    
    [1mRequesting weather for city # 420[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 420[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fasa,IR
       recording weather for [1mFasa, IR[0;0m
    
    [1mRequesting weather for city # 421[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,PT
       Ponta do Sol, PT has already been added, retrying with different city...
    
    [1mRequesting weather for city # 421[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nassau,BS
       recording weather for [1mNassau, BS[0;0m
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lata,SB
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vaitupu,WF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=General%20Roca,AR
       recording weather for [1mGeneral Roca, AR[0;0m
    
    [1mRequesting weather for city # 423[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 423[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wilhelmsburg,AT
       recording weather for [1mWilhelmsburg, AT[0;0m
    
    [1mRequesting weather for city # 424[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 424[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Khatanga,RU
       recording weather for [1mKhatanga, RU[0;0m
    
    [1mRequesting weather for city # 425[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 425[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Metro,ID
       recording weather for [1mMetro, ID[0;0m
    
    [1mRequesting weather for city # 426[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kulachi,PK
       recording weather for [1mKulachi, PK[0;0m
    
    [1mRequesting weather for city # 427[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tura,RU
       recording weather for [1mTura, RU[0;0m
    
    [1mRequesting weather for city # 428[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Inderborskiy,KZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 428[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Iracoubo,GF
       recording weather for [1mIracoubo, GF[0;0m
    
    [1mRequesting weather for city # 429[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sorsk,RU
       recording weather for [1mSorsk, RU[0;0m
    
    [1mRequesting weather for city # 430[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 430[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luang%20Prabang,LA
       recording weather for [1mLuang Prabang, LA[0;0m
    
    [1mRequesting weather for city # 431[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chabahar,IR
       recording weather for [1mChabahar, IR[0;0m
    
    [1mRequesting weather for city # 432[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Keti%20Bandar,PK
       recording weather for [1mKeti Bandar, PK[0;0m
    
    [1mRequesting weather for city # 433[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Asyut,EG
       recording weather for [1mAsyut, EG[0;0m
    
    [1mRequesting weather for city # 434[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 434[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Snyder,US
       recording weather for [1mSnyder, US[0;0m
    
    [1mRequesting weather for city # 435[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Moerai,PF
       recording weather for [1mMoerai, PF[0;0m
    
    [1mRequesting weather for city # 436[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arlit,NE
       recording weather for [1mArlit, NE[0;0m
    
    [1mRequesting weather for city # 437[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ailigandi,PA
       recording weather for [1mAiligandi, PA[0;0m
    
    [1mRequesting weather for city # 438[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Seydisehir,TR
       recording weather for [1mSeydisehir, TR[0;0m
    
    [1mRequesting weather for city # 439[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sitka,US
       recording weather for [1mSitka, US[0;0m
    
    [1mRequesting weather for city # 440[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Halalo,WF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 440[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aruja,BR
       recording weather for [1mAruja, BR[0;0m
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Attawapiskat,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tonj,SD
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Brotas,BR
       recording weather for [1mBrotas, BR[0;0m
    
    [1mRequesting weather for city # 442[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint-Francois,GP
       recording weather for [1mSaint-Francois, GP[0;0m
    
    [1mRequesting weather for city # 443[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Krishnarajpet,IN
       recording weather for [1mKrishnarajpet, IN[0;0m
    
    [1mRequesting weather for city # 444[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kyabe,TD
       recording weather for [1mKyabe, TD[0;0m
    
    [1mRequesting weather for city # 445[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grindavik,IS
       recording weather for [1mGrindavik, IS[0;0m
    
    [1mRequesting weather for city # 446[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 446[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kapit,MY
       recording weather for [1mKapit, MY[0;0m
    
    [1mRequesting weather for city # 447[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 447[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hailey,US
       recording weather for [1mHailey, US[0;0m
    
    [1mRequesting weather for city # 448[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pacific%20Grove,US
       recording weather for [1mPacific Grove, US[0;0m
    
    [1mRequesting weather for city # 449[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Carreno,CO
       recording weather for [1mPuerto Carreno, CO[0;0m
    
    [1mRequesting weather for city # 450[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yarmouth,CA
       recording weather for [1mYarmouth, CA[0;0m
    
    [1mRequesting weather for city # 451[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gannan,CN
       recording weather for [1mGannan, CN[0;0m
    
    [1mRequesting weather for city # 452[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Waddan,LY
       recording weather for [1mWaddan, LY[0;0m
    
    [1mRequesting weather for city # 453[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 453[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Novyy%20Urengoy,RU
       recording weather for [1mNovyy Urengoy, RU[0;0m
    
    [1mRequesting weather for city # 454[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Omboue,GA
       recording weather for [1mOmboue, GA[0;0m
    
    [1mRequesting weather for city # 455[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Colombia,CO
       recording weather for [1mPuerto Colombia, CO[0;0m
    
    [1mRequesting weather for city # 456[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Warqla,DZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 456[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nakhon%20Phanom,TH
       recording weather for [1mNakhon Phanom, TH[0;0m
    
    [1mRequesting weather for city # 457[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hounde,BF
       recording weather for [1mHounde, BF[0;0m
    
    [1mRequesting weather for city # 458[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 458[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ivanava,BY
       recording weather for [1mIvanava, BY[0;0m
    
    [1mRequesting weather for city # 459[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 459[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fort%20Nelson,CA
       recording weather for [1mFort Nelson, CA[0;0m
    
    [1mRequesting weather for city # 460[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chuncheng,CN
       recording weather for [1mChuncheng, CN[0;0m
    
    [1mRequesting weather for city # 461[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mecca,SA
       recording weather for [1mMecca, SA[0;0m
    
    [1mRequesting weather for city # 462[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Batangafo,CF
       recording weather for [1mBatangafo, CF[0;0m
    
    [1mRequesting weather for city # 463[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vinh,VN
       recording weather for [1mVinh, VN[0;0m
    
    [1mRequesting weather for city # 464[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santa%20Rosa,AR
       recording weather for [1mSanta Rosa, AR[0;0m
    
    [1mRequesting weather for city # 465[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sacueni,RO
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 465[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Miguel%20Auza,MX
       recording weather for [1mMiguel Auza, MX[0;0m
    
    [1mRequesting weather for city # 466[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Moose%20Factory,CA
       recording weather for [1mMoose Factory, CA[0;0m
    
    [1mRequesting weather for city # 467[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tarudant,MA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 467[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Play%20Cu,VN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 467[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Greenwood,US
       recording weather for [1mGreenwood, US[0;0m
    
    [1mRequesting weather for city # 468[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Neiafu,TO
       recording weather for [1mNeiafu, TO[0;0m
    
    [1mRequesting weather for city # 469[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nguiu,AU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 469[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lagos,PT
       recording weather for [1mLagos, PT[0;0m
    
    [1mRequesting weather for city # 470[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gigmoto,PH
       recording weather for [1mGigmoto, PH[0;0m
    
    [1mRequesting weather for city # 471[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atlantis,ZA
       recording weather for [1mAtlantis, ZA[0;0m
    
    [1mRequesting weather for city # 472[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rawannawi,KI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 472[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 472[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Vicente,PH
       recording weather for [1mSan Vicente, PH[0;0m
    
    [1mRequesting weather for city # 473[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 473[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aripuana,BR
       recording weather for [1mAripuana, BR[0;0m
    
    [1mRequesting weather for city # 474[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Poum,NC
       recording weather for [1mPoum, NC[0;0m
    
    [1mRequesting weather for city # 475[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kautokeino,NO
       recording weather for [1mKautokeino, NO[0;0m
    
    [1mRequesting weather for city # 476[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rocha,UY
       recording weather for [1mRocha, UY[0;0m
    
    [1mRequesting weather for city # 477[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 477[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wulanhaote,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 477[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fereydun%20Kenar,IR
       recording weather for [1mFereydun Kenar, IR[0;0m
    
    [1mRequesting weather for city # 478[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ornskoldsvik,SE
       recording weather for [1mOrnskoldsvik, SE[0;0m
    
    [1mRequesting weather for city # 479[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Veraval,IN
       recording weather for [1mVeraval, IN[0;0m
    
    [1mRequesting weather for city # 480[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Meadow%20Lake,CA
       recording weather for [1mMeadow Lake, CA[0;0m
    
    [1mRequesting weather for city # 481[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 481[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Northam,AU
       recording weather for [1mNortham, AU[0;0m
    
    [1mRequesting weather for city # 482[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Qeshm,IR
       recording weather for [1mQeshm, IR[0;0m
    
    [1mRequesting weather for city # 483[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ternate,ID
       recording weather for [1mTernate, ID[0;0m
    
    [1mRequesting weather for city # 484[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Maragogi,BR
       recording weather for [1mMaragogi, BR[0;0m
    
    [1mRequesting weather for city # 485[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tumannyy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 485[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=La%20Ronge,CA
       recording weather for [1mLa Ronge, CA[0;0m
    
    [1mRequesting weather for city # 486[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grafton,US
       recording weather for [1mGrafton, US[0;0m
    
    [1mRequesting weather for city # 487[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bowen,AU
       recording weather for [1mBowen, AU[0;0m
    
    [1mRequesting weather for city # 488[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Klyuchi,RU
       recording weather for [1mKlyuchi, RU[0;0m
    
    [1mRequesting weather for city # 489[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Houston,CA
       recording weather for [1mHouston, CA[0;0m
    
    [1mRequesting weather for city # 490[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lethem,GY
       recording weather for [1mLethem, GY[0;0m
    
    [1mRequesting weather for city # 491[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Washington,US
       recording weather for [1mWashington DC., US[0;0m
    
    [1mRequesting weather for city # 492[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Camana,PE
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 492[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hokitika,NZ
       recording weather for [1mHokitika, NZ[0;0m
    
    [1mRequesting weather for city # 493[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sale,AU
       recording weather for [1mSale, AU[0;0m
    
    [1mRequesting weather for city # 494[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 494[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yangjiang,CN
       recording weather for [1mYangjiang, CN[0;0m
    
    [1mRequesting weather for city # 495[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kabakovo,RU
       recording weather for [1mKabakovo, RU[0;0m
    
    [1mRequesting weather for city # 496[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nokaneng,BW
       recording weather for [1mNokaneng, BW[0;0m
    
    [1mRequesting weather for city # 497[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zyryanskoye,RU
       recording weather for [1mZyryanskoye, RU[0;0m
    
    [1mRequesting weather for city # 498[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samalaeulu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 498[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 498[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Paamiut,GL
       recording weather for [1mPaamiut, GL[0;0m
    
    [1mRequesting weather for city # 499[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 499[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yunjinghong,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 499[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Los%20Llanos%20De%20Aridane,ES
       recording weather for [1mLos Llanos de Aridane, ES[0;0m
    
    [1mRequesting weather for city # 500[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kurilsk,RU
       recording weather for [1mKurilsk, RU[0;0m
    
    [1mRecorded weather for 500 cities.[0;0m



```python
#create df
cities_dict = {
    'City':cities,
    'Country':countries,
    'Latitude':lat,
    'Longitude':lng,
    'Temperature, '+units:temp,
    'Humidity':humidity,
    'Wind Speed MPH':windspeed,
    'Clouds':cloudiness
}
cities_df = pd.DataFrame(cities_dict)

#check if there are no duplicated cities
cities_df[cities_df.duplicated(subset='City', keep=False).values]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Clouds</th>
      <th>Country</th>
      <th>Humidity</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Temperature, imperial</th>
      <th>Wind Speed MPH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>102</th>
      <td>Georgetown</td>
      <td>13.87</td>
      <td>SH</td>
      <td>100</td>
      <td>-7.93</td>
      <td>-14.42</td>
      <td>79.09</td>
      <td>0</td>
    </tr>
    <tr>
      <th>158</th>
      <td>Georgetown</td>
      <td>4.70</td>
      <td>GY</td>
      <td>100</td>
      <td>6.80</td>
      <td>-58.16</td>
      <td>75.20</td>
      <td>75</td>
    </tr>
  </tbody>
</table>
</div>




```python
#save df to CSV
cities_df.to_csv('weather_data.csv',index=False)
```


```python
def plot_map(viz_title, to_plot, cmap_label, lng, lat):
    """
    Plots colormap on the world image
    
    ------
    Params:
    ------
    viz_title  : text to show on the map
    to_plot    : array-like set of values to plot
    cmap_label : text to show on colormap label
    lng, lat   : array-like coordinates in meters of same length as to_plot
    """
    plt.style.use('seaborn-white')
    f, ax = plt.subplots(figsize=(10,10))
    
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
                llcrnrlon=-180,urcrnrlon=180,lat_ts=20,\
                resolution='c', ax=ax)
    
    m.drawparallels(np.arange(-90.,91.,30.),labels=[1,1,0,0],\
                    color='#8856a7', textcolor='#343a40')
    m.drawlsmask(land_color='#9ebcda',ocean_color='#e0ecf4',lakes=False)

    #create coordinates
    x,y= m(lng, lat)

    cax = m.scatter(x,y, latlon=False, marker='o', c=to_plot, s=50, \
                    cmap='plasma', alpha=1, linewidths=0)
    
    cbar = f.colorbar(cax, shrink=0.4, pad=0.1)
    cbar.set_label(cmap_label, fontsize=18, color='#343a40', weight='bold')
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors='#343a40')

    #remove axes borders
    ax.axis('off')

    plt.title(viz_title, fontsize=24, color='#343a40', \
              position=(0.5,1.05), weight='bold')
    
    f.savefig('img/'+viz_title+'.png',dpi=150,transparent=False,bbox_inches='tight',pad_inches=0.5)
    plt.show()
```

# Temperature (F) vs. Latitude


```python
cities_df = pd.read_csv('weather_data.csv')
```


```python
#create variables for plotting
lng = cities_df['Longitude'].values
lat = cities_df['Latitude'].values

title1 = 'Temperature vs Latitude'
temps = cities_df['Temperature, imperial'].values
temps_label = 'Temperature (°F)'
```


```python
#set variables for viz1 to plot here
viz_title = title1
to_plot = temps
cmap_label = temps_label
plot_map(viz_title, to_plot, cmap_label, lng, lat)
```

    /Users/yegor3/anaconda3/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:4995: MatplotlibDeprecationWarning: The is_scalar function was deprecated in version 2.1.
      elif masked and is_scalar(masked):



![png](output_10_1.png)


# Humidity (%) vs. Latitude


```python
title2 = 'Humidity vs Latitude'
humidity = cities_df['Humidity'].values
numidity_label = 'Humidity (%)'
```


```python
#set variables for viz2 to plot here
viz_title = title2
to_plot = humidity
cmap_label = numidity_label
plot_map(viz_title, to_plot, cmap_label, lng, lat)
```

    /Users/yegor3/anaconda3/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:4995: MatplotlibDeprecationWarning: The is_scalar function was deprecated in version 2.1.
      elif masked and is_scalar(masked):



![png](output_13_1.png)


# Cloudiness (%) vs. Latitude


```python
title3 = 'Cloudiness vs Latitude'
clouds = cities_df['Clouds'].values
clouds_label = 'Clouds (%)'
```


```python
#set variables for viz2 to plot here
viz_title = title3
to_plot = clouds
cmap_label = clouds_label
plot_map(viz_title, to_plot, cmap_label, lng, lat)
```

    /Users/yegor3/anaconda3/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:4995: MatplotlibDeprecationWarning: The is_scalar function was deprecated in version 2.1.
      elif masked and is_scalar(masked):



![png](output_16_1.png)


# Wind Speed (mph) vs. Latitude


```python
title4 = 'Wind Speed vs Latitude'
wind = cities_df['Wind Speed MPH'].values
wind_label = 'Wind Speed (MPH)'
```


```python
#set variables for viz2 to plot here
viz_title = title4
to_plot = wind
cmap_label = wind_label
plot_map(viz_title, to_plot, cmap_label, lng, lat)
```

    /Users/yegor3/anaconda3/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:4995: MatplotlibDeprecationWarning: The is_scalar function was deprecated in version 2.1.
      elif masked and is_scalar(masked):



![png](output_19_1.png)


# Scatterplots using Seaborn


```python
import seaborn as sns
f, axes = plt.subplots(ncols=2,nrows=2,figsize=(20,20))

sns.set_style('darkgrid')
sns.regplot('Temperature, imperial','Latitude',data=cities_df,fit_reg=False, ax=axes[0,0])
sns.regplot('Humidity','Latitude',data=cities_df,fit_reg=False, ax=axes[0,1])
sns.regplot('Clouds','Latitude',data=cities_df,fit_reg=False, ax=axes[1,0])
sns.regplot('Wind Speed MPH','Latitude',data=cities_df,fit_reg=False, ax=axes[1,1])

sns.set(font_scale=2)
axes[0,0].set_title('Temperature', fontweight='bold')
axes[0,1].set_title('Humidity', fontweight='bold')
axes[1,0].set_title('Clouds', fontweight='bold')
axes[1,1].set_title('Wind Speed', fontweight='bold')

plt.suptitle('Correlation between different weather measurements and latitude', fontweight='bold', y=.95)

axes[0,0].set_xlabel('')
axes[0,1].set_xlabel('')
axes[0,1].set_ylabel('')
axes[1,0].set_xlabel('')
axes[1,1].set_xlabel('')
axes[1,1].set_ylabel('')

f.savefig('img/all.png',dpi=150,transparent=False,bbox_inches='tight',pad_inches=0.5)

plt.show()
```


![png](output_21_0.png)



```python
#f, ax = plt.subplots(figsize=(10,10))
sns.set_style('darkgrid')
g = sns.PairGrid(cities_df,size=5)
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter);
g.savefig('img/pairgrid.png',dpi=150,transparent=False,bbox_inches='tight',pad_inches=0.5)
```


![png](output_22_0.png)


# Trends
* Temperatures are higher around equator
* Humidity is higher alongside cost lines and big rivers
* Amount of clouds is about the same around the globe
* Wind speed seems to be all over

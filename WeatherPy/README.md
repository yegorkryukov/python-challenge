
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
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ushuaia,AR
       recording weather for [1mUshuaia, AR[0;0m
    
    [1mRequesting weather for city # 2[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 2[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 2[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Praia,CV
       recording weather for [1mPraia, CV[0;0m
    
    [1mRequesting weather for city # 3[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint-Philippe,RE
       recording weather for [1mSaint-Philippe, RE[0;0m
    
    [1mRequesting weather for city # 4[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Longyearbyen,SJ
       recording weather for [1mLongyearbyen, SJ[0;0m
    
    [1mRequesting weather for city # 5[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jamestown,SH
       recording weather for [1mJamestown, SH[0;0m
    
    [1mRequesting weather for city # 6[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cidreira,BR
       recording weather for [1mCidreira, BR[0;0m
    
    [1mRequesting weather for city # 7[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rikitea,PF
       recording weather for [1mRikitea, PF[0;0m
    
    [1mRequesting weather for city # 8[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tuktoyaktuk,CA
       recording weather for [1mTuktoyaktuk, CA[0;0m
    
    [1mRequesting weather for city # 9[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Christchurch,NZ
       recording weather for [1mChristchurch, NZ[0;0m
    
    [1mRequesting weather for city # 10[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ranfurly,NZ
       recording weather for [1mRanfurly, NZ[0;0m
    
    [1mRequesting weather for city # 11[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Punta%20Alta,AR
       recording weather for [1mPunta Alta, AR[0;0m
    
    [1mRequesting weather for city # 12[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Souillac,MU
       recording weather for [1mSouillac, MU[0;0m
    
    [1mRequesting weather for city # 13[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Te%20Anau,NZ
       recording weather for [1mTe Anau, NZ[0;0m
    
    [1mRequesting weather for city # 14[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vila%20Velha,BR
       recording weather for [1mVila Velha, BR[0;0m
    
    [1mRequesting weather for city # 15[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cananeia,BR
       recording weather for [1mCananeia, BR[0;0m
    
    [1mRequesting weather for city # 16[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=La%20Argentina,CO
       recording weather for [1mLa Argentina, CO[0;0m
    
    [1mRequesting weather for city # 17[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Qaanaaq,GL
       recording weather for [1mQaanaaq, GL[0;0m
    
    [1mRequesting weather for city # 18[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hilo,US
       recording weather for [1mHilo, US[0;0m
    
    [1mRequesting weather for city # 19[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Victoria,SC
       recording weather for [1mVictoria, SC[0;0m
    
    [1mRequesting weather for city # 20[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sioux%20Lookout,CA
       recording weather for [1mSioux Lookout, CA[0;0m
    
    [1mRequesting weather for city # 21[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cape%20Town,ZA
       recording weather for [1mCape Town, ZA[0;0m
    
    [1mRequesting weather for city # 22[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atuona,PF
       recording weather for [1mAtuona, PF[0;0m
    
    [1mRequesting weather for city # 23[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Havoysund,NO
       recording weather for [1mHavoysund, NO[0;0m
    
    [1mRequesting weather for city # 24[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hermanus,ZA
       recording weather for [1mHermanus, ZA[0;0m
    
    [1mRequesting weather for city # 25[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Piacabucu,BR
       recording weather for [1mPiacabucu, BR[0;0m
    
    [1mRequesting weather for city # 26[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nelson%20Bay,AU
       recording weather for [1mNelson Bay, AU[0;0m
    
    [1mRequesting weather for city # 27[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lumut,MY
       recording weather for [1mLumut, MY[0;0m
    
    [1mRequesting weather for city # 28[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Talnakh,RU
       recording weather for [1mTalnakh, RU[0;0m
    
    [1mRequesting weather for city # 29[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pedernales,DO
       recording weather for [1mPedernales, DO[0;0m
    
    [1mRequesting weather for city # 30[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cabo%20San%20Lucas,MX
       recording weather for [1mCabo San Lucas, MX[0;0m
    
    [1mRequesting weather for city # 31[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aksu,KZ
       recording weather for [1mAksu, KZ[0;0m
    
    [1mRequesting weather for city # 32[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint%20George,BM
       recording weather for [1mSaint George, BM[0;0m
    
    [1mRequesting weather for city # 33[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vaini,TO
       recording weather for [1mVaini, TO[0;0m
    
    [1mRequesting weather for city # 34[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 34[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Ayora,EC
       recording weather for [1mPuerto Ayora, EC[0;0m
    
    [1mRequesting weather for city # 35[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hobart,AU
       recording weather for [1mHobart, AU[0;0m
    
    [1mRequesting weather for city # 36[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kisangani,CD
       recording weather for [1mKisangani, CD[0;0m
    
    [1mRequesting weather for city # 37[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kapaa,US
       recording weather for [1mKapaa, US[0;0m
    
    [1mRequesting weather for city # 38[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Albany,AU
       recording weather for [1mAlbany, AU[0;0m
    
    [1mRequesting weather for city # 39[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Denpasar,ID
       recording weather for [1mDenpasar, ID[0;0m
    
    [1mRequesting weather for city # 40[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Den%20Helder,NL
       recording weather for [1mDen Helder, NL[0;0m
    
    [1mRequesting weather for city # 41[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhniy%20Tsasuchey,RU
       recording weather for [1mNizhniy Tsasuchey, RU[0;0m
    
    [1mRequesting weather for city # 42[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Husavik,IS
       recording weather for [1mHusavik, IS[0;0m
    
    [1mRequesting weather for city # 43[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nguiu,AU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 43[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santa%20Helena%20De%20Goias,BR
       recording weather for [1mSanta Helena de Goias, BR[0;0m
    
    [1mRequesting weather for city # 44[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ocu,PA
       recording weather for [1mOcu, PA[0;0m
    
    [1mRequesting weather for city # 45[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bathsheba,BB
       recording weather for [1mBathsheba, BB[0;0m
    
    [1mRequesting weather for city # 46[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Maceio,BR
       recording weather for [1mMaceio, BR[0;0m
    
    [1mRequesting weather for city # 47[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nanortalik,GL
       recording weather for [1mNanortalik, GL[0;0m
    
    [1mRequesting weather for city # 48[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 48[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bambous%20Virieux,MU
       recording weather for [1mBambous Virieux, MU[0;0m
    
    [1mRequesting weather for city # 49[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Busselton,AU
       recording weather for [1mBusselton, AU[0;0m
    
    [1mRequesting weather for city # 50[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 50[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sobolevo,RU
       recording weather for [1mSobolevo, RU[0;0m
    
    [1mRequesting weather for city # 51[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 51[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hithadhoo,MV
       recording weather for [1mHithadhoo, MV[0;0m
    
    [1mRequesting weather for city # 52[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 52[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Butaritari,KI
       recording weather for [1mButaritari, KI[0;0m
    
    [1mRequesting weather for city # 53[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vredendal,ZA
       recording weather for [1mVredendal, ZA[0;0m
    
    [1mRequesting weather for city # 54[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ningyang,CN
       recording weather for [1mNingyang, CN[0;0m
    
    [1mRequesting weather for city # 55[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Thompson,CA
       recording weather for [1mThompson, CA[0;0m
    
    [1mRequesting weather for city # 56[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=New%20Norfolk,AU
       recording weather for [1mNew Norfolk, AU[0;0m
    
    [1mRequesting weather for city # 57[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 57[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Manadhoo,MV
       recording weather for [1mManadhoo, MV[0;0m
    
    [1mRequesting weather for city # 58[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kaitangata,NZ
       recording weather for [1mKaitangata, NZ[0;0m
    
    [1mRequesting weather for city # 59[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ilulissat,GL
       recording weather for [1mIlulissat, GL[0;0m
    
    [1mRequesting weather for city # 60[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bluff,NZ
       recording weather for [1mBluff, NZ[0;0m
    
    [1mRequesting weather for city # 61[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ancud,CL
       recording weather for [1mAncud, CL[0;0m
    
    [1mRequesting weather for city # 62[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nikolskoye,RU
       recording weather for [1mNikolskoye, RU[0;0m
    
    [1mRequesting weather for city # 63[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Damghan,IR
       recording weather for [1mDamghan, IR[0;0m
    
    [1mRequesting weather for city # 64[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mastic%20Beach,US
       recording weather for [1mMastic Beach, US[0;0m
    
    [1mRequesting weather for city # 65[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Elizabeth,ZA
       recording weather for [1mPort Elizabeth, ZA[0;0m
    
    [1mRequesting weather for city # 66[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 66[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Awbari,LY
       recording weather for [1mAwbari, LY[0;0m
    
    [1mRequesting weather for city # 67[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Manono,CD
       recording weather for [1mManono, CD[0;0m
    
    [1mRequesting weather for city # 68[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Colares,PT
       recording weather for [1mColares, PT[0;0m
    
    [1mRequesting weather for city # 69[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grindavik,IS
       recording weather for [1mGrindavik, IS[0;0m
    
    [1mRequesting weather for city # 70[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Carnarvon,AU
       recording weather for [1mCarnarvon, AU[0;0m
    
    [1mRequesting weather for city # 71[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Upernavik,GL
       recording weather for [1mUpernavik, GL[0;0m
    
    [1mRequesting weather for city # 72[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sitka,US
       recording weather for [1mSitka, US[0;0m
    
    [1mRequesting weather for city # 73[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 73[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Punta%20Arenas,CL
       recording weather for [1mPunta Arenas, CL[0;0m
    
    [1mRequesting weather for city # 74[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 74[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sakakah,SA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 74[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sangod,IN
       recording weather for [1mSangod, IN[0;0m
    
    [1mRequesting weather for city # 75[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Escondido,MX
       recording weather for [1mPuerto Escondido, MX[0;0m
    
    [1mRequesting weather for city # 76[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 76[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Khatanga,RU
       recording weather for [1mKhatanga, RU[0;0m
    
    [1mRequesting weather for city # 77[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rafraf,TN
       recording weather for [1mRafraf, TN[0;0m
    
    [1mRequesting weather for city # 78[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 78[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 78[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 78[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 78[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Coquimbo,CL
       recording weather for [1mCoquimbo, CL[0;0m
    
    [1mRequesting weather for city # 79[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Waipawa,NZ
       recording weather for [1mWaipawa, NZ[0;0m
    
    [1mRequesting weather for city # 80[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       recording weather for [1mMar del Plata, AR[0;0m
    
    [1mRequesting weather for city # 81[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Guadalupe%20Y%20Calvo,MX
       recording weather for [1mGuadalupe y Calvo, MX[0;0m
    
    [1mRequesting weather for city # 82[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bredasdorp,ZA
       recording weather for [1mBredasdorp, ZA[0;0m
    
    [1mRequesting weather for city # 83[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 83[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tasiilaq,GL
       recording weather for [1mTasiilaq, GL[0;0m
    
    [1mRequesting weather for city # 84[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ostrovnoy,RU
       recording weather for [1mOstrovnoy, RU[0;0m
    
    [1mRequesting weather for city # 85[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sarangani,PH
       recording weather for [1mSarangani, PH[0;0m
    
    [1mRequesting weather for city # 86[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 86[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Axim,GH
       recording weather for [1mAxim, GH[0;0m
    
    [1mRequesting weather for city # 87[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Shilovo,RU
       recording weather for [1mShilovo, RU[0;0m
    
    [1mRequesting weather for city # 88[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20Gaube,MU
       recording weather for [1mGrand Gaube, MU[0;0m
    
    [1mRequesting weather for city # 89[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Berlevag,NO
       recording weather for [1mBerlevag, NO[0;0m
    
    [1mRequesting weather for city # 90[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Castro,CL
       recording weather for [1mCastro, CL[0;0m
    
    [1mRequesting weather for city # 91[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 91[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ouesso,CG
       recording weather for [1mOuesso, CG[0;0m
    
    [1mRequesting weather for city # 92[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 92[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nemuro,JP
       recording weather for [1mNemuro, JP[0;0m
    
    [1mRequesting weather for city # 93[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Erzin,RU
       recording weather for [1mErzin, RU[0;0m
    
    [1mRequesting weather for city # 94[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alofi,NU
       recording weather for [1mAlofi, NU[0;0m
    
    [1mRequesting weather for city # 95[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Beringovskiy,RU
       recording weather for [1mBeringovskiy, RU[0;0m
    
    [1mRequesting weather for city # 96[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rovaniemi,FI
       recording weather for [1mRovaniemi, FI[0;0m
    
    [1mRequesting weather for city # 97[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kuche,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 97[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Richards%20Bay,ZA
       recording weather for [1mRichards Bay, ZA[0;0m
    
    [1mRequesting weather for city # 98[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lasa,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 98[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 98[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Am%20Timan,TD
       recording weather for [1mAm Timan, TD[0;0m
    
    [1mRequesting weather for city # 99[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mandalgovi,MN
       recording weather for [1mMandalgovi, MN[0;0m
    
    [1mRequesting weather for city # 100[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lander,US
       recording weather for [1mLander, US[0;0m
    
    [1mRequesting weather for city # 101[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dikson,RU
       recording weather for [1mDikson, RU[0;0m
    
    [1mRequesting weather for city # 102[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       recording weather for [1mArraial do Cabo, BR[0;0m
    
    [1mRequesting weather for city # 103[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yaan,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 103[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 103[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yellowknife,CA
       recording weather for [1mYellowknife, CA[0;0m
    
    [1mRequesting weather for city # 104[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Angola,US
       recording weather for [1mAngola, US[0;0m
    
    [1mRequesting weather for city # 105[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kropotkin,RU
       recording weather for [1mKropotkin, RU[0;0m
    
    [1mRequesting weather for city # 106[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kostino,RU
       recording weather for [1mKostino, RU[0;0m
    
    [1mRequesting weather for city # 107[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bengkulu,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 107[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saleaula,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 107[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Buchanan,LR
       recording weather for [1mBuchanan, LR[0;0m
    
    [1mRequesting weather for city # 108[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gerash,IR
       recording weather for [1mGerash, IR[0;0m
    
    [1mRequesting weather for city # 109[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Buenos%20Aires,CR
       recording weather for [1mBuenos Aires, CR[0;0m
    
    [1mRequesting weather for city # 110[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vyshhorod,UA
       recording weather for [1mVyshhorod, UA[0;0m
    
    [1mRequesting weather for city # 111[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Escanaba,US
       recording weather for [1mEscanaba, US[0;0m
    
    [1mRequesting weather for city # 112[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Narsaq,GL
       recording weather for [1mNarsaq, GL[0;0m
    
    [1mRequesting weather for city # 113[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Halifax,CA
       recording weather for [1mHalifax, CA[0;0m
    
    [1mRequesting weather for city # 114[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tiksi,RU
       recording weather for [1mTiksi, RU[0;0m
    
    [1mRequesting weather for city # 115[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Alfred,ZA
       recording weather for [1mPort Alfred, ZA[0;0m
    
    [1mRequesting weather for city # 116[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Severo-Kurilsk,RU
       recording weather for [1mSevero-Kurilsk, RU[0;0m
    
    [1mRequesting weather for city # 117[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gazanjyk,TM
       recording weather for [1mGazanjyk, TM[0;0m
    
    [1mRequesting weather for city # 118[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Salto,UY
       recording weather for [1mSalto, UY[0;0m
    
    [1mRequesting weather for city # 119[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Skjervoy,NO
       recording weather for [1mSkjervoy, NO[0;0m
    
    [1mRequesting weather for city # 120[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Acuitzio,MX
       recording weather for [1mAcuitzio, MX[0;0m
    
    [1mRequesting weather for city # 121[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kenai,US
       recording weather for [1mKenai, US[0;0m
    
    [1mRequesting weather for city # 122[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Moose%20Factory,CA
       recording weather for [1mMoose Factory, CA[0;0m
    
    [1mRequesting weather for city # 123[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sayyan,YE
       recording weather for [1mSayyan, YE[0;0m
    
    [1mRequesting weather for city # 124[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 124[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Umm%20Lajj,SA
       recording weather for [1mUmm Lajj, SA[0;0m
    
    [1mRequesting weather for city # 125[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ulagan,RU
       recording weather for [1mUlagan, RU[0;0m
    
    [1mRequesting weather for city # 126[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tam%20Ky,VN
       recording weather for [1mTam Ky, VN[0;0m
    
    [1mRequesting weather for city # 127[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ajdabiya,LY
       recording weather for [1mAjdabiya, LY[0;0m
    
    [1mRequesting weather for city # 128[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Xining,CN
       recording weather for [1mXining, CN[0;0m
    
    [1mRequesting weather for city # 129[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chagda,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 129[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yerbogachen,RU
       recording weather for [1mYerbogachen, RU[0;0m
    
    [1mRequesting weather for city # 130[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Olafsvik,IS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 130[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Longavi,CL
       recording weather for [1mLongavi, CL[0;0m
    
    [1mRequesting weather for city # 131[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Cortes,HN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 131[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mount%20Isa,AU
       recording weather for [1mMount Isa, AU[0;0m
    
    [1mRequesting weather for city # 132[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Norman%20Wells,CA
       recording weather for [1mNorman Wells, CA[0;0m
    
    [1mRequesting weather for city # 133[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mount%20Gambier,AU
       recording weather for [1mMount Gambier, AU[0;0m
    
    [1mRequesting weather for city # 134[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yulara,AU
       recording weather for [1mYulara, AU[0;0m
    
    [1mRequesting weather for city # 135[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Senanga,ZM
       recording weather for [1mSenanga, ZM[0;0m
    
    [1mRequesting weather for city # 136[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 136[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lebu,CL
       recording weather for [1mLebu, CL[0;0m
    
    [1mRequesting weather for city # 137[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kano,NG
       recording weather for [1mKano, NG[0;0m
    
    [1mRequesting weather for city # 138[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ahipara,NZ
       recording weather for [1mAhipara, NZ[0;0m
    
    [1mRequesting weather for city # 139[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Prainha,BR
       recording weather for [1mPrainha, BR[0;0m
    
    [1mRequesting weather for city # 140[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Portland,AU
       recording weather for [1mPortland, AU[0;0m
    
    [1mRequesting weather for city # 141[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 141[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Camacha,PT
       recording weather for [1mCamacha, PT[0;0m
    
    [1mRequesting weather for city # 142[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Novyy%20Urengoy,RU
       recording weather for [1mNovyy Urengoy, RU[0;0m
    
    [1mRequesting weather for city # 143[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pousat,KH
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 143[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Quatre%20Cocos,MU
       recording weather for [1mQuatre Cocos, MU[0;0m
    
    [1mRequesting weather for city # 144[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Douentza,ML
       recording weather for [1mDouentza, ML[0;0m
    
    [1mRequesting weather for city # 145[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 145[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 145[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barrow,US
       recording weather for [1mBarrow, US[0;0m
    
    [1mRequesting weather for city # 146[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Burica,PA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 146[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sentyabrskiy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 146[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Isangel,VU
       recording weather for [1mIsangel, VU[0;0m
    
    [1mRequesting weather for city # 147[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vestmannaeyjar,IS
       recording weather for [1mVestmannaeyjar, IS[0;0m
    
    [1mRequesting weather for city # 148[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 148[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nioro,ML
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 148[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tazovskiy,RU
       recording weather for [1mTazovskiy, RU[0;0m
    
    [1mRequesting weather for city # 149[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Meyungs,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 149[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Duluth,US
       recording weather for [1mDuluth, US[0;0m
    
    [1mRequesting weather for city # 150[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 150[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hit,IQ
       recording weather for [1mHit, IQ[0;0m
    
    [1mRequesting weather for city # 151[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Avarua,CK
       recording weather for [1mAvarua, CK[0;0m
    
    [1mRequesting weather for city # 152[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 152[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kavaratti,IN
       recording weather for [1mKavaratti, IN[0;0m
    
    [1mRequesting weather for city # 153[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dakar,SN
       recording weather for [1mDakar, SN[0;0m
    
    [1mRequesting weather for city # 154[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Necochea,AR
       recording weather for [1mNecochea, AR[0;0m
    
    [1mRequesting weather for city # 155[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sao%20Filipe,CV
       recording weather for [1mSao Filipe, CV[0;0m
    
    [1mRequesting weather for city # 156[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pasni,PK
       recording weather for [1mPasni, PK[0;0m
    
    [1mRequesting weather for city # 157[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nam%20Tha,LA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 157[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nuuk,GL
       recording weather for [1mNuuk, GL[0;0m
    
    [1mRequesting weather for city # 158[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 158[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Garden%20City,US
       recording weather for [1mGarden City, US[0;0m
    
    [1mRequesting weather for city # 159[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Porto%20Nacional,BR
       recording weather for [1mPorto Nacional, BR[0;0m
    
    [1mRequesting weather for city # 160[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tuatapere,NZ
       recording weather for [1mTuatapere, NZ[0;0m
    
    [1mRequesting weather for city # 161[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pilar,PH
       recording weather for [1mPilar, PH[0;0m
    
    [1mRequesting weather for city # 162[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Namatanai,PG
       recording weather for [1mNamatanai, PG[0;0m
    
    [1mRequesting weather for city # 163[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Auki,SB
       recording weather for [1mAuki, SB[0;0m
    
    [1mRequesting weather for city # 164[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santa%20Barbara,US
       recording weather for [1mSanta Barbara, US[0;0m
    
    [1mRequesting weather for city # 165[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 165[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Buala,SB
       recording weather for [1mBuala, SB[0;0m
    
    [1mRequesting weather for city # 166[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Faanui,PF
       recording weather for [1mFaanui, PF[0;0m
    
    [1mRequesting weather for city # 167[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pemangkat,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 167[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Pirie,AU
       recording weather for [1mPort Pirie, AU[0;0m
    
    [1mRequesting weather for city # 168[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Korla,CN
       recording weather for [1mKorla, CN[0;0m
    
    [1mRequesting weather for city # 169[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Praia%20Da%20Vitoria,PT
       recording weather for [1mPraia da Vitoria, PT[0;0m
    
    [1mRequesting weather for city # 170[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cagayan%20De%20Tawi-Tawi,PH
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 170[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Georgetown,SH
       recording weather for [1mGeorgetown, SH[0;0m
    
    [1mRequesting weather for city # 171[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Hardy,CA
       recording weather for [1mPort Hardy, CA[0;0m
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Palabuhanratu,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mrirt,MA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 172[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Poltavka,RU
       recording weather for [1mPoltavka, RU[0;0m
    
    [1mRequesting weather for city # 173[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Marawi,SD
       recording weather for [1mMarawi, SD[0;0m
    
    [1mRequesting weather for city # 174[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 174[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saldanha,ZA
       recording weather for [1mSaldanha, ZA[0;0m
    
    [1mRequesting weather for city # 175[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Egvekinot,RU
       recording weather for [1mEgvekinot, RU[0;0m
    
    [1mRequesting weather for city # 176[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ossora,RU
       recording weather for [1mOssora, RU[0;0m
    
    [1mRequesting weather for city # 177[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Uray,RU
       recording weather for [1mUray, RU[0;0m
    
    [1mRequesting weather for city # 178[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Attawapiskat,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 178[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dahod,IN
       recording weather for [1mDahod, IN[0;0m
    
    [1mRequesting weather for city # 179[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kutum,SD
       recording weather for [1mKutum, SD[0;0m
    
    [1mRequesting weather for city # 180[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kargala,RU
       recording weather for [1mKargala, RU[0;0m
    
    [1mRequesting weather for city # 181[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 181[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kodiak,US
       recording weather for [1mKodiak, US[0;0m
    
    [1mRequesting weather for city # 182[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Katsuura,JP
       recording weather for [1mKatsuura, JP[0;0m
    
    [1mRequesting weather for city # 183[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 183[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mandal,NO
       recording weather for [1mMandal, NO[0;0m
    
    [1mRequesting weather for city # 184[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mayo,CA
       recording weather for [1mMayo, CA[0;0m
    
    [1mRequesting weather for city # 185[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saskylakh,RU
       recording weather for [1mSaskylakh, RU[0;0m
    
    [1mRequesting weather for city # 186[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nardaran,AZ
       recording weather for [1mNardaran, AZ[0;0m
    
    [1mRequesting weather for city # 187[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 187[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Koygorodok,RU
       recording weather for [1mKoygorodok, RU[0;0m
    
    [1mRequesting weather for city # 188[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 188[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Madero,MX
       recording weather for [1mPuerto Madero, MX[0;0m
    
    [1mRequesting weather for city # 189[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 189[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sanok,PL
       recording weather for [1mSanok, PL[0;0m
    
    [1mRequesting weather for city # 190[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Guaruja,BR
       recording weather for [1mGuaruja, BR[0;0m
    
    [1mRequesting weather for city # 191[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lata,SB
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 191[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kulunda,RU
       recording weather for [1mKulunda, RU[0;0m
    
    [1mRequesting weather for city # 192[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chokurdakh,RU
       recording weather for [1mChokurdakh, RU[0;0m
    
    [1mRequesting weather for city # 193[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 193[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Iqaluit,CA
       recording weather for [1mIqaluit, CA[0;0m
    
    [1mRequesting weather for city # 194[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belokurikha,RU
       recording weather for [1mBelokurikha, RU[0;0m
    
    [1mRequesting weather for city # 195[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Volterra,IT
       recording weather for [1mVolterra, IT[0;0m
    
    [1mRequesting weather for city # 196[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lakes%20Entrance,AU
       recording weather for [1mLakes Entrance, AU[0;0m
    
    [1mRequesting weather for city # 197[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       recording weather for [1mPonta do Sol, CV[0;0m
    
    [1mRequesting weather for city # 198[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Batagay-Alyta,RU
       recording weather for [1mBatagay-Alyta, RU[0;0m
    
    [1mRequesting weather for city # 199[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tecoanapa,MX
       recording weather for [1mTecoanapa, MX[0;0m
    
    [1mRequesting weather for city # 200[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pisco,PE
       recording weather for [1mPisco, PE[0;0m
    
    [1mRequesting weather for city # 201[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Half%20Moon%20Bay,US
       recording weather for [1mHalf Moon Bay, US[0;0m
    
    [1mRequesting weather for city # 202[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Omsukchan,RU
       recording weather for [1mOmsukchan, RU[0;0m
    
    [1mRequesting weather for city # 203[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Torbay,CA
       recording weather for [1mTorbay, CA[0;0m
    
    [1mRequesting weather for city # 204[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santiago%20Del%20Estero,AR
       recording weather for [1mSantiago del Estero, AR[0;0m
    
    [1mRequesting weather for city # 205[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Orgun,AF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 205[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sao%20Joao%20Da%20Barra,BR
       recording weather for [1mSao Joao da Barra, BR[0;0m
    
    [1mRequesting weather for city # 206[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bilma,NE
       recording weather for [1mBilma, NE[0;0m
    
    [1mRequesting weather for city # 207[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 207[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Las%20Rosas,MX
       recording weather for [1mLas Rosas, MX[0;0m
    
    [1mRequesting weather for city # 208[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pevek,RU
       recording weather for [1mPevek, RU[0;0m
    
    [1mRequesting weather for city # 209[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Clyde%20River,CA
       recording weather for [1mClyde River, CA[0;0m
    
    [1mRequesting weather for city # 210[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 210[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Quimper,FR
       recording weather for [1mQuimper, FR[0;0m
    
    [1mRequesting weather for city # 211[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 211[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Salalah,OM
       recording weather for [1mSalalah, OM[0;0m
    
    [1mRequesting weather for city # 212[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Soavinandriana,MG
       recording weather for [1mSoavinandriana, MG[0;0m
    
    [1mRequesting weather for city # 213[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Batemans%20Bay,AU
       recording weather for [1mBatemans Bay, AU[0;0m
    
    [1mRequesting weather for city # 214[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Burica,PA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 214[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Srednekolymsk,RU
       recording weather for [1mSrednekolymsk, RU[0;0m
    
    [1mRequesting weather for city # 215[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kavieng,PG
       recording weather for [1mKavieng, PG[0;0m
    
    [1mRequesting weather for city # 216[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aklavik,CA
       recording weather for [1mAklavik, CA[0;0m
    
    [1mRequesting weather for city # 217[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 217[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cherskiy,RU
       recording weather for [1mCherskiy, RU[0;0m
    
    [1mRequesting weather for city # 218[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Ayacucho,VE
       recording weather for [1mPuerto Ayacucho, VE[0;0m
    
    [1mRequesting weather for city # 219[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Blair,IN
       recording weather for [1mPort Blair, IN[0;0m
    
    [1mRequesting weather for city # 220[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Augusta,AU
       recording weather for [1mPort Augusta, AU[0;0m
    
    [1mRequesting weather for city # 221[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Constitucion,MX
       recording weather for [1mConstitucion, MX[0;0m
    
    [1mRequesting weather for city # 222[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ayer%20Itam,MY
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 222[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Boa%20Vista,BR
       recording weather for [1mBoa Vista, BR[0;0m
    
    [1mRequesting weather for city # 223[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cumaribo,CO
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 223[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Haibowan,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 223[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Palabuhanratu,ID
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 223[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taujica,HN
       recording weather for [1mTaujica, HN[0;0m
    
    [1mRequesting weather for city # 224[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Plettenberg%20Bay,ZA
       recording weather for [1mPlettenberg Bay, ZA[0;0m
    
    [1mRequesting weather for city # 225[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Warwick,AU
       recording weather for [1mWarwick, AU[0;0m
    
    [1mRequesting weather for city # 226[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 226[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 226[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lasa,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 226[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lincoln,GB
       recording weather for [1mLincoln, GB[0;0m
    
    [1mRequesting weather for city # 227[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Impfondo,CG
       recording weather for [1mImpfondo, CG[0;0m
    
    [1mRequesting weather for city # 228[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Paradwip,IN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 228[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lolua,TV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 228[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kieta,PG
       recording weather for [1mKieta, PG[0;0m
    
    [1mRequesting weather for city # 229[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dingle,IE
       recording weather for [1mDingle, IE[0;0m
    
    [1mRequesting weather for city # 230[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Roebourne,AU
       recording weather for [1mRoebourne, AU[0;0m
    
    [1mRequesting weather for city # 231[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vaitupu,WF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 231[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 231[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 231[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Conceicao%20Do%20Araguaia,BR
       recording weather for [1mConceicao do Araguaia, BR[0;0m
    
    [1mRequesting weather for city # 232[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vostok,RU
       recording weather for [1mVostok, RU[0;0m
    
    [1mRequesting weather for city # 233[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Huarmey,PE
       recording weather for [1mHuarmey, PE[0;0m
    
    [1mRequesting weather for city # 234[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Guerrero%20Negro,MX
       recording weather for [1mGuerrero Negro, MX[0;0m
    
    [1mRequesting weather for city # 235[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kirgiz-Miyaki,RU
       recording weather for [1mKirgiz-Miyaki, RU[0;0m
    
    [1mRequesting weather for city # 236[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Comodoro%20Rivadavia,AR
       recording weather for [1mComodoro Rivadavia, AR[0;0m
    
    [1mRequesting weather for city # 237[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Klaksvik,FO
       recording weather for [1mKlaksvik, FO[0;0m
    
    [1mRequesting weather for city # 238[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20Centre,CA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 238[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kondinskoye,RU
       recording weather for [1mKondinskoye, RU[0;0m
    
    [1mRequesting weather for city # 239[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kouroussa,GN
       recording weather for [1mKouroussa, GN[0;0m
    
    [1mRequesting weather for city # 240[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Airai,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 240[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Colesberg,ZA
       recording weather for [1mColesberg, ZA[0;0m
    
    [1mRequesting weather for city # 241[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       Arraial do Cabo, BR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 241[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 241[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dzidzantun,MX
       recording weather for [1mDzidzantun, MX[0;0m
    
    [1mRequesting weather for city # 242[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bahia%20Blanca,AR
       recording weather for [1mBahia Blanca, AR[0;0m
    
    [1mRequesting weather for city # 243[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Verkhnyaya%20Inta,RU
       recording weather for [1mVerkhnyaya Inta, RU[0;0m
    
    [1mRequesting weather for city # 244[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 244[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Saint-Pierre,PM
       recording weather for [1mSaint-Pierre, PM[0;0m
    
    [1mRequesting weather for city # 245[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Palmer,US
       recording weather for [1mPalmer, US[0;0m
    
    [1mRequesting weather for city # 246[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kuytun,CN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 246[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Walcz,PL
       recording weather for [1mWalcz, PL[0;0m
    
    [1mRequesting weather for city # 247[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sabzevar,IR
       recording weather for [1mSabzevar, IR[0;0m
    
    [1mRequesting weather for city # 248[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bonthe,SL
       recording weather for [1mBonthe, SL[0;0m
    
    [1mRequesting weather for city # 249[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Coihueco,CL
       recording weather for [1mCoihueco, CL[0;0m
    
    [1mRequesting weather for city # 250[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pelym,RU
       recording weather for [1mPelym, RU[0;0m
    
    [1mRequesting weather for city # 251[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hartford,US
       recording weather for [1mHartford, US[0;0m
    
    [1mRequesting weather for city # 252[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 252[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hofn,IS
       recording weather for [1mHofn, IS[0;0m
    
    [1mRequesting weather for city # 253[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sebinkarahisar,TR
       recording weather for [1mSebinkarahisar, TR[0;0m
    
    [1mRequesting weather for city # 254[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vallenar,CL
       recording weather for [1mVallenar, CL[0;0m
    
    [1mRequesting weather for city # 255[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zhoucheng,CN
       recording weather for [1mZhoucheng, CN[0;0m
    
    [1mRequesting weather for city # 256[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port-Gentil,GA
       recording weather for [1mPort-Gentil, GA[0;0m
    
    [1mRequesting weather for city # 257[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 257[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Payson,US
       recording weather for [1mPayson, US[0;0m
    
    [1mRequesting weather for city # 258[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sitges,ES
       recording weather for [1mSitges, ES[0;0m
    
    [1mRequesting weather for city # 259[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ambovombe,MG
       recording weather for [1mAmbovombe, MG[0;0m
    
    [1mRequesting weather for city # 260[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vila%20Franca%20Do%20Campo,PT
       recording weather for [1mVila Franca do Campo, PT[0;0m
    
    [1mRequesting weather for city # 261[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pankovka,RU
       recording weather for [1mPankovka, RU[0;0m
    
    [1mRequesting weather for city # 262[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Leningradskiy,RU
       recording weather for [1mLeningradskiy, RU[0;0m
    
    [1mRequesting weather for city # 263[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atikokan,CA
       recording weather for [1mAtikokan, CA[0;0m
    
    [1mRequesting weather for city # 264[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bayonet%20Point,US
       recording weather for [1mBayonet Point, US[0;0m
    
    [1mRequesting weather for city # 265[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 265[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Xai-Xai,MZ
       recording weather for [1mXai-Xai, MZ[0;0m
    
    [1mRequesting weather for city # 266[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ceres,ZA
       recording weather for [1mCeres, ZA[0;0m
    
    [1mRequesting weather for city # 267[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Damaturu,NG
       recording weather for [1mDamaturu, NG[0;0m
    
    [1mRequesting weather for city # 268[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 268[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Anzio,IT
       recording weather for [1mAnzio, IT[0;0m
    
    [1mRequesting weather for city # 269[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,PT
       Ponta do Sol, PT has already been added, retrying with different city...
    
    [1mRequesting weather for city # 269[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lavrentiya,RU
       recording weather for [1mLavrentiya, RU[0;0m
    
    [1mRequesting weather for city # 270[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ulaanbaatar,MN
       recording weather for [1mUlaanbaatar, MN[0;0m
    
    [1mRequesting weather for city # 271[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nyakahanga,TZ
       recording weather for [1mNyakahanga, TZ[0;0m
    
    [1mRequesting weather for city # 272[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Boyolangu,ID
       recording weather for [1mBoyolangu, ID[0;0m
    
    [1mRequesting weather for city # 273[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Flinders,AU
       recording weather for [1mFlinders, AU[0;0m
    
    [1mRequesting weather for city # 274[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Elliot%20Lake,CA
       recording weather for [1mElliot Lake, CA[0;0m
    
    [1mRequesting weather for city # 275[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=East%20London,ZA
       recording weather for [1mEast London, ZA[0;0m
    
    [1mRequesting weather for city # 276[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tawau,MY
       recording weather for [1mTawau, MY[0;0m
    
    [1mRequesting weather for city # 277[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fort%20Saint%20James,CA
       recording weather for [1mFort Saint James, CA[0;0m
    
    [1mRequesting weather for city # 278[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pangnirtung,CA
       recording weather for [1mPangnirtung, CA[0;0m
    
    [1mRequesting weather for city # 279[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Susanville,US
       recording weather for [1mSusanville, US[0;0m
    
    [1mRequesting weather for city # 280[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bulgan,MN
       recording weather for [1mBulgan, MN[0;0m
    
    [1mRequesting weather for city # 281[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 281[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Edd,ER
       recording weather for [1mEdd, ER[0;0m
    
    [1mRequesting weather for city # 282[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 282[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lolua,TV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 282[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Esperance,AU
       recording weather for [1mEsperance, AU[0;0m
    
    [1mRequesting weather for city # 283[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kupang,ID
       recording weather for [1mKupang, ID[0;0m
    
    [1mRequesting weather for city # 284[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Manjo,CM
       recording weather for [1mManjo, CM[0;0m
    
    [1mRequesting weather for city # 285[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tungor,RU
       recording weather for [1mTungor, RU[0;0m
    
    [1mRequesting weather for city # 286[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 286[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Goderich,SL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 286[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nicoya,CR
       recording weather for [1mNicoya, CR[0;0m
    
    [1mRequesting weather for city # 287[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mackay,AU
       recording weather for [1mMackay, AU[0;0m
    
    [1mRequesting weather for city # 288[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhnedevitsk,RU
       recording weather for [1mNizhnedevitsk, RU[0;0m
    
    [1mRequesting weather for city # 289[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kamenskoye,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 289[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zaokskiy,RU
       recording weather for [1mZaokskiy, RU[0;0m
    
    [1mRequesting weather for city # 290[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 290[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hay%20River,CA
       recording weather for [1mHay River, CA[0;0m
    
    [1mRequesting weather for city # 291[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       Ponta do Sol, CV has already been added, retrying with different city...
    
    [1mRequesting weather for city # 291[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pilot%20Butte,CA
       recording weather for [1mPilot Butte, CA[0;0m
    
    [1mRequesting weather for city # 292[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hami,CN
       recording weather for [1mHami, CN[0;0m
    
    [1mRequesting weather for city # 293[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Viedma,AR
       recording weather for [1mViedma, AR[0;0m
    
    [1mRequesting weather for city # 294[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 294[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 294[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Takoradi,GH
       recording weather for [1mTakoradi, GH[0;0m
    
    [1mRequesting weather for city # 295[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nguiu,AU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 295[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jasper,CA
       recording weather for [1mJasper, CA[0;0m
    
    [1mRequesting weather for city # 296[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lompoc,US
       recording weather for [1mLompoc, US[0;0m
    
    [1mRequesting weather for city # 297[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Voyvozh,RU
       recording weather for [1mVoyvozh, RU[0;0m
    
    [1mRequesting weather for city # 298[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 298[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kandalaksha,RU
       recording weather for [1mKandalaksha, RU[0;0m
    
    [1mRequesting weather for city # 299[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Caravelas,BR
       recording weather for [1mCaravelas, BR[0;0m
    
    [1mRequesting weather for city # 300[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sur,OM
       recording weather for [1mSur, OM[0;0m
    
    [1mRequesting weather for city # 301[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 301[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       Arraial do Cabo, BR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 301[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ambon,ID
       recording weather for [1mAmbon, ID[0;0m
    
    [1mRequesting weather for city # 302[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 302[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Marsh%20Harbour,BS
       recording weather for [1mMarsh Harbour, BS[0;0m
    
    [1mRequesting weather for city # 303[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Touros,BR
       recording weather for [1mTouros, BR[0;0m
    
    [1mRequesting weather for city # 304[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 304[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Coihaique,CL
       recording weather for [1mCoihaique, CL[0;0m
    
    [1mRequesting weather for city # 305[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nyahururu,KE
       recording weather for [1mNyahururu, KE[0;0m
    
    [1mRequesting weather for city # 306[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pochutla,MX
       recording weather for [1mPochutla, MX[0;0m
    
    [1mRequesting weather for city # 307[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alta%20Floresta,BR
       recording weather for [1mAlta Floresta, BR[0;0m
    
    [1mRequesting weather for city # 308[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Calabozo,VE
       recording weather for [1mCalabozo, VE[0;0m
    
    [1mRequesting weather for city # 309[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gulu,UG
       recording weather for [1mGulu, UG[0;0m
    
    [1mRequesting weather for city # 310[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atlantis,ZA
       recording weather for [1mAtlantis, ZA[0;0m
    
    [1mRequesting weather for city # 311[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Barentsburg,SJ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 311[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=La%20Baule-Escoublac,FR
       recording weather for [1mLa Baule-Escoublac, FR[0;0m
    
    [1mRequesting weather for city # 312[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Senmonorom,KH
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 312[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ayiasos,GR
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 312[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Slave%20Lake,CA
       recording weather for [1mSlave Lake, CA[0;0m
    
    [1mRequesting weather for city # 313[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 313[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Walvis%20Bay,NA
       recording weather for [1mWalvis Bay, NA[0;0m
    
    [1mRequesting weather for city # 314[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tabiauea,KI
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 314[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pozo%20Colorado,PY
       recording weather for [1mPozo Colorado, PY[0;0m
    
    [1mRequesting weather for city # 315[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sola,VU
       recording weather for [1mSola, VU[0;0m
    
    [1mRequesting weather for city # 316[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Provideniya,RU
       recording weather for [1mProvideniya, RU[0;0m
    
    [1mRequesting weather for city # 317[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Daru,PG
       recording weather for [1mDaru, PG[0;0m
    
    [1mRequesting weather for city # 318[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chuy,UY
       recording weather for [1mChuy, UY[0;0m
    
    [1mRequesting weather for city # 319[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,PT
       Ponta do Sol, PT has already been added, retrying with different city...
    
    [1mRequesting weather for city # 319[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Andevoranto,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 319[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hayden,US
       recording weather for [1mHayden, US[0;0m
    
    [1mRequesting weather for city # 320[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 320[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Okato,NZ
       recording weather for [1mOkato, NZ[0;0m
    
    [1mRequesting weather for city # 321[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Lincoln,AU
       recording weather for [1mPort Lincoln, AU[0;0m
    
    [1mRequesting weather for city # 322[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rio%20Grande,BR
       recording weather for [1mRio Grande, BR[0;0m
    
    [1mRequesting weather for city # 323[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gambissara,GM
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 323[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Broome,AU
       recording weather for [1mBroome, AU[0;0m
    
    [1mRequesting weather for city # 324[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ribeira%20Brava,PT
       recording weather for [1mRibeira Brava, PT[0;0m
    
    [1mRequesting weather for city # 325[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Solnechnyy,RU
       recording weather for [1mSolnechnyy, RU[0;0m
    
    [1mRequesting weather for city # 326[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Babanusah,SD
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 326[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Solomenskoye,RU
       recording weather for [1mSolomenskoye, RU[0;0m
    
    [1mRequesting weather for city # 327[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wagar,SD
       recording weather for [1mWagar, SD[0;0m
    
    [1mRequesting weather for city # 328[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dalvik,IS
       recording weather for [1mDalvik, IS[0;0m
    
    [1mRequesting weather for city # 329[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 329[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nouadhibou,MR
       recording weather for [1mNouadhibou, MR[0;0m
    
    [1mRequesting weather for city # 330[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 330[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mahebourg,MU
       recording weather for [1mMahebourg, MU[0;0m
    
    [1mRequesting weather for city # 331[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wiarton,CA
       recording weather for [1mWiarton, CA[0;0m
    
    [1mRequesting weather for city # 332[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 332[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bosaso,SO
       recording weather for [1mBosaso, SO[0;0m
    
    [1mRequesting weather for city # 333[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dibulla,CO
       recording weather for [1mDibulla, CO[0;0m
    
    [1mRequesting weather for city # 334[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Meulaboh,ID
       recording weather for [1mMeulaboh, ID[0;0m
    
    [1mRequesting weather for city # 335[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Estancia,BR
       recording weather for [1mEstancia, BR[0;0m
    
    [1mRequesting weather for city # 336[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Iglesias,IT
       recording weather for [1mIglesias, IT[0;0m
    
    [1mRequesting weather for city # 337[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wadi,IN
       recording weather for [1mWadi, IN[0;0m
    
    [1mRequesting weather for city # 338[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mangan,IN
       recording weather for [1mMangan, IN[0;0m
    
    [1mRequesting weather for city # 339[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kirakira,SB
       recording weather for [1mKirakira, SB[0;0m
    
    [1mRequesting weather for city # 340[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ofunato,JP
       recording weather for [1mOfunato, JP[0;0m
    
    [1mRequesting weather for city # 341[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 341[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kogon,UZ
       recording weather for [1mKogon, UZ[0;0m
    
    [1mRequesting weather for city # 342[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 342[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bagdarin,RU
       recording weather for [1mBagdarin, RU[0;0m
    
    [1mRequesting weather for city # 343[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 343[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kresttsy,RU
       recording weather for [1mKresttsy, RU[0;0m
    
    [1mRequesting weather for city # 344[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 344[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Qinzhou,CN
       recording weather for [1mQinzhou, CN[0;0m
    
    [1mRequesting weather for city # 345[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pervomayskiy,RU
       recording weather for [1mPervomayskiy, RU[0;0m
    
    [1mRequesting weather for city # 346[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Laguna,BR
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 346[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sampit,ID
       recording weather for [1mSampit, ID[0;0m
    
    [1mRequesting weather for city # 347[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Pierre,US
       recording weather for [1mPierre, US[0;0m
    
    [1mRequesting weather for city # 348[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kruisfontein,ZA
       recording weather for [1mKruisfontein, ZA[0;0m
    
    [1mRequesting weather for city # 349[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ribeira%20Grande,PT
       recording weather for [1mRibeira Grande, PT[0;0m
    
    [1mRequesting weather for city # 350[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Menongue,AO
       recording weather for [1mMenongue, AO[0;0m
    
    [1mRequesting weather for city # 351[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Joshimath,IN
       recording weather for [1mJoshimath, IN[0;0m
    
    [1mRequesting weather for city # 352[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 352[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mangrol,IN
       recording weather for [1mMangrol, IN[0;0m
    
    [1mRequesting weather for city # 353[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Athabasca,CA
       recording weather for [1mAthabasca, CA[0;0m
    
    [1mRequesting weather for city # 354[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ixtapa,MX
       recording weather for [1mIxtapa, MX[0;0m
    
    [1mRequesting weather for city # 355[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Garowe,SO
       recording weather for [1mGarowe, SO[0;0m
    
    [1mRequesting weather for city # 356[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wahran,DZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 356[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Harper,LR
       recording weather for [1mHarper, LR[0;0m
    
    [1mRequesting weather for city # 357[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Maniitsoq,GL
       recording weather for [1mManiitsoq, GL[0;0m
    
    [1mRequesting weather for city # 358[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kultuk,RU
       recording weather for [1mKultuk, RU[0;0m
    
    [1mRequesting weather for city # 359[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bethel,US
       recording weather for [1mBethel, US[0;0m
    
    [1mRequesting weather for city # 360[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Codrington,AG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 360[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 360[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lovozero,RU
       recording weather for [1mLovozero, RU[0;0m
    
    [1mRequesting weather for city # 361[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zhangjiakou,CN
       recording weather for [1mZhangjiakou, CN[0;0m
    
    [1mRequesting weather for city # 362[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sentyabrskiy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 362[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tura,RU
       recording weather for [1mTura, RU[0;0m
    
    [1mRequesting weather for city # 363[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Byron%20Bay,AU
       recording weather for [1mByron Bay, AU[0;0m
    
    [1mRequesting weather for city # 364[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bontang,ID
       recording weather for [1mBontang, ID[0;0m
    
    [1mRequesting weather for city # 365[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nexo,DK
       recording weather for [1mNexo, DK[0;0m
    
    [1mRequesting weather for city # 366[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tawnat,MA
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 366[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Valparaiso,CL
       recording weather for [1mValparaiso, CL[0;0m
    
    [1mRequesting weather for city # 367[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 367[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Da%20Nang,VN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 367[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Biak,ID
       recording weather for [1mBiak, ID[0;0m
    
    [1mRequesting weather for city # 368[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Westport,NZ
       recording weather for [1mWestport, NZ[0;0m
    
    [1mRequesting weather for city # 369[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fortuna,US
       recording weather for [1mFortuna, US[0;0m
    
    [1mRequesting weather for city # 370[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Treinta%20Y%20Tres,UY
       recording weather for [1mTreinta y Tres, UY[0;0m
    
    [1mRequesting weather for city # 371[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Winneba,GH
       recording weather for [1mWinneba, GH[0;0m
    
    [1mRequesting weather for city # 372[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kamenskoye,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 372[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Olinda,BR
       recording weather for [1mOlinda, BR[0;0m
    
    [1mRequesting weather for city # 373[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 373[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 373[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bandarbeyla,SO
       recording weather for [1mBandarbeyla, SO[0;0m
    
    [1mRequesting weather for city # 374[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Delgada,PT
       recording weather for [1mPonta Delgada, PT[0;0m
    
    [1mRequesting weather for city # 375[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 375[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 375[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=College,US
       recording weather for [1mCollege, US[0;0m
    
    [1mRequesting weather for city # 376[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Port%20Hedland,AU
       recording weather for [1mPort Hedland, AU[0;0m
    
    [1mRequesting weather for city # 377[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Changuinola,PA
       recording weather for [1mChanguinola, PA[0;0m
    
    [1mRequesting weather for city # 378[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Karla,EE
       recording weather for [1mKarla, EE[0;0m
    
    [1mRequesting weather for city # 379[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ostersund,SE
       recording weather for [1mOstersund, SE[0;0m
    
    [1mRequesting weather for city # 380[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jiuquan,CN
       recording weather for [1mJiuquan, CN[0;0m
    
    [1mRequesting weather for city # 381[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Westerly,US
       recording weather for [1mWesterly, US[0;0m
    
    [1mRequesting weather for city # 382[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ridgecrest,US
       recording weather for [1mRidgecrest, US[0;0m
    
    [1mRequesting weather for city # 383[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sao%20Jose%20Da%20Coroa%20Grande,BR
       recording weather for [1mSao Jose da Coroa Grande, BR[0;0m
    
    [1mRequesting weather for city # 384[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aksarka,RU
       recording weather for [1mAksarka, RU[0;0m
    
    [1mRequesting weather for city # 385[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Igarka,RU
       recording weather for [1mIgarka, RU[0;0m
    
    [1mRequesting weather for city # 386[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Misratah,LY
       recording weather for [1mMisratah, LY[0;0m
    
    [1mRequesting weather for city # 387[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Skibbereen,IE
       recording weather for [1mSkibbereen, IE[0;0m
    
    [1mRequesting weather for city # 388[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Luderitz,NA
       recording weather for [1mLuderitz, NA[0;0m
    
    [1mRequesting weather for city # 389[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 389[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 389[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aripuana,BR
       recording weather for [1mAripuana, BR[0;0m
    
    [1mRequesting weather for city # 390[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Georgiyevka,KZ
       recording weather for [1mGeorgiyevka, KZ[0;0m
    
    [1mRequesting weather for city # 391[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Stykkisholmur,IS
       recording weather for [1mStykkisholmur, IS[0;0m
    
    [1mRequesting weather for city # 392[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 392[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Baisha,CN
       recording weather for [1mBaisha, CN[0;0m
    
    [1mRequesting weather for city # 393[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Camuy,US
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 393[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ayia%20Galini,GR
       recording weather for [1mAyia Galini, GR[0;0m
    
    [1mRequesting weather for city # 394[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Verkhnyaya%20Sysert,RU
       recording weather for [1mVerkhnyaya Sysert, RU[0;0m
    
    [1mRequesting weather for city # 395[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rocha,UY
       recording weather for [1mRocha, UY[0;0m
    
    [1mRequesting weather for city # 396[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=North%20Bend,US
       recording weather for [1mNorth Bend, US[0;0m
    
    [1mRequesting weather for city # 397[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nellikkuppam,IN
       recording weather for [1mNellikkuppam, IN[0;0m
    
    [1mRequesting weather for city # 398[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cutro,IT
       recording weather for [1mCutro, IT[0;0m
    
    [1mRequesting weather for city # 399[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Marzuq,LY
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 399[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,PT
       Ponta do Sol, PT has already been added, retrying with different city...
    
    [1mRequesting weather for city # 399[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Grand%20River%20South%20East,MU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 399[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Namibe,AO
       recording weather for [1mNamibe, AO[0;0m
    
    [1mRequesting weather for city # 400[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kastamonu,TR
       recording weather for [1mKastamonu, TR[0;0m
    
    [1mRequesting weather for city # 401[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mahon,ES
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 401[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tiarei,PF
       recording weather for [1mTiarei, PF[0;0m
    
    [1mRequesting weather for city # 402[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Praya,ID
       recording weather for [1mPraya, ID[0;0m
    
    [1mRequesting weather for city # 403[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Erice,IT
       recording weather for [1mErice, IT[0;0m
    
    [1mRequesting weather for city # 404[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jabinyanah,TN
       recording weather for [1mJabinyanah, TN[0;0m
    
    [1mRequesting weather for city # 405[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lucapa,AO
       recording weather for [1mLucapa, AO[0;0m
    
    [1mRequesting weather for city # 406[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nome,US
       recording weather for [1mNome, US[0;0m
    
    [1mRequesting weather for city # 407[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Banjarmasin,ID
       recording weather for [1mBanjarmasin, ID[0;0m
    
    [1mRequesting weather for city # 408[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bowen,AU
       recording weather for [1mBowen, AU[0;0m
    
    [1mRequesting weather for city # 409[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Magrath,CA
       recording weather for [1mMagrath, CA[0;0m
    
    [1mRequesting weather for city # 410[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Masuri,IN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 410[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dzhusaly,KZ
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 410[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Maun,BW
       recording weather for [1mMaun, BW[0;0m
    
    [1mRequesting weather for city # 411[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Momcilgrad,BG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 411[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sangar,RU
       recording weather for [1mSangar, RU[0;0m
    
    [1mRequesting weather for city # 412[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Deputatskiy,RU
       recording weather for [1mDeputatskiy, RU[0;0m
    
    [1mRequesting weather for city # 413[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Alice%20Springs,AU
       recording weather for [1mAlice Springs, AU[0;0m
    
    [1mRequesting weather for city # 414[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 414[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Doha,KW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 414[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chegdomyn,RU
       recording weather for [1mChegdomyn, RU[0;0m
    
    [1mRequesting weather for city # 415[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 415[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gombong,ID
       recording weather for [1mGombong, ID[0;0m
    
    [1mRequesting weather for city # 416[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Faya,TD
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 416[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Halapitan,PH
       recording weather for [1mHalapitan, PH[0;0m
    
    [1mRequesting weather for city # 417[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Puerto%20Concordia,CO
       recording weather for [1mPuerto Concordia, CO[0;0m
    
    [1mRequesting weather for city # 418[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Arraial%20Do%20Cabo,BR
       Arraial do Cabo, BR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 418[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tessalit,ML
       recording weather for [1mTessalit, ML[0;0m
    
    [1mRequesting weather for city # 419[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sao%20Borja,BR
       recording weather for [1mSao Borja, BR[0;0m
    
    [1mRequesting weather for city # 420[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chapais,CA
       recording weather for [1mChapais, CA[0;0m
    
    [1mRequesting weather for city # 421[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Zeya,RU
       recording weather for [1mZeya, RU[0;0m
    
    [1mRequesting weather for city # 422[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vieksniai,LT
       recording weather for [1mVieksniai, LT[0;0m
    
    [1mRequesting weather for city # 423[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Progreso,MX
       recording weather for [1mProgreso, MX[0;0m
    
    [1mRequesting weather for city # 424[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yinchuan,CN
       recording weather for [1mYinchuan, CN[0;0m
    
    [1mRequesting weather for city # 425[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ondorhaan,MN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 425[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Raton,US
       recording weather for [1mRaton, US[0;0m
    
    [1mRequesting weather for city # 426[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lamar,US
       recording weather for [1mLamar, US[0;0m
    
    [1mRequesting weather for city # 427[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Awjilah,LY
       recording weather for [1mAwjilah, LY[0;0m
    
    [1mRequesting weather for city # 428[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 428[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Turukhansk,RU
       recording weather for [1mTurukhansk, RU[0;0m
    
    [1mRequesting weather for city # 429[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Chicama,PE
       recording weather for [1mChicama, PE[0;0m
    
    [1mRequesting weather for city # 430[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=El%20Balyana,EG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 430[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       Ponta do Sol, CV has already been added, retrying with different city...
    
    [1mRequesting weather for city # 430[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hope,CA
       recording weather for [1mHope, CA[0;0m
    
    [1mRequesting weather for city # 431[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Jose,GT
       recording weather for [1mSan Jose, GT[0;0m
    
    [1mRequesting weather for city # 432[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 432[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sergeyevka,KZ
       recording weather for [1mSergeyevka, KZ[0;0m
    
    [1mRequesting weather for city # 433[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rafaela,AR
       recording weather for [1mRafaela, AR[0;0m
    
    [1mRequesting weather for city # 434[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kawalu,ID
       recording weather for [1mKawalu, ID[0;0m
    
    [1mRequesting weather for city # 435[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Asyut,EG
       recording weather for [1mAsyut, EG[0;0m
    
    [1mRequesting weather for city # 436[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sokolo,ML
       recording weather for [1mSokolo, ML[0;0m
    
    [1mRequesting weather for city # 437[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Carballo,ES
       recording weather for [1mCarballo, ES[0;0m
    
    [1mRequesting weather for city # 438[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Jimenez,MX
       recording weather for [1mJimenez, MX[0;0m
    
    [1mRequesting weather for city # 439[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bababe,MR
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 439[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Bajo%20Baudo,CO
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 439[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Artyk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 439[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Muros,ES
       recording weather for [1mMuros, ES[0;0m
    
    [1mRequesting weather for city # 440[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sentyabrskiy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 440[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Patricio,MX
       recording weather for [1mSan Patricio, MX[0;0m
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 441[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mahibadhoo,MV
       recording weather for [1mMahibadhoo, MV[0;0m
    
    [1mRequesting weather for city # 442[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Rockhampton,AU
       recording weather for [1mRockhampton, AU[0;0m
    
    [1mRequesting weather for city # 443[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 443[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Yumen,CN
       recording weather for [1mYumen, CN[0;0m
    
    [1mRequesting weather for city # 444[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samarai,PG
       recording weather for [1mSamarai, PG[0;0m
    
    [1mRequesting weather for city # 445[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 445[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Geraldton,AU
       recording weather for [1mGeraldton, AU[0;0m
    
    [1mRequesting weather for city # 446[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Beira,MZ
       recording weather for [1mBeira, MZ[0;0m
    
    [1mRequesting weather for city # 447[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nantucket,US
       recording weather for [1mNantucket, US[0;0m
    
    [1mRequesting weather for city # 448[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 448[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Komsomolskiy,RU
       recording weather for [1mKomsomolskiy, RU[0;0m
    
    [1mRequesting weather for city # 449[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 449[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mehamn,NO
       recording weather for [1mMehamn, NO[0;0m
    
    [1mRequesting weather for city # 450[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kovdor,RU
       recording weather for [1mKovdor, RU[0;0m
    
    [1mRequesting weather for city # 451[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dire%20Dawa,ET
       recording weather for [1mDire Dawa, ET[0;0m
    
    [1mRequesting weather for city # 452[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 452[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cayenne,GF
       recording weather for [1mCayenne, GF[0;0m
    
    [1mRequesting weather for city # 453[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Blackwater,AU
       recording weather for [1mBlackwater, AU[0;0m
    
    [1mRequesting weather for city # 454[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taltal,CL
       recording weather for [1mTaltal, CL[0;0m
    
    [1mRequesting weather for city # 455[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 455[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cabedelo,BR
       recording weather for [1mCabedelo, BR[0;0m
    
    [1mRequesting weather for city # 456[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mar%20Del%20Plata,AR
       Mar del Plata, AR has already been added, retrying with different city...
    
    [1mRequesting weather for city # 456[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nuevo%20Progreso,MX
       recording weather for [1mNuevo Progreso, MX[0;0m
    
    [1mRequesting weather for city # 457[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Brae,GB
       recording weather for [1mBrae, GB[0;0m
    
    [1mRequesting weather for city # 458[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Swift%20Current,CA
       recording weather for [1mSwift Current, CA[0;0m
    
    [1mRequesting weather for city # 459[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 459[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Galiwinku,AU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 459[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amurzet,RU
       recording weather for [1mAmurzet, RU[0;0m
    
    [1mRequesting weather for city # 460[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kiruna,SE
       recording weather for [1mKiruna, SE[0;0m
    
    [1mRequesting weather for city # 461[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Fairbanks,US
       recording weather for [1mFairbanks, US[0;0m
    
    [1mRequesting weather for city # 462[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 462[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Riyadh,SA
       recording weather for [1mRiyadh, SA[0;0m
    
    [1mRequesting weather for city # 463[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Charters%20Towers,AU
       recording weather for [1mCharters Towers, AU[0;0m
    
    [1mRequesting weather for city # 464[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Treinta%20Y%20Tres,UY
       Treinta y Tres, UY has already been added, retrying with different city...
    
    [1mRequesting weather for city # 464[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Khotyn,UA
       recording weather for [1mKhotyn, UA[0;0m
    
    [1mRequesting weather for city # 465[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tigil,RU
       recording weather for [1mTigil, RU[0;0m
    
    [1mRequesting weather for city # 466[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=San%20Vicente,AR
       recording weather for [1mSan Vicente, AR[0;0m
    
    [1mRequesting weather for city # 467[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 467[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Padang,ID
       recording weather for [1mPadang, ID[0;0m
    
    [1mRequesting weather for city # 468[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lata,SB
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 468[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mwinilunga,ZM
       recording weather for [1mMwinilunga, ZM[0;0m
    
    [1mRequesting weather for city # 469[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Presidente%20Epitacio,BR
       recording weather for [1mPresidente Epitacio, BR[0;0m
    
    [1mRequesting weather for city # 470[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Gamba,GA
       recording weather for [1mGamba, GA[0;0m
    
    [1mRequesting weather for city # 471[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tilichiki,RU
       recording weather for [1mTilichiki, RU[0;0m
    
    [1mRequesting weather for city # 472[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 472[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Wanning,CN
       recording weather for [1mWanning, CN[0;0m
    
    [1mRequesting weather for city # 473[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ginda,ER
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 473[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kralendijk,AN
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 473[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 473[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ahuimanu,US
       recording weather for [1mAhuimanu, US[0;0m
    
    [1mRequesting weather for city # 474[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Viligili,MV
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 474[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Redmond,US
       recording weather for [1mRedmond, US[0;0m
    
    [1mRequesting weather for city # 475[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Visnes,NO
       recording weather for [1mVisnes, NO[0;0m
    
    [1mRequesting weather for city # 476[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 476[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Aykhal,RU
       recording weather for [1mAykhal, RU[0;0m
    
    [1mRequesting weather for city # 477[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sept-Iles,CA
       recording weather for [1mSept-Iles, CA[0;0m
    
    [1mRequesting weather for city # 478[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mackenzie,CA
       recording weather for [1mMackenzie, CA[0;0m
    
    [1mRequesting weather for city # 479[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Novikovo,RU
       recording weather for [1mNovikovo, RU[0;0m
    
    [1mRequesting weather for city # 480[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Tumannyy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 480[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,PT
       Ponta do Sol, PT has already been added, retrying with different city...
    
    [1mRequesting weather for city # 480[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Marrakesh,MA
       recording weather for [1mMarrakesh, MA[0;0m
    
    [1mRequesting weather for city # 481[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Samusu,WS
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 481[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vanimo,PG
       recording weather for [1mVanimo, PG[0;0m
    
    [1mRequesting weather for city # 482[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Lagoa,PT
       recording weather for [1mLagoa, PT[0;0m
    
    [1mRequesting weather for city # 483[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Laukaa,FI
       recording weather for [1mLaukaa, FI[0;0m
    
    [1mRequesting weather for city # 484[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 484[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 484[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Khonuu,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 484[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Cururupu,BR
       recording weather for [1mCururupu, BR[0;0m
    
    [1mRequesting weather for city # 485[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Amderma,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 485[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Dubrovnik,HR
       recording weather for [1mDubrovnik, HR[0;0m
    
    [1mRequesting weather for city # 486[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Vuktyl,RU
       recording weather for [1mVuktyl, RU[0;0m
    
    [1mRequesting weather for city # 487[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Santa%20Isabel%20Do%20Rio%20Negro,BR
       recording weather for [1mSanta Isabel do Rio Negro, BR[0;0m
    
    [1mRequesting weather for city # 488[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mys%20Shmidta,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 488[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kurilsk,RU
       recording weather for [1mKurilsk, RU[0;0m
    
    [1mRequesting weather for city # 489[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kamenka,RU
       recording weather for [1mKamenka, RU[0;0m
    
    [1mRequesting weather for city # 490[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Belushya%20Guba,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 490[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Akyab,MM
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 490[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nizhneyansk,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 490[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Naze,JP
       recording weather for [1mNaze, JP[0;0m
    
    [1mRequesting weather for city # 491[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sentyabrskiy,RU
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 491[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Airai,PW
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 491[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ilhabela,BR
       recording weather for [1mIlhabela, BR[0;0m
    
    [1mRequesting weather for city # 492[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kendari,ID
       recording weather for [1mKendari, ID[0;0m
    
    [1mRequesting weather for city # 493[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Ponta%20Do%20Sol,CV
       Ponta do Sol, CV has already been added, retrying with different city...
    
    [1mRequesting weather for city # 493[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Hibbing,US
       recording weather for [1mHibbing, US[0;0m
    
    [1mRequesting weather for city # 494[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Kununurra,AU
       recording weather for [1mKununurra, AU[0;0m
    
    [1mRequesting weather for city # 495[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Nokaneng,BW
       recording weather for [1mNokaneng, BW[0;0m
    
    [1mRequesting weather for city # 496[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Sorvag,FO
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 496[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Atambua,ID
       recording weather for [1mAtambua, ID[0;0m
    
    [1mRequesting weather for city # 497[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Novobureyskiy,RU
       recording weather for [1mNovobureyskiy, RU[0;0m
    
    [1mRequesting weather for city # 498[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Illoqqortoormiut,GL
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 498[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Oistins,BB
       recording weather for [1mOistins, BB[0;0m
    
    [1mRequesting weather for city # 499[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Koungou,YT
       recording weather for [1mKoungou, YT[0;0m
    
    [1mRequesting weather for city # 500[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Mataura,PF
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 500[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Taolanaro,MG
       city not found, retrying with different city... 
    
    [1mRequesting weather for city # 500[0;0m
       requested URL: http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=imperial&q=Deloraine,CA
       recording weather for [1mDeloraine, CA[0;0m
    
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
  </tbody>
</table>
</div>




```python
cities_df.head()
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
      <th>0</th>
      <td>Ushuaia</td>
      <td>16.11</td>
      <td>AR</td>
      <td>80</td>
      <td>-54.81</td>
      <td>-68.31</td>
      <td>41.00</td>
      <td>75</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Praia</td>
      <td>17.22</td>
      <td>CV</td>
      <td>68</td>
      <td>14.92</td>
      <td>-23.51</td>
      <td>68.00</td>
      <td>75</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Saint-Philippe</td>
      <td>3.36</td>
      <td>RE</td>
      <td>66</td>
      <td>-21.36</td>
      <td>55.77</td>
      <td>84.20</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Longyearbyen</td>
      <td>18.34</td>
      <td>SJ</td>
      <td>60</td>
      <td>78.22</td>
      <td>15.64</td>
      <td>8.60</td>
      <td>20</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Jamestown</td>
      <td>14.67</td>
      <td>SH</td>
      <td>100</td>
      <td>-15.94</td>
      <td>-5.72</td>
      <td>74.27</td>
      <td>76</td>
    </tr>
  </tbody>
</table>
</div>




```python
#save df to CSV
cities_df.to_csv('weather_data.csv')
```

# Temperature (F) vs. Latitude


```python
# plot initial coordinates to see how the pick is spread
f, ax = plt.subplots(figsize=(20,15))
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c', ax=ax)
m.drawcoastlines(linewidth=0.3)

# draw parallels and meridians
m.drawparallels(np.arange(-90.,91.,30.),labels=[1,1,0,0])
m.drawmeridians(np.arange(-180.,181.,60.),labels=[0,0,1,1])

#create coordinates
lng = cities_df['Longitude'].values
lat = cities_df['Latitude'].values
temps = cities_df['Temperature, imperial'].values
x,y= m(lng, lat)

cax = m.scatter(x,y, latlon=False, c=temps, s=50, cmap='plasma', alpha=1)
cbar = f.colorbar(cax, shrink=0.8)
cbar.set_label('Temperature (°F)', fontsize=18, weight='bold')

plt.title('Temperature (°F) vs. Latitude', fontsize=24, position=(0.5,1.05), weight='bold')
plt.show()
```

    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3222: MatplotlibDeprecationWarning: The ishold function was deprecated in version 2.0.
      b = ax.ishold()
    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3231: MatplotlibDeprecationWarning: axes.hold is deprecated.
        See the API Changes document (http://matplotlib.org/api/api_changes.html)
        for more details.
      ax.hold(b)



![png](output_8_1.png)


# Humidity (%) vs. Latitude


```python
# plot initial coordinates to see how the pick is spread
f, ax = plt.subplots(figsize=(20,15))
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c', ax=ax)
m.drawcoastlines(linewidth=0.3)

# draw parallels and meridians
m.drawparallels(np.arange(-90.,91.,30.),labels=[1,1,0,0])
m.drawmeridians(np.arange(-180.,181.,60.),labels=[0,0,1,1])

#create coordinates
lng = cities_df['Longitude'].values
lat = cities_df['Latitude'].values
humidity = cities_df['Humidity'].values
x,y= m(lng, lat)

cax = m.scatter(x,y, latlon=False, c=humidity, s=50, cmap='plasma', alpha=1)
cbar = f.colorbar(cax, shrink=0.8)
cbar.set_label('Humidity (%)', fontsize=18, weight='bold')

plt.title('Humidity (%) vs. Latitude', fontsize=24, position=(0.5,1.05), weight='bold')
plt.show()
```

    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3222: MatplotlibDeprecationWarning: The ishold function was deprecated in version 2.0.
      b = ax.ishold()
    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3231: MatplotlibDeprecationWarning: axes.hold is deprecated.
        See the API Changes document (http://matplotlib.org/api/api_changes.html)
        for more details.
      ax.hold(b)



![png](output_10_1.png)


# Cloudiness (%) vs. Latitude


```python
# plot initial coordinates to see how the pick is spread
f, ax = plt.subplots(figsize=(20,15))
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c', ax=ax)
m.drawcoastlines(linewidth=0.3)

# draw parallels and meridians
m.drawparallels(np.arange(-90.,91.,30.),labels=[1,1,0,0])
m.drawmeridians(np.arange(-180.,181.,60.),labels=[0,0,1,1])

#create coordinates
lng = cities_df['Longitude'].values
lat = cities_df['Latitude'].values
clouds = cities_df['Clouds'].values
x,y= m(lng, lat)

cax = m.scatter(x,y, latlon=False, c=clouds, s=50, cmap='plasma', alpha=1)
cbar = f.colorbar(cax, shrink=0.8)
cbar.set_label('Clouds (%)', fontsize=18, weight='bold')

plt.title('Cloudiness (%) vs. Latitude', fontsize=24, position=(0.5,1.05), weight='bold')
plt.show()
```

    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3222: MatplotlibDeprecationWarning: The ishold function was deprecated in version 2.0.
      b = ax.ishold()
    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3231: MatplotlibDeprecationWarning: axes.hold is deprecated.
        See the API Changes document (http://matplotlib.org/api/api_changes.html)
        for more details.
      ax.hold(b)



![png](output_12_1.png)


# Wind Speed (mph) vs. Latitude


```python
# plot initial coordinates to see how the pick is spread
f, ax = plt.subplots(figsize=(20,15))
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c', ax=ax)
m.drawcoastlines(linewidth=0.3)

# draw parallels and meridians
m.drawparallels(np.arange(-90.,91.,30.),labels=[1,1,0,0])
m.drawmeridians(np.arange(-180.,181.,60.),labels=[0,0,1,1])

#create coordinates
lng = cities_df['Longitude'].values
lat = cities_df['Latitude'].values
wind = cities_df['Wind Speed MPH'].values
x,y= m(lng, lat)

cax = m.scatter(x,y, latlon=False, c=wind, s=50, cmap='plasma', alpha=1)
cbar = f.colorbar(cax, shrink=0.8)
cbar.set_label('Wind Speed (MPH)', fontsize=18, weight='bold')

plt.title('Wind Speed (MPH) vs. Latitude', fontsize=24, position=(0.5,1.05), weight='bold')
plt.show()
```

    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3222: MatplotlibDeprecationWarning: The ishold function was deprecated in version 2.0.
      b = ax.ishold()
    /Users/yegor/anaconda3/envs/PythonData/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py:3231: MatplotlibDeprecationWarning: axes.hold is deprecated.
        See the API Changes document (http://matplotlib.org/api/api_changes.html)
        for more details.
      ax.hold(b)



![png](output_14_1.png)


# Trends
* Temperatures are higher around equator
* Humidity is higher alongside cost lines and big rivers
* Amount of clouds is about the same around the globe
* Wind speed seems to be all over

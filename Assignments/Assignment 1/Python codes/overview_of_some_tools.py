# -*- coding: utf-8 -*-
"""overview of some tools.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XjHSeAuN7OrYnmN3lUwNfGnCE9iV40zN
"""

!pip install gitpython



# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import os
from git.repo import Repo
import matplotlib.pyplot as plt
import geopandas as gpd
import urllib
import shutil
# %matplotlib inline

# your local folder into which you want to download the covid data
covidfolder = '../../data_external/covid19'

if os.path.isdir(covidfolder): # if repo exists, pull newest data
  repo = Repo(covidfolder)
  repo.remotes.origin.pull()
else: # otherwise, clone from remote
  repo = Repo.clone_from('https://github.com/CSSEGISandData/COVID-19.git', covidfolder)
datadir = repo.working_dir + '/csse_covid_19_data/csse_covid_19_daily_reports'

c = pd.read_csv(datadir+'/03-27-2020.csv')

c.head()

# make a geometry object from Lat, Long geo = gpd.points_from_xy(c['Long_'], c['Lat']) # give the geometry to geopandas together with c gc = gpd.GeoDataFrame(c, geometry=geo) gc.head()

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot();

co = c[c['Province_State']=='Oregon']

# url of the data
census_url = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_500k.zip'
# location of your download
your_download_folder = '../../data_external'
if not os.path.isdir(your_download_folder):
    os.mkdir(your_download_folder)
us_county_file = your_download_folder + '/cb_2018_us_county_500k.zip'
# download if the file doesn't already exist
if not os.path.isfile(us_county_file):
    with urllib.request.urlopen(census_url) as response, open(us_county_file, 'wb') as out_file:
       shutil.copyfileobj(response, out_file)

us_counties = gpd.read_file(f"zip://{us_county_file}")
us_counties.head()

ore = us_counties[us_counties['STATEFP']=='41']
ore.plot();

ore = ore.astype({'GEOID': 'int64'}).rename(columns={'GEOID' : 'FIPS'})
co = co.astype({'FIPS': 'int64'})
orco = pd.merge(ore, co.iloc[:,:-1], on='FIPS')

# plot coloring counties by number of confirmed cases
fig, ax = plt.subplots(figsize=(12, 8))
orco.plot(ax=ax, column='Confirmed', legend=True,
          legend_kwds={'label': '# confimed cases',
                       'orientation':'horizontal'})
# label the counties
for x, y, county in zip(orco['Long_'], orco['Lat'], orco['NAME']):
    ax.text(x, y, county, color='grey')
ax.set_title('Confirmed COVID-19 cases in Oregon as of March 27 2020')
ax.set_xlabel('Latitude'); ax.set_ylabel('Longitude');

base = world.plot(alpha=0.3)
msz = 500 * gc['Confirmed'] / gc['Confirmed'].max()
gc.plot(ax=base, column='Confirmed', markersize=msz, alpha=0.7);
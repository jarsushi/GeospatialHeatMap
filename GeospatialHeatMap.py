# GeospatialHeatMap.py
# Create Heat Map from U.S shapefile and Census Population Data

# Import required libraries
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns


# Convert shapefile into a pandas dataframe and create a "cords" column to hold the shapes geographical points
def read_ShapeFile(sf):
	fields = [i[0] for i in sf.fields][1:]
	records = sf.records()
	shapes = [s.points for s in sf.shapes()]

	df = pd.DataFrame(columns=fields, data=records)
	df["cords"]=shapes

	return df



#Create the color for the heat map and align the data to the 6 color bins
def calc_color(data, color=None):
	if color == 'purple':
		colorScale =['#dadaebFF','#bcbddcF0','#9e9ac8F0','#807dbaF0','#6a51a3F0','#54278fF0']
	elif color == 'green':
		colorScale = ['#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494']
	elif color == 'grey': 
		colorScale = ['#f7f7f7','#d9d9d9','#bdbdbd','#969696','#636363','#252525']
	else:
		colorScale = ['#ffffd4','#fee391','#fec44f','#fe9929','#d95f0e','#993404']
	
	#Calculate the bin for each state
	new_data, bins = pd.qcut(data, 6, retbins=True, labels=list(range(6)))
	colorTone = []
	
	#Assign color to each state
	for val in new_data:
		colorTone.append(colorScale[val]) 

	return colorTone, bins



#Plot map with lim coordinates
def plot_map_fill_multiples_ids_tone(sf, title, state_ids, colorTone, bins, x_lim = None, y_lim = None, figsize=(11,9)):
	fig, ax = plt.subplots(figsize=figsize)
	fig.suptitle(title, fontsize=20)

	#Plot Shapes
	for shape in sf.shapeRecords():
		x = [i[0] for i in shape.shape.points[:]]
		y = [i[1] for i in shape.shape.points[:]]
		ax.plot(x, y, 'black')

	for id in state_ids:
		shape = sf.shape(id)
		x_lon = np.zeros(len(shape.points))
		y_lat = np.zeros(len(shape.points))

		for j in range(len(shape.points)):
			x_lon[j] = shape.points[j][0]
			y_lat[j] = shape.points[j][1]

		#Fill in states with calculated color
		ax.fill(x_lon,y_lat, colorTone[state_ids.index(id)])

	#Limit size of map to Continental United States
	if (x_lim != None) & (y_lim != None):     
	    plt.xlim(x_lim)
	    plt.ylim(y_lim)



#Plot map with selected comunes, using specific color
def plot_land_area_data(sf, title, names, data=None, color=None, x_lim = None, y_lim = None, figsize=(11,9)):
    colorTone, bins = calc_color(data, color)
    df = read_ShapeFile(sf)
    state_ids = []
    for i in names:
    	if len(df[df.NAME == i])>0:
    		state_ids.append(df[df.NAME == i].index.get_values()[0])
    plot_map_fill_multiples_ids_tone(sf, title, state_ids, colorTone, bins, x_lim = x_lim, y_lim = y_lim, figsize=figsize)




pd.set_option('display.max_columns', 50)
sns.set(style="whitegrid")

sf = shp.Reader("./data/tl_2018_us_state.shp")

census18 = pd.read_excel('./data/2018USPopulationData.xlsx')
title = 'Population Distribution of Continental United States'
data = census18.Population
names = census18.State

#Long and Lat limits for the Continental United States
y_lim = (23, 50) 
x_lim = (-128, -65)

plot_land_area_data(sf, title, names, data, x_lim=x_lim, y_lim=y_lim)
plt.show()






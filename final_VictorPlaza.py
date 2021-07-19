import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import wikipedia as wk
import mapbox
from PIL import Image

# Read data in from xlsx file into and pass it to Pandas Dataframe - df
df = pd.read_excel('Volcanoes Dataset.xlsx')

# Create a 'master" dataframe where it is possible to extract only the data necessary for the program
DF1 = pd.DataFrame(df, columns=['Country', 'Volcano_Name', 'Volcano_Type', 'Region', 'Latitude', 'Longitude', 'Elevation', 'Last_Eruption'])

# Sort the data for country and then volcano name
DF1 = DF1.sort_values(by = ['Country', 'Volcano_Name'])

# Lists derived from the "master" dataframe with unique values for possible utilization as the program develops
region_list = sorted(DF1.Region.unique())
country_list = sorted(DF1.Country.unique())
volcano_name_list = sorted(DF1.Volcano_Name.unique())
volcano_type = sorted(DF1.Volcano_Type.unique())

# Setting up a default country and volcano value for data selection from the user for the intro part of the program
default_value_country = country_list.index('United States')
default_value_volcano = volcano_name_list.index('Yellowstone')

# Create a Sidebar for the introduction inputs and map zoom
st.sidebar.header('Introduction Inputs')

# SelectBox with all the volcano countries
# with the country United States selected as default
country_selection = st.sidebar.selectbox('Select a country for the starting point: ', list(country_list), index=default_value_country)

# SelectBox with all the volcanoes
# with the yellowstone selected as default
volcano_selection_wikipedia = st.sidebar.selectbox("Select your favorite volcano for brief description: ", list(volcano_name_list), index=default_value_volcano)

# Streamlit title and an image called volcanoes.jpg
st.title('An Intro to Volcanoes Around the World')
image = Image.open('volcanoes.jpg')
st.image(image)

# SelectBox with all countries to be searched on wikipedia per their volcanoes
st.subheader('What Are Volcanoes?')
description = wk.summary('volcano', sentences=4)
st.write(description)

# SelectBox with all volcanoes to be searched on wikipedia for brief description
st.subheader(f'{volcano_selection_wikipedia} volcano short description:')
volc_result = wk.summary(f'{volcano_selection_wikipedia} Volcano', sentences=3)
st.write(volc_result)

# Slider in the Sidebar for map zoom function from 0 - 6 and default set at 3
zoom = st.sidebar.slider('Map: Zoom Factor', min_value=0, max_value=6, value=3)

# New dataframe that will locate country selected in the SelectBox to be used in the map function
DF2 = DF1[DF1['Country'] == country_selection]


# "Master" dataFrame will be displayed in the intro for visualization of the dataset
st.subheader('Complete Set of Volcanic Information')
st.dataframe(DF1)

# Mapping function that will allow user input to display specific location in the world map
def mapa(DF1, DF2, country_selection):

    # Creates dataframe based on the country selected
    DF2 = DF1[DF1['Country'] == country_selection]
    st.subheader('Global Volcano Map with Tool Tips')

    # Map display from PyDeck to allow for country location
    view_state = pdk.ViewState(latitude=DF2['Latitude'].mean(), longitude=DF2['Longitude'].mean(), zoom=zoom)


    # Scatterplot layer that will populate the volcano location in the map given long/lat and utilize scale and radius for each data point
    map_layer = pdk.Layer('ScatterplotLayer', data=DF1, pickable=True, opacity=0.3, get_position='[Longitude, Latitude]',
                          get_radius=10000, radius_scale=5, get_fill_color=[255,10,2000], )

    # Tool Tip in each data point displaying volcano name, type, elevation and location
    tool_tip = {"html":"<b>Volcano Name:</b><br/> {Volcano_Name} <b><br/>Volcano Type:</b><br/> {Volcano_Type} <br/>Elevation: {Elevation} <br/>Lat: {Latitude} <br/>Long: {Longitude}",
                "style": {"backgroundColor":"blue steel", "color": "white"}}

    # Mapa is teh variable that uses the previous inputs for the final map creation
    mapa = pdk.Deck(map_style='mapbox://styles/mapbox/outdoors-v11', layers=[map_layer], initial_view_state=view_state, tooltip=tool_tip)
    #map_style='mapbox://styles/mapbox/outdoors-v11',

    # Create and initialize the map
    st.pydeck_chart(mapa)

# Line 107-114 will display data table with count of every volcano in each country by grouping the "master" dataframe by country
st.subheader('Number of Volcanoes per Country')
DF5 = DF1[['Country', 'Elevation']].groupby(by = "Country").count()
# Allows for the replacement of the created index (country name) with a list of numbers index
DF5.reset_index(inplace=True)
# Renames the count column from a dummy column names elevation to the count
DF5.rename(columns= {'Elevation':"Number of Volcanoes"}, inplace=True)
st.dataframe(DF5)

# Displays the map function
mapa(DF1, DF2, country_selection)


def piechart(DF1, country_selection):

    # The loop below allows for the creation of a dictionary with the volcano type count of each selected country
    volc_type_count = {}

    for type in DF1['Volcano_Type']:
        if type not in volc_type_count:
            volc_type_count[type] = 1
        else:
            volc_type_count[type] += 1

    # Separates the keys from the dictionary as labels and the values as size/count
    label = volc_type_count.keys()
    size = volc_type_count.values()

    fig, ax = plt.subplots()
    fig.tight_layout()

    ax.pie(size, labels=label, autopct='%.1f%%', shadow=True, startangle=120)

    ax.axis('equal')

    ax.set_title(f'Distinct Volcano Types in {country_selection}')

    fig.tight_layout()

    st.pyplot(fig)

'''

'''

def lineplot(DF1, country_selection):

    # Line chart that will display up tot he top 10 tallest volcanoes in the selected country for analysis
    x = np.arange(len(DF1))

    fig, ax = plt.subplots()

    elevation = ax.bar(x, DF1['Elevation'], color='maroon')


    ax.set_ylabel('Elevation', fontname='Comic Sans MS', fontsize = 10)
    ax.set_title(f'Tallest Volcanoes in {country_selection}', fontname='Comic Sans MS', fontsize = 20)
    ax.set_xlabel('Volcano Name', fontname='Comic Sans MS', fontsize = 10)
    ax.set_xticks(x)
    ax.set_xticklabels(DF1['Volcano_Name'], rotation='30', fontname='Comic Sans MS', fontsize = 10)

    ax.bar_label(elevation, padding=0)

    fig.tight_layout()

    return fig

'''

'''
st.subheader('BEGIN INDIVIDUAL AND COMPARATIVE ANALYSIS')

# Provides the user with a choice of analysis - individual or comparative
analysis = st.radio('Select Type of Analysis', ['Individual Analysis', 'Comparative Analysis'])

# If user chooses individual analysis
if analysis == 'Individual Analysis':

    # Prompts the user to choose between a region or country mode of filtering the list
    choice = st.radio('Filter by:',['Region', 'Country'])

    if choice == 'Region':
        # Creates a dropbox of teh different regions for selection
        region_selection = st.selectbox('Select Region to Analyze:', region_list)
        # Creates a dataframe filtered by the selected region
        DF3 = DF1[DF1['Region'] == region_selection]
        # Prompts the user to select a country in the region selected
        country_analysis = st.selectbox('Select Country to Analyze:', list(DF3['Country'].unique()))
        st.subheader(f"Data Table of Tallest Volcanoes in {country_analysis}")
        # Creates a new dataframe with the country selected as filter for analysis
        DF4 = DF1[DF1['Country'] == country_analysis]
        # Slices the dataframe above to provide only the below selected columns
        tv = DF4[['Country', 'Volcano_Name', 'Elevation', "Last_Eruption"]]
        # Creates a list of the top 10 (or less if the selected country has less than 10 volcanoes)
        # volcanoes sorted by elevation
        tallest_volcanoes = tv.sort_values(by=['Elevation'], ascending=False).head(10)
        # Displays the top volcanoes in a table
        st.table(tallest_volcanoes)
        # Uses teh map function to display the selected country
        mapa(DF1, DF4, country_analysis)
        # Uses the piechart function to display the different types of volcanoes in the selected country
        piechart(DF4, country_analysis)
        # Prompts the user if he/she would like a brief description of the different types of volcanoes in that country
        wiki_volcano_types = st.radio('Would You Like an Explanation of the Different Types of Volcanoes?', ["Yes, I wouldn't mind a refresher.", "No, I'm a genius and already know everything!"])

        # Returns a three sentence brief description of the selected type of volcano
        if wiki_volcano_types == "Yes, I wouldn't mind a refresher.":
            type_selection = st.selectbox(f'Select a Volcano Type in {country_analysis} for Description:', list(DF4['Volcano_Type'].unique()))
            result = wk.summary(f'{type_selection} volcano', sentences=3)
            st.write(result)

        # Line plot function called via streamlit pyplot
        st.pyplot(lineplot(tallest_volcanoes, country_analysis))

    # Performs the same functions as the previous section without having the region filter as a primary source of filtering
    else:
        country_analysis = st.selectbox('Select Country to Analyze:', list(DF1['Country'].unique()))
        st.subheader(f"Data Table of Tallest Volcanoes in {country_analysis}")
        DF4 = DF1[DF1['Country'] == country_analysis]
        tv = DF4[['Country', 'Volcano_Name', 'Elevation', "Last_Eruption"]]
        tallest_volcanoes = tv.sort_values(by=['Elevation'], ascending=False).head(10)
        st.table(tallest_volcanoes)
        mapa(DF1, DF4, country_analysis)
        piechart(DF4, country_analysis)
        wiki_volcano_types = st.radio('Would You Like an Explanation of the Different Types of Volcanoes?', ["Yes, I wouldn't mind a refresher.", "No, I'm a genius and already know everything!"])

        if wiki_volcano_types == "Yes, I wouldn't mind a refresher.":
            type_selection = st.selectbox(f'Select a Volcano Type in {country_analysis} for Description:', list(DF4['Volcano_Type'].unique()))
            result = wk.summary(f'{type_selection} volcano', sentences=3)
            st.write(result)

        st.pyplot(lineplot(tallest_volcanoes, country_analysis))

# If user has selected the comparative analysis:
else:
    # Asks the suer to select three countries for analysis
    lista = st.multiselect('Please select 3 countries for comparative analysis:', country_list)

    # Makes sure the user selects three counties by displaying an alert message
    if len(lista) != 3:
        st.warning("Please select 3 countries.")
        st.stop()

    # Groups the "master" dataframe by country and applies a count (similar to lines 107-114)
    DF5 = DF1[['Country', 'Elevation']].groupby(by = "Country").count()
    DF5.reset_index(inplace=True)

    # Creates a dataframe that will display a table with the selected countries and their respective number of volcanoes
    DF6 = DF5[DF5['Country'].isin(lista)]
    DF6.rename(columns= {'Elevation':"Number of Volcanoes"}, inplace=True)
    st.subheader('Comparative Count of Volcanoes per Country')
    st.table(DF6)

    # Creates a dataframe including only the selected three countries
    DF7 = DF1[DF1['Country'].isin(lista)]
    # Creates a pivot table that calculates the minimum, maximum, and the average altitude of all the volcanoes in each
    # of the selected three countries for a comparative display
    DF8 = pd.pivot_table(data=DF7, values=['Elevation'], index=['Country'], aggfunc={'Elevation':[min, max, np.mean]})
    st.subheader('Comparative Volcanic Characteristic by Elevation')
    st.table(DF8)

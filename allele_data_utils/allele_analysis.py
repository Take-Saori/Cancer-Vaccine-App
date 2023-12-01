import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px

df = pd.read_csv('allele_data_utils/Cleaned_AlleleFrequencies_Temp.csv')

def get_all_allele():
    all_allele_list = list(df.Allele.unique())
    all_allele_list = [x.replace("['", "") for x in all_allele_list]
    all_allele_list = [x.replace("']", "") for x in all_allele_list]
    return tuple(all_allele_list)

def get_all_continent():
    all_continent = list(df.Continent.unique())
    all_continent = [x.replace("['", "") for x in all_continent]
    all_continent = [x.replace("']", "") for x in all_continent]
    return tuple(all_continent)

def get_all_region():
    all_region = list(df.Region.unique())
    all_region = [x.replace("['", "") for x in all_region]
    all_region = [x.replace("']", "") for x in all_region]
    return tuple(all_region)

def get_all_country():
    return tuple(df.Country.unique())

def get_unique_studies_num():
    return df['Population'].nunique()

def get_regions_num():
    return df['Region'].nunique()

def get_countries_num():
    return df['Country'].nunique()

def get_pop_per_region_fig():
    # Number of populations per region
    populations_per_region = df.groupby('Region').nunique()['Population']
    populations_per_region_sorted = populations_per_region.sort_values(ascending=False)

    # Create a DataFrame with the sorted data
    data = pd.DataFrame({'Region': populations_per_region_sorted.index, 'Population': populations_per_region_sorted.values})

    # Plot the bar chart using Plotly Express
    fig = px.bar(data, x='Region', y='Population',
                color_discrete_sequence=['blue'])

    return fig

def get_pop_per_continent_fig():
    # Number of populations per continent
    populations_per_continent = df.groupby('Continent').nunique()['Population']
    populations_per_continent_sorted = populations_per_continent.sort_values(ascending=False)

    # Create a DataFrame with the sorted data
    data = pd.DataFrame({'Continent': populations_per_continent_sorted.index, 'Population': populations_per_continent_sorted.values})

    # Plot the bar chart using Plotly Express
    fig = px.bar(data, x='Continent', y='Population',
                color_discrete_sequence=['blue'])

    return fig

def get_pop_per_country_fig():
    # Number of populations per country
    populations_per_country = df.groupby('Country').nunique()['Population']
    populations_per_country_sorted = populations_per_country.sort_values(ascending=False)

    # Create a DataFrame with the sorted data
    data = pd.DataFrame({'Country': populations_per_country_sorted.index, 'Population': populations_per_country_sorted.values})

    # Plot the bar chart using Plotly Express
    fig = px.bar(data, x='Country', y='Population',
                color_discrete_sequence=['blue'])

    return fig

def filter_and_analyze_with_expected_population_size(country=None, region=None, continent=None):
    # Filter based on the provided parameters
    if country:
        df = df[df['Country'] == country]
    if region:
        df = df[df['Region'] == region]
    if continent:
        df = df[df['Continent'] == continent]
    
    # Calculate numbers for the selected filters
    unique_populations = df['Population'].nunique()
    filtered_sample_size = df['Sample Size'].sum()
    
    # Calculate expected population size for each allele
    top_alleles_by_expected_population_size = df.groupby('Allele')['Expected Population Size'].sum().nlargest(20)
    
    return {
        "Number of unique populations": unique_populations,
        "Sample Size": filtered_sample_size,
        "Top 20 HLA Alleles by Expected Population Size": top_alleles_by_expected_population_size
    }


def update_choropleth(selected_alleles):
    selected_alleles = selected_alleles.split(', ')
    
    if 'Show All' in selected_alleles:
        filtered_df = df.copy()
    else:
        filtered_df = df[df['Allele'].isin(selected_alleles)]
    
    # Group data by country and sum the 'Expected Population Size'
    grouped_data = filtered_df.groupby('Country')['Expected Population Size'].sum().reset_index()
    
    # Load a built-in dataset of world countries
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Merge the world geodataframe with the grouped data
    world_merged = world.merge(grouped_data, how='left', left_on='name', right_on='Country')

    # Define the color scale range using percentiles to make the color distribution more uniform
    scale_min = np.percentile(world_merged['Expected Population Size'].dropna(), 5)  # 5th percentile
    scale_max = np.percentile(world_merged['Expected Population Size'].dropna(), 95)  # 95th percentile

    # Create a choropleth map
    fig = px.choropleth(
        world_merged,
        locations='iso_a3',  # Use the ISO Alpha 3 country codes
        color='Expected Population Size',  # Color by expected population size
        title="Choropleth Map of Expected Allele Population Size",
        color_continuous_scale='YlOrRd',  # Custom color palette
        range_color=[scale_min, scale_max]  # Define the range of the color scale
    )
    
    # Update layout for coastlines and map background color
    fig.update_layout(
        geo=dict(
            showcoastlines=True, 
            coastlinecolor="Black",
            showcountries=True,  # Show country borders
            countrycolor="Black",  # Set country border color
            landcolor='rgba(255,255,255,1)'  # Set land color to white
        ),
        paper_bgcolor='rgba(255,255,255,1)',  # Set paper background color to white
        plot_bgcolor='rgba(255,255,255,1)',  # Set plot background color to white
        width=900, 
        height=600, 
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    # Setting color for NaN data
    fig.update_traces(marker_line_width=0, selector=dict(type='choropleth'))
    return fig
    
    # fig.show()
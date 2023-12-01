import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px

df = pd.read_csv('allele_data_utils/Cleaned_AlleleFrequencies_Temp.csv')

def get_all_allele():
    return tuple(df.Allele.unique())

def filter_and_analyze_with_expected_population_size(df, country=None, region=None, continent=None):
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
import folium
import pandas as pd
import branca.colormap as cm
import json

# Load aggregated data
with open('2023/total/aggregated_municipios.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Process data similar to main.html
def get_state_from_code(code):
    state_map = {
        '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
        '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE', '29': 'BA',
        '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP',
        '41': 'PR', '42': 'SC', '43': 'RS',
        '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'
    }
    return state_map.get(code[:2], 'Unknown')

def get_grupo_from_sources(sources):
    for source in sources:
        if 'criacao_de_suinos' in source:
            return 'criacao_suinos'
        elif 'criacao_de_aves' in source:
            return 'criacao_aves'
        elif 'abates' in source:
            return 'abate_suinos_aves'
    return 'other'

data = []
for item in raw_data:
    if item['municipio'] == 'TOTAL':
        continue
    processed = {
        'municipio': item['municipio'],
        'municipio_nome': item.get('municipio_nome', ''),
        'latitude': item.get('latitude'),
        'longitude': item.get('longitude'),
        'total_vinculos': int(item['total_vinculos']),
        'sources': item.get('sources', []),
        'state': get_state_from_code(item['municipio']),
        'grupo': get_grupo_from_sources(item.get('sources', []))
    }
    data.append(processed)

df = pd.DataFrame(data)

# Filter out entries without grupo or coordinates
df_filtered = df.dropna(subset=['latitude', 'longitude', 'grupo']).copy()

# Get unique groups
unique_groups = df_filtered['grupo'].unique()

# Determine global min/max for colormap
min_count = df_filtered['total_vinculos'].min()
max_count = df_filtered['total_vinculos'].max()

# Define colormap
colormap = cm.LinearColormap(['yellow', 'orange', 'red'], vmin=min_count, vmax=max_count, caption='Employment Links')

# Group titles
group_titles = {
    'criacao_suinos': 'Criação de Suínos',
    'criacao_aves': 'Criação de Aves',
    'abate_suinos_aves': 'Abate de Suínos/Aves',
    'other': 'Other Activities'
}

# Create maps for each group
for group in unique_groups:
    # Create base map
    m = folium.Map(location=[-14.235, -51.9253], zoom_start=4)

    # Filter data for the group
    group_df = df_filtered[df_filtered['grupo'] == group].copy()

    # Convert to numeric
    group_df['latitude'] = pd.to_numeric(group_df['latitude'])
    group_df['longitude'] = pd.to_numeric(group_df['longitude'])
    group_df['total_vinculos'] = pd.to_numeric(group_df['total_vinculos'])

    # Add colormap
    m.add_child(colormap)

    # Add markers
    for idx, row in group_df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            fill_color = colormap(row['total_vinculos'])

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color='black',
                weight=1,
                fill=True,
                fill_color=fill_color,
                fill_opacity=0.7,
                tooltip=f"Município: {row['municipio_nome']}<br>State: {row['state']}<br>Employment: {int(row['total_vinculos'])}"
            ).add_to(m)

    # Save map
    group_title_formatted = group_titles.get(group, group).replace(' ', '_').replace('/', '_')
    map_filename = f"brazil_map_{group_title_formatted}.html"
    m.save(map_filename)
    print(f"Map for {group_titles.get(group, group)} saved as {map_filename}")
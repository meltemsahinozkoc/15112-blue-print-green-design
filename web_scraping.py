########### API Call
# access token:
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzE5NTgyMDksImV4cCI6MjA0NzMxODIwOSwidG9rZW5fdHlwZSI6ImRldmVsb3Blcl9hY2Nlc3MiLCJmaXJzdF9uYW1lIjoiTWVsdGVtIiwibGFzdF9uYW1lIjoiU2FoaW4gT3prb2MiLCJvY2N1cGF0aW9uIjoiU3R1ZGVudCIsInVzZXJfY29tcGFueSI6IkNNVSIsInVzZXJfZW1haWwiOiJtc2FoaW5vekBhbmRyZXcuY211LmVkdSJ9.nra6GVmWF2Wjt895AWcZjp35cmblbm7c7r0RNVHA0NM


############################################################
# COMPONENTS
############################################################ 
import requests
from bs4 import BeautifulSoup

def fetch_filtered_thermal_conductivity_data():
    url = 'https://neutrium.net/heat-transfer/thermal-conductivity-of-common-materials/'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    # parse html
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table_container = soup.find('div', class_='articleTableContainerScrollFrame') # found via inspect
    if not table_container:
        print("Table container not found.")
        return

    # locate the table within the container
    table = table_container.find('table', class_='centered')
    if not table:
        print("Table not found.")
        return

    # extract data from the table
    data = []
    current_subheader = None
    target_categories = {"Soils and Earth", "Building Materials", "Insulation"}
    rows = table.find_all('tr')

    for row in rows:
        # check subheader
        subheader = row.find('th')
        if subheader and 'colspan' in subheader.attrs:
            current_subheader = subheader.get_text(strip=True)
        elif current_subheader in target_categories:
            # extract material data if it's a regular row under the target (Soils and Earth, Building Materials, Insulation) category
            cols = row.find_all('td')
            if len(cols) >= 5:
                material = cols[0].get_text(strip=True)
                temp_c = cols[1].get_text(strip=True)
                conductivity_w_mk = cols[2].get_text(strip=True)
                temp_f = cols[3].get_text(strip=True)
                conductivity_btu_ft_h_f = cols[4].get_text(strip=True)

                data.append({
                    'Category': current_subheader,
                    'Material': material,
                    'Temperature (°C)': temp_c,
                    'Conductivity (W/m·K)': conductivity_w_mk,
                    'Temperature (°F)': temp_f,
                    'Conductivity (BTU·ft/h·°F)': conductivity_btu_ft_h_f
                })
    
    return data


thermal_data = fetch_filtered_thermal_conductivity_data()
if thermal_data:
    for entry in thermal_data:
        print(f"Category: {entry['Category']}")
        print(f"  Material: {entry['Material']}")
        print(f"    Temperature (°C): {entry['Temperature (°C)']}")
        print(f"    Conductivity (W/m·K): {entry['Conductivity (W/m·K)']}")
        print(f"    Temperature (°F): {entry['Temperature (°F)']}")
        print(f"    Conductivity (BTU·ft/h·°F): {entry['Conductivity (BTU·ft/h·°F)']}\n")

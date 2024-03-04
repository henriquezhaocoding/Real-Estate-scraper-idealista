import requests
import json

# Getting the required location id
def Get_location_id(name, key):
    url_location_id = "https://idealista2.p.rapidapi.com/auto-complete"

    querystring_location_id = {"prefix": name, "country": "pt"}

    headers_location_id = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "idealista2.p.rapidapi.com"
    }

    response_location_id = requests.request(
        "GET", url_location_id, headers=headers_location_id, params=querystring_location_id)

    response = json.loads(response_location_id.text)

    location_id = response["locations"][0]['locationId']
    location_name = response["locations"][0]['name']

    return location_id, location_name

# Getting scraped information
# For 'location_name' check the file LX_Zones_names for a full list of names for Portugal, Lisbon

def Scraper(location_id, location_name, radius="500", maxsize="50000", minsize="50", maxprice="20000000", minprice="10000000", max="2", key=""):
    url_scraper = "https://idealista2.p.rapidapi.com/properties/list"

    querystring_scraper = {"locationId": location_id,
                           "locationName": location_name,
                           "operation": "sale",
                           "numPage": "1",
                           "maxItems": str(max),
                           "sort": "asc",
                           "locale": "en",
                           "country": "pt",
                           "distance": radius,
                           "maxSize": maxsize,
                           "minSize": minsize,
                           "maxPrice": maxprice,
                           "minPrice": minprice}

    headers_scraper = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "idealista2.p.rapidapi.com"
    }

    response_scraper = requests.request(
        "GET", url_scraper, headers=headers_scraper, params=querystring_scraper)
    response = json.loads(response_scraper.text)

    return response

def Save_list(input_list):
    with open('saved_properties.txt','w') as file:
        for item in input_list:
            print(item)
            file.write(json.dumps(item))
            file.write("\n")
        file.close()

def main():
    # Insert your valid API key
    KEY = "" # Insert valid API key here, sign up at https://rapidapi.com/apidojo/api/idealista2/
    MAX_PROPS = 1 #Customize MAX_PROPS based on your API subscription allowance and needs

    # Example for 'Benfica' to get location_id for scraper
    # For 'location_name' check the file LX_Zones_names for a full list of zone names for Portugal, Lisbon
    zone_name = "Benfica"

    location_id, location_name = Get_location_id(zone_name, KEY)
    print(location_id, location_name)

    information = Scraper(str(location_id), zone_name,
                        minprice="1", minsize="1", max=MAX_PROPS, key=KEY)

    info = dict(information)

    # Processed information
    info_prop = []
    index = 0
    for prop in info["elementList"]:
        prop_info = {}
        prop_info = {
            "Index": index,
            "PropertyCode": prop['propertyCode'],
            "URL": prop['url'],
            "Size": prop['size'],
            "Price": prop['price'],
            "Price per sqm": prop['priceByArea']
        }
        info_prop.append(prop_info)
        index += 1

    # Export information of each property onto a text file - saved_properties.txt
    Save_list(info_prop)

if __name__ == "__main__":
    main()




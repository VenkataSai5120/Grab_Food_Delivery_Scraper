# import os
# import json
# import gzip
# import requests
# import time

# def main():
#     # Read proxies from the file
#     with open("proxies_list.txt", "r", encoding="utf-8") as proxies_file:
#         proxies = proxies_file.read().split("\n")

#     counter = 0
#     length = len(proxies)

#     # Read IDs from the RestaurantList.txt file
#     combined_list_file_path = "RestaurantList.txt"
#     with open(combined_list_file_path, "r", encoding="utf-8") as combined_list_file:
#         ids = json.load(combined_list_file)

#     # Fetching responses and saving to individual JSON files
#     url_template = "https://portal.grab.com/foodweb/v2/merchants/{}"
#     output_folder = "responses"
#     os.makedirs(output_folder, exist_ok=True)

#     for merchant_id in ids:

#         while True:
#             url = url_template.format(merchant_id)
#             try:
#                 response = requests.get(url, proxies={'http': proxies[counter % length], 'https': proxies[counter % length]})
#                 print(merchant_id, response.status_code)
                
#                 if response.status_code == 200:
#                     output_file_path = os.path.join(output_folder, f"{merchant_id}_response.json")
#                     with open(output_file_path, "w", encoding="utf-8") as output_file:
#                         output_file.write(response.text)
                        
#                     break  # Break the loop if response status is 200
#                 else:
#                     print(f"Retrying for ID {merchant_id} in 5 seconds...")
#                     time.sleep(5)  # Wait for 5 seconds before retrying
#             except Exception as e:
#                 print(f"Error occurred for ID {merchant_id}")
#                 proxy = proxies[counter % length]
#                 print(f"Changing proxy to {proxy}")
#                 counter += 1
#                 # time.sleep(5)
            

#     # Extracting data
#     all_data = []

#     for merchant_id in ids:
#         input_file_path = os.path.join(output_folder, f"{merchant_id}_response.json")
        
#         with open(input_file_path, "r", encoding="utf-8") as input_file:
#             data = json.load(input_file)
#             merchant_info = data.get("merchant", {})
            
#             # Extract specific fields
#             merchant_id = merchant_info.get("ID")
#             name = merchant_info.get("name")
#             cuisine = merchant_info.get("cuisine")
#             timezone = merchant_info.get("timeZone")
#             photo_href = merchant_info.get("photoHref")
#             eta = merchant_info.get("ETA")
#             latlng = merchant_info.get("latlng")
#             rating = merchant_info.get("Rating")
#             distance_in_km = merchant_info.get("distanceInKm")
            
#             estimated_delivery_fee = merchant_info.get("estimatedDeliveryFee", {})
#             currency = estimated_delivery_fee.get("currency")
#             price = estimated_delivery_fee.get("price")
#             price_display = estimated_delivery_fee.get("priceDisplay")
#             status = estimated_delivery_fee.get("status")
#             multiplier = estimated_delivery_fee.get("Multiplier")
            
#             promotions = merchant_info.get("promotions")

#             all_data.append({
#                 "ID": merchant_id,
#                 "Details": {
#                     "Name": name,
#                     "Cuisine": cuisine,
#                     "TimeZone": timezone,
#                     "PhotoHref": photo_href,
#                     "ETA": eta,
#                     "Latlng": latlng,
#                     "Rating": rating,
#                     "DistanceInKm": distance_in_km,
#                     "EstimatedDeliveryFee": {
#                         "Currency": currency,
#                         "Price": price,
#                         "PriceDisplay": price_display,
#                         "Status": status,
#                         "Multiplier": multiplier,
#                     },
#                     "Promotions": promotions,
#                     # Add more fields here
#                 }
#             })

#     # Save all extracted data to a single compressed (gzip) ndjson file in the main directory
#     output_file_path = "all_responses.ndjson.gz"
#     with gzip.open(output_file_path, "wt", encoding="utf-8") as output_file:
#         for data in all_data:
#             json.dump(data, output_file, indent=4)
#             output_file.write('\n')

#     print(f"All responses saved to individual JSON files and extracted data saved to {output_file_path}")

# if __name__ == "__main__":
#     main()


# import os
# import json
# import gzip
# import requests
# import time

# def main():
#     # Read proxies from the file
#     with open("proxies_list.txt", "r", encoding="utf-8") as proxies_file:
#         proxies = proxies_file.read().split("\n")

#     counter = 0
#     length = len(proxies)

#     # Read IDs from the RestaurantList.txt file
#     combined_list_file_path = "RestaurantList.txt"
#     with open(combined_list_file_path, "r", encoding="utf-8") as combined_list_file:
#         ids = json.load(combined_list_fil
import os
import json
import gzip
import requests
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_data(merchant_id, proxies, counter, length, url_template, output_folder):
    while True:
        url = url_template.format(merchant_id)
        try:
            response = requests.get(url, proxies={'http': proxies[counter % length], 'https': proxies[counter % length]})
            print(merchant_id, response.status_code)

            if response.status_code == 200:
                output_file_path = os.path.join(output_folder, f"{merchant_id}_response.json")
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(response.text)
                break
            else:
                print(f"Retrying for ID {merchant_id} in 5 seconds...")
                time.sleep(5)
        except Exception as e:
            print(f"Error occurred for ID {merchant_id}")
            proxy = proxies[counter % length]
            print(f"Changing proxy to {proxy}")
            counter += 1

def main():
    with open("proxies_list.txt", "r", encoding="utf-8") as proxies_file:
        proxies = proxies_file.read().split("\n")

    counter = 0
    length = len(proxies)

    combined_list_file_path = "RestaurantList.txt"
    with open(combined_list_file_path, "r", encoding="utf-8") as combined_list_file:
        ids = json.load(combined_list_file)

    output_folder = "responses"
    os.makedirs(output_folder, exist_ok=True)

    url_template = "https://portal.grab.com/foodweb/v2/merchants/{}"

    with ThreadPoolExecutor() as executor:
        futures = []
        for merchant_id in ids:
            futures.append(executor.submit(fetch_data, merchant_id, proxies, counter, length, url_template, output_folder))
            counter += 1

        for future in futures:
            future.result()

    all_data = []

    for merchant_id in ids:
        input_file_path = os.path.join(output_folder, f"{merchant_id}_response.json")

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)
            merchant_info = data.get("merchant", {})
            
            merchant_id = merchant_info.get("ID")
            name = merchant_info.get("name")
            cuisine = merchant_info.get("cuisine")
            timezone = merchant_info.get("timeZone")
            photo_href = merchant_info.get("photoHref")
            eta = merchant_info.get("ETA")
            latlng = merchant_info.get("latlng")
            rating = merchant_info.get("Rating")
            distance_in_km = merchant_info.get("distanceInKm")
            
            estimated_delivery_fee = merchant_info.get("estimatedDeliveryFee", {})
            currency = estimated_delivery_fee.get("currency")
            price = estimated_delivery_fee.get("price")
            price_display = estimated_delivery_fee.get("priceDisplay")
            status = estimated_delivery_fee.get("status")
            multiplier = estimated_delivery_fee.get("Multiplier")
            
            promotions = merchant_info.get("promotions")

            all_data.append({
                "ID": merchant_id,
                "Details": {
                    "Name": name,
                    "Cuisine": cuisine,
                    "TimeZone": timezone,
                    "PhotoHref": photo_href,
                    "ETA": eta,
                    "Latlng": latlng,
                    "Rating": rating,
                    "DistanceInKm": distance_in_km,
                    "EstimatedDeliveryFee": {
                        "Currency": currency,
                        "Price": price,
                        "PriceDisplay": price_display,
                        "Status": status,
                        "Multiplier": multiplier,
                    },
                    "Promotions": promotions,
                }
            })

    output_file_path = "all_responses.ndjson.gz"
    with gzip.open(output_file_path, "wt", encoding="utf-8") as output_file:
        for data in all_data:
            json.dump(data, output_file, indent=4)
            output_file.write('\n')

    print(f"All responses saved to individual JSON files and extracted data saved to {output_file_path}")

if __name__ == "__main__":
    main()

import json
import time  # Added import for time module
import ListMaking  # Assuming ListMaking is another Python file/module

# Function to process JSON data and combine recommended merchants and restaurant list
def process_json(json_file_path, output_file_path):
    try:
        # Read the JSON content
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Extract data from JSON
        recommended_merchants = data.get("props", {}).get("initialReduxState", {}).get("pageRestaurantsV2", {}).get("collections", {}).get("recommendedMerchants", {})
        restaurant_list = data.get("props", {}).get("initialReduxState", {}).get("pageRestaurantsV2", {}).get("collections", {}).get("restaurantList", {})

        # Combine both lists into a single dictionary
        combined_list = {
            "getRecommendedMerchantsV2/countryCode=SG&latitude=1.287953&longitude=103.851784": recommended_merchants,
            "getRestaurantsV2/countryCode=SG&latlng=1.287953%2C103.851784": restaurant_list
        }

        # Print or process the combined list as needed
        print("Combined List:", combined_list)

        # Store the combined list in a text file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(json.dumps(combined_list, indent=2))

        # Logging that the combined list has been stored
        print(f"Combined list stored.....")

    except json.JSONDecodeError as e:
        # Logging error if JSON decoding fails
        print(f"Error decoding JSON: {e}")

    except FileNotFoundError:
        # Logging error if file is not found
        print(f"Error: File not found at path '{json_file_path}'")

# Main function
def main():
    # Paths for input and output files
    json_file_path = r'resultJson.json'
    output_file_path = r'C:\Users\vsai5\OneDrive\Desktop\Anakins\output_list.txt'

    # Process the JSON file
    process_json(json_file_path, output_file_path)

    # Call the main function from ListMaking module
    print("Waiting for 5 seconds before combining the restaurant list...")
    time.sleep(5)
    ListMaking.main()

# Entry point of the script
if __name__ == "__main__":
    main()

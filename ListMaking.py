import json
import time  # Added import for time module
import GrabDetails  # Assuming GrabDetails is another Python file/module

# Function to combine JSON arrays from different sources
def combine_json_arrays(json_file_path, output_file_path):
    try:
        # Read the JSON content
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Extract data from JSON for recommended merchants and restaurant list
        recommended_merchants = data.get("getRecommendedMerchantsV2/countryCode=SG&latitude=1.287953&longitude=103.851784", {}).get("getRecommendedMerchantsV2/countryCode=SG&latitude=1.287953&longitude=103.851784", [])
        restaurant_list = data.get("getRestaurantsV2/countryCode=SG&latlng=1.287953%2C103.851784", {}).get("getRestaurantsV2/countryCode=SG&latlng=1.287953%2C103.851784", [])

        # Combine both lists into a single list
        combined_list = recommended_merchants + restaurant_list

        # Print or process the combined list as needed
        print("Combined List Array:", combined_list)

        # Store the combined list as a JSON array in a text file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(combined_list, output_file, indent=2)

        # Logging that the combined list has been stored
        print(f"Combined list stored in '{output_file_path}'")

    except json.JSONDecodeError as e:
        # Logging error if JSON decoding fails
        print(f"Error decoding JSON: {e}")

    except FileNotFoundError:
        # Logging error if file is not found
        print(f"Error: File not found at path '{json_file_path}'")

# Main function
def main():
    # Paths for input and output files
    json_file_path = r'output_list.txt'
    output_file_path = r'combined_listArray.txt'

    # Combine JSON arrays
    combine_json_arrays(json_file_path, output_file_path)

    # Call the main function from GrabDetails module
    print("Waiting for 5 seconds for extracting the details...")
    time.sleep(5)
    GrabDetails.main()

# Entry point of the script
if __name__ == "__main__":
    main()

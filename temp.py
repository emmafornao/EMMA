import json


def main():

    key_map = {
    # CF : WC
    "screenshots": "screenshots",
    "id": "iD",
    "gameId": "gameId",
    "name": "name",
    "slug": "slug",
    "links": "links",
    "summary": "summary",
    # "status": "status",            // this goes from digits to names so might cause issues
    "downloadCount": "downloadCount",
    "isFeatured": "isFeatured",
    "primaryCategoryId": "primaryCategoryId",
    "categories": "categories",
    "classId": "classId",
    "authors": "authors",
    "logo": "logo",
    "mainFileId": "mainFileId",
    "latestFiles": "latestFiles",
    "latestFilesIndexes": "latestFilesIndexes",
    "dateCreated": "cateCreated",
    "dateModified": "dateModified",
    "dateReleased": "dateReleased",
    "allowModDistribution": "allowModDistribution",
    "gamePopularityRank": "gamePopularityRank",
    "isAvailable": "isAvailable",
    # "ratingDetails": "ratingDetails"       // score goes from digit to names
    # "featuredProjectTag": "isFeatured"   //unclear if these are the same. also goes from 0/1 to false/true
    }


    with open("G:/GoogleDriveEmma/ARK/EMMA_general/other/replacetestlibrary.json", 'r', encoding='utf-8-sig') as file:
        library = json.load(file)  # Load the JSON data
    
    with open("G:/GoogleDriveEmma/ARK/EMMA_general/other/replacetestentry.json", 'r', encoding='utf-8-sig') as file:
        new_entry = json.load(file)  # Load the JSON data


    # Access the list of installed mods
    installed_mods = library# .get("installedMods", [])

    mod_id = new_entry.get("data", {}).get("id", "")
    for mod in installed_mods:
        if mod.get("details", {}).get("iD", "") == mod_id:
            for value, key in key_map.items(): # yes, it should be "value, key". key_map is flipped
                print(key)
                print(value)
                mod["details"][key] = new_entry["data"][value]
            break


    # Save the updated JSON back to the file
    with open("G:/GoogleDriveEmma/ARK/EMMA_general/other/replacetestlibrary.json", 'w') as file:
        json.dump(installed_mods, file, indent=4)  # Use indent for pretty printing




if __name__ == "__main__":
    main()
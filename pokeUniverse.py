__author__ = "zj4ck3"

# fetches Pokemon information from the API
# return data of the pokemon if are available, None otherwise
def pokemon_API_data(pokemon) -> dict:
    import requests

    header = {"Content-Type":"application/json"}
    URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

    try:
        response = requests.get(URL,headers=header,timeout=10)
        response.raise_for_status()
        pokeData = response.json() # create the dict

    # Error handling
    except requests.exceptions.Timeout:
        print(f"\n[X] Timeout exceeded: {response.status_code}")
        return

    except requests.exceptions.ConnectionError:
        print(f"\n[X] Unable to connect to server: {response.status_code}")
        return

    except requests.exceptions.HTTPError as error:
        if response.status_code == 404:
            print("\n[X] Pokemon not found")
        else:
            print(f"\n[X] HTTP Error: {error}")
        return

    except requests.exceptions.RequestException as error:
        print(f"\n[X] Error during the request: {error}\n")
        return

    return pokeData

# print pokemon info in human readable format
def print_pokemon_info(pokemon: dict) -> None:
    # Get the Pokémon name.
    # Use "Unknown" if the "name" key does not exist.
    name = pokemon.get("name", "Unknown").capitalize()

    # Get the Pokémon ID.
    # Use "?" if the "id" key does not exist.
    pokemon_id = pokemon.get("id", "?")
    height = pokemon.get("height")
    weight = pokemon.get("weight")

    print()
    print("=" * 40)
    print(f"[V] {name} (#{pokemon_id})")
    print("=" * 40)

    # Convert height from decimeters to meters.
    if height is not None:
        print(f"Height: {height / 10:.1f} m")
    else:
        print("Height: unavailable")

    # Convert weight from hectograms to kilograms.
    if weight is not None:
        print(f"Weight: {weight / 10:.1f} kg")
    else:
        print("Weight: unavailable")

    # Extract the names of the Pokémon's types.
    types = [
        item["type"]["name"].capitalize()
        for item in pokemon.get("types", [])
        if "type" in item and "name" in item["type"]
    ]

    if types:
        print(f"Types: {', '.join(types)}")
    else:
        print("Types: unavailable")

    # Extract the names of the Pokémon's abilities.
    abilities = [
        item["ability"]["name"]
        .replace("-", " ")
        .capitalize()
        for item in pokemon.get("abilities", [])
        if "ability" in item and "name" in item["ability"]
    ]

    if abilities:
        print(f"Abilities: {', '.join(abilities)}")
    else:
        print("Abilities: unavailable")

    # Create a dictionary containing the base statistics.
    stats = {
        item["stat"]["name"]: item["base_stat"]
        for item in pokemon.get("stats", [])
        if "stat" in item and "base_stat" in item
    }

    print("\nBase stats:")

    if stats:
        # Print each statistic on a separate line.
        for stat_name, value in stats.items():
            formatted_name = (
                stat_name.replace("-", " ").capitalize()
            )

            print(f"  {formatted_name:<17} {value}")
    else:
        print("  Unavailable")

    print("=" * 40)
    input("[V] Press anything to continue: ")
    return

# for option 5
def give_information() -> None:
    print()
    print("All information available in README.md file")
    print("For pull requests or comment contact me at: https://github.com/zj4ck3/pokeUniverse.git")
    print(f"Created by: {__author__}")
    return


if __name__ == "__main__":
    while True:
        print("## WELCOME TO POKEUNIVERSE !!! ##")
        print("[#] 1 - Pokemon info")
        print("[#] 2 - Random pokemon")
        print("[#] 3 - Guess the pokemon")
        print("[#] 4 - Compare 2 pokemons")
        print("[#] 5 - Information")
        print("[#] other number - Exit")
        
        try:
            option = int(input("[?] Choose an option: "))

            if option == 1:
                pokemon = input("[?] Name of the pokemon: ").capitalize()
                pokeData = pokemon_API_data(pokemon) # the description must be readable

                if pokeData != None:
                    print_pokemon_info(pokeData)

            elif option == 2:
                print("2")

            elif option == 3:
                print("3")

            elif option == 4:
                print("4")

            elif option == 5:
                give_information()

            else:
                quit()
            
        except ValueError:
            print("[X] Only numbers are allowed")
        finally:
        	print()
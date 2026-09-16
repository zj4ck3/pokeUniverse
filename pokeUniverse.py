__author__ = "zj4ck3"

# fetches Pokemon information from the API
# return data of the pokemon if are available, None otherwise
def pokemon_description(pokemon) -> dict:
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
                pokeData = pokemon_description(pokemon) # the description must be readable

                if pokeData != None:
                    print(pokeData)

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
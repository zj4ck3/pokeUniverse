__author__ = "zj4ck3"

# fetches Pokemon information from the API
def pokemon_description(pokemon) -> dict:
    pass

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
                pokemon = input("Name of the pokemon: ")
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
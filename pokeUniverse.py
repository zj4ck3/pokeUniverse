from pokemonFunction import *
from databaseFunction import *
__author__ = "zj4ck3"

# parser for CLI argument
def parseArgument() -> list:
    from argparse import ArgumentParser

    parser = ArgumentParser(description="PokeUniverse - Pokemon information and guessing game")
    parser.add_argument(
        "option",
        type=int,
        nargs="?",
        help="Operation to perform"
    )
    parser.add_argument("pokemon", nargs="?")
    parser.add_argument("pokemon2", nargs="?")
    args = parser.parse_args()
    args_list = list(vars(args).values())# for create a list from namespace object type

    if args_list[0] == 1 and args_list[1] == None:
        print("[X] Another argument is required: pokemon")
        quit()
    if args_list[0] == 4 and (args_list[1] == None or args_list[2] == None):
        print("[X] Another argument is required: pokemon and/or pokemon2")
        quit()
    return args_list # returned [None, None, None] if no arguments are given

# for option 5
def give_information() -> None:
    print()
    print("[#] All information available in README.md file")
    print("[#] For pull requests or comment contact me at: https://github.com/zj4ck3/pokeUniverse.git")
    print(f"[#] Created by: {__author__}")
    input("[#] Press anything to continue: ")
    return


if __name__ == "__main__":
    init_dbs()
    args_list = parseArgument()
    fromCLI = False

    if args_list[0] == None:
        usr = input("[?] Insert username: ")
        print()
    else: usr = ""

    while True:    
        if args_list[0] == None:
            print("## WELCOME TO POKEUNIVERSE !!! ##")
            print("[#] 1 - Pokemon info")
            print("[#] 2 - Random pokemon")
            print("[#] 3 - Guess the pokemon")
            print("[#] 4 - Compare 2 pokemons")
            print("[#] 5 - Statistics")
            print("[#] 6 - Delete user")
            print("[#] 7 - Delete cache - IN PROD")
            print("[#] 8 - Information")
            print("[#] other number - Exit")
        
        try:
            if args_list[0] == None:
                option = int(input("[?] Choose an option: "))
                fromCLI = False
            else:
                option = args_list[0]
                fromCLI = True

                # ask the username only if it needs it
                if option == 3 or option == 5:
                    usr = input("[?] Insert username: ")
                    print()

            if option == 1:
                if not fromCLI:
                    pokemon = input("[?] Name of the pokemon: ").capitalize()
                else:
                    pokemon = args_list[1]
                pokeData = pokemon_API_data(pokemon) # the description must be readable

                if pokeData != None:
                    print_pokemon_info(pokeData, usr)

            elif option == 2:
                pokeData = pokemon_API_data(None, randomize=True)
                print_pokemon_info(pokeData, usr)

            elif option == 3:
                pokeData = pokemon_API_data(None, randomize=True)
                print_pokemon_info(pokeData, usr, guess=True)

            elif option == 4:
                if not fromCLI:
                    pokemon1 = input("[?] Name of the first pokemon: ").capitalize()
                    pokemon2 = input("[?] Name of the second pokemon: ").capitalize()
                else:
                    pokemon1 = args_list[1]
                    pokemon2 = args_list[2]
                pokeData1 = pokemon_API_data(pokemon1)
                pokeData2 = pokemon_API_data(pokemon2)

                if pokeData1 != None and pokeData2 != None:
                    compare_pokemon(pokeData1, pokeData2)

            elif option == 5:
                statistic(usr)

            elif option == 6:
                usr = input("[?] Insert the user that you want to delete: ")
                del_usr(usr)

            elif option == 7:
                delete_cache()

            elif option == 8:
                give_information()

            else:
                quit()
            
        except ValueError:
            print("[X] Only numbers are allowed")
        print()
        if fromCLI:
            quit()
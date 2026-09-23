from requests import get, exceptions
from sqlite3 import connect
from pathlib import Path

__author__ = "zj4ck3"
PATH = Path(__file__).resolve().parent

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

# create a database if it's not already there
def init_db() -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS guesses(
            id INTEGER PRIMARY KEY,
            date TEXT DEFAULT (strftime('%Y-%m-%d', 'now')),
            user TEXT NOT NULL,
            guessed INTEGER NOT NULL CHECK(guessed == 0 OR guessed == 1),
            attemp INTEGER NOT NULL CHECK(attemp < 4 AND attemp > 0)
        )""")
        return

# for insert information into the database
def insert_info(user:str, guessed:bool, attemp:int) -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO guesses(user, guessed, attemp)
        VALUES (?,?,?)""",(user, guessed, attemp))
    return

# for delete a user from a database
def del_usr(user:str) -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM guesses WHERE user=?""",(user,))
        conn.commit()
    return

# query for statistic
def statistic(user:str) -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        # first query for total not guessed
        cursor.execute("""SELECT COUNT(*)
            FROM guesses
            WHERE user=? AND guessed=0""",(user,))
        totNotGuessed = cursor.fetchone()[0]

        # query for total guessed
        cursor.execute("""SELECT COUNT(*)
            FROM guesses
            WHERE user=? AND guessed=1""",(user,))
        totGuessed = cursor.fetchone()[0]

        # query for max streak for that user made with AI (i'm not that good)
        cursor.execute("""WITH groups AS (
                SELECT
                id,
                guessed,
                SUM(CASE WHEN guessed = 0 THEN 1 ELSE 0 END)
                OVER (ORDER BY date) AS group_id
                FROM guesses
                WHERE user = ?
            ),
            streaks AS (
                SELECT group_id, COUNT(*) AS streak
                FROM groups
                WHERE guessed = 1
                GROUP BY group_id
            )
            SELECT COALESCE(MAX(streak), 0)
            FROM streaks;""", (user,))
        streakUsr = cursor.fetchone()[0]

        # modified query for general max streak, if more than 1 user have identical max streak
        # only one user will be shown
        cursor.execute("""WITH groups AS (
                SELECT
                id,
                user,
                guessed,
                SUM(CASE WHEN guessed = 0 THEN 1 ELSE 0 END)
                    OVER (
                        PARTITION BY user
                        ORDER BY id
                ) AS group_id
                FROM guesses
                ),
            streaks AS (
                SELECT
                user,
                group_id,
                COUNT(*) AS streak
                FROM groups
                WHERE guessed = 1
                GROUP BY user, group_id
            )
            SELECT user, MAX(streak) AS max_streak
            FROM streaks
            GROUP BY user
            ORDER BY max_streak DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()

    print()
    print("=" * 40)
    print(f"[V] Statistics of user {user}: ")
    print("=" * 40)
    print(f"Total pokemon guesses: {totGuessed + totNotGuessed}")
    print(f"Correct pokemon guesses: {totGuessed}")
    print(f"Wrong pokemon guesses: {totNotGuessed}")
    if totNotGuessed+totGuessed != 0:
        print(f"General accuracy: {((totGuessed/(totGuessed+totNotGuessed))*100):.2f} %")
    print()
    print(f"Max streak of {user}: {streakUsr}")
    if result != None and result[0] != None and result[1] != None:
        print(f"General streak record: {result[1]} of {result[0]}")
    print("=" * 40)
    input("[V] Press anything to continue: ")
    return

# fetches Pokemon information from the API
# return data of the pokemon if are available, None otherwise
# if the user choose option 2 it choose a random name for fetch the info
def pokemon_API_data(pokemon:str, randomize:bool=False) -> dict | None:
    header = {"Content-Type":"application/json"}
    if randomize:
        from random import choice
        true_URL = "https://pokeapi.co/api/v2/pokemon?limit=10000000" # hardcoded because API doesn't have max_id or similar
    else:
        true_URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

    try:
        response = get(true_URL,headers=header,timeout=10)
        response.raise_for_status()
        pokeData = response.json() # create the dict

    # Error handling
    except exceptions.Timeout:
        print(f"\n[X] Timeout exceeded")
        return

    except exceptions.ConnectionError:
        print(f"\n[X] Unable to connect to server")
        return

    except exceptions.HTTPError as error:
        if response.status_code == 404:
            print(f"\n[X] Pokemon {pokemon} not found")
        else:
            print(f"\n[X] HTTP Error: {error}")
        return

    except exceptions.RequestException as error:
        print(f"\n[X] Error during the request: {error}\n")
        return

    if randomize: # recursive call
        pokemon_list = pokeData.get("results", [])
        if not pokemon_list:
            print("\n[X] No pokemon available")
            return None

        random_pokemon = choice(pokemon_list)
        return pokemon_API_data(random_pokemon["name"])
    return pokeData

# print pokemon info in human readable format
# or make the user guess one
def print_pokemon_info(pokemon:dict, guess:bool=False) -> None:
    global usr
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
    if guess:
        print(f"[V] Guess the pokemon {usr}")
    else:
        print(f"{name} (#{pokemon_id})")
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
    if guess:
        print()
        for i in range(3):
            name_guess = input("[?] Enter the name of the pokemon: ")
            if name_guess.capitalize() == name:
                input("[V] Correct !!! Press anything to continue: ")
                insert_info(usr, 1, i+1)
                return
            else:
                if i+1 == 3:
                    print(f"[X] Ultimate guess: wrong!! the name was: {name}")
                    input("[X] Press anything to continue: ")
                    insert_info(usr, 0, 3)
                else:
                    print(f"[X] Wrong, guess {i+1}/3")
    else:
        input("[V] Press anything to continue: ")
    return

# compare 2 pokemon for option 4
# i could put it all in print_pokemon_info but that would be caothic
# and i also don't feel like it
def compare_pokemon(pokemon1: dict, pokemon2: dict) -> None:
    # Get the Pokémon names and IDs.
    name1 = pokemon1.get("name", "Unknown").capitalize()
    name2 = pokemon2.get("name", "Unknown").capitalize()
    pokemon_id1 = pokemon1.get("id", "?")
    pokemon_id2 = pokemon2.get("id", "?")

    print()
    print("=" * 50)
    print("[V] Pokemon comparison")
    print("=" * 50)
    print(f"{name1} (#{pokemon_id1}) VS {name2} (#{pokemon_id2})")
    print("=" * 50)

    # Compare height.
    height1 = pokemon1.get("height")
    height2 = pokemon2.get("height")

    print()
    print("Physical comparison:")

    if height1 is not None and height2 is not None:
        height1_m = height1 / 10
        height2_m = height2 / 10

        print(f"Height: {name1}: {height1_m:.1f} m | {name2}: {height2_m:.1f} m")
    else:
        print("Height: unavailable")

    # Compare weight.
    weight1 = pokemon1.get("weight")
    weight2 = pokemon2.get("weight")

    if weight1 is not None and weight2 is not None:
        weight1_kg = weight1 / 10
        weight2_kg = weight2 / 10

        print(f"Weight: {name1}: {weight1_kg:.1f} kg | {name2}: {weight2_kg:.1f} kg")
    else:
        print("Weight: unavailable")

    # Extract base statistics.
    stats1 = {
        item["stat"]["name"]: item["base_stat"]
        for item in pokemon1.get("stats", [])
        if "stat" in item and "base_stat" in item
    }

    stats2 = {
        item["stat"]["name"]: item["base_stat"]
        for item in pokemon2.get("stats", [])
        if "stat" in item and "base_stat" in item
    }

    print()
    print("Base stats comparison:")
    print("-" * 50)

    # Compare stats that exist in both Pokemon.
    common_stats = stats1.keys() & stats2.keys()
    total1 = 0
    total2 = 0

    for stat_name in common_stats:
        value1 = stats1[stat_name]
        value2 = stats2[stat_name]
        total1 += value1
        total2 += value2

        formatted_name = stat_name.replace("-", " ").capitalize()
        print(f"{formatted_name:<17} {name1}: {value1:<3} | {name2}: {value2:<3}")
    print("-" * 50)

    # Compare total base stats.
    print(f"Total stats: {name1}: {total1} | {name2}: {total2}")
    if total1 > total2:
        print(f"[V] {name1} has higher total stats")
    elif total2 > total1:
        print(f"[V] {name2} has higher total stats")
    else:
        print("[=] Both Pokemon have the same total stats")

    print("=" * 50)
    input("[V] Press anything to continue: ")

# for option 5
def give_information() -> None:
    print()
    print("[#] All information available in README.md file")
    print("[#] For pull requests or comment contact me at: https://github.com/zj4ck3/pokeUniverse.git")
    print(f"[#] Created by: {__author__}")
    input("[#] Press anything to continue: ")
    return


if __name__ == "__main__":
    init_db()
    args_list = parseArgument()
    fromCLI = False

    if args_list[0] == None:
        usr = input("[?] Insert username: ")
        print()

    while True:    
        if args_list[0] == None:
            print("## WELCOME TO POKEUNIVERSE !!! ##")
            print("[#] 1 - Pokemon info")
            print("[#] 2 - Random pokemon")
            print("[#] 3 - Guess the pokemon")
            print("[#] 4 - Compare 2 pokemons")
            print("[#] 5 - Statistics")
            print("[#] 6 - Delete user")
            print("[#] 7 - Information")
            print("[#] other number - Exit")
        
        try:
            if args_list[0] == None:
                option = int(input("[?] Choose an option: "))
                fromCLI = False
            else:
                option = args_list[0]
                fromCLI = True

                # ask the username only if it needs it
                if option == 3:
                    usr = input("[?] Insert username: ")
                    print()

            if option == 1:
                if not fromCLI:
                    pokemon = input("[?] Name of the pokemon: ").capitalize()
                else:
                    pokemon = args_list[1]
                pokeData = pokemon_API_data(pokemon) # the description must be readable

                if pokeData != None:
                    print_pokemon_info(pokeData)

            elif option == 2:
                pokeData = pokemon_API_data(None, randomize=True)
                print_pokemon_info(pokeData)

            elif option == 3:
                pokeData = pokemon_API_data(None, randomize=True)
                print_pokemon_info(pokeData,guess=True)

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
                give_information()

            else:
                quit()
            
        except ValueError:
            print("[X] Only numbers are allowed")
        print()
        if fromCLI:
            quit()
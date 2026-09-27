from sqlite3 import connect
from pathlib import Path
from json import dump
PATH = Path(__file__).resolve().parent

# create the 2 database if there's not already there
def init_dbs() -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS guesses(
            id INTEGER PRIMARY KEY,
            date TEXT DEFAULT (strftime('%Y-%m-%d', 'now')),
            user TEXT NOT NULL,
            guessed INTEGER NOT NULL CHECK(guessed == 0 OR guessed == 1),
            attemp INTEGER NOT NULL CHECK(attemp < 4 AND attemp > 0)
        )""")

    with connect(PATH / "cache/cacheHandling.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS mostChoose(
                id INTEGER PRIMARY KEY,
                date TEXT DEFAULT (strftime('%Y-%m-%d', 'now')) NOT NULL,
                pokemon TEXT NOT NULL UNIQUE,
                nOfTime INTEGER NOT NULL CHECK(nOfTime > 0)
            )""")
    return

# for insert information into the pokemon database
def insert_info(user:str, guessed:bool, attemp:int) -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO guesses(user, guessed, attemp)
        VALUES (?,?,?)""",(user, guessed, attemp))
    return

# for delete a user from a pokemon database
def del_usr(user:str) -> None:
    with connect(PATH / "usrGuess.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM guesses WHERE user=?""",(user,))
        conn.commit()
    return

# query for statistic in pokemon database
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

# add the pokemon in database and in file if there isn't yet
def add_cache_pokemon(pokemon:str, pokeData:dict) -> None:
    with connect(PATH / "cache/cacheHandling.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT nOfTime 
            FROM mostChoose 
            WHERE pokemon=?""",(pokemon,))
        nOfTime = cursor.fetchone()

        if nOfTime == None:
            cursor.execute("""INSERT INTO mostChoose(pokemon,nOfTime)
                VALUES (?,1)""", (pokemon,))
            with open(PATH / f"cache/{pokemon}.json", "w") as file:
                dump(pokeData, file, ensure_ascii=False, indent=4)
        else:
            cursor.execute("""UPDATE mostChoose
                SET nOfTime = ?, date = strftime('%Y-%m-%d', 'now')
                WHERE pokemon = ?""", (nOfTime[0]+1,pokemon))
        return
        

# it checked if there is space for cache otherwise it delete
# the older and less use
def check_cache_space() -> None:
    dir = PATH / "cache"
    nFileJson = 0
    for file in dir.glob("*.json"):
        nFileJson += 1

    if nFileJson >= 6:
        with connect(dir / "cacheHandling.db") as conn:
            cursor = conn.cursor()
            # la formula permette di scegliere e pesare il +
            # vecchio e allo stesso tempo quello scelto meno volte
            cursor.execute("""SELECT pokemon
                FROM mostChoose 
                ORDER BY (julianday('now') - julianday(date)) / sqrt(nOfTime)
                DESC LIMIT 1""" )
            result = cursor.fetchone()
        
        if result != None:
            file = dir / f"{result[0]}.json"
            file.unlink()

            with connect(dir / "cacheHandling.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("""DELETE FROM mostChoose WHERE pokemon=?""",(result[0],))
    return

# delete the rows on the table on cacheHandling.db and all the cache
def delete_cache() -> None:
    dir = PATH / "cache"
    done = True

    # delete all the rows on the table
    with connect(dir / "cacheHandling.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM mostChoose""")

    # delete all the .json file
    for file in dir.glob("*.json"):
        try:
            file.unlink()
        except OSError as error:
            print(f"[X] Can't delete {file}: {error}")
            done = False
    if done:
        print("[V] Done")
    return
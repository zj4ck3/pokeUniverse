# pokeUniverse

`pokeUniverse` is a Python command-line application for exploring Pokémon data through the [PokéAPI](https://pokeapi.co/).

The application allows users to look up Pokémon, discover random Pokémon, play a Pokémon guessing game, compare two Pokémon, and view statistics collected from the guessing game.

## Features

- Display a Pokémon's:
  - ID
  - Height
  - Weight
  - Types
  - Abilities
  - Base stats
- Fetch a random Pokémon from the PokéAPI catalog.
- Guess the name of a randomly selected Pokémon with up to three attempts.
- Store guessing-game results in a local SQLite database.
- Track correct and incorrect guesses for each user.
- Display user statistics, including:
  - Total guesses
  - Correct guesses
  - Wrong guesses
  - General accuracy
  - Maximum personal winning streak
  - General maximum winning streak
- Delete all stored data associated with a username.
- Compare the physical data and total base stats of two Pokémon.
- Handle common API and network errors with user-friendly messages.
- Support command-line arguments.
- Provide an interactive terminal menu.

## Requirements

- Python 3.9 or newer
- Internet access

The application uses:

- `requests` to communicate with PokéAPI.
- `argparse` for command-line argument parsing.
- `sqlite3` for storing guessing-game statistics.
- `pathlib` for handling the database path.

## Installation

1. Clone the repository and enter its directory:

	```bash
	git clone https://github.com/zj4ck3/pokeUniverse.git
	cd pokeUniverse
	```

2. Create and activate a virtual environment (recommended):

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

	On Windows PowerShell, activate it with:

	```powershell
	.venv\Scripts\Activate.ps1
	```

3. Install the dependencies:

	```bash
	python3 -m pip install -r requirements.txt
	```

## Usage

Start the application with:

```bash
python3 pokeUniverse.py
```

Choose an option from the interactive menu:

| Option | Action |
| --- | --- |
| `1` | Search for a Pokemon by name and display its information |
| `2` | Display information for a random Pokemon |
| `3` | Play the Pokemon guessing game |
| `4` | Compare two Pokemon |
| `5` | View some statistics |
| `6` | Delete a username |
| `7` | Display project information |
| Any other number | Exit the application |

Pokemon names can be entered using their standard names, such as `pikachu` or `charizard`. The API lookup is case-insensitive in practice because the application normalizes the input before making the request.

You can also use the app with command-line arguments:
```bash
python3 pokeUniverse.py [option] [pokemon1 if option == 1 or option == 4] [pokemon2 if option == 4]
```

## Project Structure

```text
pokeUniverse/
├── pokeUniverse.py   # Application menu and Pokemon functionality
├── requirements.txt  # Python dependencies
├── LICENSE           # MIT license
├── README.md         # Project documentation
```

## API

Pokemon data is provided by [PokéAPI](https://pokeapi.co/), a free and open RESTful API for Pokemon data. The application requests data from the Pokemon endpoint and formats selected fields for terminal output.

## Contributing

Bug reports, suggestions, and pull requests are welcome. Before submitting a change, verify that the application starts successfully and that the affected menu option works with both valid and invalid Pokemon names.

## License

This project is licensed under the [MIT License](LICENSE).

# pokeUniverse

`pokeUniverse` is a Python command-line application for exploring Pokemon data through the [PokéAPI](https://pokeapi.co/). Look up a Pokemon, discover a random Pokemon, play a guessing game, or compare the stats of two Pokemon from your terminal.

## Features

- Display a Pokemon's ID, height, weight, types, abilities, and base stats.
- Fetch a random Pokemon from the PokéAPI catalog.
- Guess the name of a randomly selected Pokemon with up to three attempts.
- Compare the physical data and total base stats of two Pokemon.
- Handle common API and network errors with user-friendly messages.
- Supports execution with command-line arguments
- Use of sqlite3 Database for statistics (IN PRODUCTION)

## Requirements

- Python 3.9 or newer
- Internet access

The application uses the `requests` package to communicate with PokéAPI and the
builtin `argparse` package for command_line arguments interactions.

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
| `5` | View some statistics - IN PROD |
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

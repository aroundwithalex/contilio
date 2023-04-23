# Contilio Project

This project represents the completion of a coding challenge set by Contilio. Data is extracted from an [Transportation API](https://developer.transportapi.com/) and loaded
into a SQLite database. 

# Running the code

You can run the code by changing your directory to the root level of the project via the `cd` command, and then running `python3 main.py`. Note that before you do this, you should install the requirements via the requirements.txt file via `pip install -r requirements.txt`. This should be done within a virtual environment.

Alteratively, you can create a virtual environment and install the package within that environment via the `pip install .` command. This should also install all required dependencies, and you should then be able to run `python3 main.py`.

# Building the database

To build the database, you can run this command `python3 build_database.py`. Note that you should follow the instructions above to extract the relevant dependencies.

# Running the tests

To run the unit tests, utilise the built-in command within Python. For instance, `python3 unittest -v`.

# Lyrics Counter API
## Requirements prior to set up
Python version >= 3.6

pip must be installed

Developed on mac (unix) therefore the set up on Windows is less automated
## How to set up on mac (unix)
1. Clone the repository from https://github.com/joewheelhouse1990/tech-test.git onto your local drive.
2. Open a terminal at the cloned project.
3. Run the setup_venv.sh file using 'sh setup_venv.sh'. This will set up the virtual environment for the project.

## How to run on mac (unix)
1. Either use the terminal used above, or open a new terminal at the cloned project.
2. Run the project using 'sh run_api.sh'
3. Enter an artist name, or enter QUIT to leave API at any time.

## How to set up on Windows
1. Clone the repository from https://github.com/joewheelhouse1990/tech-test.git
2. Open a cmd at the cloned project.
3. Run 'python -m venv .env' to create a virtual environment.
4. Change cursor using 'cd .env/Scripts/' and then run 'activate.bat'.
5. Change cursor to setup folder 'cd ../..' and then 'cd setup/'.
6. Install the requirements using 'python -m pip install -r requirements.txt'.

## How to run on Windows
1. Open a cmd at the cloned project or change the cursor from setup to the main project folder using 'cd ..'.
2. Run project using 'python -m controller.py'.
3. Enter an artist name, or enter QUIT to leave API at any time.
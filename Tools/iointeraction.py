"""
This program is super-simple.
It assume you have jupyter installed.
Then it takes you directly to Jupyter Notebook Dashboard
in Jnotes folder and thus
makes for easy and full access to Python code 
for Braille displays because your default browser and 
your screen reader software are already tied together.
"""

# import from Python libraries
import subprocess, os

os.chdir("../Jnotes")
subprocess.Popen(["jupyter", "notebook"], creationflags=subprocess.CREATE_NEW_CONSOLE)
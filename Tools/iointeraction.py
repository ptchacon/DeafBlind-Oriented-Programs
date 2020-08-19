"""
A place to build code for adding database data to the db
"""

# import from Python libraries
import pprint, subprocess, sys, os, inspect, importlib

# Third party libraries
import wx, sqlalchemy, sqlalchemy.orm

# Start redirection to output.txt file for 
# the duration of this program.
ofile = open("output.txt", "w")
sys.stdout = ofile

"""
Here you put in code intended for typical print output but 
because of this program, after you finish typing code,
it will launch notepad with your output for inspection.
"""
        
ofile.close()
subprocess.run(["notepad", "output.txt"])
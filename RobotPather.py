import math

import tkinter as tk
from tkinter import filedialog

#YOU CAN EDIT THESE TO MATCH YOUR FUNCTIONS
#_____________________________________________

velocity = 100

DRIVE_FORMAT = "driveInches({dist});"
TURN_FORMAT = "turnInertial({rot}, {dir}, {vel});"

#_____________________________________________





#DEFINING FUNCTIONS

def readfile(filepath):
    try:
        with open(filepath, "r") as file:
            xCoords = []
            yCoords = []
            for line in file:
                coords = line.strip().split(",")  # Fixed splitting issue
                if len(coords) == 2:
                    xCoords.append(float(coords[0].strip()))
                    yCoords.append(float(coords[1].strip()))
        return xCoords, yCoords
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None, None  # Ensure consistent return type
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


# PROMPT FILE

root = tk.Tk() # opens background tab 
root.withdraw() # hide background tab

file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])

if file_path:
    xC, yC = readfile(file_path)
else:
    print("Error when selecting file.")

print(" ") # Move to new line

if xC is None or yC is None:  # Prevent further execution if file read failed
    exit()






# CALCULATIONS

previousAngle = 0 # Set starting angle to 0

for i in range(len(xC) - 1):  # Fixed loop range to avoid index error
    deltaX = xC[i+1] - xC[i]
    deltaY = yC[i+1] - yC[i]
    distance = math.sqrt(deltaX**2 + deltaY**2)
    newAngle = math.degrees(math.atan2(deltaY, deltaX))

    if newAngle < 0:
        newAngle += 360
    
    if i > 0:
        rotation = previousAngle - newAngle
        if rotation > 180:
            rotation -= 360
        if rotation < -180:
            rotation += 360

        if rotation < 0:
            print(TURN_FORMAT.format(rot = rotation, dir = "left", vel = velocity))
        elif rotation > 0:
            print(TURN_FORMAT.format(rot = rotation, dir = "right", vel = velocity))

    print(DRIVE_FORMAT.format(dist = distance))
    previousAngle = newAngle

print("\n\nPath Completed")

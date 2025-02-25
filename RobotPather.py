import math

import tkinter as tk
from tkinter import filedialog

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

def insertClicked():
    text_widget.delete("1.0", tk.END)
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
    if file_path:
        fileLabel.config(text = file_path)
        xC, yC = readfile(file_path)
        if xC is None or yC is None:  # Prevent further execution if file read failed
            exit()
        print(" ") # Move to a new line
        calculateInstructions(xC, yC)
    else:
        print("Error when selecting file.")
        fileLabel.config(text = "Nothing Selected")

def copyOutput():
    window.clipboard_clear()  # Clear clipboard
    window.clipboard_append(text_widget.get("1.0", tk.END))  # Copy text
    window.update()  # Ensures clipboard updates

def calculateInstructions(xC, yC):
    previousAngle = 0 # Set starting angle to 0
    instructionList = ""

    DRIVE_FORMAT = format_drive.get("1.0", 'end-1c')
    TURN_FORMAT = format_turn.get("1.0", 'end-1c')
    velocity = format_velocity.get("1.0", 'end-1c')

    error_encountered = False

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
                #print(TURN_FORMAT.format(rot = rotation, dir = "left", vel = velocity))
                try:
                    instructionList = instructionList + TURN_FORMAT.format(rot = rotation, dir = "left", vel = velocity) + "\n"
                except:
                    error_encountered = True
            elif rotation > 0:
                #print(TURN_FORMAT.format(rot = rotation, dir = "right", vel = velocity))
                try:
                    instructionList = instructionList + TURN_FORMAT.format(rot = rotation, dir = "right", vel = velocity) + "\n"
                except:
                    error_encountered = True
            #print(DRIVE_FORMAT.format(dist = distance))
        try:
            instructionList = instructionList + DRIVE_FORMAT.format(dist = distance, vel = velocity) + "\n"
        except:
            error_encountered = True
        previousAngle = newAngle

    print("\n\nPath Completed")

    if(error_encountered==True):
        text_widget.insert(tk.END, "Unknown replacement field(s).\nThe only replacement fields are:\n\tDrive:\n\t\t{dist} = distance\n\tTurn:\n\t\t{rot} = rotation in degrees\n\t\t{dir} = direction (left or right)\n\t\t{vel} = velocity")
    else:
        text_widget.insert(tk.END, instructionList)
    #print("\n\n\n\n\n")
    #print(instructionList)

# PROMPT FILE

window = tk.Tk() # opens main window
window.title("Robot Pather")
window.geometry("600x400")

# creating label
fileLabel = tk.Label(window, text="Insert Text File")
fileLabel.config(font=("Arial", 15))
fileLabel.pack()

# creating button

insertButton = tk.Button(window, text="Insert", command=insertClicked)
insertButton.pack()

# creating copy-button

copyButton = tk.Button(window, text="Copy", command=copyOutput)
copyButton.pack()

# Formatting Labels

formatDriveDefault = "driveInches({dist}, {vel});"
formatTurnDefault = "turnInertial({rot}, {dir}, {vel});"
velocityDefault = "100"

format_velocity = tk.Text(window, height = 1, width = 8)
format_velocity.insert(tk.END, velocityDefault)
format_velocity.pack(expand=True)

format_drive = tk.Text(window, height = 1, width = 50)
format_drive.insert(tk.END, formatDriveDefault)
format_drive.pack(expand=True)

format_turn = tk.Text(window, height = 1, width = 50)
format_turn.insert(tk.END, formatTurnDefault)
format_turn.pack(expand=True)

# Create a Text widget

text_widget = tk.Text(window, wrap="word", height=15, width=50)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar and attach it to the Text widget

scrollbar = tk.Scrollbar(window, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

window.mainloop()



import math

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


coordsFilePath = input("Enter the file path of the text file: ")
print(" ") # Move to new line

xC, yC = readfile(coordsFilePath)

if xC is None or yC is None:  # Prevent further execution if file read failed
    exit()

previousAngle = 0



# CALCULATIONS

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
            print("turn left for", abs(rotation), "degrees")
        elif rotation > 0:
            print("turn right for", rotation, "degrees")

    print("drive for", distance)
    previousAngle = newAngle

print("\n\nPath Completed")

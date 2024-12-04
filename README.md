Welcome!

## Project Title
### BLUE PRINT GREEN DESIGN

## Project Description
**BLUE PRINT GREEN DESIGN** is an interactive app for anyone who wants to create and visualize simple building plans in 2D, calculate and visualize their heat loss, and get energy analysis for each component to make informed decisions to improve energy efficiency.

The “Home” screen allows users to design layouts by defining the project name, location, and dimensions, as well as defining rooms, walls, windows, doors, floors, and roofs. The “Detail” screen allows users to either directly input component U-values (thermal transmittance) or enter material layers for each building component. The app uses web-scraping to fetch thermal conductivity values for component heat loss calculations. After the heat loss calculations, the “Calculate” screen breaks down the building’s heat loss, detects the least efficient components, and gives prioritized retrofit suggestions.

This project aims to integrate design and basic sustainability evaluation in a user-friendly, visually compelling interface.


## Run Instructions
### Running the Project
1. **Main File**: Run `main.py` in an editor (or IDE) that supports Python.

2. **Required Libraries/Modules**:
   - `cmu_graphics`: A library for creating interactive graphics.
   - `requests`: For web scraping to fetch material thermal conductivity data.
   - `beautifulsoup4`: For parsing HTML content.
   - `webbrowser`: To be directed to web as needed (e.g. degreedays.net for HDD). Native Python, no need to install.


### Installation Instructions
Run the following libraries to install the necessary libraries: 
   - `cmu_graphics`: pip install cmu-graphics
   - `requests`: pip install requests
   - `beautifulsoup4`: pip install beautifulsoup4


## Shortcut Commands

### Key Navigation
- **`0`**: Navigate to the **Home Screen**.
- **`1`**: Open the **Draw Screen** to create building plans.
- **`2`**: Open the **Detail Screen** to add U-values or material layers to each component.
- **`3`**: Open the **Calculate Screen** to display the calculated heat loss and energy report.

### Component Detail Shortcuts (on Detail Screen)
- **`w`**: Enter U-values or material layers to **Walls**.
- **`g`**: Enter U-values or material layers to **Windows**.
- **`d`**: Enter U-values or material layers to **Doors**.
- **`f`**: Enter U-values or material layers to **Floors**.
- **`r`**: Enter U-values or material layers to to **Roofs**.

### Drawing & Adding Components
- **Add Components (Buttons on Screen)**:
  - Use **`+ADD WINDOW`**, **`+ADD DOOR`**, **`+ADD ROOM`** buttons in the **Draw Screen** to add respective components.
- **Undo**:
  - Use **`UNDO WINDOW`**, **`UNDO DOOR`**, **`UNDO ROOM`** buttons in the **Draw Screen** to remove the most recently added window, door, or room.

### Data Input & Updates
- **Heat Loss Calculation**:
  - Press **`s`** to update and print building details, heat loss coefficients, and component information to the console for testing and validation.

### Mouse Events
- **Mouse Clicks**: Used to add components such as **windows**, **doors**, and **rooms** to the building.
- **Mouse Hover**: Used for button hover over effects.

### Gallery Actions
- **Reset Gallery**: Click the button **`RESET GALLERY`** on the **Home Screen** to remove all saved building projects from the gallery. Click the button **`SAVE & CLOSE`** to save a project to the gallery.





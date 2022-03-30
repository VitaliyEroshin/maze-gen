# Maze Generator
## Idea
This is first project from python 3.x course at MIPT

## What to do?
1) Install requirements (Tkinter):
``` 
pip3 install -r requirements.txt
```
or 
```
pip3 install tk
```

2) Run the app: 
``` 
python3 src/main.py
```

3) Enjoy! 🥳

## Documentation
### Buttons:
  **Run** - Start maze generation
  
  **Stop** - Stop maze generation
  
  **Reset** - Clear maze canvas
  
  **Save** - Save maze. After click, program will ask a filename. Default save location is project folder.
  
  **Play** - Enter playground mode. You will be spawned at left top corner, and your aim is to get to right bottom corner.
  
  **Algorithm** - Choose another generation algorithm. Algorithm must be ```.py``` file, containing generator ```def algorithm(maze)```, where maze is visited vertices array (see ```dfs.py``` for example). By default there are two algorithms ```dfs.py``` and ```kruskal.py``` located in ```./src/algorithms```.
  
  **Path** - Show path from left top to right bottom corners.
  
  **Paint** - Run beautiful color flood into maze.
  
### Sliders:
  **Wall thickness** - is value between 2 and 32 (wall thickness in pixels). Wall thickness cannot be less than way thickness.
  
  **Way thickness** - is value between 2 and 32 (way thickness in pixels).
  
  **Speed** - is a logarithmic slider of generation speed.


## Demo
https://user-images.githubusercontent.com/36928556/159808615-1a81228b-32f0-44f5-a1c2-a9bdfb6ba93c.mov

https://user-images.githubusercontent.com/36928556/160942251-3a6c865b-b8b2-4296-9f15-788306d6f405.mov


﻿# GJK: narrow phase collision detection 

## Requirements

*	**Two 2D convex poly-line objects**
	*	Implement object definition
	*	either read line segment positions from text file
	*	or implement user interface to create poly-line by clicking on canvas
	*	Implement 2D Proximity GJK algorithm
*	**Implement method ClosestPoint() on simplex**
	*	Implement method SupportHC() for Hill Climbing support function
	*	Implement method 2D BestSimplex() for simplex refinement (simpler case as in 3D)
*	**Implement user interaction with object**
	*	User can move object (rotation is optional)
	*	Show closest points (features) on both geometries

## How to run:
* You need Kivy library to run this project.
* Run python3 -m pip install -r requirements.txt in your shell
* Then just run python3 app.py
## Demo link : https://youtu.be/QgIEynUqJLI
# Robot Kinematics Simulation

The goal of this program is to provide a simple and visual way to represent the kinematics of a robot.

This software uses Pygame to display and control the different aspect of this simulation

To get the frames position of the robot the software uses the DH method to solve the direct kinematics problem

## Installation

if you want to run this program please install `python3` at this [link](https://www.python.org/downloads/) and also the module `numpy` and `pygame`.

here are the commande that can be use to install the modules with pip3

```bash
  pip3 install numpy
  pip3 install pygame
```
finaly to run the program please clone the repo and run the `main.py` with this command.

```bash
  python3 main.py 
```
## Settings

There are many settings that can be changed in this software that change the way the camera is defined or the pygame user control.

Here are the main variables that can be changed, It is adviced to not change the other variable because they might directly impact the program features.

### main.py
- DH_mat: This impact directly the robot structure following the DH convention and is the main setting of this software (IHM might be put to configurate easily the structure)
- thetas: This variable impact the initial configuration of the robot kinematic
- displayFrame/size: size of the frame unit vectors
- displayGrid/cell: size of the grid cells

### Camera.py
- depth : define the distance of the camera from the origin
- res_mile: define the angular distance of the camera (in pixel/m)
- dist : define the minimum and maximum distance the camera can see
- zoom : It is an other way to define the focal of the camera (it shows the scaling that is applied from the minimum distance to the maximum distance 

## Control

- you can control the zoom of the simulation by pressing the up and down arrows
- You can rotate the simulation by clicking and dragging on the simulation screen
- you can change the theta values by pressing the 0 to 7 keys to change each thetas defined
- you can click on each values on the bottom to change the theta's values
- you can click on the DH button to display the DH matrix
- from this DH matrix you can change each values (angles in radian) and add or delete a row (be careful you can only add at the end)
- you can press the space bar to print in the terminal the traforms matrix and the DH model





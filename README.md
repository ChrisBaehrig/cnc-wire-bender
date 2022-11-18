# cnc-wire-bender
Open Source Project by ChrisBaehrig for a cnc controlled wire bender based on an arduino and cad fusion360 file

## Concept and changes 
The Hardware bases on the Idea of Pensas diwire bender (https://code.google.com/archive/p/diwire/ License: https://creativecommons.org/licenses/by-sa/3.0/us/) and the Project from HowtoMechatronics Wire Bender (https://howtomechatronics.com/projects/arduino-3d-wire-bending-machine/). 
Power electronic ist improved to for more durability and stronger wires. 
Software is new developed for the end to end production from the cad tool fusion 360 until the cnc wire bending

## Workflow and Architecture
![image](https://user-images.githubusercontent.com/60329834/202792362-5203a7a0-5221-4389-9dc4-5816899560f9.png)

![image](https://user-images.githubusercontent.com/60329834/202801029-710168b7-b5dd-4b51-b331-91631d460f81.png)



## Overview GCode commands

### G1 single Axis 
Example: ```N4 G01 X10 I1500 Y2 J1200 Z9 K1300```
  - Row: 4 
  - Command: G1
  - X-Axis: Angle: +10 degree, Speed: 1500 steps / sec
  - Y-Axis: Angle: +2 degree, Speed: 1200 steps / sec
  - Z-Axis: Angle: +9 degree, Speed: 1300 steps / sec

### G2 multi Axis similstaniouly --> tbd

### G3 Circle bending 
Example: ```N4 G03 R100 Y10 Z10 L200 I1500 J1200 K1300 P0.1``` 
  - Row: 4 
  - Command: G3
  - R: Radius + 10mm clockwise, Speed: 1500 steps / sec
  - Y: Y-Angle: +10 degree, Speed: 1200 steps / sec
  - Z: Z-Angle: +10 degree, Speed: 1500 steps / sec
  - L: Absolute Lenght: 200mm
  - (Optional) Correctionfactor P0.1 = 10% overbending

Example: ```N4 G03 R100 Y10 Z10 H2.5 I1500 J1200 K1300```
  - H: count of turns (2.5 turns)

### G4 Wait 
Example: ```G04 H5```
  - Wait 5 sec

### G5 Wait for Event --> tbd

### G28 Go Home
Example: ```G28```
  - Drive to home position
  <img src="https://user-images.githubusercontent.com/60329834/202800320-6cf4278f-aaba-4bc1-9ac1-806bc5389ff6.png" alt="image" width="400"/>

### G92 Set all Positions to Null
Example: ```G92```
  - Set all Positions to Null to Calibrate 

### M10 Drive Wire to bender
Example: ```M10```
  - drive feeder 2000 steps 

### M11 Drive Wire for manuel cutting
Example: ```M11```
  - drive feeder 200 steps 

### M20 Pin down
Example: ```M20```
  - Moves Pin down

### M21 Pin up
Example: ```M21```
  - Moves Pin up

### M30 Program end
Example: ```M30```



## Serial connection API Commands: 

| variable      	| < 	| row 	| , 	| command 	| , 	| value1 	    | , 	| value2    	| , 	| value3 	| , 	| value4 	| > 	|
|---------------	|---	|-----	|---	|---------	|---	|--------   	|---	|--------   	|---	|--------	|---	|--------	|---	|
| datatyp       	|   	| int 	|   	| int     	|   	| long      	|   	| long      	|   	| long   	|   	| float  	|   	|
| X-Axis (bend) 	| < 	| 1    	| , 	| 1        	| , 	| steps 	    | , 	| steps/sec 	| , 	| 0      	| , 	| 0.0    	| > 	|
| Y-Axis (feed) 	| < 	| 1   	| , 	| 2        	| , 	| steps 	    | , 	| steps/sec 	| , 	| 0      	| , 	| 0.0    	| > 	|
| Z-Axis (turn) 	| < 	| 1   	| , 	| 3        	| , 	| steps     	| , 	| steps/sec 	| , 	| 0      	| , 	| 0.0    	| > 	|
| p-Axis (pin)   	| < 	| 1   	| , 	| 4        	| , 	| degree    	| , 	| 0         	| , 	| 0      	| , 	| 0.0    	| > 	|
| Wait for taster	| < 	| 1   	| , 	| 5        	| , 	| 0     	    | , 	| 0         	| , 	| 0      	| , 	| 0.0    	| > 	|
| tbd            	| < 	| 1   	| , 	| 6        	| , 	| 0     	    | , 	| 0         	| , 	| 0      	| , 	| 0.0    	| > 	|
| tbd            	| < 	| 1   	| , 	| 7        	| , 	| 0     	    | , 	| 0         	| , 	| 0      	| , 	| 0.0    	| > 	|
| wait in ms     	| < 	| 1   	| , 	| 8        	| , 	| ms     	    | , 	| 0         	| , 	| 0      	| , 	| 0.0    	| > 	|
| switch debug   	| < 	| 1   	| , 	| 9        	| , 	| 1=ON 0=OFF	| , 	| 0         	| , 	| 0      	| , 	| 0.0    	| > 	|

Examples: 
```<123, 1, 100, 2000, 0, 0>```

```<1,4,160,0>``` Pin oben ```<1,4,50,0>``` Pin unten


## Changelog
### [1.0.0] - 2022-10-10

- Initial release


## Acknowledgements

Many thanks to

- [Pensas diwire bender](https://code.google.com/archive/p/diwire/) for the development the first bender
- [How to Mechatronics](https://howtomechatronics.com/projects/arduino-3d-wire-bending-machine/) for a lot of improvments


## Disclaimer
The Projekt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

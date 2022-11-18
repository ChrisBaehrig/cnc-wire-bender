# cnc-wire-bender
Open Source Project by ChrisBaehrig for a cnc controlled wire bender based on an arduino and cad fusion360 file

## Concept and changes 
The Hardware bases on the Idea of Pensas diwire bender (https://code.google.com/archive/p/diwire/ License: https://creativecommons.org/licenses/by-sa/3.0/us/) and the Project from HowtoMechatronics Wire Bender (https://howtomechatronics.com/projects/arduino-3d-wire-bending-machine/). 
Power electronic ist improved to for more durability and stronger wires. 
Software is new developed for the end to end production from the cad tool fusion 360 until the cnc wire bending

## Workflow and Architecture
![image](https://user-images.githubusercontent.com/60329834/202792362-5203a7a0-5221-4389-9dc4-5816899560f9.png)



## Mechanic


## Electronic


## Software

### Fusion 360 Macro


### Transformation coordiantes to G-code
List of G-code commands

### G-code Parser to Machine commands

### Bender API

### Serial connection API Commands: 

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
<123, 1, 100, 2000, 0, 0>
<1,4,160,0> Pin oben <1,4,50,0> Pin unten


## Changelog
### [1.0.0] - 2022-10-10

- Initial release


## Acknowledgements

Many thanks to

- [Pensas diwire bender](https://code.google.com/archive/p/diwire/) for the development the first bender
- [How to Mechatronics](https://howtomechatronics.com/projects/arduino-3d-wire-bending-machine/) for a lot of improvments


## Disclaimer
The Projekt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# bridge-dp-display
App to reflect ship movements commanded from ROV Jason van to the host ship's DP system.
During a lowering the ROV Jason navigator moves the vehicle above the sea bottom by inserting
commands into the host ship's dynamic positioning system. This app was developed to inform ship's
personnel of the effect of these commands. That is, the app presents pictorial (compass and
arrows) and textual information about the direction and speed of the current move being requested
by the Jasoin navigator, as well as estimated time to completion. Currently it is run on a RaspPi
system (Ubuntu16.04) with a 7" screen.

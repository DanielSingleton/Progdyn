# ProgdynTrial2

A full listing of the subprograms of PROGDYN is given below.  To allow the reader to understand or make use of PROGDYN, we describe here first the overall structure of the program.  We also list and describe in this section some helper programs that were used to analyze the data from the trajectory calculations.

The master control program for dynamics, in the form of a Unix Shell Script, is called progdynstarterHP.  For a user to start to use progdynstarterHP, some early lines in it that assign the scratch space and the location of the program files and input files would have to be modified for the local environment.  These lines are between lines 45 and 60 and should be apparent.  The location of the scratch space is usually passed to progdynstarterHP as a parameter.

progdynstarterHP takes as input files:

    freqinHP - This is the standard output from a Gaussian 98, 03, 09, or 16 frequency calculation using freq=hpmodes.   For isotopically labeled compounds, use freq=(hpmodes,readisotopes). 

    progdyn.conf – This is a file giving a variety of configuration options, called on by many of the subprograms.  progdyn.conf examples are listed below and contains explanations of the program options. 

    detour – A signal file that, by existing, signals the program to do a side calculations. This is usually omitted.

    nogo – A signal file that, by existing, signals the program to stop between points This is usually omitted.

    bypassproggen - A signal file that, by existing, signals the program to use a supplied input file geoPlusVel instead of generating one for itself.  This is most often used when running dynamics in solution, and was not employed here.

    methodfile – A file that contains lines to be added to the end of each g09.com input file, such as lines that call for an NMR calculation.  This is usually omitted.

    ZMAT – An input file for the CFOUR (http://www.cfour.de) suite of programs.  When ZMAT is supplied, progdynstarterHP will automatically run call CFOUR (which must be set up independently by the user) by making use of the script progcfour.   This is usually omitted.

    cannontraj – A file containing a vector for each atom, used to fire an initial geometry in a particular direction.  This is usually omitted.

progdynstarterHP calls the following programs:

proggenHP - An awk program that starts a trajectory, giving each mode its zero point energy (if a quasiclassical calculation) plus random additional excitations depending on the temperature. Because proggenHP calls two python 3 programs, the local environment has to be set up in whatever way will get the python calls to work. 

prog1stpoint – Awk program that creates the first Gaussian input file for each run

prog2ndpoint – Awk program that creates the second Gaussian input file for each run.  prog2ndpoint also checks the energy of the first point to see if it fits with the desired energy, and aborts the run if it does not by creating appropriate output in file Echeck

progdynb – Creates subsequent Gaussian input files until run is completed, written in awk

proganal – A program to analyze the latest point and see if a run is done.  This program must be redone for each new system.  Elaborate changes are sometimes programmed into proganal, such as the automatic changing of configuration variables.  proganal creates the output to dynfollowfile and NMRlist or NMRlistdis

progcfour – A control script to run CFOUR calculations (not needed for most kinds of runs, not used or listed here). 

 
proggenHP calls three python 3 programs:

randgen.py – A python program that generates random numbers between 0 and 1.  These are generated all at once and stored in a temporary file for use by proggenHP.

tozmat.py – a python 3 program that takes a temporary geometry file in cartesian format and converts it to another temporary geometry file in internal coordinates.

toxyz.py – a python 3 program that takes a temporary geometry file in internal coordinates format and converts it to another temporary geometry file in cartesian coordinates.

 
progdynstarterHP has the following output files:

isomernumber – A running tab of the trajectory number

runpointnumber – a running tab of the point in the trajectory

Echeck – output from where prog2ndpoint checks the energy of the trajectory to see if it fits with the desired energy

geoRecord – A record of all of the geoPlusVel files.

geoPlusVel – Created by proggen, this gives the starting positions, velocities, isotopic masses, excitations of the normal modes, and initial displacements of the normal modes for current run.

g09.com or g16.com – Created by prog1stpoint, prog2ndpoint, and progdynb, this is the latest input file for Gaussian09 or Gaussian 16 for current run and latest point.

olddynrun, olddynrun2, olddynrun3 – files containing the last three outputs from Gaussian, for creation of the next point

traj, traj1, traj2, traj3, etc. – files containing the geometries and energies for each trajectory, numbered by the isomernumber, in a format suitable for reading by Molden.  The energies listed in these files are for the previous point.

dynfollowfile – A short record of the runs and their results.  The data desired for dynfollowfile must be programed into the script proganal as needed for each system studied.

NMRlist or NMRlistdis – output of NMR predictions at each point in a trajectory, when desired. Usually not used.

skipstart - A signal file that, by existing, tells progdynstarterHP that we are in the middle of a run.  For trajectories that are propagated forward and backward in time, skipstart keeps track of whether one is in the forward or reverse part.

diagnostics – optional output that follows which subprograms are running and configuration variables, decided by variable in progdyn.conf.

vellist – optional output that lists the velocities of each atom, decided by variable in progdyn.conf, or lists the total kinetic energy in the system and the classical temperature, often also keeps track of the density

A number of files starting with 'temp' are created then later erased.

Of the series of files:

prog1stpoint, prog2ndpoint, progdynb, and proggenHP should not need modified (unless you end up doing new kinds of things)

For most forms of dynamics you need to make a freqinHP file, which is the output from a gaussian freq calculation on your system of interest, ran with freq=hpmodes or, if you just ran a regular freq calc, freq=(readfc,hpmodes)

randgen is a program that generates 10,000 random numbers.  If it does not work on your system, recompile it from randgen.c

proganal is an awk script that pulls out whatever you want to keep track of from the geometry of each point in the trajectory, and it decides when a trajectory is done by writing XXX to one of the output files.  Proganal will have to be modified for each system.  

progdyn.conf is the main file where you set options for the trajectory run, and it contains most of the documentation, such as it is

Some of the early lines of progdynstarterHP need modified to  tell the program where to find gaussian, randgen, freqinHP, and all of the program files, along with the initialization of gaussian.  Modify these lines as needed.

    echo $1
    scratchdir=$1
    export g09root=/software/lms/g09_D01
    . $g09root/g09/bsd/g09.profile
    origdir=`pwd`
    cd $origdir
    logfile=docslog
    randdir=~/bin
    proggramdir=~/binall
    freqfile=~/binall/freqinHP

call progdynstarterHP from a queue job submission file, and I usually set things up so that I pass the location of gaussian scratch files from the job submission script to progdynstarterHP as a $1 parameter

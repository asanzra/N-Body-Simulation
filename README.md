# Description
This project gives the programs and tools to simulate the gravitation of N-bodies (N-body-problem) through the resolution of the corresponding differential equations.

It uses Python and the corresponding libraries listed in the requirements file.

# Attention ⚠️​
Some general results of the program can be viewed in the file **"Results-Report.pdf"**. This was the project report for the Univesity of Nottingham's Physics proffesors in the Scientific Computing subject.

# Some of the images and videos resulting from applying the program to varied scenarios.

### Video and graph of the Burrau problem (3 bodies in orbit).

https://github.com/user-attachments/assets/ce1b16d4-e551-4616-9bab-6c94661ab83d

![F4_3](https://github.com/user-attachments/assets/da054012-bcf6-424b-af5a-aa73737ad3a7)

### Solar system orbits and stability.
![F3_2](https://github.com/user-attachments/assets/b0b4d427-e811-4924-aa2e-4bda24e0b87a)
![F2_2](https://github.com/user-attachments/assets/55858f37-f64f-4378-88cf-2879f00ebc50)
![F2_3](https://github.com/user-attachments/assets/4dad3d84-8d0f-4d65-88c3-1fd9c14234c0)

### Video example and result of a 3D oct-tree creation, implemented for optimization

https://github.com/user-attachments/assets/d5400360-f85f-4af0-8f30-97cb0a374bac

![F8](https://github.com/user-attachments/assets/a618a2ed-4d34-45cd-b9f1-a2a0cf245e16)

# Running the program
To run the files first make sure you have the needed extensions by running:
pip install -r requirements.txt

The files than should be run start with "_N_impl" and are .py files, the rest .py files contain utility functions used in the other ones.

N goes from 1 to 8, corresponding to each figure (and 9 corresponds to figure 10)
The variables may be changed to change behaviour, but they are set to recommended state.
Changing this settings may change the run times too.

Additionally, you can also run 6_7_8_9_barnes_hut/parallel_velocities.py,
this corresponds to figure 9.

## RUN TIMES (on my machine):
*Plane means with no input or output file

- 1  
    - Around 5 secs plain.
    - Around 5 secs with input file. 
    - Around 30 secs saving .csv.
- 2 
    - Under 20 secs with input file.
    - Around 9 minutes plain.
    - Even more saving .csv
- 3:  
    - Around 20 secs plain. 
    - Around 30 secs loading from file
    - Around 2 mins saving .csv. 
- 4:  
    - Under 1 min and fastest animation loading from file
    - Under 1 min plain
    - Around 5 mins saving .csv
- 5:  
    - Around 2 mins plain
    - Around 2 mins loading from file
    - Around 3 mins saving .csv
- 6:  
    - Instant. No file.
- 7:  
    - Around 5 secs loading from file
    - Over 10 mins plain, and saving .csv
- 8:  
    - Instant. No file.
- 9:  Remember to close overview of initial points to start program
    - Around 5 secs loading from file
    - Over 6 mins plain
    - Around 15 minutes saving .csv

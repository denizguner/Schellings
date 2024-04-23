# Schelling Segregation Model
This is a python simulation of the Schellings Segregation model that I created for an assignment for the class "14.15, Networks" that I took at MIT during Spring 2024.

## Usage

The simulation can be ran in one of two modes, "animate", which creates an animation of the progression of the model board over time for a given threshold parameter,
and "plot", which creates a plot of mean satisfaction ratios in the long term for different threshold parameters.

run the file with the command:

```
python Schellings.py mode e q p
```

Where mode is one of "animate" or "plot", e is the number of empty cells in the simulation, q is the fraction of cells that are of group 1, and p, which is to only be specified
if the mode is "animate" is the satisfaction threshold parameter for the model.

Sample usages:

```
python Schellings.py animate 250 0.6 0.5
python Schellings.py plot 300 0.75
```

## Sample Plots:

Here are two plots generated with this program:

![](https://raw.githubusercontent.com/denizguner/Schellings/main/Figure_1.png)

![](https://raw.githubusercontent.com/denizguner/Schellings/main/Figure_2.png)

These plots were generated with parameters e = 250, q = 0.5 and e = 250, q = 0.75 respectively


## Acknowledgements

Special thanks to my friend Amir Kolic (kolic@mit.edu), whose deep investigation into the possible variations of the Schellings model greatly contributed to the creation of this project.
Please find his implementation of this assignment here: https://github.com/lutscha/ShellingSegregationModel

I would also like to thank my friends Ege Kabasakaloglu (egekabas@mit.edu), Yaman Bora Otuzbir (ybora31@gmail.com) and Jasna Ilieva (jasna23@mit.edu), whom I discussed much of this assignment with.

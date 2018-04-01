## Tips data
[archive](https://github.com/Moons08/personal-project-archive)

- [First analysis note](https://github.com/Moons08/personal-project-archive/blob/master/180209_seaborn_tips/180209_seaborn_tips.ipynb)

- [With Scikit-learn](https://github.com/Moons08/personal-project-archive/blob/master/180209_seaborn_tips/Tips_classification.ipynb)

data status (*from seaborn*)
    - columns : total_bill, tip, sex, smoker, day, time, size
    - number of rows : 244

#### what to do
- find a way to get more tips

#### what I used
> pandas | seaborn | pgmpy

#### hypothesis
- First
    1. total_bill
    1. size
    1. time (Dinner > Lunch)

- Second
    1. sex
    1. smoker
    1. day

- Last
    - there could be the feature of upper class


#### conclusion

- there is the feature of upper class
- if every conditions below are fulfilled, the possibility of getting more tips goes up to **24%** rather than nothing fulfilled.
    - here are the conditions:
        >*In order of importance*
        > 1. size (>= 4)
        > 1. day (weekend)
        > 1. sex (man)
        > 1. time (dinner)
        > 1. smoker (no)

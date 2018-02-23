## Tips data

- data status (*from seaborn*)
    - columns : total_bill, tip, sex, smoker, day, time, size
    - number of rows : 244

#### what to do
- find a way to get more tip

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
- if every below conditions are fulfilled, the posibility of getting more tip goes up to **24%** rather than nothing fulfilled.
    - here are the conditions:
        >*In order of importance*
        > 1. size (>= 4)
        > 1. day (weekend)
        > 1. sex (man)
        > 1. time (dinner)
        > 1. smoker (no)

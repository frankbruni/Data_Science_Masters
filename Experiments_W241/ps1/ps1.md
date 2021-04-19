Problem Set 1
================
Alex, Micah, and Scott
12/01/2020

``` r
library(data.table)

knitr::opts_chunk$set(echo = TRUE)
```

# Potential Outcomes Notation

1.  Explain the notation \(Y_i(1)\).
2.  Explain the notation \(Y_1(1)\).
3.  Explain the notation \(E[Y_i(1)|d_i=0]\).
4.  Explain the difference between the notation \(E[Y_i(1)]\) and
    \(E[Y_i(1)|d_i=1]\)

**1.The potential outcome of a given treated subject.**

**2.The potential outcome of the first (i = 1) treated subject.**

**3. Expected value of what the potential outcome would be for treated
subjects. We are not able to actually observe this since d = 0.**

**4. The first one is the expected potential outcome for the entire set
of subjects while the second equation is the expected potential outcome
for treated subjects. If we properly do random assignment these will be
equal values.**

# Potential Outcomes and Treatment Effects

1.  Use the values in the table below to illustrate that
    \(E[Y_i(1)]-E[Y_i(0)] = E[Y_i(1)- [Y_i(0)]\).
2.  Is it possible to collect all necessary values and construct a table
    like the one below in real life? Explain why or why not.

<!-- end list -->

``` r
table <- data.table(
  subject = 1:7, 
  y_0 = c(10, 12, 15, 11, 10, 17, 16), 
  y_1 = c(12, 12, 18, 14, 15, 18, 16),
  tau = c(2, 0, 3, 3, 5, 1, 0)
)
table
```

    ##    subject y_0 y_1 tau
    ## 1:       1  10  12   2
    ## 2:       2  12  12   0
    ## 3:       3  15  18   3
    ## 4:       4  11  14   3
    ## 5:       5  10  15   5
    ## 6:       6  17  18   1
    ## 7:       7  16  16   0

``` r
E_y_0 = mean(table[,y_0])
E_y_1 = mean(table[,y_1])

E_T = mean(table[,tau])

E_y_1 - E_y_0 == E_T
```

    ## [1] TRUE

**2. In actually we cannot make this table because each subject can
either be treated or not. We can never observe both control and
treatment in a single subject. The best we can do is use random
assignment by creating two groups of observations that are identical in
expectation.**

# Visual Acuity

Suppose we are interested in the hypothesis that children playing
outside leads them to have better eyesight.

Consider the following population of ten children whose visual acuity we
can measure.

  - Visual acuity is the decimal version of the fraction given as output
    in standard eye exams.
  - Someone with 20/20 vision has acuity 1.0, while someone with 20/40
    vision has acuity 0.5.
  - Numbers greater than 1.0 are possible for people with better than
    “normal” visual acuity.

<!-- end list -->

``` r
d <- data.table(
  child = 1:10, 
  y_0 = c(1.2, 0.1, 0.5, 0.8, 1.5, 2.0, 1.3, 0.7, 1.1, 1.4), 
  y_1 = c(1.2, 0.7, 0.5, 0.8, 0.6, 2.0, 1.3, 0.7, 1.1, 1.4)
)
```

In this table:

  - `y_1` means means the measured *visual acuity* if the child were to
    play outside at least 10 hours per week from ages 3 to 6’  
  - `y_0` means the measured *visual acuity* if the child were to play
    outside fewer than 10 hours per week from age 3 to age 6;
  - Both of these potential outcomes *at the child level* would be
    measured at the same time, when the child is 6.

<!-- end list -->

1.  Compute the individual treatment effect for each of the ten
    children.
2.  Tell a “story” that could explain this distribution of treatment
    effects. In particular, discuss what might cause some children to
    have different treatment effects than others.
3.  For this population, what is the true average treatment effect (ATE)
    of playing outside.
4.  Suppose we are able to do an experiment in which we can control the
    amount of time that these children play outside for three years. We
    happen to randomly assign the odd-numbered children to treatment and
    the even-numbered children to control. What is the estimate of the
    ATE you would reach under this assignment? (Please describe your
    work.)
5.  How different is the estimate from the truth? Intuitively, why is
    there a difference?
6.  We just considered one way (odd-even) an experiment might split the
    children. How many different ways (every possible ways) are there to
    split the children into a treatment versus a control group (assuming
    at least one person is always in the treatment group and at least
    one person is always in the control group)?
7.  Suppose that we decide it is too hard to control the behavior of the
    children, so we do an observational study instead. Children 1-5
    choose to play an average of more than 10 hours per week from age 3
    to age 6, while Children 6-10 play less than 10 hours per week.
    Compute the difference in means from the resulting observational
    data.
8.  Compare your answer in (7) to the true ATE. Intuitively, what causes
    the difference?

<!-- end list -->

``` r
d <- data.table(
  child = 1:10, 
  y_0 = c(1.2, 0.1, 0.5, 0.8, 1.5, 2.0, 1.3, 0.7, 1.1, 1.4), 
  y_1 = c(1.2, 0.7, 0.5, 0.8, 0.6, 2.0, 1.3, 0.7, 1.1, 1.4)
)

d[, tau := y_1-y_0]
d
```

    ##     child y_0 y_1  tau
    ##  1:     1 1.2 1.2  0.0
    ##  2:     2 0.1 0.7  0.6
    ##  3:     3 0.5 0.5  0.0
    ##  4:     4 0.8 0.8  0.0
    ##  5:     5 1.5 0.6 -0.9
    ##  6:     6 2.0 2.0  0.0
    ##  7:     7 1.3 1.3  0.0
    ##  8:     8 0.7 0.7  0.0
    ##  9:     9 1.1 1.1  0.0
    ## 10:    10 1.4 1.4  0.0

**2. The treatment effects are distributed in this way because children
in this age have different eye sight due to genetics. Some children have
good eye sight when they are young and some need glasses at a young age.
This is usually due to genetics or diet (carrots).**

**3.**

``` r
mean(d[,tau])
```

    ## [1] -0.03

**4.**

``` r
d[, treatment := ifelse(child %% 2 == 0, 0, 1)]
mean(d[treatment==1][,y_1])-mean(d[treatment==0][,y_0])
```

    ## [1] -0.06

**5. We are off from the truth because of the way we randomly selected
our children there was a bias.**

**6.**

``` r
2**10 -2
```

    ## [1] 1022

**7.**

``` r
d[, treatment := ifelse(child <= 5 , 1, 0)]
mean(d[treatment==1][,y_1])-mean(d[treatment==0][,y_0])
```

    ## [1] -0.54

**8. This is very far from the true ATE. This can be because children
with good eyesight prefer to go outside more. There could be many
reasons in an observational study why a subject chooses to do what they
did, this is not good for our experiment**

# Randomization and Experiments

1.  Assume that researcher takes a random sample of elementary school
    children and compare the grades of those who were previously
    enrolled in an early childhood education program with the grades of
    those who were not enrolled in such a program. Is this an
    experiment, an observational study, or something in between?
    Explain\!
2.  Assume that the researcher works together with an organization that
    provides early childhood education and offer free programs to
    certain children. However, which children that received this offer
    was not randomly selected by the researcher but rather chosen by the
    local government. (Assume that the government did not use random
    assignment but instead gives the offer to students who are deemed to
    need it the most) The research follows up a couple of years later by
    comparing the elementary school grades of students offered free
    early childhood education to those who were not. Is this an
    experiment, an observational study, or something in between?
    Explain\!
3.  Does your answer to part (2) change if we instead assume that the
    government assigned students to treatment and control by “coin toss”
    for each student? Why or why not?

**1. This is an observational study because the researcher did not
interfere and give a treatment to two identical groups. Rather, the
researcher observed two different groups that by nature are different
from each other.**

**2. This is in between an experiment and observational study because
the government did not pick students at random. Becasue of this there is
a selection bias. There could be an issue where the students who are
picked need it the most so they work extra hard to receive the best
grades. This is different from an experiement since it would be two
equal groups picked at random to receive the free schooling.**

**3. If a coin toss was implemented this would now be an experiment
because there is no more selection bias. By randomizing our control and
treatment groups we no longer need to worry about the case where
children in need will try extra hard because this is all inclusive in
the study. Randomization ensures the two groups are statistically
similar.**

# Moral Panic

Suppose that a researcher finds that high school students who listen to
death metal music at least once per week are more likely to perform
badly on standardized test. :metal: As a consequence, the researcher
writes an opinion piece in which she recommends parents to keep their
kids away from “dangerous, satanic music”.

  - Let the potential outcomes to control, \(Y_i(0)\), be each student’s
    test score when listening to death metal at least one time per week.
  - Let \(Y_i(1)\) be the test score when listening to death metal less
    than one time per week.

<!-- end list -->

1.  Explain the statement \(E[Y_i(0)|D_i=0] = E[Y_i(0)|D_i=1]\) in
    words. First, state the rote english language translation –
    i.e. “The expected value of …” – but then, second, tell us the
    *meaning* of this statement.
2.  Do you expect that this circumstance actually matches with the
    meaning that you’ve just written down? Why or why not?

**1. The expected value of the test scores of students when listening to
metal once per week is equal to what the expected value of the test
scores of students would have been had they listened to metal once per
week. We can measure the first value but not the second value. The
potential outcome of the test scores for students that listen to metal
once per week is the same (it is a value that exisits) if they are in
treatment or control.**

**2. This circumstance does not match the meaning because we cannot
measure both these things in real life. We would need to create to
statistically equal groups and randomly assign them to control and
treatment to have a proper experiement.**

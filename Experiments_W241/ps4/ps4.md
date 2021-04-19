Experiments and Causality: Problem Set \#4
================
Alex, Scott & Micah
12/9/2020

``` r
library(data.table)

library(sandwich)
library(lmtest)
```

    ## Loading required package: zoo

    ## 
    ## Attaching package: 'zoo'

    ## The following objects are masked from 'package:base':
    ## 
    ##     as.Date, as.Date.numeric

``` r
library(knitr)
library(stargazer)
```

    ## 
    ## Please cite as:

    ##  Hlavac, Marek (2018). stargazer: Well-Formatted Regression and Summary Statistics Tables.

    ##  R package version 5.2.2. https://CRAN.R-project.org/package=stargazer

# 1\. Noncompliance in Recycling Experiment

Suppose that you want to conduct a study of recycling behavior. A number
of undergraduate students are hired to walk door to door and provide
information about the benefits of recycling to people in the treatment
group. Here are some facts about how the experiment was actually carried
out.

  - 1,500 households are assigned to the treatment group.
  - The undergrads tell you that they successfully managed to contact
    700 households.
  - The control group had 3,000 households (not contacted by any
    undergraduate students).
  - The subsequent recycling rates (i.e. the outcome variable) are
    computed and you find that 500 households in the treatment group
    recycled. In the control group, 600 households recycled.

<!-- end list -->

1.  What is the ITT? Do the work to compute it, and store it into the
    object `recycling_itt`.

<!-- end list -->

``` r
recycling_itt <- (500/1500) - (600/3000)
```

2.  What is the CACE? Do the work to compute it, and store it into the
    object `recycling_cace`.

<!-- end list -->

``` r
ittd=  700/1500 - 0/3000
recycling_cace <-recycling_itt/ittd
```

There appear to be some inconsistencies regarding how the undergraduates
actually carried out the instructions they were given.

  - One of the students, Mike, tells you that they actually lied about
    the the number of contacted treatment households and that the true
    number was 500.
  - Another student, Andy, tells you that the true number was actually
    600.

<!-- end list -->

3.  What is the CACE if Mike is correct?

<!-- end list -->

``` r
mike=  500/1500 - 0/3000
cace_mike <-recycling_itt/mike
```

4.  What is the CACE if Andy is correct?

<!-- end list -->

``` r
andy = 600/1500 - 0/3000
cace_andy <- recycling_itt/andy
```

For the rest of this question, suppose that **in fact** Mike was telling
the truth.

5.  What was the impact of the undergraduates’s false reporting on our
    estimates of the treatment’s effectiveness?

> The more the undergraduates false report the lower our cace estimate
> will be.

6.  Does your answer change depending on whether you choose to focus on
    the ITT or the CACE?

> The ITT does not change based off the false reporting. The cace
> changes depending on the number of false reporting.

# 2\. Fun with the placebo

The table below summarizes the data from a political science experiment
on voting behavior. Subjects were randomized into three groups: a
baseline control group (not contacted by canvassers), a treatment group
(canvassers attempted to deliver an encouragement to vote), and a
placebo group (canvassers attempted to deliver a message unrelated to
voting or politics).

| Assignment | Treated? |    N | Turnout |
| :--------- | :------- | ---: | ------: |
| Baseline   | No       | 2463 |  0.3008 |
| Treatment  | Yes      |  512 |  0.3890 |
| Treatment  | No       | 1898 |  0.3160 |
| Placebo    | Yes      |  476 |  0.3002 |
| Placebo    | No       | 2108 |  0.3145 |

## Evaluating the Placebo Group

1.  Construct a data set that would reproduce the table. (Too frequently
    we receive data that has been summarized up to a level that is
    unuseful for our analysis. Here, we’re asking you to “un-summarize”
    the data to conduct the rest of the analysis for this question.)

<!-- end list -->

``` r
d = data.table('assignment' = rep(c('Baseline','Treatment','Treatment','Placebo','Placebo'),summary_table[,N]),
           'treatment' = rep(c(0,1,0,1,0),summary_table[,N]),
            'turnout' = c(rep(1,741),rep(0,1722),rep(1,200),rep(0,312),rep(1,600),rep(0,1298),rep(1,143),rep(0,333),rep(1,663),rep(0,1445)))
d
```

    ##       assignment treatment turnout
    ##    1:   Baseline         0       1
    ##    2:   Baseline         0       1
    ##    3:   Baseline         0       1
    ##    4:   Baseline         0       1
    ##    5:   Baseline         0       1
    ##   ---                             
    ## 7453:    Placebo         0       0
    ## 7454:    Placebo         0       0
    ## 7455:    Placebo         0       0
    ## 7456:    Placebo         0       0
    ## 7457:    Placebo         0       0

2.  Estimate the proportion of compliers by using the data on the
    treatment group.

<!-- end list -->

``` r
compliance_rate_t <- nrow(d[(assignment=='Treatment' & treatment == 1),])/nrow(d[(assignment=='Treatment'),])
compliance_rate_t 
```

    ## [1] 0.2124481

3.  Estimate the proportion of compliers by using the data on the
    placebo group.

<!-- end list -->

``` r
compliance_rate_p <- nrow(d[(assignment=='Placebo' & treatment == 1),])/nrow(d[(assignment=='Placebo'),])
compliance_rate_p
```

    ## [1] 0.1842105

4.  Are the proportions in parts (1) and (2) statistically significantly
    different from each other? Provide *a test* and n description about
    why you chose that particular test, and why you chose that
    particular set of data.

<!-- end list -->

``` r
proportions_difference_test <- prop.test(x=c(512,476),n = c(1898+512,2108+476))
proportions_difference_test 
```

    ## 
    ##  2-sample test for equality of proportions with continuity
    ##  correction
    ## 
    ## data:  c(512, 476) out of c(1898 + 512, 2108 + 476)
    ## X-squared = 6.0887, df = 1, p-value = 0.0136
    ## alternative hypothesis: two.sided
    ## 95 percent confidence interval:
    ##  0.005698449 0.050776764
    ## sample estimates:
    ##    prop 1    prop 2 
    ## 0.2124481 0.1842105

> I used a two sample proportions z test to determine that these
> propotions are significantly different since the p value is less than
> 0.05.

5.  What critical assumption does this comparison of the two groups’
    compliance rates test? Given what you learn from the test, how do
    you suggest moving forward with the analysis for this problem?

> The two group compliance rates tests whether the teatment and placebo
> are a proper comparision. Since we have a different amount of
> compliers in placebo and treatment we cannot use the intent to treat,
> we can use the CACE.

6.  Estimate the CACE of receiving the placebo. Is the estimate
    consistent with the assumption that the placebo has no effect on
    turnout?

<!-- end list -->

``` r
itt= (((476/(476+2108))*.3002) + ((2108/(476+2108))*.3145))-.3008
ittd = 476/(476+2108)
cace_estimate <- itt/ittd
cace_estimate
```

    ## [1] 0.06007143

> The cace tells us that the placebo has almost no affect on voter
> turnout and this is consistent with what we expect.

## Estimate the CACE Several Ways

7.  Using a difference in means (i.e. not a linear model), compute the
    ITT using the appropriate groups’ data. Then, divide this ITT by the
    appropriate compliance rate to produce an estiamte the CACE.

<!-- end list -->

``` r
itt <-  (((512/(512+1898))*.389) + ((1898/(512+1898))*.316))-.3008
ittd <- (512/(512+1898))
cace_means <- itt/ittd 
cace_means
```

    ## [1] 0.1445469

8.  Use two separate linear models to estimate the CACE of receiving the
    treatment by first estimating the ITT and then dividing by
    \(ITT_{D}\). Use the `coef()` extractor and in line code evaluation
    to write a descriptive statement about what you learn after your
    code.

<!-- end list -->

``` r
itt_model   <- lm(turnout~assignment,data=d)

itt_d_model <- lm(treatment~assignment,data=d)
cace_estimate <-coef(itt_model)[3]/coef(itt_d_model)[3]
```

> Estimating the cace of receiving the treatment using two linear models
> is the same as estimating the cace using the difference in means from
> the previous part.

9.  When a design uses a placebo group, one additional way to estiamte
    the CACE is possible – subset to include only compliers in the
    treatment and placebo groups, and then estimate a linear model.
    Produce that estimate here.

<!-- end list -->

``` r
t = d[(assignment=='Treatment' & treatment == 1) | (assignment=='Placebo' & treatment == 1) ,]

itt_model   <- lm(turnout~assignment,data=t)

itt_d_model <- lm(treatment~assignment,data=t)

cace_subset_model <- coef(itt_model)[2]/coef(itt_d_model)[2]
cace_subset_model
```

    ## assignmentTreatment 
    ##        8.706979e+13

10. In large samples (i.e. “in expectation”) when the design is carried
    out correctly, we have the expectation that the results from 7, 8,
    and 9 should be the same. Are they? If so, does this give you
    confidence that these methods are working well. If not, what
    explains why these estimators are producing different estimates?

> 7 and 8 are the same but 9 is different. A possible reason 9 is
> different is because we are including placebo data and we previously
> proved that the placebo data is statistically different from the
> treatment data since they have a different proportion of compliers..

11. In class we discussed that the rate of compliance determines whether
    one or another design is more efficient. (You can review the
    textbook expectation on page 162 of *Field Experiments*)). Given the
    compliance rate in this study, which design *should* provide a more
    efficient estimate of the treatment effect?

> ITTd \< 1/2 implies that a placebo design is prefered. Conventional
> design is prefered when ITTD \> 1/2 since it provides estimates with
> less sampling variability.

12. When you apply what you’ve said in part (11) against the data that
    you are working with, does the {placebo vs. treatment} or the
    {control vs. treatment} comparison produce an estimate with smaller
    standard errors?

> Placebo vs treatment comparison produces smaller standard errors since
> the comparision would be less noisy by dropping out the never takers.
> It is less practical since in most cases it takes more resources to
> carry out a placebo design.

# 3\. Turnout in Dorms

Guan and Green report the results of a canvassing experiment conduced in
Beijing on the eve of a local election. Students on the campus of Peking
University were randomly assigned to treatment or control groups.

  - Canvassers attempted to contact students in their dorm rooms and
    encourage them to vote.
  - No contact with the control group was attempted.
  - Of the 2,688 students assigned to the treatment group, 2,380 were
    contacted.
  - A total of 2,152 students in the treatment group voted; of the 1,334
    students assigned to the control group, 892 voted.
  - One aspect of this experiment threatens to violate the exclusion
    restriction. At every dorm room they visited, even those where no
    one answered, canvassers left a leaflet encouraging students to
    vote.

<!-- end list -->

``` r
d <- fread('https://ucb-mids-w241.s3-us-west-1.amazonaws.com/Guan_Green_CPS_2006.csv')
d
```

    ##       turnout treated   dormid treatment_group
    ##    1:       0       0  1010101               0
    ##    2:       0       0  1010101               0
    ##    3:       0       0  1010101               0
    ##    4:       0       0  1010102               0
    ##    5:       0       0  1010102               0
    ##   ---                                         
    ## 4020:       1       1 24033067               1
    ## 4021:       1       1 24033068               1
    ## 4022:       1       1 24033068               1
    ## 4023:       1       1 24033068               1
    ## 4024:       1       1 24033068               1

Here are definitions for what is in that data:

  - `turnout` did the person turn out to vote?
  - `treated` did someone at the dorm open the door?
  - `dormid` a unique ID for the door of the dorm
  - `treatment_group` whether the dorm door was assigned to be treated
    or not

## Use Linear Regressions

1.  Estimate the ITT using a linear regression on the appropriate subset
    of data. Notice that there are two `NA` in the data. Just na.omit to
    remove these rows so that we are all working with the same data.
    Given the ways that randomization was conducted, what is the
    appropriate way to construct the standard errors?

<!-- end list -->

``` r
d = na.omit(d)
dorm_model <-lm(turnout ~treatment_group,data = d)
dorm_model
```

    ## 
    ## Call:
    ## lm(formula = turnout ~ treatment_group, data = d)
    ## 
    ## Coefficients:
    ##     (Intercept)  treatment_group  
    ##          0.6687           0.1319

``` r
coeftest(dorm_model,vcovCL(dorm_model))
```

    ## 
    ## t test of coefficients:
    ## 
    ##                 Estimate Std. Error t value  Pr(>|t|)    
    ## (Intercept)     0.668666   0.012890 51.8730 < 2.2e-16 ***
    ## treatment_group 0.131930   0.015019  8.7839 < 2.2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

> The best way to construct the standard errors is through robust
> standard errors. This helps account for when the structure of
> variation is unknown.

## Use Randomization Inference

1.  How many people are in treatment and control? Does this give you
    insight into how the scientists might have randomized? As ususal,
    include a narrative setence after your code.

<!-- end list -->

``` r
n_treatment <- 2688
n_control   <- 1334
```

> It looks like they assigned more to the treatment to account for the
> possibility of non compliance. They randomized by dorm room.

2.  Write an algorithm to conduct the Randomization Inference. Be sure
    to take into account the fact that random assignment was clustered
    by dorm room.

<!-- end list -->

``` r
treatment_group_mean <- d[, .(group_mean = mean(turnout)), keyby = treatment_group]

ate  <-  treatment_group_mean[treatment_group == 1, group_mean] - treatment_group_mean[treatment_group == 0, group_mean]

ri   <- rep(NA, 1000)

for (i in 1:1000) {
ri[i] <- d[, .(group = mean(turnout)), keyby = .(sample(treatment_group))][ , .('ate' = diff(group))]
}
p_value <- sum(ri >= ate) / 1000
p_value
```

    ## [1] 0

``` r
riTest <- function(tbl, reps) {
  riArray <- rep(NA, reps)
  for (ri in 1:reps) {
    riArray[ri] <- tbl[, .(mean_value = mean(turnout)), keyby = .(sample(treatment_group))][, diff(mean_value)]
  }
  return(riArray)
}
getPval <- function(riResults, ate) {
  res <- (sum(riResults >= ate) + sum(riResults <= -ate)) / length(riResults)
  return(res)
}


getPval(riTest(d,10000),0.13)
```

    ## [1] 0

> I got 0 for both p values.

3.  What is the value that you estimate for the treatment effect?

<!-- end list -->

``` r
dorm_room_ate <- sum(riTest(d,10000))/10000
dorm_room_ate
```

    ## [1] -8.335642e-05

4.  What are the 2.5% and 97.5% quantiles of this distribution?

<!-- end list -->

``` r
riresults = riTest(d,10000)

dorm_room_ci <- c(quantile(riresults,0.025),quantile(riresults,0.975))
dorm_room_ci
```

    ##        2.5%       97.5% 
    ## -0.02846624  0.02873786

5.  What is the p-value that you generate for the test: How likely is
    this treatment effect to have been generated if the sharp null
    hypothesis were true.

<!-- end list -->

``` r
p_value <- 0
```

> Very unlikely that the treatment was generated if the sharp null
> hypothesis was true.

6.  Assume that the leaflet (which was left in case nobody answered the
    door) had no effect on turnout. Estimate the CACE either using ITT
    and ITT\_d or using a set of linear models. What is the CACE, the
    estimated standard error of the CACE, and the p-value of the test
    you conduct?

<!-- end list -->

``` r
itt = lm(turnout~treatment_group, data = d)
ittd = lm(treated ~ treatment_group, data = d)

dorm_room_cace <- coef(itt)[2]/coef(ittd)[2]
dorm_room_cace
```

    ## treatment_group 
    ##       0.1489402

7.  What if the leaflet that was left actually *did* have an effect? Is
    it possible to estimate a CACE in this case? Why or why not?

> We would not be able to determine the effects of the leaflet since we
> do not know who received the leaflets.

# 4\. Another Turnout Question

We’re sorry; it is just that the outcome and treatment spaces are so
clear\!

Hill and Kousser (2015) report that it is possible to increase the
probability that someone votes in the California *Primary Election*
simply by sending them a letter in the mail. This is kind of surprising,
because who even reads the mail anymore anyways? (Actually, if you talk
with folks who work in the space, they’ll say, “We know that everybody
throws our mail away; we just hope they see it on the way to the
garbage.”)

Can you replicate their findings? Let’s walk through them.

``` r
number_rows <- 100 # you should change this for your answer. full points for full data

d <- data.table::fread(
  input = 'https://ucb-mids-w241.s3-us-west-1.amazonaws.com/hill_kousser_analysis_file.csv')
```

(As an aside, you’ll note that this takes some time to download. One
idea is to save a copy locally, rather than continuing to read from the
internet. One problem with this idea is that you might be tempted to
make changes to this cannonical data; changes that wouldn’t be reflected
if you were to ever pull a new copy from the source tables. One method
of dealing with this is proposed by [Cookiecutter data
science](https://drivendata.github.io/cookiecutter-data-science/#links-to-related-projects-and-references).)

Here’s what is in that data.

  - `age.bin` a bucketed, descriptive, version of the `age.in.14`
    variable
  - `party.bin` a bucketed version of the `Party` variable
  - `in.toss.up.dist` whether the voter lives in a district that often
    has close races
  - `minority.dist` whether the voter lives in a majority minority
    district, i.e. a majority black, latino or other racial/ethnic
    minority district
  - `Gender` voter file reported gender
  - `Dist1-8` congressional and data districts
  - `reg.date.pre.08` whether the voter has been registered since before
    2008
  - `vote.xx.gen` whether the voter voted in the `xx` general election
  - `vote.xx.gen.pri` whether the voter voted in the `xx` general
    primary election
  - `vote.xx.pre.pri` whether the voter voted in the `xx` presidential
    primary election
  - `block.num` a block indicator for blocked random assignment.
  - `treatment.assign` either “Control”, “Election Info”, “Partisan
    Cue”, or “Top-Two Info”
  - `yvar` the outcome variable: did the voter vote in the 2014 primary
    election

These variable names are horrible. Do two things:

  - Rename the smallest set of variables that you think you might use to
    something more useful. (You can use `data.table::setnames` to do
    this.)
  - For the variables that you think you might use; check that the data
    makes sense;

When you make these changes, take care to make these changes in a way
that is reproducible. In doing so, ensure that nothing is positional
indexed, since the orders of columns might change in the source data).

While you’re at it, you might as well also modify your `.gitignore` to
ignore the data folder. Because you’re definitely going to have the data
rejected when you try to push it to github. And every time that happens,
it is a 30 minute rabbit hole to try and re-write git history.

## Some questions\!

1.  **A Simple Treatment Effect**: Load the data and estimate a `lm`
    model that compares the rates of turnout in the control group to the
    rate of turnout among anybody who received *any* letter. This model
    combines all the letters into a single condition – “treatment”
    compared to a single condition “control”. Report robust standard
    errors, and include a narrative sentence or two after your code.

<!-- end list -->

``` r
d[,assigned_treatment:=ifelse(treatment.assign == 'Control',0,1)]
model_simple <- lm(yvar~assigned_treatment,data= d)
model_simple_se <- coeftest(model_simple,vcov = vcovHC(model_simple))
model_simple_se
```

    ## 
    ## t test of coefficients:
    ## 
    ##                      Estimate Std. Error  t value  Pr(>|t|)    
    ## (Intercept)        0.09312478 0.00015062 618.2813 < 2.2e-16 ***
    ## assigned_treatment 0.00489923 0.00078340   6.2538 4.007e-10 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

> the robust standard errors

2.  **Specific Treatment Effects**: Suppose that you want to know
    whether different letters have different effects. To begin, what are
    the effects of each of the letters, as compared to control? Estimate
    an appropriate linear model and use robust standard errors.

<!-- end list -->

``` r
model_letters <- lm(yvar~as.factor(treatment.assign),data=d)
model_letters_se <- coeftest(model_letters,vcov=vcovHC(model_letters))
model_letters_se
```

    ## 
    ## t test of coefficients:
    ## 
    ##                                            Estimate Std. Error  t value
    ## (Intercept)                              0.09312478 0.00015062 618.2813
    ## as.factor(treatment.assign)Election info 0.00498464 0.00172734   2.8857
    ## as.factor(treatment.assign)Partisan      0.00525971 0.00122666   4.2878
    ## as.factor(treatment.assign)Top-two info  0.00449610 0.00122250   3.6778
    ##                                           Pr(>|t|)    
    ## (Intercept)                              < 2.2e-16 ***
    ## as.factor(treatment.assign)Election info 0.0039050 ** 
    ## as.factor(treatment.assign)Partisan      1.804e-05 ***
    ## as.factor(treatment.assign)Top-two info  0.0002353 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

> Roughly 4% less peeople turnout to vote as compared to the control
> group.

3.  Does the increased flexibilitiy of a different treatment effect for
    each of the letters improve the performance of the model? Test,
    using an F-test. What does the evidence suggest, and what does this
    mean about whether there **are** or **are not** different treatment
    effects for the different letters?

<!-- end list -->

``` r
model_anova <- var.test(model_simple,model_letters)
model_anova
```

    ## 
    ##  F test to compare two variances
    ## 
    ## data:  model_simple and model_letters
    ## F = 1, num df = 3872266, denom df = 3872264, p-value = 0.9996
    ## alternative hypothesis: true ratio of variances is not equal to 1
    ## 95 percent confidence interval:
    ##  0.9985915 1.0014086
    ## sample estimates:
    ## ratio of variances 
    ##          0.9999995

4.  **More Specific Treatment Effects** Is one message more effective
    than the others? The authors have drawn up this design as a
    full-factorial design. Write a *specific* test for the difference
    between the *Partisan* message and the *Election Info* message.
    Write a *specific* test for the difference between *Top-Two Info*
    and the *Election Info* message. Report robust standard errors on
    both tests and include a short narrative statement after your
    estimates.

<!-- end list -->

``` r
model_partisan_vs_info <- 'fill this in'
model_top_two_vs_info  <- 'fill this in'
```

5.  **Blocks? We don’t need no stinking blocks?** The blocks in this
    data are defined in the `block.num` variable (which you may have
    renamed). There are a *many* of blocks in this data, none of them
    are numerical – they’re all category indicators. How many blocks are
    there?

> 

6.  **SAVE YOUR CODE FIRST** but then try to estimate a `lm` that
    evaluates the effect of receiving *any letter*, and includes this
    block-level information. What happens? Why do you think this
    happens? If this estimate *would have worked* (that’s a hint that we
    don’t think it will), what would the block fixed effects have
    accomplished?

<!-- end list -->

``` r
model_block_fx  <- 'fill this in'
```

6.  Even though we can’t estimate this fixed effects model directly, we
    can get the same information and model improvement if we’re *just a
    little bit clever*. Create a new variable that is the *average
    turnout within a block* and attach this back to the data.table. Use
    this new variable in a regression that regresses voting on
    `any_letter` and this new `block_average`. Then, using an F-test,
    does the increased information from all these blocks improve the
    performance of the *causal* model? Use an F-test to check.

<!-- end list -->

``` r
model_block_average <- 'fill this in'
f_test_results      <- 'fill this in'
```

7.  Doesn’t this feel like using a bad-control in your regression? Has
    the treatment coefficient changed from when you didn’t include the
    `block_average` measure to when you did? Have the standard errors on
    the treatment coefficient changed from when you didn’t include the
    `block_average` measure to when you did? Why is this OK to do?

> 

# Consider Designs

Determine the direction of bias in estimating the ATE for each of the
following situations when we randomize at the individual level. Do we
over-estimate, or underestimate? Briefly but clearly explain your
reasoning.

1.  Suppose that you’re advertising games – Among Us? – to try and
    increase sales, and you individually randomly-assign people into
    treatment and control. After you randomize, you learn that some
    treatment-group members are friends with control-group members IRL.

> There would be more sales so we would end up underestimating the ate.
> This effect of more sales is due to spillover.

2.  As we’re writing this question, end-of-year bonuses are being given
    out in people’s companies. (This is not a concept we have in the
    program – each day with your smiling faces is reward enough – and
    who needs money anyways?) Suppose that you’re interested in knowing
    whether this is a good idea from the point of view of worker
    productivity and so you agree to randomly assign bonuses to some
    people. *What might happen to your estimated treatment effects if
    people learn about the bonuses that others have received?*

> Productivity may go down if the workers that did not receive a bonus
> get upset when they see fellow co workers received one. If this is the
> case we would over estimated the worth of giving bonuses.

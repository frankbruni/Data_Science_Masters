Problem Set 2
================
Alex, Micah, and Scott
12/07/2020

``` r
library(data.table)
library(sandwich)
library(lmtest)

library(ggplot2)
library(knitr)
```

# 1. What happens when pilgrims attend the Hajj pilgrimage to Mecca?

What happens when a diverse set of people are brought together toward a
common purpose? Maybe it brings people together, or maybe instead it
highlights the differences between groups. [Clingingsmith, Khwaja and
Kremer (2009)](https://dash.harvard.edu/handle/1/3659699) investigate
the question. by asking Pakistani nationals to provide information about
their views about people from other nations.

The random assignment and data is collected in the following way
(detailed in the paper):

-   Pakistani nationals apply for a chance to attend the Hajj at a
    domestic bank. Saudi Arabia agreed in the time period of the
    study (2006) to grant 150,000 visas.
-   Of the 135,000 people who applied for a visa, 59% of those who
    applied were successful.
-   The remainder of the visas were granted under a different allocation
    method that was not randomly assigned, and so this experiment cannot
    provide causal evidence about other allocation mechanisms.
-   Among the 135,000 who apply, the authors conduct a random sample and
    survey about these respondents views about others.

Using the data collected by the authors, test, using randomization
infernece, whether there is a change in beliefs about others as a result
of attending the Hajj.

-   Use, as your primary outcome the `views` variable. This variable is
    a column-sum of each respondent’s views toward members of other
    countries.
-   Use, as your treatment feature `success`. This variable encodes
    whether the respondent successfully attended the Hajj.

``` r
d <- fread("../data/clingingsmith_2009.csv")
```

1.  State the sharp-null hypothesis that you will be testing.

> Fill this in with your null.

1.  Using `data.table`, group the data by `success` and report whether
    views toward others are generally more positive among lottery
    winners or lottery non-winners. This answer should be of the form
    `d[ , .(mean_views = ...), keyby = ...]` where you have filled in
    the `...` with the appropriate functions and varaibles.

``` r
hajj_group_mean <- 'fill this in' # the result should be a data.table with two colums and two rows
hajj_ate        <- 'fill this in' # from the `hajj_group_mean` produce a single, numeric vector that is the ate. check that it is numeric using `class(hajj_ate)`
```

But is this a “meaningful” difference? Or, could a difference of this
size have arisen from an “unlucky” randomization? Conduct 10,000
simulated random assignments under the sharp null hypothesis to find
out. (Don’t just copy the code from the async, think about how to write
this yourself.)

``` r
## do your work to conduct the randomiation inference here.
## as a reminder, RI will randomly permute / assign the treatment variable
## and recompute the test-statistic (i.e. the mean difference) under each permutation

hajj_ri_distribution <- 'fill this in' # this should be a numeric vector that has a length equal to the number of RI permutations you ran
```

1.  How many of the simulated random assignments generate an estimated
    ATE that is at least as large as the actual estimate of the ATE?
    Conduct your work in the code chunk below, saving the results into
    `hajj_count_larger`, but also support your coding with a narrative
    description. In that narrative description (and throughout), use R’s
    “inline code chunks” to write your answer consistent with each time
    your run your code.

``` r
hajj_count_larger <- 'fill this in' # length 1 numeric vector from comparison of `hajj_ate` and `hajj_ri_distribution`
```

1.  If there are `hajj_count_larger` randomizations that are larger than
    `hajj_ate`, what is the implied *one-tailed* p-value? Both write the
    code in the following chunk, and include a narrative description of
    the result following your code.

``` r
hajj_one_tailed_p_value <- 'fill this in' # length 1 numeric vector 
```

1.  Now, conduct a similar test, but for a two-sided p-value. You can
    either use two tests, one for larger than and another for smaller
    than; or, you can use an absolute value (`abs`). Both write the code
    in the following chunk, and include a narrative description of the
    result following your code.

``` r
hajj_two_tailed_p_value <- 'fill this in' # length 1 numeric vector 
```

# 2. Randomization Inference Practice

Suppose that you’ve been hired as the data scientist at a quack
nootropics company. Despite their fraudulent intent, you’re dedicated to
doing good data science. Or, at least science as good as you can.

Their newest serum, *kniht* purports to raise its users’ executive
function. You think that it is just amphetamines.

As the data scientist for the company, you convince them to conduct a
trial. Great! The good news is this:

-   Each person is measured twice.
-   Before one of the measurements, they are given a placebo. Before the
    other of the measurements they are given *kniht*.
-   You ask for instrumentation on two concepts:
    -   Creativity, measured as number of proposed alternative uses of
        an object. (This is a classic, test of “creativity”, proposed by
        J.P. Guilford. For example, how many things can you propose
        doing with a camera tripod? )
    -   Physical Arousal, measured through skin conductance (i.e. how
        sweaty is someone).

The bad news is this: The company knows that they’re selling nonsense,
and they don’t want you to be able to prove it. They reason that if they
provide you only six test subjects, that you won’t be able to prove
anything, and that they can hide behind a “fail-to-reject” claim.

``` r
kniht <- data.table(
  person  = rep(LETTERS[1:6], each = 4), 
  treat   = rep(0:1, each = 2), 
  measure = rep(c('creative', 'sweat'))
)


kniht[measure == 'creative' & treat == 0, 
      value := c(10, 13, 14, 16, 25, 40)]
kniht[measure == 'creative' & treat == 1, 
      value := c(12, 11, 13, 20, 21, 46)]
kniht[measure == 'sweat' & treat == 0, 
      value := c(0.4, 0.7, 0.3, 0.8, 1.0, 1.4)]
kniht[measure == 'sweat' & treat == 1, 
      value := c(0.4, 0.7, 2.0, 0.9, 1.6, 2.2)]
```

Conduct the following tests.

1.  Conduct the appropriate t-test that respects the repeated-measures
    nature of the data (is this a paired or independent samples t-test?)
    for both the `creative` and the `sweat` outcomes. After you conduct
    your tests, write a narrative statement about what you conclude.

``` r
t_test_creative <- 'fill this in'
```

``` r
t_test_sweat <- 'fill this in'
```

1.  Conduct the appropriate randomization inference test that respects
    the repeated-measures nature of the data. After you conduct your
    tests, write a narrative statement about what you conclude.

``` r
# do your work, and then save your computed p-value in the object
creative_ate     <- 'fill this in'
creative_ri      <- 'fill this in'
creative_p_value <- 'fill this in'
```

``` r
# do your work, and then save your computed p-value in the object
sweat_ate     <- 'fill this in'
sweat_ri      <- 'fill this in'
sweat_p_value <- 'fill this in'
```

1.  Which of these tests are more appropriate to the task at hand, and
    why? Based on the tests that you have run, what do you conclude
    about the effectiveness of *kniht*?

# 3. Sports Cards

In this experiment, the experimenters invited consumers at a sports card
trading show to bid against one other bidder for a pair trading cards.
We abstract from the multi-unit-auction details here, and simply state
that the treatment auction format was theoretically predicted to produce
lower bids than the control auction format. We provide you a relevant
subset of data from the experiment.

In this question, we are asking you to produce p-values and confidence
intervals in three different ways:

1.  Using a `t.test`;
2.  Using a regression; and,
3.  Using randomization inference.

``` r
d <- fread('../data/list_data_2019.csv')
```

1.  Using a `t.test`, compute a 95% confidence interval for the
    difference between the treatment mean and the control mean. After
    you conduct your test, write a narrative statement, using inline
    code evaluation that describes what your tests find, and how you
    interpret these results. (You should be able to look into
    `str(t_test_cards)` to find the pieces that you want to pull to
    include in your written results.)

``` r
t_test_cards <- 'fill this in' # this should be the t.test object. Extract pieces from this object in-text below the code chunk. 
```

1.  In plain language, what does this confidence interval mean?

1.  Conduct a randomization inference process using an estimator that
    you write by hand (i.e. in the same way as earlier questions). On
    the sharp-null distribution that this process creates, compute the
    2.5% quantile and the 97.5% quantile using the function `quantile`
    with the appropriate vector passed to the `probs` argument. After
    you conduct your test, write a narrative statement of your test
    results.

``` r
## first, do you work for the randomization inference
ri_distribution <- 'fill this in' # numeric vector of length equal to your number of RI permutations
ri_quantiles    <- 'fill this in' # there's a built-in to pull these. 
```

1.  Do you learn anything different if you regress the outcome on a
    binary treatment variable? To answer this question, regress `bid` on
    a binary variable equal to 0 for the control auction and 1 for the
    treatment auction and then calculate the 95% confidence interval
    using *classical standard errors* (in a moment you will calculate
    with *robust standard errors*). There are two ways to do this – you
    can code them by hand; or use a built-in, `confint`. After you
    conduct your test, write a narrative statement of your test results.

``` r
mod <- 'fill this in' # this should be a model object, class = 'lm'. 
```

1.  Calculate the 95% confidence interval using robust standard errors,
    using the `sandwich` package. There is a function in `lmtest` called
    `coefci` that can help with this. It is also possible to do this
    work by hand. After you conduct your test, write a narrative
    statement of your test results.

2.  Characterize what you learn from each of these different methods –
    are the results contingent on the method of analysis that you
    choose?

# Power Analysis

Understanding whether your experiment design and data collection
strategy are able to reject the null hypothesis *when they should* is
valuable! And, this isn’t theoretical value. If your design and data
collection cannot reject the null hypothesis, why even run the
experiment in the first place?

The classical formulation of power asks, “Given a test procedure and
data, what proportion of the tests I *could conduct* would reject the
null hypothesis?”

Imagine that you and David Reiley are going to revive the sports card
experiment from the previous question. However, because it is for a
class project, and because you’ve already spent all your money on a
shiny new data science degree :raised\_hands: :money\_with\_wings: ,
you’re not going to be able to afford to recruit as many participants as
before.

1.  Describe a t-test based testing procedure that you might conduct for
    this experiment. What is your null hypothesis, and what would it
    take for you to reject this null hypothesis? (This second statement
    could either be in terms of p-values, or critical values.)

1.  Suppose that you are only able to recruit 10 people to be a part of
    your experiment – 5 in treatment and another 5 in control. Simulate
    “re-conducting” the sports card experiment once by sampling from the
    data you previously collected, and conducting the test that you’ve
    written down in part 1 above. Given the results of this 10 person
    simulation, would your test reject the null hypothesis?

``` r
t_test_ten_people <- 'fill this in' # this should be a test object
```

1.  Now, repeat this process – sampling 10 people from your existing
    data and conducting the appropriate test – one-thousand times. Each
    time that you conduct this sample and test, pull the p-value from
    your t-test and store it in an object for later use. Consider
    whether your sampling process should sample with or without
    replacement.

``` r
t_test_p_values <- rep(NA, 1000) # fill this in with the p-values from your power analysis

## you can either write a for loop, use an apply method, or use replicate (which is an easy-of-use wrapper to an apply method)
```

1.  Use `ggplot` and either `geom_hist()` or `geom_density()` to produce
    a distribution of your p-values, and describe what you see. What
    impression does this leave you with about the power of your test?

2.  Suppose that you and David were to actually run this experiment and
    design – sample 10 people, conduct a t-test, and draw a conclusion.
    **And** suppose that when you get the data back, **lo and behold**
    it happens to reject the null hypothesis. Given the power that your
    design possesses, does the result seem reliable? Or, does it seem
    like it might be a false-positive result?

1.  Apply the decision rule that you wrote down in part 1 above to each
    of the simulations you have conducted. What proportion of your
    simulations have rejected your null hypothesis? This is the p-value
    that this design and testing procedure generates. After you write
    and execute your code, include a narrative sentence or two about
    what you see.

``` r
t_test_rejects <- 'fill this in'
```

1.  Does buying more sample increase the power of your test? Apply the
    algorithm you have just written onto different sizes of data.
    Namely, conduct the exact same process that you have for 10 people,
    but now conduct the process for every 10% of recruitment size of the
    original data: Conduct a power analysis with a 10%, 20%, 30%, … 200%
    sample of the original data. (You could be more granular if you
    like, perhaps running this task for every 1% of the data).

``` r
percentages_to_sample <- 'fill this in'
```

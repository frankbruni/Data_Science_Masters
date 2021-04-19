Experiments and Causality: Problem Set 3
================
Alex, Micah and Scott
12/7/2020

``` r
library(data.table)

library(sandwich)
library(lmtest)

library(ggplot2)
library(patchwork)

library(foreign)
```

# 1\. Replicate Results

Skim [Broockman and Green’s](./readings/brookman_green_ps3.pdf) paper on
the effects of Facebook ads and download an anonymized version of the
data for Facebook users only.

``` r
d <- fread("../data/broockman_green_anon_pooled_fb_users_only.csv")
d
```

    ##       studyno treat_ad                     cluster name_recall
    ##    1:       2        0   Study 2, Cluster Number 1           0
    ##    2:       2        0   Study 2, Cluster Number 2           1
    ##    3:       2        0   Study 2, Cluster Number 3           0
    ##    4:       2        0   Study 2, Cluster Number 4           1
    ##    5:       2        1   Study 2, Cluster Number 7           1
    ##   ---                                                         
    ## 2702:       1        1 Study 1, Cluster Number 802           0
    ## 2703:       1        1 Study 1, Cluster Number 802           1
    ## 2704:       1        1 Study 1, Cluster Number 802           0
    ## 2705:       1        1 Study 1, Cluster Number 802           1
    ## 2706:       1        1 Study 1, Cluster Number 802           0
    ##       positive_impression
    ##    1:                   0
    ##    2:                   0
    ##    3:                   0
    ##    4:                   0
    ##    5:                   1
    ##   ---                    
    ## 2702:                   0
    ## 2703:                   0
    ## 2704:                   0
    ## 2705:                   1
    ## 2706:                   0

1.  Using regression without clustered standard errors (that is,
    ignoring the clustered assignment), compute a confidence interval
    for the effect of the ad on candidate name recognition in Study 1
    only (the dependent variable is `name_recall`). After you estimate
    your model, write a narrative description about what you’ve learned.

<!-- end list -->

  - **Note**: Ignore the blocking the article mentions throughout this
    problem.
  - **Note**: You will estimate something different than is reported in
    the study.

<!-- end list -->

``` r
study1 = d[d$studyno==1]
mod_study1 <- lm(name_recall~treat_ad,data=study1) # should be a lm class object
confint(mod_study1)
```

    ##                   2.5 %     97.5 %
    ## (Intercept)  0.15080247 0.21413492
    ## treat_ad    -0.05101765 0.03142188

> For people in study 1 the effect of being shown the ad is between -.05
> and 0.03 which means we cannot come to a conclusion that name\_recall
> is effected by the ad.

2.  What are the clusters in Broockman and Green’s study? Why might
    taking clustering into account increase the standard errors?

> The study clustered across 18 age ranges, 35 towns, and 2 genders.
> Taking clustering into account would increase the standard errors
> because there could exist a relationship between each of the clusters
> and the outcome of interest. Our randomization is not as perfect
> because of this. Clustering is not ideal but sometimes due to
> experimental setup is neccessary.

3.  Estimate a regression that estimates the effect of the ad on
    candidate name recognition in Study 1, but this time take take
    clustering into account when you compute the standard errors.

<!-- end list -->

  - The estimation of the *model* does not change, only the estimation
    of the standard errors.
  - You can estimate these clustered standard errors using
    `sandwich::vcovCL`, which means: "The `vcovCL` function from the
    `sandwich` package.
  - We talk about this more in code that is availbe in the course repo.

<!-- end list -->

``` r
coefci(x=mod_study1,level=0.95,vcov=sandwich::vcovCL(mod_study1,cluster= study1$cluster))
```

    ##                   2.5 %     97.5 %
    ## (Intercept)  0.14619376 0.21874363
    ## treat_ad    -0.05639555 0.03679977

4.  Change the context: estimate the treatment effect in Study 2, using
    clustered standard errors. If you’ve written your code for part 3
    carefully, you should be able to simply change the row-scoping that
    you’re calling. If you didn’t write it carefully, for legibility for
    your colleagues, you might consider re-writting your solution to the
    last question. Descriptively, do the treatment effects look
    different between the two studies? Are you able to conduct a formal
    test by comparing these coefficients? Why, or why not?

<!-- end list -->

``` r
study2 = d[d$studyno==2]
mod_study2 <- lm(name_recall~treat_ad,data=study2) # should be a lm class object
coefci(x=mod_study2,level=0.95,vcov=sandwich::vcovCL(mod_study2,cluster= study2$cluster))
```

    ##                   2.5 %     97.5 %
    ## (Intercept)  0.57010652 0.64147033
    ## treat_ad    -0.07245159 0.06684489

> 

5.  Run a regression to test for the effect of the ad on candidate name
    recognition, but this time use the entire sample from both studies –
    do not take into account which study the data is from (more on this
    in a moment), but just “pool” the data.

<!-- end list -->

  - Does this estimate tell you anything useful?
  - Why or why not?
  - Can you say that the treatment assignment procedure used is fully
    random when you estimate this model? Or is there some endogeneous
    process that could be confounding your estimate?

<!-- end list -->

``` r
mod_pooled <- lm(name_recall~treat_ad,data=d) # should be a lm class object
coefci(x=mod_pooled,level=0.95,vcov=sandwich::vcovCL(mod_pooled,cluster=d[,cluster]))
```

    ##                  2.5 %     97.5 %
    ## (Intercept)  0.4177710  0.4906211
    ## treat_ad    -0.2074875 -0.1026590

> Since the 95% confidence interval does not include 0 we know the
> treatment effect is below 0.

6.  Estimate a model that uses all the data, but this time include a
    variable that identifies whether an observation was generated during
    Study 1 or Study 2.

<!-- end list -->

  - What is estimated in the “Study 2 Fixed Effect”?
  - What is the treatment effect estimate and associated p-value?
  - Think a little bit more about the treatment effect that you’ve
    estimated: Can this treatment effect, as you’ve entered it in the
    model be *different* between Study 1 and Study 2?
  - Why or why not?

<!-- end list -->

``` r
mod_fe <- lm(name_recall~treat_ad+as.factor(studyno),data=d)

summary(mod_fe)
```

    ## 
    ## Call:
    ## lm(formula = name_recall ~ treat_ad + as.factor(studyno), data = d)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -0.6068 -0.1807 -0.1739  0.3932  0.8261 
    ## 
    ## Coefficients:
    ##                      Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)          0.180685   0.015994  11.297   <2e-16 ***
    ## treat_ad            -0.006775   0.018177  -0.373    0.709    
    ## as.factor(studyno)2  0.426099   0.017955  23.731   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.4381 on 2698 degrees of freedom
    ##   (5 observations deleted due to missingness)
    ## Multiple R-squared:  0.1931, Adjusted R-squared:  0.1925 
    ## F-statistic: 322.8 on 2 and 2698 DF,  p-value: < 2.2e-16

``` r
summary(mod_fe)$coefficients[2,4]
```

    ## [1] 0.7093688

> 

7.  Estimate a model that lets the treatment effects be different
    between Study 1 and Study 2. With this model, conduct a formal test
    – it must have a p-value associated with the test – for whether
    the treatment effects are different in Study 1 than Study 2.

<!-- end list -->

``` r
mod_interaction <- lm(name_recall~treat_ad:as.factor(studyno)+as.factor(studyno),data=d)
summary(mod_interaction)
```

    ## 
    ## Call:
    ## lm(formula = name_recall ~ treat_ad:as.factor(studyno) + as.factor(studyno), 
    ##     data = d)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -0.6058 -0.1825 -0.1727  0.3942  0.8273 
    ## 
    ## Coefficients:
    ##                               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                   0.182469   0.018534   9.845   <2e-16 ***
    ## as.factor(studyno)2           0.423320   0.023133  18.299   <2e-16 ***
    ## treat_ad:as.factor(studyno)1 -0.009798   0.024125  -0.406    0.685    
    ## treat_ad:as.factor(studyno)2 -0.002803   0.027655  -0.101    0.919    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.4382 on 2697 degrees of freedom
    ##   (5 observations deleted due to missingness)
    ## Multiple R-squared:  0.1931, Adjusted R-squared:  0.1922 
    ## F-statistic: 215.2 on 3 and 2697 DF,  p-value: < 2.2e-16

# 2\. Peruvian Recycling

Look at [this article](./readings/recycling_peru.pdf) about encouraging
recycling in Peru. The paper contains two experiments, a “participation
study” and a “participation intensity study.” In this problem, we will
focus on the latter study, whose results are contained in Table 4 in
this problem. You will need to read the relevant section of the paper
(starting on page 20 of the manuscript) in order to understand the
experimental design and variables. (*Note that “indicator variable” is a
synonym for “dummy variable,” in case you haven’t seen this language
before.*)

1.  In Column 3 of Table 4A, what is the estimated ATE of providing a
    recycling bin on the average weight of recyclables turned in per
    household per week, during the six-week treatment period? Provide a
    95% confidence interval.

> The estimated ATE of providing a recycling bin on the average weight
> of recyclables turned in per household per week is 0.187kg of
> recyclables. The 95% confidence interval is 0.187 +- 0.032.

2.  In Column 3 of Table 4A, what is the estimated ATE of sending a text
    message reminder on the average weight of recyclables turned in per
    household per week? Provide a 95% confidence interval.

> The estimated ATE of sending a text message reminder on the average
> weight of recyclables turned in per houseshold per week is -0.024kg.
> The 95% confidence interval is -0.024 +- 0.039.

3.  Which outcome measures in Table 4A show statistically significant
    effects (at the 5% level) of providing a recycling bin?

> Outcomes from column 1-4. This includes Percentage of visits turned in
> bag, Avg. no of bins turned in per week, Avg. Weight of recyclables
> turned in per week, and avg market value of recyclables per week.

4.  Which outcome measures in Table 4A show statistically significant
    effects (at the 5% level) of sending text messages?

> None of them are statistically significant.

5.  Suppose that, during the two weeks before treatment, household A
    turns in 2kg per week more recyclables than household B does, and
    suppose that both households are otherwise identical (including
    being in the same treatment group). From the model, how much more
    recycling do we predict household A to have than household B, per
    week, during the six weeks of treatment? Provide only a point
    estimate, as the confidence interval would be a bit complicated.
    This question is designed to test your understanding of slope
    coefficients in regression.

> I expect household A to have 0.562 kg of reclycing more per week than
> houssehold B.

6.  Suppose that the variable “percentage of visits turned in bag,
    baseline” had been left out of the regression reported in Column 1.
    What would you expect to happen to the results on providing a
    recycling bin? Would you expect an increase or decrease in the
    estimated ATE? Would you expect an increase or decrease in the
    standard error? Explain our reasoning.

> Leaving this out would increase our standard error but not change our
> ATE. ATE is not changed by covariates since it was randomized
> beforehand and only depends on the treatment. The covariates help
> reduce the standard error by giving us more imformation on the
> subjects and experiment.

7.  In column 1 of Table 4A, would you say the variable “has cell phone”
    is a bad control? Explain your reasoning.

> Bad controls are controls that impact the outcome. Has cell phone is a
> bad control if it was measured after the treatment since recycling
> more could have made people enough money to buy a cell phone. If it
> was measured before hand it is not a bad control.

8.  If we were to remove the “has cell phone” variable from the
    regression, what would you expect to happen to the coefficient on
    “Any SMS message”? Would it go up or down? Explain your reasoning.

> I think the standard error would go up since regression helps us
> reduce our errors.

# 3\. Multifactor Experiments

Staying with the same experiment, now think about multifactor
experiments.

1.  What is the full experimental design for this experiment? Tell us
    the dimensions, such as 2x2x3. (Hint: the full results appear in
    Panel 4B.)

> 3x2x2 because you get a bin with sticker, bin without sticker, or no
> bin (3) you have a phone or you dont have a phone(2) and you get a
> personal message or you get a generic message(2).

2.  In the results of Table 4B, describe the baseline category. That is,
    in English, how would you describe the attributes of the group of
    people for whom all dummy variables are equal to zero?

> The baselines tell you the value of that category before a person
> receives treatment.

3.  In column (1) of Table 4B, interpret the magnitude of the
    coefficient on “bin without sticker.” What does it mean?

> The ATE from bin without sticker is lower than the ATE for bin with
> sticker. It is highly significant with Avg. no of bins turned in per
> week, Avg. Weight of recyclables turned in per week, and avg market
> value of recyclables per week. It is significant with Percentage of
> visits turned in bag. It is not significant with avg percentage of
> contamination per week.

4.  In column (1) of Table 4B, which seems to have a stronger treatment
    effect, the recycling bin with message sticker, or the recycling bin
    without sticker? How large is the magnitude of the estimated
    difference?

> Bin with sticker is consistently higher ATE than bin without sticker.
> Roughly between 0.02 and 0.03.

5.  Is this difference you just described statistically significant?
    Explain which piece of information in the table allows you to answer
    this question.

> This is significant because the ATE are all significant and the
> standard error are almost exactly the same.

6.  Notice that Table 4C is described as results from “fully saturated”
    models. What does this mean? Looking at the list of variables in the
    table, explain in what sense the model is “saturated.”

> They did every combination of the experiment treatments. There are no
> other treatment effects you can explore so it is essentially
> saturated.

# 4\. Now\! Do it with data

Download the data set for the recycling study in the previous problem,
obtained from the authors. We’ll be focusing on the outcome variable
Y=“number of bins turned in per week” (avg\_bins\_treat).

``` r
d <- foreign::read.dta("../data/karlan_data_subset_for_class.dta")
d <- data.table(d)

d[,street_fixed:=ifelse(street<0,0,1)]
head(d)
```

    ##    street havecell avg_bins_treat base_avg_bins_treat bin sms bin_s bin_g
    ## 1:      7        1      1.0416666               0.750   1   1     1     0
    ## 2:      7        1      0.0000000               0.000   0   1     0     0
    ## 3:      7        1      0.7500000               0.500   0   0     0     0
    ## 4:      7        1      0.5416667               0.500   0   0     0     0
    ## 5:      6        1      0.9583333               0.375   1   0     0     1
    ## 6:      8        0      0.2083333               0.000   1   0     0     1
    ##    sms_p sms_g street_fixed
    ## 1:     0     1            1
    ## 2:     1     0            1
    ## 3:     0     0            1
    ## 4:     0     0            1
    ## 5:     0     0            1
    ## 6:     0     0            1

``` r
## Do some quick exploratory data analysis with this data. 
## There are some values in this data that seem a bit strange. 

## Determine what these are. 
## Don't make an assessment about keeping, changing, or 
## dropping just yet, but at any point that your analysis touches 
## these variables, you'll have to determine what is appropriate 
## given the analysis you are conducting. 
```

1.  For simplicity, let’s start by measuring the effect of providing a
    recycling bin, ignoring the SMS message treatment (and ignoring
    whether there was a sticker on the bin or not). Run a regression of
    Y on only the bin treatment dummy, so you estimate a simple
    difference in means. Provide a 95% confidence interval for the
    treatment effect, using **of course** robust standard errors (use
    these throughout).

<!-- end list -->

``` r
mod_1 <- lm(avg_bins_treat~bin,data=d)
coefci(x=mod_1,level=0.95,vcov=vcovHC(mod_1,type='HC1'))
```

    ##                  2.5 %    97.5 %
    ## (Intercept) 0.61284690 0.6578525
    ## bin         0.09457479 0.1761852

> 95% interval of \[0.09457479 0.1761852\]

2.  Now add the pre-treatment value of Y as a covariate. Provide a 95%
    confidence interval for the treatment effect. Explain how and why
    this confidence interval differs from the previous one.

<!-- end list -->

``` r
mod_2 <- lm(avg_bins_treat~bin+base_avg_bins_treat,data=d)
coefci(x=mod_2,level=0.95,vcov=vcovHC(mod_2,type='HC1'))
```

    ##                          2.5 %    97.5 %
    ## (Intercept)         0.30921501 0.3899901
    ## bin                 0.09107834 0.1583076
    ## base_avg_bins_treat 0.33541695 0.4505124

> tighter confidence interval becasue we are addcing a covariate which
> reduces our standard erros

3.  Now add the street fixed effects. (You’ll need to use the R command
    factor().) Provide a 95% confidence interval for the treatment
    effect.

<!-- end list -->

``` r
mod_3 <-  lm(avg_bins_treat~bin+base_avg_bins_treat+factor(street_fixed),data=d)
coefci(x=mod_3,level=0.95,vcov=vcovHC(mod_3,type='HC1'))
```

    ##                             2.5 %     97.5 %
    ## (Intercept)            0.28464598 0.42182000
    ## bin                    0.09067771 0.15788046
    ## base_avg_bins_treat    0.33210552 0.44789518
    ## factor(street_fixed)1 -0.06167068 0.05911998

> 95% interval of \[0.09067771 0.15788046\]

4.  Recall that the authors described their experiment as “stratified at
    the street level,” which is a synonym for blocking by street. Does
    including these block fixed effects change the standard errors of
    the estimates *very much*? Conduct the appropriate test for the
    inclusion of these block fixed effects, and interpret them in the
    context of the other variables in the regression.

<!-- end list -->

``` r
mod_4 <- lm(avg_bins_treat~bin+base_avg_bins_treat + as.factor(street_fixed),data=d)
coefci(x=mod_4,level=0.95,vcov=vcovHC(mod_4,type='HC1'))
```

    ##                                2.5 %     97.5 %
    ## (Intercept)               0.28464598 0.42182000
    ## bin                       0.09067771 0.15788046
    ## base_avg_bins_treat       0.33210552 0.44789518
    ## as.factor(street_fixed)1 -0.06167068 0.05911998

``` r
test_fixed_effects <- anova(mod_4)
test_fixed_effects 
```

    ## Analysis of Variance Table
    ## 
    ## Response: avg_bins_treat
    ##                           Df  Sum Sq Mean Sq  F value    Pr(>F)    
    ## bin                        1   7.079   7.079  63.9640 2.262e-15 ***
    ## base_avg_bins_treat        1  93.250  93.250 842.5634 < 2.2e-16 ***
    ## as.factor(street_fixed)    1   0.000   0.000   0.0016    0.9677    
    ## Residuals               1778 196.780   0.111                       
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

> 

5.  Perhaps having a cell phone helps explain the level of recycling
    behavior. Instead of “has cell phone,” we find it easier to
    interpret the coefficient if we define the variable " no cell
    phone." Give the R command to define this new variable, which equals
    one minus the “has cell phone” variable in the authors’ data set.
    Use “no cell phone” instead of “has cell phone” in subsequent
    regressions with this dataset.

<!-- end list -->

``` r
d[,no_cell_phone:=(1-havecell)]
d
```

    ##       street havecell avg_bins_treat base_avg_bins_treat bin sms bin_s
    ##    1:      7        1      1.0416666               0.750   1   1     1
    ##    2:      7        1      0.0000000               0.000   0   1     0
    ##    3:      7        1      0.7500000               0.500   0   0     0
    ##    4:      7        1      0.5416667               0.500   0   0     0
    ##    5:      6        1      0.9583333               0.375   1   0     0
    ##   ---                                                                 
    ## 1781:    258        0      0.8333333               1.000   1   0     1
    ## 1782:    258        0      0.6666667               0.375   0   0     0
    ## 1783:     NA        1      2.2916667               3.000   1   1     1
    ## 1784:     NA        0      0.0000000               0.000   0   0     0
    ## 1785:     NA        1      0.1666667               0.500   1   1     1
    ##       bin_g sms_p sms_g street_fixed no_cell_phone
    ##    1:     0     0     1            1             0
    ##    2:     0     1     0            1             0
    ##    3:     0     0     0            1             0
    ##    4:     0     0     0            1             0
    ##    5:     1     0     0            1             0
    ##   ---                                             
    ## 1781:     0     0     0            1             1
    ## 1782:     0     0     0            1             1
    ## 1783:     0     0     1           NA             0
    ## 1784:     0     0     0           NA             1
    ## 1785:     0     1     0           NA             0

6.  Now add “no cell phone” as a covariate to the previous regression.
    Provide a 95% confidence interval for the treatment effect. Explain
    why this confidence interval does not differ much from the previous
    one.

<!-- end list -->

``` r
mod_5 <- lm(avg_bins_treat~bin+base_avg_bins_treat + as.factor(street_fixed)+no_cell_phone,data=d)
coefci(x=mod_5,level=0.95,vcov=vcovHC(mod_5,type='HC1'))
```

    ##                                2.5 %      97.5 %
    ## (Intercept)               0.30316999  0.44275902
    ## bin                       0.09161935  0.15875685
    ## base_avg_bins_treat       0.33139737  0.44766217
    ## as.factor(street_fixed)1 -0.06063557  0.05887580
    ## no_cell_phone            -0.07966270 -0.01836043

> 95% interval of \[0.09161935 0.15875685\]

7.  Now let’s add in the SMS treatment. Re-run the previous regression
    with “any SMS” included. You should get the same results as in Table
    4A. Provide a 95% confidence interval for the treatment effect of
    the recycling bin. Explain why this confidence interval does not
    differ much from the previous one.

<!-- end list -->

``` r
mod_6 <- lm(avg_bins_treat~bin+base_avg_bins_treat + as.factor(street_fixed)+no_cell_phone+sms,data=d)
coefci(x=mod_6,level=0.95,vcov=vcovHC(mod_6,type='HC1'))
```

    ##                                2.5 %      97.5 %
    ## (Intercept)               0.31660520  0.46414036
    ## bin                       0.09166341  0.15878008
    ## base_avg_bins_treat       0.33024053  0.44629090
    ## as.factor(street_fixed)1 -0.06077600  0.05822011
    ## no_cell_phone            -0.10387475 -0.02640522
    ## sms                      -0.07256684  0.01081840

8.  Now reproduce the results of column 2 in Table 4B, estimating
    separate treatment effects for the two types of SMS treatments and
    the two types of recycling-bin treatments. Provide a 95% confidence
    interval for the effect of the unadorned recycling bin. Explain how
    your answer differs from that in part (g), and explain why you think
    it differs.

<!-- end list -->

``` r
mod_7 <- lm(avg_bins_treat~base_avg_bins_treat + as.factor(street_fixed)+no_cell_phone+bin_s+bin_g+sms_p+sms_g,data=d)
coefci(x=mod_7,level=0.95,vcov=vcovHC(mod_7,type='HC1'))
```

    ##                                2.5 %       97.5 %
    ## (Intercept)               0.31684029  0.464248211
    ## base_avg_bins_treat       0.33082097  0.446922152
    ## as.factor(street_fixed)1 -0.06191456  0.056823301
    ## no_cell_phone            -0.10341261 -0.025685848
    ## bin_s                     0.09845485  0.182566927
    ## bin_g                     0.06548347  0.155817410
    ## sms_p                    -0.09292461  0.006957683
    ## sms_g                    -0.06737938  0.033386148

> 95% interval of \[0.06548347 0.155817410\] The control before was not
> receiving a bin while now it is receiving a bin without a sticker.
> This question shows us the treatment effect of receving a bin with
> sticker.

# 5\. A Final Practice Problem

Now for a fictional scenario. An emergency two-week randomized
controlled trial of the experimental drug ZMapp is conducted to treat
Ebola. (The control represents the usual standard of care for patients
identified with Ebola, while the treatment is the usual standard of care
plus the drug.)

Here are the (fake) data.

``` r
d <- fread("../data/Ebola_rct2.csv")
head(d)
```

    ##    temperature_day0 dehydrated_day0 treat_zmapp temperature_day14
    ## 1:         99.53168               1           0          98.62634
    ## 2:         97.37372               0           0          98.03251
    ## 3:         97.00747               0           1          97.93340
    ## 4:         99.74761               1           0          98.40457
    ## 5:         99.57559               1           1          99.31678
    ## 6:         98.28889               1           1          99.82623
    ##    dehydrated_day14 male
    ## 1:                1    0
    ## 2:                1    0
    ## 3:                0    1
    ## 4:                1    0
    ## 5:                1    0
    ## 6:                1    1

You are asked to analyze it. Patients’ temperature and whether they are
dehydrated is recorded on day 0 of the experiment, then ZMapp is
administered to patients in the treatment group on day 1. Dehydration
and temperature is again recorded on day 14.

1.  Without using any covariates, answer this question with regression:
    What is the estimated effect of ZMapp (with standard error in
    parentheses) on whether someone was dehydrated on day 14? What is
    the p-value associated with this estimate?

<!-- end list -->

``` r
mod_1 <- lm(dehydrated_day14~treat_zmapp,data=d)
summary(mod_1)
```

    ## 
    ## Call:
    ## lm(formula = dehydrated_day14 ~ treat_zmapp, data = d)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.84746 -0.03803  0.15254  0.21197  0.39024 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  0.84746    0.05483  15.456   <2e-16 ***
    ## treat_zmapp -0.23770    0.08563  -2.776   0.0066 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.4212 on 98 degrees of freedom
    ## Multiple R-squared:  0.0729, Adjusted R-squared:  0.06343 
    ## F-statistic: 7.705 on 1 and 98 DF,  p-value: 0.006595

> This is significant and has a p value of 0.0066. The ATE of zmapp is
> -0.2377 (0.086).

2.  Add covariates for dehydration on day 0 and patient temperature on
    day 0 to the regression from part (a) and report the ATE (with
    standard error). Also report the p-value.

<!-- end list -->

``` r
mod_2 <- lm(dehydrated_day14~treat_zmapp+dehydrated_day0+temperature_day0,data=d)
summary(mod_2)
```

    ## 
    ## Call:
    ## lm(formula = dehydrated_day14 ~ treat_zmapp + dehydrated_day0 + 
    ##     temperature_day0, data = d)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.79643 -0.18106  0.04654  0.23122  0.68413 
    ## 
    ## Coefficients:
    ##                   Estimate Std. Error t value Pr(>|t|)   
    ## (Intercept)      -19.46966    7.44095  -2.617  0.01032 * 
    ## treat_zmapp       -0.16554    0.07567  -2.188  0.03113 * 
    ## dehydrated_day0    0.06456    0.14635   0.441  0.66013   
    ## temperature_day0   0.20555    0.07634   2.693  0.00837 **
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3668 on 96 degrees of freedom
    ## Multiple R-squared:  0.311,  Adjusted R-squared:  0.2895 
    ## F-statistic: 14.45 on 3 and 96 DF,  p-value: 7.684e-08

> The ate of receiving zmapp is -0.16554 with std error of 0.076 and a p
> value of 0.03113.

3.  Do you prefer the estimate of the ATE reported in part (a) or part
    (b)? Why? Report the results of the F-test that you used to form
    this opinion.

<!-- end list -->

``` r
test_object <- var.test(mod_1,mod_2)
test_object
```

    ## 
    ##  F test to compare two variances
    ## 
    ## data:  mod_1 and mod_2
    ## F = 1.3182, num df = 98, denom df = 96, p-value = 0.1759
    ## alternative hypothesis: true ratio of variances is not equal to 1
    ## 95 percent confidence interval:
    ##  0.8829135 1.9664492
    ## sample estimates:
    ## ratio of variances 
    ##           1.318202

> I prefer part b since we have more covariates and it gives us more
> information and smaller standard error on our ATE.

4.  The regression from part (2) suggests that temperature is highly
    predictive of dehydration. Add, temperature on day 14 as a covariate
    and report the ATE, the standard error, and the p-value.

<!-- end list -->

``` r
mod_3 <- lm(dehydrated_day14~treat_zmapp+dehydrated_day0+temperature_day0+temperature_day14,data=d)
summary(mod_3)
```

    ## 
    ## Call:
    ## lm(formula = dehydrated_day14 ~ treat_zmapp + dehydrated_day0 + 
    ##     temperature_day0 + temperature_day14, data = d)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.87745 -0.27436  0.04701  0.24801  0.66445 
    ## 
    ## Coefficients:
    ##                    Estimate Std. Error t value Pr(>|t|)   
    ## (Intercept)       -22.59159    7.47727  -3.021  0.00323 **
    ## treat_zmapp        -0.12010    0.07768  -1.546  0.12541   
    ## dehydrated_day0     0.04604    0.14426   0.319  0.75033   
    ## temperature_day0    0.17664    0.07642   2.312  0.02296 * 
    ## temperature_day14   0.06015    0.02937   2.048  0.04335 * 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3609 on 95 degrees of freedom
    ## Multiple R-squared:  0.3402, Adjusted R-squared:  0.3124 
    ## F-statistic: 12.24 on 4 and 95 DF,  p-value: 4.545e-08

> Ate of -0.12 with a standard error of 0.078 and p value of 0.125.

5.  Do you prefer the estimate of the ATE reported in part (b) or part
    (d)? What is this preference based on?

> I prefer b since in part d treap\_zmapp is no longer significant and
> we see that the temperatures are more significant when it comes to
> deheydration.

6.  Now let’s switch from the outcome of dehydration to the outcome of
    temperature, and use the same regression covariates as in the chunk
    titled `add pre-treatment measures`. Test the hypothesis that ZMapp
    is especially likely to reduce mens’ temperatures, as compared to
    womens’, and describe how you did so. What do the results suggest?

<!-- end list -->

``` r
mod_4 <- lm(temperature_day14~treat_zmapp+dehydrated_day0+temperature_day0+dehydrated_day14+male,data=d)
summary(mod_4)
```

    ## 
    ## Call:
    ## lm(formula = temperature_day14 ~ treat_zmapp + dehydrated_day0 + 
    ##     temperature_day0 + dehydrated_day14 + male, data = d)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -1.24404 -0.46153 -0.05401  0.45935  1.22131 
    ## 
    ## Coefficients:
    ##                  Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)       51.1967    12.8633   3.980 0.000136 ***
    ## treat_zmapp       -0.8894     0.1300  -6.839 7.96e-10 ***
    ## dehydrated_day0   -0.1938     0.2456  -0.789 0.432043    
    ## temperature_day0   0.4774     0.1322   3.611 0.000491 ***
    ## dehydrated_day14   0.7887     0.1702   4.635 1.15e-05 ***
    ## male               2.1972     0.1284  17.111  < 2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.6114 on 94 degrees of freedom
    ## Multiple R-squared:  0.8277, Adjusted R-squared:  0.8185 
    ## F-statistic:  90.3 on 5 and 94 DF,  p-value: < 2.2e-16

> Adding in male makes everything significant. We see a difference of 2
> degrees in temperature difference in male and females so this confirms
> our hypothesis.

7.  Which group – those that are coded as `male == 0` or `male == 1`
    have better health outcomes in control? What about in treatment? How
    does this help to contextualize whatever heterogeneous treatment
    effect you might have estimated?

<!-- end list -->

``` r
d[, .(Mean_Tem=mean(temperature_day14)), by=list(male,treat_zmapp)]
```

    ##    male treat_zmapp  Mean_Tem
    ## 1:    0           0  98.48654
    ## 2:    1           1  99.10071
    ## 3:    0           1  98.16308
    ## 4:    1           0 101.69167

``` r
#d
d[,.(Mean_Deh=mean(dehydrated_day14)), by=list(male,treat_zmapp)]
```

    ##    male treat_zmapp  Mean_Deh
    ## 1:    0           0 0.8250000
    ## 2:    1           1 0.5555556
    ## 3:    0           1 0.6521739
    ## 4:    1           0 0.8947368

``` r
#d
```

> Female has much better health outcomes in control. In treatment the
> males show a big improvement but end up around where the females are.
> There is definitely a difference between males and females which leads
> to a heterogeneous treatment effect. Next time blocking on gender
> would help the experiement.

8.  Suppose that you had not run the regression in part (7). Instead,
    you speak with a colleague to learn about heterogeneous treatment
    effects. This colleague has access to a non-anonymized version of
    the same dataset and reports that they looked at heterogeneous
    effects of the ZMapp treatment by each of 80 different covariates to
    examine whether each predicted the effectiveness of ZMapp on each of
    20 different indicators of health. Across these regressions your
    colleague ran, the treatment’s interaction with gender on the
    outcome of temperature is the only heterogeneous treatment effect
    that he found to be statistically significant. They reason that this
    shows the importance of gender for understanding the effectiveness
    of the drug, because nothing else seemed to indicate why it worked.
    Bolstering your colleague’s confidence, after looking at the data,
    they also returned to his medical textbooks and built a theory about
    why ZMapp interacts with processes only present in men to cure.
    Another doctor, unfamiliar with the data, hears your colleague’s
    theory and finds it plausible. How likely do you think it is ZMapp
    works especially well for curing Ebola in men, and why? (This
    question is conceptual can be answered without performing any
    computation.)

> It is unlikely that zmapp works better for men than women. If we
> continue to look at men versus women and test it again and again we
> are bound to find some statistical significance. If we are testing
> repeatedly over many indicators it could very well be a false
> positive.

9.  Now, imagine that your colleague’s fishing expedition did not
    happen, but that you had tested this heterogeneous treatment effect,
    and only this heterogeneous treatment effect, of your own accord.
    Would you be more or less inclined to believe that the heterogeneous
    treatment effect really exists? Why?

> I would be more inclinded to believe the heterogeneous treatment
> effect because I found it on my own and looks significant.

10. Now, imagine that your colleague’s fishing expedition **did**
    happen, but that you on your own tested this and only this HTE,
    discover a positive result and conclude there is an effect. How does
    your colleague’s behavior change the interpretation of your test?
    Does this seem fair or reasonable?

> I would be more inclinded to be skeptical of my results because of the
> fishing expedition. This seems fair that I will make sure my results
> are real and check with other replications of the experiement.

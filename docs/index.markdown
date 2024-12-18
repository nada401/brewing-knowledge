---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

title: Brewing Knowledge
subtitle: Expertise Growth in Beer Reviewers
layout: post
ext-js: "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"
cover-img: "background.jpg"
date: 2024-12-05
kramdown:
  toc_levels: 1..6
---

* TOC
{:toc}
# Introduction
[BeerAdvocate](https://www.beeradvocate.com/) and [RateBeer](https://www.ratebeer.com/) are vibrant online communities where beer enthusiasts gather to share their thoughts on a vast selection of beers. Over the years, these platforms have attracted tens of thousands of users, reflecting both the accessibility of these websites and the popularity of beer appreciation. Yet, beer critique can be far more than a casual pastime - it is a craft that may be pursued with remarkable depth and precision. This becomes evident when you consider the [Beer Judge Certification Program](https://www.bjcp.org/) (BJCP): achieving their recognition demands rigorous study and practical experience. Aspiring judges must master topics ranging from water alkalinity and malt types to hop varieties, yeast characteristics, and the nuances of fermentation by-products, as outlined in the [BJCP's comprehensive study guide](https://legacy.bjcp.org/docs/BJCP_Study_Guide.pdf).

But what about the wider community of more casual reviewers on BeerAdvocate and BeerReview? Can we, in a similar spirit but with less granularity, evaluate the expertise demonstrated in their reviews? This question opens the door to intriguing possibilities: Do users hone their beer critique skills as they write more reviews? Do linguistic factors, such as native language, influence their reviewing style?

In this data story, we invite you to join us as we explore these questions, using data to uncover insights about beer critique and the diverse community of reviewers behind it.

# Datasets
We have used two datasets, one for BeerAdvocate and one for RateBeer. Both datasets were generously provided by EPFL's Data Science Lab, which makes them available upon request. Originally, these datasets were used in the lab's 2018 paper, [their 2018 paper](https://dlab.epfl.ch/people/west/pub/Lederrey-West_WWW-18.pdf) *When Sheep Shop: Measuring Herding Effects in Product Ratings with Natural Experiments*.

Each dataset contains a comprehensive crawling of all beer types, user information, and reviews posted to the respective platforms until 2017. For our study, we have made key additions:
- **Language Tagging:** Each review was tagged with the language in which it was written. English-language reviews account for 99% of BeerAdvocate reviews and 93% of RateBeer reviews. This allows us to focus exclusively on English reviews without sacrificing data scale, retaining over 9 million reviews for analysis.
- **Stemming**: We applied a stemming algorithm to the reviews, enabling us to focus on the specific terms used.

# The Metric
Developing a methodology to judge a beer critique unavoidably requires some level of domain knowledge from the developers' side. Here is what we learned, distilled to a pint. 

Beers are judged on 4 fundamental factors: *Appearance*, *Aroma*, *Flavor*, and *Mouthfeel*. Both RateBeer and BeerAdvocate allow users to assign individual ratings for each of these factors as well as the overall score. However, our goal requires exploring how each of these categories are addressed in the textual portion of the review. The terminology for beer critique is largely standardized, and the 1979 paper *"Beer Flavour Terminology"* by Dr. Meilgaard et al. gives an in-depth presentation of it as well as this handy chart:  

![Flavour Wheel](wheel.jpg)

Our goal is to assess how thoroughly the review discusses each category in their written reviews. To achieve this, we employ a simple yet surprisingly effective approach that we apply to each review:
1. For every term in the above Flavor Wheel that appeared in the review, we add a point to the review's coverage score of that term's category’s.
2. We sum every coverage score to obtain the final expertise score for the review.

Here is a small demo of our metric: we illustrate our metric through two example reviews, one that achieved a low score and one that achieved a high score.
**FILL THIS OUT**

## Word Cloud
Here is a pretty word cloud of the metric terms most commonly used in both websites
word_occurrencies

# Results
Now that we’ve outlined how we evaluate the expertise level demonstrated in a review, let's see if we can get some interesting insights with our metric.

## Categorical Coverage by Beer Style
[Beer styles](https://www.bjcp.org/style/2021/beer/) categorize beers based on shared attributes such as ingredients, brewing techniques, and flavor profiles. The interactive radar chart below visualizes the average contribution of each term category to the final expertise score across several popular beer styles. The values are normalized as fractions of the maximum average weight achieved by each category.
<div class="l-page">
  <iframe src="{{ '/plots/radar_importance.html' | relative_url }}" frameborder='0' scrolling='no' height="600px" width="110%" style="border: 1px dashed grey;"></iframe>
</div>
Reviews of beers in the *Black & Tan* style show the highest reliance on Appearance terms, which reflects the visually striking looks of these beers. The most striking anomaly however emerges with the *Gueuze* beer style, whose reviews are dominated by terms in the off-flavor category (which corresponds to the undesirable flavors in Meilgaard's wheel). Gueuze is indeed a peculiar beer style. Its fermentation process involves wild yeasts and bacteria, which produce complex flavors that [can include what are traditionally considered "off-flavors"](https://www.thetakeout.com/1711564/why-belgian-geueze-beer-taste-funky/) in other beer styles, such as funk and sourness. These flavors are not defects in the context of Gueuze but are instead key elements of its profile.

| ![Black & Tan](pics/blacktan.jpg) | ![alt text](pics/gueuze.png) | 
| *Black & Tan* | *Gueuze* |

## Expertise Over Time
show improvement over time for all users (even already expert), once for BA and once for RB
not that good... what if we consider people who started out bad? it improves!
in ba_analysis_exp_metric users that don't begin as experts correlation time - expertise score, with median because it's good (0.04 pvalue for the correlation when taking the first 50, then there is a plateu)
the distributions are different, can we explain that? need to check if these people are a lot more international

then division of expert nonexpert english nonenglish
average scores (normalized) by location over time posted by vikhyat on whatsapp

## Expertise Per Country
English-Speaking countries performing better (not over time)
10/12/2024 13:42
use the normalized graph (score given by the category is divided by the number of words belonging to that category)

expertise per country over time too but need to choose which ones we show

## Beer Styles (not doing it - maybe)
Most Frequent Words and Expertness Score, both by country, for:
- BA American IPA, Imperial Stout, 
- RB IPA, Imperial Stout, Pale Lager

## More about our metric - Scores Correlation Matrix
10/12/2024 14:22 correlation that includes expertness score - review rating
Expert score is relatively highly correlated with flavor score and appearance score (interpretation: they're the most important features...?)
it's a very big square, we can have a menu that selects 1 of the three squares (upper left, lower left, lower right)


## A plot
<div class="l-page">
  <iframe src="{{ '/plots/test_plot.html' | relative_url }}" frameborder='0' scrolling='no' height="400px" width="100%" style="border: 1px dashed grey;"></iframe>
</div>

# Conclusions


##  The Team
This Data Story is brought to you by the Nada-401 team as part of a project for the 2024 Applied Data Analysis course at EPFL. The team members are, in alphabetical order:
- ![vikhyatavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/82029380?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Vikhyat Agrawal
- ![manuelavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/160757986?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Manuel Curnis
- ![alessandroeavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/181464875?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Alessandro Di Maria
- ![nicolaavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/76104087?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Nicola Stocco
- ![danieleavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/43929743?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Daniele Pusceddu
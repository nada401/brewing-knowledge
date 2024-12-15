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
[BeerAdvocate](https://www.beeradvocate.com/) and [RateBeer](https://www.ratebeer.com/) are vibrant online communities where beer enthusiasts gather to share their thoughts on a vast selection of beers. Over the years, these platforms have attracted hundreds of thousands of users, reflecting both the accessibility of these websites and the popularity of beer appreciation. Yet, beer critique can be far more than a casual pastime - it is a craft that may be pursued with remarkable depth and precision. This becomes evident when you consider the [Beer Judge Certification Program](https://www.bjcp.org/) (BJCP): achieving their recognition demands rigorous study and practical experience. Aspiring judges must master topics ranging from water alkalinity and malt types to hop varieties, yeast characteristics, and the nuances of fermentation by-products, as outlined in the [BJCP's comprehensive study guide](https://legacy.bjcp.org/docs/BJCP_Study_Guide.pdf).

But what about the wider community of more casual reviewers on BeerAdvocate and BeerReview? Can we, in a similar spirit but with less granularity, evaluate the expertise demonstrated in their reviews? This question opens the door to intriguing possibilities: Do users hone their beer critique skills as they write more reviews? Do linguistic factors, such as native language, influence their reviewing style?

In this data story, we invite you to join us as we explore these questions, using data to uncover insights about beer critique and the diverse community of reviewers behind it.

# Datasets
## Pre-Processing
Mostly language tagging, then trivial things such as dropping duplicates and removing beers with no reviews.
Stemming
7% 1%
We considered english language reviews only, which makes up around 94% of the entire dataset.

# The Metric
## Review Texts Compared

## Word Cloud
Here is a pretty word cloud of the metric terms most commonly used in both websites
word_occurrencies

# Results
## Beer Styles
Most Frequent Words and Expertness Score, both by country, for:
- BA American IPA, Imperial Stout, 
- RB IPA, Imperial Stout, Pale Lager

## Expertise Per Country
English-Speaking countries performing better
10/12/2024 13:42
use the normalized graph (score given by the category is divided by the number of words belonging to that category)

## Expertise Over Time
average scores (normalized) by location over time posted by vikhyat on whatsapp
in ba_analysis_exp_metric users that don't begin as experts correlation time - expertise score, with median because it's good (0.04 pvalue for the correlation when taking the first 50, then there is a plateu), then division of expert nonexpert english nonenglish

## Scores Correlation Matrix
10/12/2024 14:22 correlation that includes expertness score - review rating
Expert score is relatively highly correlated with flavor score and appearance score (interpretation: they're the most important features...?)
it's a very big square, we can have a menu that selects 1 of the three squares (upper left, lower left, lower right)


## A plot
<div class="l-page">
  <iframe src="{{ '/plots/test_plot.html' | relative_url }}" frameborder='0' scrolling='no' height="400px" width="100%" style="border: 1px dashed grey;"></iframe>
</div>

# Conclusions


##  The Team
This Data Story is brought to you by the Nada-401 team as project for the 2024 Machine Learning Course at EPFL. The group's members are, in alphabetic order:
- ![vikhyatavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/82029380?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Vikhyat Agrawal
- ![manuelavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/160757986?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Manuel Curnis
- ![alessandroeavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/181464875?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Alessandro Di Maria
- ![nicolaavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/76104087?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Nicola Stocco
- ![danieleavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/43929743?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Daniele Pusceddu
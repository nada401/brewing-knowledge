# Brewing Knowledge: Expertise Growth in Beer Reviewers
[This data analysis project comes with a data story.](https://epfl-ada.github.io/ada-2024-project-nada401/)

## Repository Structure
- `/data`: The datasets we work on as well as some reusable json results of our analysis. The main datasets may be obtained from EPFL's Applied Data Analysis upon request.
- `/docs`: The Jekyll page for our data story.
- `/src`: Helper functions. More specifically:
  - `/src/data_cleaning`: basic pre-processing (such as dropping duplicates)
  - `/src/lang_tagger`: language detection (used to then filter-out non-english reviews)
  - `/src/expert_metric`: definition of our metric (including the required stemming utilities)
  - `/src/expert_analysis`: various utilities for the overall analysis (e.g. filtering by expertise in the reviews that were first posted by user)
  - `/src/country_analysis`: per-country analysis (such as obtaining the most commonly used words by each country)
  - `/src/word_occurrences`: word frequency inspection for the word cloud generation
  - `/src/embedding`: generator for the embeddings for our failed approach
  - `/src/helpers.py`: misc helper functions (including more general-purpose stemming)
  - `/src/load_file.py`: utilities for loading the datasets
- `/results.ipynb`: The Jupyter notebook with our main results.

## Team Contribution
- **Everyone**: General trajectory of the project and general design of the metric.
- **Nicola Stocco**: Embeddings, interactivity in the plots, analysis of beer celebration events.
- **Daniele Pusceddu**: Background literature, lexical diversity measures, writing, data story website.
- **Alessandro di Maria**: Core of the codebase, analysis of the usage of expert terms.
- **Vikhyat Agrawal**: Country-wise analysis, basic explorations, gathering the expert terms.
- **Manuel Curnis**: Data cleaning, analysis of the usage of expert terms.

We are satisfied with how the workload was split.

## Abstract
User reviews often include a textual component as well as numeric ratings for each of the most important features of the product. While it is straightforward to process the numeric ratings, it comes at the cost of neglecting the expertise of the reviewer and the information accounted for by them while selecting each rating. In this project we will explore methodologies to quantify the richness and technical depth of natural language reviews and apply them to the BeerAdvocate and RateBeers datasets. The intuition of the resulting metrics will be evaluated through a qualitative analysis. Thereafter, we will explore relations between the resulting ratings with other parameters: for example, how a singular user’s technical depth tends to change as they write more reviews, or the site-wide technical depth of the reviews by seasonality or country of the writer.

## Research Questions
- Can we define an effective and explainable metric to quantify the technical depth of natural language beer reviews? Then, utilizing such a metric;
- Do singular users improve the depth of their reviews as they gain more experience with writing beer reviews? Our hypothesis is that new users will initially be improving their reviews but they will quickly start experiencing diminishing returns and reach a plateau.
- Does review depth change with seasons? For example, do the websites experience a surge of lower-depth reviews for Oktoberfest?
- Are there some countries that tend to write more in-depth reviews? If not, do they tend to use different terms while keeping the same level of depth?
- What’s the degree of separation in review richness when comparing a sample of selected, accredited beer experts versus the average user of the site?

# Brewing Knowledge: Expertise Growth in Beer Reviewers

## Abstract <!-- ~150 words -->
User reviews often include a textual component as well as numeric ratings for each of the most important features of the product. While it is straightforward to process the numeric ratings, it comes at the cost of neglecting the expertise of the reviewer and the information accounted for by them while selecting each rating. In this project we will explore methodologies to quantify the richness and technical depth of natural language reviews and apply them to the BeerAdvocate and RateBeers datasets. The intuition of the resulting metrics will be evaluated through a qualitative analysis. Thereafter, we will explore relations between the resulting ratings with other parameters: for example, how a singular user’s technical depth tends to change as they write more reviews, or the site-wide technical depth of the reviews by seasonality or country of the writer.

## Research Questions
- Can we define an effective and explainable metric to quantify the technical depth of natural language beer reviews? Then, utilizing such a metric;
- Do singular users improve the depth of their reviews as they gain more experience with writing beer reviews? Our hypothesis is that new users will initially be improving their reviews but they will quickly start experiencing diminishing returns and reach a plateau.
- Does review depth change with seasons? For example, do the websites experience a surge of lower-depth reviews for Oktoberfest?
- Are there some countries that tend to write more in-depth reviews? If not, do they tend to use different terms while keeping the same level of depth?
- What’s the degree of separation in review richness when comparing a sample of selected, accredited beer experts versus the average user of the site?

## Additional Datasets (if any) <!-- We shouldn't have them -->

We don’t plan to add any additional datasets. We plan however to use some accreditable beer reviews as a ground truth to test our metric.

## Methods

### Data cleaning
- Format the attributes of dataframes
- Clean ratings dataframe
  - Checking for duplicated reviews made by same user on same day for the same beer 
  - Drops rows that have nan values in all metrics and text simultaneously
  - Update column “review”  indicating whether a review is actually present
  - Add tag column that indicates the language of the review (NaN if no review)
  - N.B for ratebeer we consider user_name to match users between the rating dataset and the user dataset, for beeradvocate itìs fine using user_id
- Clean user dataframe
  - Check for user with same user-id (should be unique), and delete duplicate users (only present in rateBeer)
  -  Add column “date_first_review” indicating the date on which they made the first review 
  - Update column nbr_ratings doing a merge with ratings dataframe (using user_name as key)
- Clean beer dataframes
  - Since the original dataframes where confusing and with a lot of NaN values, recompute the avg and std of all the metrics for all the beers,
  - Update column nbr_ratings and nbr_reviews, computed with a merge on the ratings database cleaned 


### Review analysis

We need to find a good metric to evaluate the reviews of the users. Among the already tested methods are:
- Lexical Richness (unsatisfactory): Too much weight given to words unrelated to the domain (beers). 
- Ad-hoc metric (satisfactory, to be improved): Simple, but effective
  -  The goal is to develop a domain-specific metric. In this initial implementation, we define several key categories: flavor, aroma, mouthfeel, brewing, technical aspects, appearance, judgment, off-flavors, and miscellaneous. Each category contains specific terms relevant to beer evaluation. For every occurrence of these terms in a review, we increment the respective category score. The overall "expertness" score is calculated as the sum of these category scores. To account for the fact that different beers may have varying average scores due to distinct flavor profiles, each score is normalized using the mean and standard deviation of scores for the specific beer being reviewed. This approach aims to establish a consistent and meaningful metric that reflects the depth and expertise conveyed in beer reviews.

- Word Embeddings (unsatisfactory so far): Initial analysis didn't give satisfactory results, but we plan to try this method again (with better models) to get more insights over the reviews.

## Timeline and Internal Milestones

**Week 1:** Expand data by extracting the English RateBeer reviews, further fortifying the metric. Explore possible improvements to our ad-hoc metric including: different weights for different categories and having specific word list for specific beer styles instead of a generic one.

**Week 2:** Find a way of handling reviews in different languages. One idea is to test how the expert-metric score for reviews translated to English varies as compared to our current expert-metric score for native English reviews. Alternatively, we need to tailor our metric for such a task, i.e, being adaptive to multi-lingual datasets.

**Week 3:** Start answering the said research questions and extract insights based on our final improved metric. This would mainly include analyzing the evolution of reviews/metric-score with time and identifying interesting clusters in our dataset based on the metric score. 

**Week 4:** Start writing the data story. Conduct further analysis on the data as required by the data story (if any).

**Week 5:** Finalize the data story and prepare for final submission.



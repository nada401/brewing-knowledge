# Title

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
This involved cleaning the dataset by: (*explain what we did so far*)
- language tagging
- NaN values removal

### Review analysis
**EXPAND:**
We need to find a good metric to evaluate the reviews of the users. Among the already tested methods are:
- language depth (unsatisfactory): too much focus on non-topic specific language
- ad-hoc metric (satisfactory, to be improved): simple but effective
- embedding (unsatisfactory....so far): initial analysis didn't gave satisfactory results

### Translation (do we want to mention it?)

## Timeline

Week1: Expand data with English RateBeer reviews, further improve the metric, (translation?)

Week2: 

Week3: Further analysis using the metric.

Week4: Plan and start building the data story

Week5: finalize the data story
 
## Internal Milestone

## Questions for TAs



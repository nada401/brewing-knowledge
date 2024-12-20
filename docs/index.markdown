---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

title: Brewing Knowledge
subtitle: Expertise Growth in Beer Reviewers
layout: post
ext-js: "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"
cover-img: "/pics/post.jpg"
date: 2024-12-05
kramdown:
  toc_levels: 1..6
---

* TOC
{:toc}
<div class="l-page">
  <iframe src="{{ '/plots/graphic-stroke-animation.html' | relative_url }}" frameborder='0' scrolling='no' height="100px" width="110%" style="border: 0px dashed grey;"></iframe>
</div>

<link rel="stylesheet" href="{{ '/assets/css/custom.css' | relative_url }}">

# Introduction
[BeerAdvocate](https://www.beeradvocate.com/) and [RateBeer](https://www.ratebeer.com/) are vibrant online communities where beer enthusiasts gather to share their thoughts on a vast selection of beers. Over the years, these platforms have attracted tens of thousands of users, reflecting both the accessibility of these websites and the popularity of beer appreciation. Yet, beer critique can be far more than a casual pastime - it is a craft that may be pursued with remarkable depth and precision. This becomes evident when you consider the [Beer Judge Certification Program](https://www.bjcp.org/) (BJCP): achieving their recognition demands rigorous study and practical experience. Aspiring judges must master topics ranging from water alkalinity and malt types to hop varieties, yeast characteristics, and the nuances of fermentation by-products, as described in the BCJP's beer exam study guide\[[3](#ref-studyguide)\].

But what about the wider community of more casual reviewers on BeerAdvocate and BeerReview? Can we, in a similar spirit but with less granularity, evaluate the expertise demonstrated in their reviews? This question opens the door to intriguing possibilities: Do users hone their beer critique skills as they write more reviews? Do linguistic factors, such as native language, influence their reviewing style?

In this data story, we invite you to join us as we explore these questions, using data to uncover insights about beer critique and the diverse community of reviewers behind it.

# Datasets
We have used two datasets, one for BeerAdvocate and one for RateBeer. Both datasets were generously provided by EPFL's Data Science Lab, who makes them available upon request\[[2](#ref-sheep)\].

Each dataset contains a comprehensive crawling of all beer types, user information, and reviews posted to the respective platforms until 2017. For our study, we have made key additions:
- **Language Tagging:** Each review was tagged with the language in which it was written. English-language reviews account for 99% of BeerAdvocate reviews and 93% of RateBeer reviews. This allows us to focus exclusively on English reviews without sacrificing data scale, retaining over 9 million reviews for analysis.
- **Stemming**: We applied a stemming algorithm to the reviews, enabling us to focus on the specific terms used.

# The Metric
Developing a methodology to judge a beer critique unavoidably requires some level of domain knowledge from the developers' side. Here is what we learned, distilled to a pint. 

Beers are judged on 4 fundamental factors: *Appearance*, *Aroma*, *Flavor*, and *Mouthfeel*. Both RateBeer and BeerAdvocate allow users to assign individual ratings for each of these factors as well as the overall score. However, our goal requires exploring how each of these categories are addressed in the textual portion of the review. The terminology for beer critique is largely standardized, and the 1979 paper *"Beer Flavour Terminology"* by Dr. Meilgaard et al.\[[1](#ref-wheel)\] gives an in-depth presentation of it as well as this handy chart:  

![Flavour Wheel](pics/wheel.jpg)

Our goal is to assess how thoroughly the review discusses each category in their written reviews. To achieve this, we employ a simple yet surprisingly effective approach that we apply to each review:
1. For every term in the above Flavor Wheel that appeared in the review, we add a point to the review's coverage score of that term's category’s.
2. We sum every coverage score to obtain the final expertise score for the review.

Here is a small demo of our metric: we illustrate our metric through pairs of example reviews. Each pair corresponds to a type of beer and includes a review that achieves a low expertise score and one that achieves a high expertise score. You may use the buttons to highlight words belonging to each category obtained from the flavor wheel.
<div class="l-page">
  <iframe src="{{ '/plots/text_highlight.html' | relative_url }}" frameborder='0' scrolling='yes' height="720px" width="100%" style="border: 1px dashed grey;"></iframe>
</div>

## Word Cloud
This word cloud reveals key descriptive terms from a beer reviews dataset, highlighting common attributes and sensory details that beer reviewers focus on:

1) Flavor Attributes: Words like "bitterness," "malt," "citrus," "caramel," and "chocolate" indicate flavor profiles commonly discussed in reviews.
2) Sensory Experience: Terms like "light," "body," "carbonated," and "drying" reflect the beer's mouthfeel.
3) Aroma and Notes: Words such as "fruity," "hoppy," "dark," and "spicy" capture aromatic characteristics.
4) Finish and Aftertaste: "Finish," "lacing," and "drying" point to the importance of a beer's aftertaste.

It shows a rich vocabulary used to articulate beer experiences, offering insight into consumer preferences and sensory dimensions.

![Word Cloud](pics/word_cloud_BA_RB.png)

# Results
Now that we’ve outlined how we evaluate the expertise level demonstrated in a review, let's see if we can get some interesting insights with our metric.

## Categorical Coverage by Beer Style
[Beer styles](https://www.bjcp.org/style/2021/beer/) categorize beers based on shared attributes such as ingredients, brewing techniques, and flavor profiles. The interactive radar chart below visualizes the average contribution of each term category to the final expertise score across several popular beer styles. The values are normalized as fractions of the maximum average weight achieved by each category.
<div class="l-page">
  <iframe src="{{ '/plots/radar_importance.html' | relative_url }}" frameborder='0' scrolling='no' height="600px" width="100%" style="border: 0px dashed grey;display: flex;"></iframe>
</div>

Reviews of beers in the *Black & Tan* style show the highest reliance on Appearance terms, which reflects the visually striking looks of these beers. The most striking anomaly however emerges with the *Gueuze* beer style, whose reviews are dominated by terms in the off-flavor category (which corresponds to the undesirable flavors in Meilgaard's wheel). Gueuze is indeed a peculiar beer style. Its fermentation process involves wild yeasts and bacteria, which produce complex flavors that [can include what are traditionally considered "off-flavors"](https://www.thetakeout.com/1711564/why-belgian-geueze-beer-taste-funky/) in other beer styles, such as funk and sourness. These flavors are not defects in the context of Gueuze but are instead key elements of its profile.
<table>
  <tr>
    <td style="width: 50%; text-align: center; font-size: 12px;">
      <img src="pics/blacktan.jpg" alt="Black & Tan" style="max-width: 100%; height: auto;"><br>
      <strong>Black & Tan</strong>: A black and tan is prepared by filling a glass halfway with pale ale, then adding stout to fill the glass completely. An upside-down tablespoon may be placed over the glass to avoid splashing and mixing the layers. A specially designed black-and-tan spoon is bent in the middle so that it can balance on the edge of the pint-glass for easier pouring. The "layering" of Guinness on top of the pale ale or lager is possible because of the lower relative density of the Guinness.
    </td>
    <td style="width: 50%; text-align: center; font-size: 12px;">
      <img src="pics/gueuze.png" alt="Gueuze" style="max-width: 100%; height: auto;">
      <strong>Gueuze</strong>: Due to its lambic blend, gueuze has a different flavor than traditional ales and lagers. Because of their use of aged hops, lambics lack the characteristic hop aroma or flavor found in most other beers. Furthermore, the wild yeasts that are specific to lambic-style beers give gueuze a dry, cider-like, musty, sour, acetic acid, lactic acid taste. Many describe the taste as sour and "barnyard-like". 
    </td>
  </tr>
</table>



## Expertise Over Time
It would be reasonable to hypothesize that the reviewers in both websites would improve at critiquing beers as they gain more experience. Under this assumption, if our metric is any good, we should be able to see for the average user a positive upwards trend in the overall expertise score achieved by the reviews they publish over time. Let's put this to the test by doing just that.

**IMPROVEMENT OVER TIME PLOT FOR ALL OF THE USERS**

These results are not as clear as expected would've hoped. While working further on the topic, we realized that many of the users might have been very proficient before joining the website already. Such users would be experiencing diminishing returns over the reviews they post. So, what if we try grouping users based on their starting expertise? We could do this by quartiles on the average overall expertise score achieved in, say, the first 5 reviews they post on the website. Here is what we get when running this analysis on users with at least a thousand reviews in the BeerAdvocate and RateBeer datasets respectively:

![Users Improvement Over Time](pics/exp_nonexp_evol.png)

Indeed, in both websites we see that the bottom 20% achieves a very sharp improvement in their expertise scores, slowly reaching a plateau between the 300 and 400 review mark. For these users in the bottom 20% of beginners, the Pearson correlation between posting time and overall expertise is in median 0.32 and 0.25, with median p-values of 0.02 and 0.06, for BeerAdvocate and RateBeer respectively.

| Platform      | Median Pearson Correlation | Median p-value |
|---------------|----------------------------|----------------|
| BeerAdvocate  | 0.32                       | 0.02           |
| RateBeer      | 0.25                       | 0.06           |


We also see impressive improvements for the middle 20-80% group of beginners, while the top 20% of beginners has the least amount of improvement and the earliest plateau. 
Although the trends on improvements closely match each other, we can see that users on RateBeer perform worse than those on BeerAdvocate. A possible explanation that we would like to explore is that RateBeer has a more international community (**put actual numbers**), which might translate into a poorer vocabulary on average. This brings us to performing an analysis of the metric per country.

<div class="image-switcher" style="text-align: center;">
  <select id="imageSelector3" onchange="switchImage('imageSelector3', 'displayedImage3')">
    <option value="{{ '/pics/BA_exp_nonexp_eng_nongl_evol.png' | relative_url }}">BeerAdvocate</option>
    <option value="{{ '/pics/RB_exp_nonexp_eng_nongl_evol.png' | relative_url }}">RateBeer</option>
  </select>

  <div style="margin-top: 20px;">
    <img id="displayedImage3" src="{{ '/pics/BA_exp_nonexp_eng_nongl_evol.png' | relative_url }}" alt="Selected Image" style="max-width: 100%; height: auto;">
  </div>
</div>


## Expertise Per Country

One of the hypothesis we have is that we expect the average expertness score of English speaking countries to be higher than non-English speaking countries. To test this out, we compute the average score grouped by the location of the users. This includes all the reviews made by users from a particular country. We also filter out countries which have less than 2000 reviews, to have some confidence in our computed average. Since the location for the United States is state-wise for BeerAdvocate, we combine all users into a single "United States" location. We observe that our hypothesis holds to some extent, with the general trend being that the English Speaking countries outscore the non-English speaking countries. This largely corresponds with the EF English Proficiency Index of 2013\[[4](#ref-english)\], where we see that the non-English countries on top of the list indeed have a high average expertness score. We note however the presence of one significant outlier, and that is Belgium, which obtains a low expertness score despite having good English proficiency as a country. For other countries like Sweden, Netherlands, France, Germany, Italy and Spain, we see that there is a relation between their english proficiency and their expertness score. 


<div class="l-page">
  <select class="iframeSelector" onchange="switchIframe(event, '.plotIframe1')">
    <option value="{{ '/plots/mean_countries_BA.html' | relative_url }}">BeerAdvocate dataset</option>
    <option value="{{ '/plots/mean_countries_RB.html' | relative_url }}">RateBeer dataset</option>
  </select>
  <iframe class="plotIframe1" src="{{ '/plots/mean_countries_BA.html' | relative_url }}" frameborder='0' scrolling='no' height="620px" width="100%" style="visibility: visible; position: relative;"></iframe>
  <iframe class="plotIframe1" src="{{ '/plots/mean_countries_RB.html' | relative_url }}" frameborder='0' scrolling='no' height="620px" width="100%" style="visibility: hidden; position: absolute;"></iframe>
</div>

We further investigate the country-wise distribution of expertness scores by looking at the time evolution of the yearly average for some countries. To make sure we have enough samples for each year, we set a filter of 5000 reviews per country and plot the evolution over time. We notice that the United States maintains a higher score from the beginning, while we observe evolution in all the other countries. There is quite a sharp evolution initially between 2000-2005, and then the scores plateau. This evolution graph is similar to the Expert/Non-Expert analysis we did, but here we have plotted the evolution with time, as compared to the evolution with the number of reviews earlier. 

<div class="l-page" width="100%">
  <select class="iframeSelector" onchange="switchIframe(event, '.plotIframe2')">
    <option value="{{ '/plots/evolution_countries_BA.html' | relative_url }}">BeerAdvocate dataset</option>
    <option value="{{ '/plots/evolution_countries_RB.html' | relative_url }}">RateBeer dataset</option>
  </select>

  <!-- <iframe src="{{ '/plots/evolution_countries.html' | relative_url }}" frameborder='0' scrolling='no' height="800px" width="100%"></iframe> -->
  <iframe class="plotIframe2" src="{{ '/plots/evolution_countries_BA.html' | relative_url }}" frameborder='0' scrolling='no' height="800px" width="100%" style="visibility: visible; position: relative;"></iframe>
  <iframe class="plotIframe2" src="{{ '/plots/evolution_countries_RB.html' | relative_url }}" frameborder='0' scrolling='no' height="800px" width="100%" style="visibility: hidden; position: absolute;"></iframe>
</div>

## Beer Styles

<div class="image-switcher" style="text-align: center;">
  <select id="imageSelector1" onchange="switchImage('imageSelector1', 'displayedImage1')">
    <option value="{{ '/pics/expertness_score_stylewise.png' | relative_url }}">Expertise score</option>
    <option value="{{ '/pics/flavour_score_stylewise.png' | relative_url }}">Flavor</option>
    <option value="{{ '/pics/mouthfeel_score_stylewise.png' | relative_url }}">Mouthfeel</option>
    <option value="{{ '/pics/brewing_score_stylewise.png' | relative_url }}">Brewing</option>
    <option value="{{ '/pics/technical_score_stylewise.png' | relative_url }}">Technical</option>
    <option value="{{ '/pics/appearance_score_stylewise.png' | relative_url }}">Appearance</option>
    <option value="{{ '/pics/off_flavours_score_stylewise.png' | relative_url }}">Off flavor</option>
  </select>

  <div style="margin-top: 20px;">
    <img id="displayedImage1" src="{{ '/pics/expertness_score_stylewise.png' | relative_url }}" alt="Selected Image" style="max-width: 100%; height: auto;">
  </div>
</div>

## More about our metric - Scores Correlation Matrix
How do our expertise scores correlate with the reviewer's rating of the review? Could it be that reviewers show more expertise for beers that they have enjoyed? Let's use a correlation matrix to find out.

- The upper left quadrant (shaded red) shows us the correlations between the different numeric ratings given by the reviewer (this is independent from our metric). It is interesting to see how the taste rating is so heavily correlated to the overall rating of the beer, in comparison to the other numerical ratings.
- Our expertise scores are not strongly correlated to the numerical ratings left by the user, which gives a blue shade to our lower left quadrant. This is good, although we do note in general a slightly positive correlation. A possible explanation for this is that reviewers tend to write more in-depth for beers that they have enjoyed.
- The expertise score for off-flavor is unique in having a negative correlation with all of the numeric ratings, which matches with the generally negative connotation carried by terms in that category.
- The overall expertise score is most heavily influenced by the expertise score for flavor, which means that reviewers tend to write more in-depth about that aspect of the beer. This adds evidence to flavor being the aspect to which reviewers tend to give the most weight.

<div class="image-switcher" style="text-align: center;">
  <select id="imageSelector2" onchange="switchImage('imageSelector2', 'displayedImage2')">
    <option value="{{ '/pics/corr_matrix_all_BA.png' | relative_url }}">BeerAdvocate</option>
    <option value="{{ '/pics/corr_matrix_all_RB.png' | relative_url }}">RateBeer</option>
  </select>

  <div style="margin-top: 20px;">
    <img id="displayedImage2" src="{{ '/pics/corr_matrix_all_BA.png' | relative_url }}" alt="Selected Image" style="max-width: 100%; height: auto;">
  </div>
</div>

<!-- ![Correlation matrix for all scores for BA](pics/corr_matrix_all_BA.png)
![Correlation matrix for all scores for BA](pics/corr_matrix_all_RB.png) -->

## Impact of popular beer events on reviews quality
Throughout the year there are many events around the world dedicated at least in part to celebrating beer. These events may lead to a noticeable increase in the number of beer reviews posted around the time period. Notable examples are **St. Patrick’s Day** (Ireland), **Oktoberfest** (Germany) and **4th of July** (USA).

**PUT A PLOT HERE SHOWCASING THE CHANGE IN QUANTITY OF REVIEWS**

It would be interesting to analyze how these events and the resulting influx of reviews affect the expertise scores of the involved beers and locations. Given the unique nature of each event, we conducted an ad-hoc analysis for each:
- For Oktoberfest we analyzed reviews for beers brewed by the six breweries that participate annually in the event. Specifically, we compared the average expertise score of reviews posted during the Oktoberfest period (across all years) with the overall average expertise score of Guinness beer reviews.
- For St. Patrick's Day we focused on reviews of Guinness beers, comparing the average expertise score of reviews posted on March 17th (across all years) with the overall average expertise score of Guinness beer reviews.
- For the 4th of July we examined all reviews from U.S.-based reviewers, comparing the average expertise score of reviews posted on Independence Day with the annual average expertise score of U.S. reviewers.

<div class="l-page">
  <iframe src="{{ '/plots/big_events.html' | relative_url }}" frameborder='0' scrolling='no' height="620px" width="100%"></iframe>
</div>


# Our Recommendations

So, which expert should you follow to get the best reviews? To answer this, we have curated a list with the top experts on BeerAdvocate you can check out to get to know about the beers you want to try out. 

| Username          | Location                  | Number of reviews | Expert Score |
|-------------------|---------------------------|-------------------|--------------|
| [StephenRich](https://www.beeradvocate.com/user/beers/?ba=StephenRich)       | Canada                   | 176               | 17.23        |
| [TheBrewo](https://www.beeradvocate.com/user/beers/?ba=TheBrewo)          | United States, New York  | 1236              | 15.17        |
| [911CROFT](https://www.beeradvocate.com/user/beers/?ba=911CROFT)          | England                  | 144               | 13.60        |
| [superspak](https://www.beeradvocate.com/user/beers/?ba=superspak)         | United States, Michigan  | 5603              | 13.19        |
| [CHickman](https://www.beeradvocate.com/user/beers/?ba=CHickman)          | United States, New York  | 1795              | 12.55        |
| [flayedandskinned](https://www.beeradvocate.com/user/beers/?ba=flayedandskinned)  | United States, California| 135               | 12.35        |
| [Jadjunk](https://www.beeradvocate.com/user/beers/?ba=Jadjunk)           | United States, Georgia   | 1175              | 12.20        |
| [Bmoyer0301](https://www.beeradvocate.com/user/beers/?ba=Bmoyer0301)        | United States, Pennsylvania| 114            | 12.10        |
| [fmccormi](https://www.beeradvocate.com/user/beers/?ba=fmccormi)          | United States, California| 532               | 12.07        |
| [BarryMFBurton](https://www.beeradvocate.com/user/beers/?ba=BarryMFBurton)     | United States, Indiana   | 628               | 11.89        |
| [hustlesworth](https://www.beeradvocate.com/user/beers/?ba=hustlesworth)      | United States, Ohio      | 689               | 11.85        |
| [mdagnew](https://www.beeradvocate.com/user/beers/?ba=mdagnew)           | Northern Ireland         | 1143              | 11.52        |


Here are the experts from RateBeer:

| Username                         | Location                  | Number of Ratings | Expert Score |
|----------------------------------|---------------------------|-------------------|--------------|
| [GoufCustom](https://www.ratebeer.com/user/233863/)       | Hong Kong                | 1832              | 13.34        |
| [superspak](https://www.ratebeer.com/user/105791/)        | United States, Michigan  | 4847              | 13.14        |
| [msnelling09](https://www.ratebeer.com/user/241026/)     | United States, Massachusetts | 148        | 12.72        |
| [pinkie](https://www.ratebeer.com/user/237851/)         | United States, New York  | 386               | 11.23        |
| [FlacoAlto](https://www.ratebeer.com/user/8187/)        | United States, Arizona   | 3538              | 11.21        |
| [ksurkin](https://www.ratebeer.com/user/66818/)         | United States, Virginia  | 722               | 10.51        |
| [Bierdimpfe](https://www.ratebeer.com/user/371540/)     | Canada                   | 639               | 9.94         |
| [Night_Cap](https://www.ratebeer.com/user/397374/)      | Australia                | 109               | 9.83         |
| [Alengrin](https://www.ratebeer.com/user/325955/)       | Belgium                  | 5507              | 9.44         |
| [beermatrix](https://www.ratebeer.com/user/7911/)       | United States, Minnesota | 1233              | 9.07         |
| [otakuden](https://www.ratebeer.com/user/78541/)        | United States, Florida   | 1446              | 8.98         |
| [Jabic](https://www.ratebeer.com/user/64352/)           | United States, Vermont   | 452               | 8.97         |
| [brewandbbq](https://www.ratebeer.com/user/34515/)      | United States, New Hampshire | 233          | 8.89         |
| [jpm30](https://www.ratebeer.com/user/28003/)           | United States, Georgia   | 1451              | 8.81         |

One of the most interesting things to notice in the top experts for the 2 datasets is that on average, the raw scores for BeerAdvocate are higher than RateBeer. Thus, you are more likely to find better worded reviews on BeerAdvocate than on RateBeer. It is also interesting to see the user "superspak" turn up on the top experts for both the datasets. They also have roughly the same expert score for both the datasets. So, if you want good quality beer reviews, we would recommend checking out some of these experts' reviews on the 2 websites.

##  The Team
This Data Story is brought to you by the Nada-401 team as part of a project for the 2024 Applied Data Analysis course at EPFL. The team members are, in alphabetical order:
- ![vikhyatavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/82029380?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Vikhyat Agrawal
- ![manuelavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/160757986?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Manuel Curnis
- ![alessandroeavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/181464875?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Alessandro Di Maria
- ![nicolaavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/76104087?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Nicola Stocco
- ![danieleavatar](https://images.weserv.nl/?url=avatars.githubusercontent.com/u/43929743?v=4&h=100&w=100&fit=cover&mask=circle&maxage=7d) Daniele Pusceddu

## References
1. Meilgaard, M.C., Dalgliesh, C.E. and Clapperton, J.F., 1979. Beer flavor terminology. *Journal of the American Society of Brewing Chemists*, 37(1), pp.47-52. <a name="ref-wheel"></a>
2. Lederrey, G. and West, R., 2018, April. When sheep shop: Measuring herding effects in product ratings with natural experiments. In *Proceedings of the 2018 world wide web conference* (pp. 793-802). <a name="ref-sheep"></a>
3. Edward Wolfe, Scott Bickham, David Houseman, Ginger Wotring, Dave Sapsis, Peter Garofalo, Chuck Hanning, Steve Piatz, Gordon Strong, 2017.*BCJP Beer Exam Study Guide*.<a name="ref-studyguide"></a>
4. EF English Proficiency Index, 2013. [https://www.ef.com/assetscdn/WIBIwq6RdJvcD9bc8RMd/cefcom-epi-site/reports/2013/ef-epi-2013-english.pdf](https://www.ef.com/assetscdn/WIBIwq6RdJvcD9bc8RMd/cefcom-epi-site/reports/2013/ef-epi-2013-english.pdf) <a name="ref-english"></a>
4. Beer Judge Certification Programme. [BJCP](https://www.bjcp.org/). <a name="ref-bjcp"></a>
5. Beer Analytics. [Beer Analytics](https://www.beer-analytics.com/). <a name="ref-beeranalytics"></a>

<script>
  function switchIframe(event, iframe_name) {
    var selector = event.target;
    var plotIframes = document.querySelectorAll(iframe_name);
    console.log("We are changing this = ", iframe_name);
    plotIframes.forEach(function(iframe) {
      // iframe.style.display = 'none'; // Hide all iframes
      iframe.style.visibility = 'hidden';
      iframe.style.position = 'absolute';
      if (iframe.src.includes(selector.value)) {
        console.log("We are displaying now = ", iframe.src, "\nSelector.value = ", selector.value);
        // iframe.style.display = 'flex'; // Show the selected iframe
        iframe.style.visibility = 'visible';
        iframe.style.position = 'relative';
      }
    });
  }

  function switchImage(img_selector_id, displayed_img_id) {
    const selector = document.getElementById(img_selector_id);
    const selectedValue = selector.value;
    const image = document.getElementById(displayed_img_id);
    image.src = selectedValue;
  } 
</script>

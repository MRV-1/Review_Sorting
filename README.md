# Review_Sorting
It includes strategies for sorting reviews of products on marketplaces.🙇‍♀️

# SORTING REVIEWS

# Up-Down Diff Score = (up ratings) − (down ratings)

* The method used in this section is the Up-Down Diff Score method. The difference between up rates and down rates is taken and a ranking is made.<br/>

## After Examine

* While review 1's score is 200, review 2's score is 1000, but when analyzed on a percentage basis, it is seen that review 1 is higher.<br/>

* It is therefore not sensible to use this method.<br/>

* # Score = Average rating = (up ratings) / (all ratings)

* This method was more successful than the other method.<br/>

* When sorted, review 1 will be at the top.<br/>
* This is not the way it should normally win, this method failed to take into account the high frequency.<br/>

* So why are we evaluating what won't happen first?<br/>

* Looking at the literature, the wilson_lower_bound method also preferred this point of view.<br/>

* When the examples and some local sites are examined, it will be seen that there are no approaches that cannot be right or even these approaches.<br/>

* Therefore, knowing what is wrong will help us to develop the right method along with its necessity.<br/>

* Such a method should be found so that it makes an evaluation by holding both frequency and ratio information.<br/>

  # Wilson Lower Bound Score

--> Method description : allows you to score an item, product or review that contains any binary interactions.<br/>

* Likes on Youtube are like/dislike, comments on question and answer forms are helpful/not helpfull.<br/>

* It helps in all measurement problems that arise as a result of binary interactions.<br/>

* Bernoulli is a probability distribution and is used to calculate the probability of binary events.<br/>
* For example, it is used to calculate the probability of a coin toss coming up tails, or the probability of how an event with two outcomes can occur.<br/>

* This method is used when we do not have all the data, when we have a sample, and when we want to make a generalization from it, so that this value is reflected in the whole population. <br/>

* The method reaches the result by determining a confidence interval.<br/>

# Case Study

This data set is from an e-commerce company and includes the number of times the user's comment was found useful or not.

**For more information about review sorting : https://medium.com/@merveatasoy48/review-sorting-7c8c6bd77195

**Click here for a sample article in the literature on this topic --> https://www.evanmiller.org/how-not-to-sort-by-average-rating.html

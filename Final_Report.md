### Capstone 2 - AirBnB Fair Fare Estimator

It can be difficult in a big city such as New York to figure out whether you are getting a fair price for an AirBnB, or on the opposite side, to determine what price to set your room or apartment at for renting. The goal of this project is to use machine learning to suggest fair prices for rooms and apartments on AirBnB in New York City, with the goal of helping hosts and renters on AirBnB. 

I found a dataset pulled by Tom Slee that contains the basic AirBnB listing data for apartments in NYC in July 2017. The dataset contained ~41000 rows and was fairly clean already. Unfortunately some key info like number of bathrooms was not pulled successfully, making the column useless. I also cut out columns that were AirBnB specific, like `room_id`, `host_id`, and `location`.  

One of my first tasks with the data was to make sure the prices did not change dramatically throughout the year. I did a bootstrap test between the July 2017 data and the Feb 2017 data to see if there was a practical and/or statistical difference between the prices for the two months. Visualizing the data, there was a slight difference but the statistical significance was low (p value of ~.11) and the actual difference in mean price was only $2.00, so practically there’s very little difference in price. With that insight I did not think it is necessary to add more data beyond the July 2017 dataset. 

![july-feb price compare](https://raw.githubusercontent.com/claireramming/Capstone-2/master/imgs/bootstrap_year.png)

Once that was settled, I did some basic data exploration to see any obvious correlations. I found that to get any meaningful insights I had to cut out all listings that were priced at over $500.

![borough prices](https://raw.githubusercontent.com/claireramming/Capstone-2/master/imgs/borough_prices.png)

The category `room_type` contained wether the listing was for a room in a house, apartment, condo, etc.. This seems to be a free-text field, while most locations fell under apartment/house/condo there are some options like 'casa particular' and 'castle'. There was also already another option of 'other.' I changed all listings that did not have around or over 100 entries into 'other' to cut down on the number of categories.

Another feature that needed modification was the `overall_satisfaction` column. Most listings were rated between 4 and 5, and there were also ~8000 listings that have 0 ratings, so are currently rated at 0 (there are ~7000 listings that are actually rated at 0). For my linear regression model I tested two options: 
1. Changing the non-rated listings to the mean of the overall satisfaction
2. Removing all low-rated or non-rated listings

I ultimately went with the second option as there ended up being less variance in the model due to better standardization of the feature (standardized over values ranging from 3-5 rather than 0-5). Practically, low rated listings would be less likely to be rented and listings that do not have ratings have not been found to be good or bad quality yet so are not great to include in a model that is looking for fair prices for quality listings. 

For linear regression I also removed a lot of very expensive outliers and one listing that is listed as having 50 rooms. This left me with ~24000 listings remaining.

I broke my data out into a 30% testing and 70% training set, fit the training data to a standard scalar, and fit the training data to a linear regression model. The output on the testing data led to a lot of very overpriced (>$1 million) predictions, so I took a look at the coefficients and found that some of the coefficients were set to very high values (both positive and negative). Regularization was needed to smooth out the coefficients. 

I decided to switch to an ElasticNet model. This would potentially cut out some less important features, and smooth the coefficient variance so the model could generalize better. Scaling and fitting the data to this model led to coefficients between 16.5 and -19.6, which are much more reasonable. What I hoped to see if I plotted the predictions vs the actual prices was a mostly linear 1:1 plot that would somewhat flatten out as the prices got higher (most likely some of the higher priced listings are over-priced so my model should predict lower prices than the actual listing). This is essentially what I saw for the ElasticNet model, it also did not predict any negative room prices, or predict any listings to be over $350. 

![elasticnet](https://raw.githubusercontent.com/claireramming/Capstone-2/master/imgs/Elasticnet_out.png)

I also used R<sup>2</sup> as a metric for how well my model was doing. My ElasticNet model was a .57 (in comparison, my original linear regression model had an  R<sup>2</sup> value of -3.8x10<sup>18</sup>). 

To see if I could get similar results with a model that wouldn't require me to drop any of the original data, I tried a random forest regression model. This ultimately led to higher predicted prices and an R<sup>2</sup> of .22

![randomforest](https://raw.githubusercontent.com/claireramming/Capstone-2/master/imgs/randomforest_out.png)

If I remove the same data that I removed for ElasticNet, I increase my R<sup>2</sup> to .58 but the predictions still tend to skew higher than the actual prices although in the upper price ranges (>$300) it skewed lower and only predicted a few listings to be over $400. 

![random forest 2](https://raw.githubusercontent.com/claireramming/Capstone-2/master/imgs/randomforest_lessdata.png)

Once I had my final model (my ElasticNet model), I turned the process of scaling and transforming the features into a pipeline, and saved off the pipeline fitted to my training data to a file (a pickle file using the dill package). I then built a function to return a suggested price given details of a listing. From the perspective of a renter, or someone just putting up a listing, they should have all the feature info available except for `overall_satisfaction` and `ratings`. To make sure this was taken into account, my function randomly creates an overall satisfaction between 3 and 5, and a number of ratings between 1 and the max number of ratings in the dataset, which is 454. This is done 10 times, the random features are put in an array that contains the remaining given features, and the array is scaled and run through the model. The predictions are then averaged, and the average prediction is what is given to the user. 

I created a simple prototype web app with flask and wtform that takes in all of the required inputs and returns a message with the suggested price (via my prediction function and model). All code and required files to locally host it are on my github. 

![webapp](https://raw.githubusercontent.com/claireramming/Capstone-2/master/imgs/weppapp_example.png)
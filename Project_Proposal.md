####Project Proposal

There are a lot of AirBnB listings in NYC, it can be overwhelming for a person trying to book a room, or a new renter trying to rent a space, to figure out what a fair price is for a listing. With this project I would like to create a tool that uses machine learning to find fair price ranges for AirBnB listings in New York City. 

The client for this project is AirBnB. They can use this tool to help customers find a good deal, or decide on a fair price to list their apartment/room for. With a few tweaks if could probably also be used to find anomalous listings that are very overpriced or underpriced and warn the poster or potential renters. 

I will be using the NYC AirBnB data collected by Tom Slee (which can be found here: http://tomslee.net/airbnb-data-collection-get-the-data) for this project. It contains listing information from 2014-2017 including specific neighborhood info that will come in handy since prices will most likely vary by borough and neighborhood. I will do some preliminary checks to see if prices change dramatically depending on time of year, if it does not I will only be using the 2017-07-12 data, if it does I will combine that data with data from different parts of the year and include time of year in the model.

To solve this problem, I plan on using linear regression or another supervised machine learning algorithm with an emphasis on generalization of the data so it can be used to predict prices of listings. A user will be able to fill in room details and the tool will return a “fair” price range for the listing based on the model. 

All code will be publicly listed on github in a jupyter notebook. The project will be presented at [claireramming.github.io](http://claireramming.github.io) when complete.
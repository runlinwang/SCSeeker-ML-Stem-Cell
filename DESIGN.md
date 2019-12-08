# Our Design

Below we've walked through the design decisions that we made in each step of the process, from how we got the data to what we chose to show on the website.

## Choosing the Data

We chose our 6 genes that we were going to analyze with the help of a number of papers and resources, including https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4633996/?fbclid=IwAR3Ty_EZV2xyc5WzOb030Kv8eHxHN1pk3920ugbRZRhwPjP9XERqKYCtGjg and https://journals.plos.org/plosone/article/file?type=supplementary&id=info:doi/10.1371/journal.pone.0053372.s003. These genes chosen represented a diverse distribution of cellular functions ranging from cell self-renewal to differentiation. We kept the number of genes tested at 6 in order to keep the amount of data required managable and to reduce the additional processing power required for the neural network to run, but it is certainly possible to expand our model for many more genes.

## Processing the Data

As mentioned previously, we used StemCellDB to obtain genetic data, as it is an authoritative open-source platform run by the National Institutes of Health. We downloaded the gene expression data for the 6 genes that we decided to use, and compiled all the sheets into the Excel file `MasterSheet.xlsx`. We then isolated the median gene expression value columns rather than the general quantile value columns, since we believe that the median is more straightforward and still has a good representation of the data. These median values for each gene and cell type were compiled into `MasterSheetFormatted.xlsx`, where we also added a column indicating whether a cell type was a stem cell or a non-stem cell, with 0 representing not a stem cell and 1 representing a stem cell.

At this point, we noticed that there were exactly 1/3 as many non-stem cell types as there were stem cell types. This was problematic for the initial models that we created, as the imbalanced data often threw off the models. In order to resolve this, we employed oversampling, a common method that duplicates the non-stem cell data to make them equal in number to the data of the stem cell types. This data was stored, and then exported in .csv form in `MasterSheetCleaned.csv`. We are now done pre-processing of the data!

In `modelsetup.py`, where the actual regression model is created using Keras/Tensorflow, we did processed the data in lines 1 to 36. Using pandas, we read the CSV into the program and removed the column of the cell line name. From there, we randomly divided the data into 80% for the training dataset and 20% for the testing dataset, and popped the column indicating whether or not it was a stem cell out into `train_labels` and `test_labels` respectively. Furthermore, since there is a large distribution of gene expression (some genes' degrees of expression have a maximum raw value of about 50 while others were in the hundreds), we normalized all the data to values between 0 and 1, similar to how z scores work. We are now done processing the data and ready to build our model!

Note that we did not use SQL at any point for this data; we initially considered this, but it did not make sense to import all the Excel data to SQL when we are not going to be modifying the data or adding to it at any point beyond the processing stage.

## Building the Model

We decided to use a neural network to create our regression model due to its ability to effectively and accurately build out models that match the data by adapting from the previous iterations. Keras sitting on top of Tensorflow was our top choice for building out the model since the syntax was easily accessible and applicable. 

Our neural network generally followed standard parameters; we had 3 layers with 6 nodes (1 for each gene) in the first 2 layers and 1 node telling us the probability that it was a stem cell from 0 to 1 in the last layer. We used a root mean squared optimizer and used mean squared error as the loss metric. Additionally, we made our neural network check the model against the validation error as it went along as well with a patience of 10 epochs to check for improvements in the model for the validation error, in order to address the issue of overfitting. The program would stop 10 epochs after the validation error stopped improving, thereby alleviating the concerns surrounding overfitting. We decided to show the model being built on the command line with epoch dots, in order to have a visual gauge on the process of the neural network.

## Calculating Accuracy

The model itself outputs the mean absolute error, which we converted to percentage form and printed in the terminal on line 80. 

Then, we used the model to predict our normalized test data. In order to see how accurate it was, we put the original values and predicted values into lists, which we then compared for a one-tailed 5% deviation. This model worked since the values were all between 0 and 1, allowing us to easily designate 5% as 0.05. These one-tailed tests were as follows: if the original value was 1 (it was a stem cell), then if the predicted value was lower than 0.95 then it was not categorized correctly based on this 5% deviation. Similarly, if the original value was 0 (it was not a stem cell), then if the predicted value was higher than 0.05 then it was not categorized correctly based on this 5% deviation. Since our data is the probability that a cell is a stem cell or not, testing for these one-tailed 5% deviations is essentially a 95% confidence interval test, as those that are categorized correctly within this 5% error would have over 95% certainty.

Afterwards, our model was saved to the disk as `model.h5`.

The accuracy of our model was also shown visually using `matplotlib`, where the x axis was the actual values of stem cell categorization (0 or 1) while the y axis was the predicted value. A perfect prediction model would have all the datapoints on the line y=x, which is also shown on the graph. 

In general, after 10 trials of creating models using Keras, we recorded the individual errors and number categorized correctly under the 95% confidence interval in `AveragesCIdata.xlsx`. The average error was 3.726%, and we correctly categorized 94.167% of the datapoints correctly within the 95% confidence interval. Our models also visually matched the line in the `matplotlib` graph relatively closely, and we saved the images of the graphs as Figures 1 through 10 in our directory.

## Constructing our Website

In regards to the design of our website, we implemented a "Context" page to explain the details of why stem cells have a lot of therapeutic potential and the challenges surrounding them. In this page we incorporated a video that we think explains stem cells well, blockquotes introducing the ethical debates surrounding them, and links to other educational sources.

In the "Methodology" page, we explained how we built our model, how it works, and how accurate it is. We incorporated the screencap video of me showing how the model was run, a public link to download our code from Github, and a table with the Figures 1-10 showing the visual interpretation of our model. 

The "About Us" page is simply brief bios about us with pictures, followed by links to our social accounts. 

Finally, the "Demonstration" page is where the interactive Flask part comes in. The user inputs values between 0 and 100 for each of the genes, representing the percent of maximum expression for each of the genes in this theoretical cell. We load the Keras model and request the inputs from the form. Extensive error checking is done, first making sure that the input can be turned into a float and then making sure that all the values are between 0 and 100. If any of these conditions are not fulfilled, they are brought back to the "Demonstration" page with an alert that they inputted the data wrong. If everything works, then the data is converted from percentage form to a value between 0 and 1. This is inserted into a pandas dataframe, which is then fed into the model for prediction. Finally, the model outputs a number between 0 and 1 representing the probability that this cell is a stem cell, which is then converted to percentage form and displayed on our website.



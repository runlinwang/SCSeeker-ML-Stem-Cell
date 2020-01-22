# SCSeeker: Machine Learning for Stem Cell Discovery
By RunLin Wang and Jonathan Liu, Harvard University

## Background Information
Stem cells are unspecialized cells that can differentiate into various different types of cells, such as muscle cells and white blood cells. They have tremendous potential in regenerative medicine, since stem cells could theoretically be used to replace the tissues of damaged organs that cannot self-heal, such as the brain. This would allow for the development of cures for currently untreatable conditions like leukemia.

On our website, we outline the issues surrounding stem cells in more detail, but in short the justification behind our project is that the stem cells required to treat certain diseases are often dangerous to extract or are surrounded by ethical debates. Thus, scientists have aimed to create stem cells from normal cells in the laboratory, which are called "induced" stem cells. 

In order to make induced stem cells, researchers often modify the genetic expression of normal cells. Many genes related to cellular self-renewal, growth, and differentiation may be correlated to stem cell activity. However, it is difficult to reliably predict how changing a combination of closely connected genes could impact the cell as a whole. In this case, a computational model that predicts whether a combination of genes is likely to be a stem cell based on the genetic data of known stem cells would be highly beneficial for the scientific community. Such a model would allow researchers to screen particular combinations of genes for stem cell potential before investing further time and effort into genetically modifying a cell.

As such, we created a machine learning model using Tensorflow to predict the likelihood that a particular combination of genes will result in a stem cell. In particular, we utilized the Keras deep learning library to create a neural network that takes gene expressions as inputs and creates a regression model. This regression model outputs a probability that the given combination of genes will result in a stem cell. We chose 6 genes known to be linked to stem cells for our model: FGF13, GDF3, SKIL, ERAS, TRIM28, and ZFX. We trained and tested our model using the expression data of these genes in both stem cell lines and non-stem cell lines, which was obtained through StemCellDB, an open-source database with genetic information about stem cells and normal cells.

Our program `modelsetup.py` contains the code used to build the model from Keras, while our Flask based website showcases this model and allows for a demonstration of its prediction power.

## Instructions for Use

1. Download all files in this directory, keeping the folder organization intact. We strongly recommend that you do this on a local IDE (eg. Pycharm).
2. In your terminal, navigate to this folder using `cd`.
3. Install all libraries indicated in `requirements.txt`.
4. In your terminal, run `python modelsetup.py` to create a regression model based on the genetic data of stem cells and normal cells using Tensorflow and Keras. A number of statistics will show in the terminal regarding the accuracy of the model, and a graph will show the correlation of the actual stem cell expression to the predicted datapoints. Close the graph to proceed with the next step.
5. 

## References
The following sources were all very helpful in both understanding the problems surrounding stem cells and for helping us develop our code for both the ML model and the website, and we would like to reference them below:

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4633996/?fbclid=IwAR3Ty_EZV2xyc5WzOb030Kv8eHxHN1pk3920ugbRZRhwPjP9XERqKYCtGjg

https://www.sciencedirect.com/science/article/pii/S1873506112000888?via%3Dihub&fbclid=IwAR1ckAcTIE0g0m4pnQlH8Emw6lP2IO7-S2yRG2BGEvITmMNWXegFRR50Ti8

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4919381/

https://www.ncbi.nlm.nih.gov/pubmed/29441649

https://journals.plos.org/plosone/article/file?type=supplementary&id=info:doi/10.1371/journal.pone.0053372.s003

https://askubuntu.com/questions/764032/how-to-uninstall-tensorflow-completely

https://www.tensorflow.org/install/pip?lang=python3

https://stackoverflow.com/questions/47304999/attributeerror-module-tensorflow-has-no-attribute-python/47306203#47306203

https://github.com/tensorflow/tensorflow/issues/25224

https://www.tensorflow.org/api_docs/python/tf/keras/models/load_model

https://keras.io/getting-started/faq/

https://stackoverflow.com/questions/45548426/store-numpy-array-in-cells-of-a-pandas-dataframe

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html

https://pypi.org/project/Flask/

https://docs.scipy.org/doc/numpy-1.13.0/user/basics.creation.html

https://keras.io/models/model/

https://machinelearningmastery.com/save-load-keras-deep-learning-models/

https://towardsdatascience.com/having-an-imbalanced-dataset-here-is-how-you-can-solve-it-1640568947eb

https://stackoverflow.com/questions/35520587/how-to-determine-the-number-of-layers-and-nodes-of-a-neural-network

https://stackoverflow.com/questions/35911252/disable-tensorflow-debugging-information

https://stackoverflow.com/questions/36269746/matplotlib-plots-arent-shown-when-running-file-from-bash-terminal

https://www.w3schools.com/howto/howto_css_fullscreen_video.asp

https://stackoverflow.com/questions/3594512/css-body-background-image-fixed-to-full-screen-even-when-zooming-in-out

https://stackoverflow.com/questions/4380105/html5-video-scale-modes

https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int

https://bootsnipp.com/snippets/Bq909

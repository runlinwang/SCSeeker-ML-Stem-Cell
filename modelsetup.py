# importing relevant libraries for general dataset analysis and visualization
import os
import pandas as pd
import matplotlib.pyplot as plt

# importing tensorflow library to begin building out the model
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.modeling

# preventing warning indications from showing up, which clutter the interface
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# importing the CSV obtained from pre-processing of Excel files from StemCellDB
dataset = pd.read_csv('MasterSheetCleaned.csv')

# cleaning the dataset of the cell line name
dataset.pop("Cell line name")

# splitting the data randomly into a training dataset and a testing dataset
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# remove the column revealing whether or not it is a stem cell from the test and train dataset labels
train_labels = train_dataset.pop("Stem Cell Y/N")
test_labels = test_dataset.pop("Stem Cell Y/N")

# since the ranges of the data are very different and can throw off the machine learning algorithm, we normalize the data based on the means and stds here
statistics = train_dataset.describe()
statistics = statistics.transpose()
# resembles z score normalization, to make everything between 0 and 1
normal_train_data = (train_dataset - statistics["mean"]) / statistics["std"]
normal_test_data = (test_dataset - statistics["mean"]) / statistics["std"]

# defining a function that utilizes a Keras/tensorflow based sequential neural net


def build():
    modelML = keras.Sequential([
        # implementing 3 layers, first knowing what the shape is, last one is linear activation, 6 nodes in each layer since 6 parameters
        layers.Dense(6, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
        layers.Dense(6, activation=tf.nn.relu),
        layers.Dense(1)
    ])

    # establishing the optimizer using root mean squared
    optimizer = tf.keras.optimizers.RMSprop(0.001)

    # running the model with the loss as the mean squared error
    modelML.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])

    return modelML


# saving this model as the variable model
modelML = build()

# since the validation error cloud just fluctuate instead of improving, we set an early stop
# patience makes sure that we give it leeway of 10 epochs to check for any improvement
stoptime = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10)

# training the model for up to 2000 epochs, but stopping when improvement stops
history = modelML.fit(
    normal_train_data,
    train_labels,
    epochs=2000,
    validation_split=0.2,
    verbose=0,
    callbacks=[stoptime, tfdocs.modeling.EpochDots()]
)

# using the test data to evaluate the effectiveness of the model created
loss, mae, mse = modelML.evaluate(normal_test_data, test_labels, verbose=2)

# printing the mean absolute error in percentage form
print("")
print("Mean error: {:5.2f}% chance for stem cell categorization".format(mae*100))

# saving the predictions of each of the rest
predictionsAll = modelML.predict(normal_test_data).flatten()

# creating the blank lists for iterating over next, for comparison
labelslist = []
predictionslist = []

for element in test_labels:
    labelslist.append(element)

for element in predictionsAll:
    predictionslist.append(element)

counter = 0
fixed = len(labelslist)

# testing for 95% confidence interval
for index in range(fixed):
    if labelslist[index] == 1 and 1 - predictionslist[index] > 0.05:
        counter += 1
    elif labelslist[index] == 0 and predictionslist[index] > 0.05:
        counter += 1

print("")
print("Using a 95% confidence interval,", (fixed - counter), "of the", fixed, "test datapoints are categorized correctly.")
print("")

# saving the model to a file that we can open in the future
modelML.save("model.h5")
print("Model saved to disk.")
print("")

# establishing the plot of the correlation between prediction and reality
plt.axes(aspect="equal")
plt.scatter(test_labels, predictionsAll)
plt.xlabel('Actual Values of Stem Cell Categorization')
plt.ylabel('Predictions of Stem Cell Categorization')
lims = [-0.5, 1.5]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)

plt.show()
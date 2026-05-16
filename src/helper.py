import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.metrics import confusion_matrix

class Helper:
    
    def set_gpu_enviorement(self):
        gpu_device = tf.config.list_physical_devices('GPU')
        tf.config.set_visible_devices(gpu_device[0], 'GPU')

    def get_train_valid_gen(self, image_folder, img_size=(224,224),batch_size=32, random_seed=232323):
        
        data_gen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            # shear_range=0.2,
            # zoom_range=0.2,
            # horizontal_flip=False,
            # vertical_flip=False,
            # samplewise_center=True, 
            validation_split=0.2
        )

        train_gen = data_gen.flow_from_directory(
            image_folder,
            target_size=img_size,
            batch_size=batch_size,
            class_mode="categorical",
            subset="training",
            shuffle=False
        )

        # define test data generator
        valid_gen = data_gen.flow_from_directory(
            image_folder,
            target_size=img_size,
            batch_size=batch_size,
            class_mode="categorical",
            subset="validation",
            shuffle=False
        )
        return (train_gen, valid_gen)
    
    def plot_training_set(self, train_gen, num_row=5, num_col=5):
        
        # Set the number of images to display
        num_images = num_row * num_col

        # Create a figure and axes for subplot
        fig, axes = plt.subplots(num_row, num_col, figsize=(10, 10))

        # Iterate over the train_gen generator to get random images
        for i, (image, label) in enumerate(train_gen):
            # print(i, i//5, i%5)
            
            # Access individual images and labels
            image = image[0]  # Access the first image in the batch

            # Convert image from rescaled form to original form (multiply by 255)
            image = image * 255

            # Convert image to uint8 data type
            image = image.astype('uint8')
            # print(image.shape)

            # Get the subplot index
            row = i // 5
            col = i % 5

            # Display the image in the subplot
            axes[row, col].imshow(image)

            # Set the subplot title as the label
            axes[row, col].set_title(label[0])

            # Break the loop when desired number of images are displayed
            if i == num_images - 1:
                break

        # Hide axis labels and tick marks
        for ax in axes.flat:
            ax.axis('off')

        # Adjust subplot spacing
        plt.tight_layout()

        # Show the plot
        plt.show()
    
    def plot_train_and_val_curves(self, history):
    
        # collect data for result
        result = {}
        result["epoch"] = history.epoch
        result["accuracy"] = history.history["accuracy"]
        result["val_accuracy"] = history.history["val_accuracy"]
        result["loss"] = history.history["loss"]
        result["val_loss"] = history.history["val_loss"]

        # create a data frame
        result = pd.DataFrame(result)

        # get some values
        acc_train = result.iloc[-1]["accuracy"]
        acc_valid = result.iloc[-1]["val_accuracy"]
        loss = result.iloc[-1]["loss"]
        loss_valid = result.iloc[-1]["val_loss"]

        plt.figure(figsize=(10,4), dpi=150)
        plt.subplot(121)
        plt.plot(result.epoch, result.accuracy, label=f"Train acc {acc_train:.2f}")
        plt.plot(result.epoch, result.val_accuracy, label=f"Validation acc {acc_valid:.2f}")
        plt.ylabel("Acc")
        plt.xlabel("Epoch")
        plt.legend()

        plt.subplot(122)
        plt.plot(result.epoch, result.loss, label=f"Train loss {loss:.2f}")
        plt.plot(result.epoch, result.val_loss, label=f"Validation loss {loss_valid:.2f}")
        plt.ylabel("Loss")
        plt.xlabel("Epoch")
        plt.legend()
    
    
    def get_confusion_matrix(self, model, valid_gen):

        # Make prediction
        predictions = model.predict(valid_gen)
        y_pred = np.argmax(predictions, axis=1)

        # Get real labels
        y_true = valid_gen.classes

        # Classification report
        print('Classification Report:')
        print(classification_report(y_true, y_pred))

        # Karmaşıklık matrisini hesaplayın ve yazdırın
        cm = confusion_matrix(y_true, y_pred)
        print('Confusion Matrix:')
        print(cm)

        return cm
    
    
    def plot_confusion_matrix(self, model, valid_gen):
        predicted = np.argmax(model.predict(valid_gen), axis=1)
        cm = pd.DataFrame(
            confusion_matrix(valid_gen.labels, predicted),
            columns=[f for f in valid_gen.class_indices.keys()],
            index=[f for f in valid_gen.class_indices.keys()]
            )
        sns.heatmap(cm, annot=True, cmap="crest", linewidths=0.5, cbar=False, fmt="d")

    def plot_roc_curve(self, model, valid_gen):
        y_true = valid_gen.classes
        class_labels = list(valid_gen.class_indices.keys())

        # One-hot encode the labels
        y_true = tf.keras.utils.to_categorical(y_true, num_classes=len(class_labels))

        # Generate predictions
        y_pred = model.predict(valid_gen)

        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(len(class_labels)):
            fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_pred[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_pred.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

        # Plot ROC curve
        plt.figure(figsize=(8, 6))
        plt.plot(fpr["micro"], tpr["micro"], label='micro-average ROC curve (area = {0:0.2f})'.format(roc_auc["micro"]),
                 color='deeppink', linestyle=':', linewidth=4)

        for i in range(len(class_labels)):
            plt.plot(fpr[i], tpr[i],
                     label='ROC curve of class {0} (area = {1:0.2f})'.format(class_labels[i], roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.show()

The dataset contains 5000 "24 chromosome class annotations" and 2000 "single chromosome annotations". Each directory has an image and the associated annotation available in xml format.

Single chromosomal annotations are stored in the "single_chromosomes_object" files. This data set only provides users with a distinction between chromosomes and backgrounds.
Chromosomes are not classified in this dataset --> this can be used to train a classifier to separate chromosomes from non-chromosomes.

"24_chromsomes_object" has images along with individual annotation for each chromsome (1-23, X, Y).

Goal: Train a classifer to output the chromosome identity for a given metaphase image. You should plot the auPRC curve. Use the list of images in train.txt to train and in test.txt to evaluate your model.


train & test: File names for the training and test sets. "train.txt" "test.txt"


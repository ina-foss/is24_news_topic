# Automatic Classification of News Subjects in Broadcast News: Application to a Gender Bias Representation Analysis

## About

Source code for the Interpseech 2024 paper about automatic classifcation of news
subjects in broadcast news. The code contains evaluation scripts, models 
training and interfence source.

### Dataset

The annotated dataset contains about 03h44min of broadcast news, with 605 
dialogues for the Test set. The dataset can be downloaded at the following 
URL: [https://www.ina.fr/recherche/dataset-project](https://www.ina.fr/recherche/dataset-project), under the name `is24_news_topic`.

### Evaluation scripts

The scripts to eval your own models are included in the folder `evaluation/`. 
You will need an original copy of the dataset (see above.).

You may use the following script:
```bash
source_dataset=PATH_TO_THE_ORIGINAL_UNZIPPED_DATASET
predictions=PATH_TO_YOUR_PREDICTION_FOLDER
evaluation/eval \
	--reference $source_dataset \
	--prediction $predictions \
	--subset dev # dev or test
```
The results will be saved inside `$predictions` folder. You need to format your
predictions into the following format:
```
TODO: TO_COME
```

### Models

The source code of training and inference of the models presented in the paper 
are included in the folder `models/` (`models/BERT` and `models/Mixtral`).

## Installation 

You need `python3`, `pip3`.

```bash
pip3 install -r requirements.txt
```

## Citation

If you use this corpus or the source code of this repository, please cite the 
following article:
```bib
TODO: TO_COME
```

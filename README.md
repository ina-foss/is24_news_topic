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
evaluation/eval \
	--reference ORIGINAL_DATASET_FOLDER \
	--prediction PRED_FOLDER/predictions.json \
	--subset dev # dev or test
```

The results will be saved inside `PRED_FOLDER` folder, with the name
`results.json`. You need to format your predictions into the following format:

```json
{
	"DIALOGUE_ID_1": {
		"text": "input text for that dialogue (this field is not required in your output file, but it allow you to easily browse the file while reading the predicted output, and manually see if what your model predicted)",
		"class__ARTS/CULTURE/ENTERTAINMENT": false,
		"class__COMMERCIAL": false,
		"class__CRIME/LAW/JUSTICE": true,
		"class__DISASTER/ACCIDENT": false,
		"class__ECONOMY/BUSINESS/FINANCE": false,
		"class__EDUCATION": false,
		"class__ENVIRONMENTAL_ISSUE": false,
		"class__HEALTH": false,
		"class__LABOUR": false,
		"class__LIFESTYLE/LEISURE": false,
		"class__OTHER": false,
		"class__POLITICS": false,
		"class__RELIGION/BELIEF": false,
		"class__SCIENCE/TECHNOLOGY": false,
		"class__SOCIAL_ISSUE": false,
		"class__SPORT": false,
		"class__UNREST/CONFLICTS/WAR": true,
		"class__WEATHER": false
	},
	"DIALOGUE_ID_2": {
		"..."
	}
}
```

### Models

The source code of training and inference of the models presented in the paper 
are included in the folder `models/` (`models/BERT` and `models/Mixtral`).

#### BERT finetuning

The script to finetune all models presented in the paper is in 
`models/BERT/train_all`. It calls the `train` script. To generate the 
predictions of a specific model, use `models/BERT/predict`. You can then 
use `evaluation/eval` to get metric scores of your model.

#### Mixtral

The prompt used for the Mixtral model is in the file `models/Mixtral/prompt.txt`.
Use the script `models/Mixtral/inference_mixtral` to generate the outputs of 
Mixtral (or an other model) base on this prompt and input dialogues. Then, 
call `parse_safe_json` to convert the output of the model into a valid JSON 
format, which you can then use with generate_prediction_dataset to create a 
valid training/validation/testing dataset. You then can use `evaluation/eval` 
to evaluate Mixtral response if the inference was on the dataset dialogues, 
or `models/BERT/train` to finetune BERT on these annotations.

## Installation 

You need `python3`, `pip3`.

```bash
pip3 install -r requirements.txt
```

## Citation

If you use this corpus or the source code of this repository, please cite the 
following article:
```bib
@inproceedings{pelloin2024automatic,
    title = {Automatic Classification of News Subjects in Broadcast News: Application to a Gender Bias Representation Analysis},
    author = {Valentin Pelloin and Lena Dodson and \'Emile Chapuis and Nicolas Hervé and David Doukhan},
    booktitle = {Proc. InterSpeech 2024},
    month = 9,
    year = 2024,
    address = "Kos Island, Greece",
}
```

## Credits

This work has been partially funded by the [French National Research Agency](https://anr.fr) under the Gender Equality Monitor (ANR-19-CE38-0012) and Pantagruel (ANR-23-IAS1-0001) projects.

# Dialogue generation with VRNNs
This is a Python implementation of the work [Learning Interpretable Latent Dialogue Actions With Less Supervision](https://arxiv.org/abs/2209.11128).
For questions or comments, contact **hudecek@ufal.mff.cuni.cz**.

### Data
We implement several readers for different datasets. Namely it is:
 - [CamRest](https://github.com/shawnwun/NNDIAL/tree/master/data), [ontology](https://github.com/shawnwun/NNDIAL/tree/master/resource)
 - [SMD](http://nlp.stanford.edu/projects/kvret/kvret_dataset_public.zip)
 - [MultiWOZ](https://www.repository.cam.ac.uk/handle/1810/294507)

You can use Makefile to download & prepare the data:
```commandline
make DATA_DIR=data_dir_path [camrest|smd|multiwoz]
``` 
If you cannot/do not want to use the Makefile, please refer to the script to prepare the data manually.

### Installation
The codebase is written in Python 3.6 and requires the dependencies specified at `requirements.txt` file.
To install, simply run in your environment:
```
pip install -r requirements.txt
```

### Training
To train the model, first prepare the configuration.
Sample configuration is located at `config/vrnn.yaml`.

After the configuration is prepared, run:
```
python -m VRNN-generation.run VRNN-generation/config/vrnn.yaml --output VRNN-generation/output/$DATA
```
where `$DATA=[camrest|multiwoz|smd]` 

### Evaluation
To evaluate various metrics, you can use the prepares evaluation script as follows:
```
python -m evaluation.run --work_dir output_model_dir --fn model_predictions.txt --metrics $METRIC_MODE
```
where `$METRIC_MODE` can be one or more values from the following list:
 - *bleu* Evaluate the BLEU score
 - *z_semantics* Train and evaluate a DT classifier that predicts system actions from latent variables.
 - *z_info* Compute Mutual Information between the latent variables and ground truth actions.
 - *ppl* Compute perplexity
 - *success* Compute (modified) dialogue success rate
 - *emr* Compute Entity Match Rate

### Acknowledgements

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

### Citing
To cite this work, please use the following record:
```
@misc{https://doi.org/10.48550/arxiv.2209.11128,
  doi = {10.48550/ARXIV.2209.11128},
  
  url = {https://arxiv.org/abs/2209.11128},
  
  author = {Hude??ek, Vojt??ch and Du??ek, Ond??ej},
  
  keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
  
  title = {Learning Interpretable Latent Dialogue Actions With Less Supervision},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
### Acknowledgements
This work was partially supported by Charles University projects PRIMUS/19/SCI/10, GA UK No. 302120 and SVV No. 260575 and by the European Research Council (Grant agreement No. 101039303 NG-NLG). It used resources provided by the LINDAT/CLARIAH-CZ Research Infrastructure (Czech Ministry of Education, Youth and Sports project No. LM2018101).

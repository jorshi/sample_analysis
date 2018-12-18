# Intelligent classification and browsing of kick and snare samples using manifold learning methods
This code was written for research performed at University of Victoria for analyzing, classifying, and visualizing kick and snare drum samples. This application will load a set of audio samples, perform audio feature extraction algorithms on those samples, perform PCA for analysis purposes and dimension reduction, perform a number of manifold dimension reduction techniques, and run various classification experiments for evaluation. The results of this work are documented in an AES conference plublication: http://www.aes.org/e-lib/browse.cfm?elib=19284

An audio plugin was created based on this work; the code for that can be found here: https://github.com/jorshi/sieve
A paper related to the development of this plugin was presented at the 2017 Workshop on Intelligent Music Production: http://www.semanticaudio.co.uk/events/wimp2017/#shier

### Requirements and Installation

Requirments: Python 2.7, MySQL, Essentia

MySQL: https://dev.mysql.com/doc/refman/8.0/en/installing.html

Essentia: http://essentia.upf.edu/documentation/installing.html

Install python project requirements with pip:  `pip install -r ./requirements.txt`

The python Django framework is used to interface with the MySQL database. Django will be installed with pip
and is included in requirements.txt.

For more information about Django: https://docs.djangoproject.com/en/2.1/

### Setup DB

Once everything is installed, a new MySQL database with the current permissions must be setup
which will allow for Django to interact with the database.

`mysql < ./sample_analysis/db_utils/setup_db.sql`

or depending on how you setup mysql

`mysql -uroot < ./sample_analysis/du_utils/setup.sql`

## Commands

All commands are setup through the django command interface. They can be accessed using:

`cd sample_analysis`
`python manage.py command arguments [optional-arguments]`

ALL COMMANDS LISTED BELOW, INCLUDING SHELL SCRIPTS WILL ASSUME YOU ARE IN THE sample_analysis FOLDER. ie the folder that contains manage.py

For more information on Django commands and how to write your own: https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

### Models & Migration

The different data models that are used are described in https://github.com/jorshi/sample_analysis/blob/master/sample_analysis/analysis/models.py

Instances of each model are stored in separate database tables and hold information related to the samples
that have been loaded, data from audio feature extraction, dimensions after manifold learning, etc.

In order to create tables in the database for each model, a Django command must be run:
`python manage.py migrate`

If you make any changes to models.py the database tables will need to be updated to reflect those changes. <br />
`python manage.py makemigrations` <br />
Django will automatically detect changes to models.py and create the SQL commands to update the database <br />
Then: `python manage.py migrate` <br />
to run those SQL commands

Project should now be ready to start loading in samples!

### Loading Samples

`python manage.py loadsamples directory [--tags]` <br />
  options:
    --tags any tag words to associate with this directory of samples, multiple tags are comma separated

SAMPLES MUST BE ORGANIZED CORRECTLY <br />
A particular folder structure is assumed so that samples are correctly organized by Sample Pack (Drum Machine), Kit, and Sample Type (kick or snare)

This structure is as follows:
`DrumSamples/SamplePackName/kit_x/kick/sample_name.wav`<br />
or<br />
`DrumSamples/SamplePackName/kick/sample_name.wav`<br />
if there are not multiple kits.

Replace kick with snare for snare drum samples.

### Running Feature Analysis

`python manage.py run_analysis_full [--window_length] [--window_start]`

`--window_length` and `--window_start` are optional arguments that can be used to specify
the windowing scheme that is applied to each audio sample prior to audio feature extraction.
Window length is given in milliseconds and window start is given in the percantage of the attack
portion of the audio signal. If both window length and window start are left out, then the full
sample length will be used starting from the beginning of the sample. This will be stored
in the database as a window length and window start of 0 and 0.

Audio feature extraction is performed using Essentia and 133 features are extracted for each audio sample.

Alternatively, there is a shell script can be executed that will run a full analysis on a selection
of window lengths and start times that were used for this research.

`./scripts/full_analysis.sh`

Results of audio feature extraction are stored in the data model AnalysisFull

### Principal Component Analysis

Principal Component Analysis (PCA) is used here as an analysis tool to evaluate the effects of windowing audio samples prior to audio feature extraction.

To run PCA on a set of samples: <br/>
`python manage.py pca_full sample_type window_length window_start`<br/><br/>

Where `sample_type` is either 'ki' or 'sn', `window_length` is the window length in ms, and `window_start` is the starting time of the window in percentage of the attack. The combination of `window_length` and `window_start` must have already been extracted during feature analysis in the previous step.

Tests for sample adequecy and the null hypothesis are performed and the outputs for these are printed to stdout. Tests performed are Bartlett's Test of Sphericity, Levene's Test, and Kaiser-Meyer-Olkin.

Explained variance ratio, explained variance, and top components are printed to stdout. The first four dimensions resulting from PCA for each sample are saved as a AnalysisPCA object in the database and the explained variance ratio is saved as a PCAStat object in the database. Each PCAStat data object has a unique sample type, window length and window start. 

There are two shell scripts that will run PCA on all window length and start variations used in the research. They can be executed using:
`./scripts/full_pca_kick.sh && ./scripts/full_pca_snare.sh`

#### PCA - Maximum Variance Windowing Scheme
In addition to the regular command `pca_full` which allows you to specifiy the sample type and window length and start combination, another command was created to test an alternative windowing scheme. This command is: <br />
`python manage.py full_pca_window sample_type window_length window_start` <br /><br />
This command uses a windowing scheme that we call Maximum Variance Windowing. In this scheme, multiple combinations of window_length and window_start are used in order to maximize the variance for each dimension across all samples of a particular type. For example, for snare drums, the variance of the spectral centroid feature might be maximized when using a window length of 250ms and a window start of 50%, and the variance of the first MFCC band feature might be maximized when using a window length of 100ms and a window start of 20%. In Maximum Variance Windowing, all 133 feature dimensions have a window length and start combination selected so that the variance is maximized for that feature. AnalysisPCA objects generated from this command will be stored with a window_start and and window_length of -1. 

*Note that arguments for `window_length` and `window_start` are still required. This is just used to extract the correct number of samples from the database. Use any combination of length and start that was used when running feature analysis.

### Manifold Learning
Manifold learning is used here for dimension reduction to 2 dimensions for visual plotting. The command to perform manifold learning is: <br />
`python manage.py manifold manifold_method sample_type window_length window_start`<br /><br />
Where `manifold_method` is one of `tsne`, `tsne_pca`, `isomap`, `locally_linear`, `mds`, or `spectral`
For more information on each of these manifold learning methods see: https://scikit-learn.org/stable/modules/classes.html#module-sklearn.manifold

To use the maximum variance windowing scheme method described above, use the command:<br/>
`python manage.py manifold manifold_method sample_type window_length window_start`<br /><br />
Similar to above, the `window_length` and `window_start` parameters when using this method are simply required to extract the correct number of samples from the database, the window length and start time will be selected automatically to maximize variance for each dimension.

Results of manifold learning dimension reduction are stored as a Manifold object in the database.

To run all manifold methods on all combinations of window start and length used in this research use the shell scripts:<br />
`./scripts/manifold_ki.sh && ./scripts/manifold_sn.sh` <br/>

### Classification
Classification is used to evaluate the windowing methods as well as to evaluate the effects of the various dimension reduction techniques. Classification is performed using SVC, Perceptron, and Random Forest methods. For each classification task, the baseline score is printed, along with the score achieved by each individual method, and then an average of the three methods. Each of these scores is saved to the database as a Classification object.
#### Sample Type Classification
`python manage.py classifier_sample_type window_length window_start`

or to use the maximum variance windowing scheme as described above: 
`python manage.py classifier_type_window window_length window_start`

Sample type classification attempts to classify kicks and snare samples.
#### Drum Machine Classification
`python manage.py classifier_dm sample_type window_length window_start`

or to use the maximum variance windowing scheme as described above: 
`python manage.py classifier_dm_window sample_type window_length window_start`

To run drum machine classification on the samples after dimension reduction:
`python manage.py classifier_dm_reduced reduction_method sample_type window_length window_start`

Where reduction method is one of the manifold methods or pca

Drum machine classification attempts to classify either kicks or snares by drum machine. THE DRUM MACHINES USED ARE HARD CODED INTO THE CLASSIFICATION COMMAND SCRIPTS. The ids for each drum machine will need to be updated by you depending on which drum machines you want to include in your classification. Here, the drum machine id is the SamplePack model id.

In the research, we used drum machines that had 50 or more samples. You can use this MySQL command to find the SamplePack ids for SamplePacks that have more than 50 kick samples: <br />
`select p.id, p.name, count(*) from analysis_sample s join analysis_kit k on s.kit_id=k.id join analysis_samplepack p on k.sample_pack_id=p.id where s.sample_type='ki' group by p.id having count(*) > 50;`<br/>
Replace `s.sample_type='ki'` with `s.sample_type='sn'` to get SamplePacks with more than 50 snare drums

The resulting SamplePack ids need to be updated in the drum machine classification scripts:
https://github.com/jorshi/sample_analysis/blob/master/sample_analysis/analysis/management/commands/classifier_dm.py
https://github.com/jorshi/sample_analysis/blob/master/sample_analysis/analysis/management/commands/classifier_dm_window.py
https://github.com/jorshi/sample_analysis/blob/master/sample_analysis/analysis/management/commands/classifier_dm_reduced.py

##### Running MySQL Commands
In order to run raw SQL commands you need to enter into the mysql interface:<br />
`mysql` or `mysql -uroot`<br />
Then select the sample_analysis database:<br />
`use sample_analysis;`<br />
Then run the raw SQL command, such as the one outlined above for retrieving SamplePack ids.

#### Manufacturer Classification
`python manage.py classifier_manu sample_type window_length window_start`

or to use the maximum variance windowing scheme as described above: 
`python manage.py classifier_manu_window sample_type window_length window_start`

Manufacturer classification attempts to classify either kick or snares by manufacturer. THE MANUFACTURERS ARE HARD CODED INTO THE CLASSIFICATION COMMAND SCRIPTS. Manufacturers need to be added manually to the database and to each SamplePack model. The easiest way to do this is through raw mysql commands. Then, the manufacturer ids need to be updated in the manufacturer classification scripts:

https://github.com/jorshi/sample_analysis/blob/master/sample_analysis/analysis/management/commands/classifier_manu.py
https://github.com/jorshi/sample_analysis/blob/master/sample_analysis/analysis/management/commands/classifier_manu_window.py


## Exporting Data

There are a number of scripts in `./sample_analysis/db_utils/export_commands` for exporting DB contents to a .csv file. They are currently hard-coded with the output file, so that will need to be editted for a new user.







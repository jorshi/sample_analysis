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

If you make any changes to models.py the database tables will need to be updated to reflect those changes. Run:
`python manage.py makemigrations` - Django will automatically detect changes to models.py and create the SQL commands
to update the database
Then:
`python manage.py migrate` to run those SQL commands

Project should now be ready to start loading in samples!

### Loading Samples

`python manage.py loadsamples directory [--tags]` <br />
  options:
    --tags any tag words to associate with this directory of samples, multiple tags are comma separated

!SAMPLES MUST BE ORGANIZED CORRECTLY!
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

Alternatively, there is a shell script can be executed that will run a full analysis on a selection
of window lengths and start times that were used for this research.

### Statistical Analysis

Check for outlier samples are mark them as outliers to be removed from any further analysis
`python ./sample_analysis/manage.py remove_outliers sample_type`

Run primrary component analysis<br />
`python ./sample_analysis/manage.py pca sample_type`

Variance, variance ratios, and component weightings for pca will be printed to stdout. The points of each sample in corresponding to the new dimensions is saved to the analysis_analysispca mysql table.

sample_type is either 'ki' or 'sn'

### Exporting Data

There are a number of scripts in `./sample_analysis/db_utils/export_commands` for exporting DB contents to a .csv file. They are currently hard-coded with the output file, so that will need to be editted for a new user.







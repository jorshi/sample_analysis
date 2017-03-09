# Sample Analysis
Drum Sample Analysis Project for UVic JCURA. The of this project is to run a number of audio feature extraction algorithms from Essentia on a set of kick and snare drum samples. Outlier detection and Primary Component Analysis are implemented for statistical analysis. 

The Django framework is used because of the ease that it allows for interfacing with a MySQL DB, as well as I thought it might be cool to but these results in an interactive web interface at some point.

### Requirements and Installation

Requirments: Python 2.7, MySQL, Essentia

Essentia: http://essentia.upf.edu/documentation/installing.html

Install python project requirements with pip:  `pip -r ./requirements.txt`

### Setup DB

`mysql < ./sample_analysis/db_utils/setup_db.sql`

### Run Migrations

`python ./sample_analysis/manage.py migrate`

Project should now be ready to start loading in samples and running feature analysis

### Loading Samples

`python ./sample_analysis/manage.py loadsamples [options] directory` <br />
  options:
    --tags any tag words to associate with this directory of samples, multiple tags are comma separated

It is assumed that samples are in the following folder structure:
`DrumSamples/SamplePackName/kit_x/kick/samples.wav`<br />
or<br />
`DrumSamples/SamplePackName/kick/samples.wav`<br />
if there are not multiple kits.

Replace kick with snare for snare drum samples.

### Running Feature Analysis

`python ./sample_analysis/manage.py runanalysis analysis_type`

Alternatively, `./sample_analysis/full_analysis.sh` will run the full feature set

### Statistical Analysis

Check for outlier samples are mark them as outliers to be removed from any further analysis
`python ./sample_analysis/manage.py remove_outliers sample_type`

Run primrary component analysis<br />
`python ./sample_analysis/manage.py pca sample_type`

Variance, variance ratios, and component weightings for pca will be printed to stdout. The points of each sample in corresponding to the new dimensions is saved to the analysis_analysispca mysql table.

sample_type is either 'ki' or 'sn'

### Exporting Data

There are a number of scripts in `./sample_analysis/db_utils/export_commands` for exporting DB contents to a .csv file. They are currently hard-coded with the output file, so that will need to be editted for a new user.







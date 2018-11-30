python ./manage.py runanalysis equal_loudness
python ./manage.py runanalysis rms
echo "Normalizing RMS\n"
python ./manage.py normalizerms
python ./manage.py runanalysis temporal_centroid
python ./manage.py runanalysis spectral_centroid
python ./manage.py runanalysis spectral_centroid_1
python ./manage.py runanalysis spectral_centroid_2
python ./manage.py runanalysis spectral_kurtosis
python ./manage.py runanalysis pitch_salience
echo "Calculating sample durations\n"
python ./manage.py duration

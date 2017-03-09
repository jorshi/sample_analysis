
USE sample_analysis;

SELECT 'Drum Machine', 'Duration', 'Equal Loudness', 'RMS', 'Temporal Centroid', 'Spectral Centroid', 'Spectral Centroid 1', 'Spectral Centroid 2', 'Spectral Kurtosis', 'Pitch Salience'
UNION ALL
SELECT
    p.name, 
    AVG(a.duration), 
    AVG(a.equal_loudness), 
    AVG(a.rms), 
    AVG(a.temporal_centroid), 
    AVG(a.spectral_centroid), 
    AVG(a.spectral_centroid_1),
    AVG(a.spectral_centroid_2),
    AVG(a.spectral_kurtosis), 
    AVG(a.pitch_salience)
INTO OUTFILE '/Users/jshier/Development/School/jcura/sample_analysis/db_utils/output_sn_grp.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM analysis_analysis a 
    join analysis_sample s on a.sample_id=s.id 
    join analysis_kit k on s.kit_id=k.id 
    join analysis_samplepack p on k.sample_pack_id=p.id
WHERE
    s.sample_type = 'sn' AND s.exclude = 0 AND p.exclude = 0 AND a.outlier = 0
GROUP BY
    p.name;

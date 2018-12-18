
USE sample_analysis;

SELECT 'Index', 'Drum Machine', 'Type', 'Sample', 'Duration', 'Loudness', 'Equal Loudness', 'RMS', 'Temporal Centroid', 'Spectral Centroid', 'Spectral Kurtosis', 'Pitch Salience'
UNION ALL
SELECT
    s.id,
    p.name, 
    s.sample_type, 
    s.path,
    a.duration, 
    a.loudness, 
    a.equal_loudness, 
    a.rms, 
    a.temporal_centroid, 
    a.spectral_centroid, 
    a.spectral_kurtosis, 
    a.pitch_salience
INTO OUTFILE '/Users/jshier/Development/School/jcura/sample_analysis/db_utils/output.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM analysis_analysisz a 
    join analysis_sample s on a.sample_id=s.id 
    join analysis_kit k on s.kit_id=k.id 
    join analysis_samplepack p on k.sample_pack_id=p.id
WHERE
    s.exclude = 0 AND p.exclude = 0;
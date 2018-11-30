
USE sample_analysis;

SELECT 'Window Length', 'Window Start', 'Spectral Energy'
UNION ALL
SELECT
    a.window_length,
    a.window_start,
    a.spectral_energy
INTO OUTFILE '/Users/jshier/Development/School/jcura/sample_analysis/db_utils/ki_spectral_energy.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM analysis_analysisfull a 
    join analysis_sample s on a.sample_id=s.id 
WHERE
    s.sample_type = 'ki' AND s.exclude = 0;

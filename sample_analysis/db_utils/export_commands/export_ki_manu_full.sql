
USE sample_analysis;

SELECT
    s.id,
    p.name, 
    s.sample_type, 
    s.path,
    a.*

INTO OUTFILE '/Users/jshier/Development/School/jcura/sample_analysis/db_utils/output_ki_manu_full.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM analysis_analysisfull a 
    join analysis_sample s on a.sample_id=s.id 
    join analysis_kit k on s.kit_id=k.id 
    join analysis_samplepack p on k.sample_pack_id=p.id
WHERE
    s.sample_type = 'ki' AND s.exclude = 0 AND p.exclude = 0 AND p.id IN (146, 105, 149, 94, 46) AND a.window_length=250;

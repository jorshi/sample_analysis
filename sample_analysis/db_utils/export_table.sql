
USE sample_analysis;

SELECT p.name, s.sample_type, a.loudness, a.equal_loudness
INTO OUTFILE '/Users/jshier/Development/School/jcura/sample_analysis/db_utils/output.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM analysis_analysis a 
    join analysis_sample s on a.sample_id=s.id 
    join analysis_kit k on s.kit_id=k.id 
    join analysis_samplepack p on k.sample_pack_id=p.id;

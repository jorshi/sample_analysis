
USE sample_analysis;

SELECT 'Sample Id', 'Drum Machine', 'Dimension 1', 'Dimension 2', 'Dimension 3', 'Dimension 4'
UNION ALL
SELECT
    s.id,
    p.name, 
    a.dim_1,
    a.dim_2,
    a.dim_3,
    a.dim_4
INTO OUTFILE '/Users/jshier/Development/School/jcura/sample_analysis/db_utils/output_pca_ki.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM analysis_analysispca a 
    join analysis_sample s on a.sample_id=s.id 
    join analysis_kit k on s.kit_id=k.id 
    join analysis_samplepack p on k.sample_pack_id=p.id
WHERE
    s.sample_type = 'ki' AND s.exclude = 0 AND p.exclude = 0;

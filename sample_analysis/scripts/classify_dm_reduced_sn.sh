echo "Running Drum Machine Classification on Dimension Reduced Samples\n"

echo "pca: 25ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced pca sn 25  20
echo "pca: 100ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  100  20
echo "pca: 250ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  250  20
echo "pca: 500ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  500  20
echo "pca: 25ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  25  50
echo "pca: 100ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  100  50
echo "pca: 250ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  250  50
echo "pca: 500ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  500  50
echo "pca: 25ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  25  100
echo "pca: 100ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  100  100
echo "pca: 250ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  250  100
echo "pca: 500ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced pca  sn  500  100
echo "pca: full sample length\n"
python ./manage.py classifier_dm_reduced pca  sn  0  0
echo "pca: maximum variance windows\n"
python ./manage.py classifier_dm_reduced pca  sn  -1  -1

echo "tnse: 25ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne sn 25  20
echo "tsne: 100ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  100  20
echo "tsne: 250ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  250  20
echo "tsne: 500ms window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  500  20
echo "tsne: 25ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  25  50
echo "tsne: 100ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  100  50
echo "tsne: 250ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  250  50
echo "tsne: 500ms window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  500  50
echo "tsne: 25ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  25  100
echo "tsne: 100ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  100  100
echo "tsne: 250ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  250  100
echo "tsne: 500ms window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne  sn  500  100
echo "tsne: full sample length\n"
python ./manage.py classifier_dm_reduced tsne  sn  0  0
echo "tsne: maximum variance windows\n"
python ./manage.py classifier_dm_reduced tsne  sn  -1  -1

echo "tsne_pca: 25ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca sn 25  20
echo "tsne_pca: 100ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  100  20
echo "tsne_pca: 250ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  250  20
echo "tsne_pca: 500ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  500  20
echo "tsne_pca: 25ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  25  50
echo "tsne_pca: 100ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  100  50
echo "tsne_pca: 250ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  250  50
echo "tsne_pca: 500ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  500  50
echo "tsne_pca: 25ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  25  100
echo "tsne_pca: 100ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  100  100
echo "tsne_pca: 250ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  250  100
echo "tsne_pca: 500ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  500  100
echo "tsne_pca: Full Sample Length\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  0  0
echo "tsne_pca: Maximum Variance Windows\n"
python ./manage.py classifier_dm_reduced tsne_pca  sn  -1  -1

echo "isomap: 25ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced isomap sn 25  20
echo "isomap: 100ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  100  20
echo "isomap: 250ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  250  20
echo "isomap: 500ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  500  20
echo "isomap: 25ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  25  50
echo "isomap: 100ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  100  50
echo "isomap: 250ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  250  50
echo "isomap: 500ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  500  50
echo "isomap: 25ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  25  100
echo "isomap: 100ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  100  100
echo "isomap: 250ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  250  100
echo "isomap: 500ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced isomap  sn  500  100
echo "isomap: Full Sample Length\n"
python ./manage.py classifier_dm_reduced isomap  sn  0  0
echo "isomap: Maximum Variance Windows\n"
python ./manage.py classifier_dm_reduced isomap  sn  -1  -1

echo "locally_linear: 25ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear sn 25  20
echo "locally_linear: 100ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  100  20
echo "locally_linear: 250ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  250  20
echo "locally_linear: 500ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  500  20
echo "locally_linear: 25ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  25  50
echo "locally_linear: 100ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  100  50
echo "locally_linear: 250ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  250  50
echo "locally_linear: 500ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  500  50
echo "locally_linear: 25ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  25  100
echo "locally_linear: 100ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  100  100
echo "locally_linear: 250ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  250  100
echo "locally_linear: 500ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  500  100
echo "locally_linear: Full Sample Length\n"
python ./manage.py classifier_dm_reduced locally_linear  sn  0  0
echo "locally_linear: Maximum Variance Windows\n"
python ./manage.py classifier_dm_reduced locally_linear sn  -1  -1


echo "mds: 25ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced mds sn 25  20
echo "mds: 100ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  100  20
echo "mds: 250ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  250  20
echo "mds: 500ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  500  20
echo "mds: 25ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  25  50
echo "mds: 100ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  100  50
echo "mds: 250ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  250  50
echo "mds: 500ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  500  50
echo "mds: 25ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  25  100
echo "mds: 100ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  100  100
echo "mds: 250ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  250  100
echo "mds: 500ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced mds  sn  500  100
echo "mds: Full Sample Length\n"
python ./manage.py classifier_dm_reduced mds  sn  0  0
echo "mds: Maximum Variance Windows\n"
python ./manage.py classifier_dm_reduced mds  sn  -1 -1


echo "spectral: 25ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced spectral sn 25  20
echo "spectral: 100ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  100  20
echo "spectral: 250ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  250  20
echo "spectral: 500ms Window - 20% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  500  20
echo "spectral: 25ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  25  50
echo "spectral: 100ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  100  50
echo "spectral: 250ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  250  50
echo "spectral: 500ms Window - 50% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  500  50
echo "spectral: 25ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  25  100
echo "spectral: 100ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  100  100
echo "spectral: 250ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  250  100
echo "spectral: 500ms Window - 100% of attack\n"
python ./manage.py classifier_dm_reduced spectral  sn  500  100
echo "spectral: Full Sample Length\n"
python ./manage.py classifier_dm_reduced spectral  sn  0  0
echo "spectral: Maximum Variance Windows\n"
python ./manage.py classifier_dm_reduced spectral sn  -1  -1

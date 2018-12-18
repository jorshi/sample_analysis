echo "Running full Manifold Reduction on Snares\n"

echo "TNSE: 25ms Window - 20% of attack\n"
python ./manage.py manifold tsne sn 25  20
echo "TSNE: 100ms Window - 20% of attack\n"
python ./manage.py manifold tsne  sn  100  20
echo "TSNE: 250ms Window - 20% of attack\n"
python ./manage.py manifold tsne  sn  250  20
echo "TSNE: 500ms Window - 20% of attack\n"
python ./manage.py manifold tsne  sn  500  20
echo "TSNE: 25ms Window - 50% of attack\n"
python ./manage.py manifold tsne  sn  25  50
echo "TSNE: 100ms Window - 50% of attack\n"
python ./manage.py manifold tsne  sn  100  50
echo "TSNE: 250ms Window - 50% of attack\n"
python ./manage.py manifold tsne  sn  250  50
echo "TSNE: 500ms Window - 50% of attack\n"
python ./manage.py manifold tsne  sn  500  50
echo "TSNE: 25ms Window - 100% of attack\n"
python ./manage.py manifold tsne  sn  25  100
echo "TSNE: 100ms Window - 100% of attack\n"
python ./manage.py manifold tsne  sn  100  100
echo "TSNE: 250ms Window - 100% of attack\n"
python ./manage.py manifold tsne  sn  250  100
echo "TSNE: 500ms Window - 100% of attack\n"
python ./manage.py manifold tsne  sn  500  100
echo "TSNE: Full Sample Length\n"
python ./manage.py manifold tsne  sn  0  0
echo "TSNE: Maximum Variance Windows\n"
python ./manage.py manifold_window tsne  sn  25  20

echo "tsne_pca: 25ms Window - 20% of attack\n"
python ./manage.py manifold tsne_pca sn 25  20
echo "tsne_pca: 100ms Window - 20% of attack\n"
python ./manage.py manifold tsne_pca  sn  100  20
echo "tsne_pca: 250ms Window - 20% of attack\n"
python ./manage.py manifold tsne_pca  sn  250  20
echo "tsne_pca: 500ms Window - 20% of attack\n"
python ./manage.py manifold tsne_pca  sn  500  20
echo "tsne_pca: 25ms Window - 50% of attack\n"
python ./manage.py manifold tsne_pca  sn  25  50
echo "tsne_pca: 100ms Window - 50% of attack\n"
python ./manage.py manifold tsne_pca  sn  100  50
echo "tsne_pca: 250ms Window - 50% of attack\n"
python ./manage.py manifold tsne_pca  sn  250  50
echo "tsne_pca: 500ms Window - 50% of attack\n"
python ./manage.py manifold tsne_pca  sn  500  50
echo "tsne_pca: 25ms Window - 100% of attack\n"
python ./manage.py manifold tsne_pca  sn  25  100
echo "tsne_pca: 100ms Window - 100% of attack\n"
python ./manage.py manifold tsne_pca  sn  100  100
echo "tsne_pca: 250ms Window - 100% of attack\n"
python ./manage.py manifold tsne_pca  sn  250  100
echo "tsne_pca: 500ms Window - 100% of attack\n"
python ./manage.py manifold tsne_pca  sn  500  100
echo "tsne_pca: Full Sample Length\n"
python ./manage.py manifold tsne_pca  sn  0  0
echo "tsne_pca: Maximum Variance Windows\n"
python ./manage.py manifold_window tsne_pca  sn  25  20

echo "isomap: 25ms Window - 20% of attack\n"
python ./manage.py manifold isomap sn 25  20
echo "isomap: 100ms Window - 20% of attack\n"
python ./manage.py manifold isomap  sn  100  20
echo "isomap: 250ms Window - 20% of attack\n"
python ./manage.py manifold isomap  sn  250  20
echo "isomap: 500ms Window - 20% of attack\n"
python ./manage.py manifold isomap  sn  500  20
echo "isomap: 25ms Window - 50% of attack\n"
python ./manage.py manifold isomap  sn  25  50
echo "isomap: 100ms Window - 50% of attack\n"
python ./manage.py manifold isomap  sn  100  50
echo "isomap: 250ms Window - 50% of attack\n"
python ./manage.py manifold isomap  sn  250  50
echo "isomap: 500ms Window - 50% of attack\n"
python ./manage.py manifold isomap  sn  500  50
echo "isomap: 25ms Window - 100% of attack\n"
python ./manage.py manifold isomap  sn  25  100
echo "isomap: 100ms Window - 100% of attack\n"
python ./manage.py manifold isomap  sn  100  100
echo "isomap: 250ms Window - 100% of attack\n"
python ./manage.py manifold isomap  sn  250  100
echo "isomap: 500ms Window - 100% of attack\n"
python ./manage.py manifold isomap  sn  500  100
echo "isomap: Full Sample Length\n"
python ./manage.py manifold isomap  sn  0  0
echo "isomap: Maximum Variance Windows\n"
python ./manage.py manifold_window isomap  sn  25  20

echo "locally_linear: 25ms Window - 20% of attack\n"
python ./manage.py manifold locally_linear sn 25  20
echo "locally_linear: 100ms Window - 20% of attack\n"
python ./manage.py manifold locally_linear  sn  100  20
echo "locally_linear: 250ms Window - 20% of attack\n"
python ./manage.py manifold locally_linear  sn  250  20
echo "locally_linear: 500ms Window - 20% of attack\n"
python ./manage.py manifold locally_linear  sn  500  20
echo "locally_linear: 25ms Window - 50% of attack\n"
python ./manage.py manifold locally_linear  sn  25  50
echo "locally_linear: 100ms Window - 50% of attack\n"
python ./manage.py manifold locally_linear  sn  100  50
echo "locally_linear: 250ms Window - 50% of attack\n"
python ./manage.py manifold locally_linear  sn  250  50
echo "locally_linear: 500ms Window - 50% of attack\n"
python ./manage.py manifold locally_linear  sn  500  50
echo "locally_linear: 25ms Window - 100% of attack\n"
python ./manage.py manifold locally_linear  sn  25  100
echo "locally_linear: 100ms Window - 100% of attack\n"
python ./manage.py manifold locally_linear  sn  100  100
echo "locally_linear: 250ms Window - 100% of attack\n"
python ./manage.py manifold locally_linear  sn  250  100
echo "locally_linear: 500ms Window - 100% of attack\n"
python ./manage.py manifold locally_linear  sn  500  100
echo "locally_linear: Full Sample Length\n"
python ./manage.py manifold locally_linear  sn  0  0
echo "locally_linear: Maximum Variance Windows\n"
python ./manage.py manifold_window locally_linear sn  25  20


echo "mds: 25ms Window - 20% of attack\n"
python ./manage.py manifold mds sn 25  20
echo "mds: 100ms Window - 20% of attack\n"
python ./manage.py manifold mds  sn  100  20
echo "mds: 250ms Window - 20% of attack\n"
python ./manage.py manifold mds  sn  250  20
echo "mds: 500ms Window - 20% of attack\n"
python ./manage.py manifold mds  sn  500  20
echo "mds: 25ms Window - 50% of attack\n"
python ./manage.py manifold mds  sn  25  50
echo "mds: 100ms Window - 50% of attack\n"
python ./manage.py manifold mds  sn  100  50
echo "mds: 250ms Window - 50% of attack\n"
python ./manage.py manifold mds  sn  250  50
echo "mds: 500ms Window - 50% of attack\n"
python ./manage.py manifold mds  sn  500  50
echo "mds: 25ms Window - 100% of attack\n"
python ./manage.py manifold mds  sn  25  100
echo "mds: 100ms Window - 100% of attack\n"
python ./manage.py manifold mds  sn  100  100
echo "mds: 250ms Window - 100% of attack\n"
python ./manage.py manifold mds  sn  250  100
echo "mds: 500ms Window - 100% of attack\n"
python ./manage.py manifold mds  sn  500  100
echo "mds: Full Sample Length\n"
python ./manage.py manifold mds  sn  0  0
echo "mds: Maximum Variance Windows\n"
python ./manage.py manifold_window mds  sn  25  20


echo "spectral: 25ms Window - 20% of attack\n"
python ./manage.py manifold spectral sn 25  20
echo "spectral: 100ms Window - 20% of attack\n"
python ./manage.py manifold spectral  sn  100  20
echo "spectral: 250ms Window - 20% of attack\n"
python ./manage.py manifold spectral  sn  250  20
echo "spectral: 500ms Window - 20% of attack\n"
python ./manage.py manifold spectral  sn  500  20
echo "spectral: 25ms Window - 50% of attack\n"
python ./manage.py manifold spectral  sn  25  50
echo "spectral: 100ms Window - 50% of attack\n"
python ./manage.py manifold spectral  sn  100  50
echo "spectral: 250ms Window - 50% of attack\n"
python ./manage.py manifold spectral  sn  250  50
echo "spectral: 500ms Window - 50% of attack\n"
python ./manage.py manifold spectral  sn  500  50
echo "spectral: 25ms Window - 100% of attack\n"
python ./manage.py manifold spectral  sn  25  100
echo "spectral: 100ms Window - 100% of attack\n"
python ./manage.py manifold spectral  sn  100  100
echo "spectral: 250ms Window - 100% of attack\n"
python ./manage.py manifold spectral  sn  250  100
echo "spectral: 500ms Window - 100% of attack\n"
python ./manage.py manifold spectral  sn  500  100
echo "spectral: Full Sample Length\n"
python ./manage.py manifold spectral  sn  0  0
echo "spectral: Maximum Variance Windows\n"
python ./manage.py manifold_window spectral sn  25  20

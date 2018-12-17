echo "Running Full Drum Machine Classification for Kicks\n"
echo "25ms Window - 20% of attack\n"
python ./manage.py classifier_dm ki  25  20
echo "100ms Window - 20% of attack\n"
python ./manage.py classifier_dm ki  100  20
echo "250ms Window - 20% of attack\n"
python ./manage.py classifier_dm ki  250  20
echo "500ms Window - 20% of attack\n"
python ./manage.py classifier_dm ki  500  20
echo "25ms Window - 50% of attack\n"
python ./manage.py classifier_dm ki  25  50
echo "100ms Window - 50% of attack\n"
python ./manage.py classifier_dm ki  100  50
echo "250ms Window - 50% of attack\n"
python ./manage.py classifier_dm ki  250  50
echo "500ms Window - 50% of attack\n"
python ./manage.py classifier_dm ki  500  50
echo "25ms Window - 100% of attack\n"
python ./manage.py classifier_dm ki  25  100
echo "100ms Window - 100% of attack\n"
python ./manage.py classifier_dm ki  100  100
echo "250ms Window - 100% of attack\n"
python ./manage.py classifier_dm ki  250  100
echo "500ms Window - 100% of attack\n"
python ./manage.py classifier_dm ki  500  100
echo "Full Sample Length\n"
python ./manage.py classifier_dm ki 0 0
echo "Maximum Variance Sample Window\n"
python ./manage.py classifier_dm_window ki 25 20


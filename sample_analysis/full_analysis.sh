echo "Running full analsis\n"
echo "25ms Window - 20% of attack\n"
python ./manage.py run_analysis_full --window_length 25 --window_start 20
echo "100ms Window - 20% of attack\n"
python ./manage.py run_analysis_full --window_length 100 --window_start 20
echo "25oms Window - 20% of attack\n"
python ./manage.py run_analysis_full --window_length 250 --window_start 20
echo "500ms Window - 20% of attack\n"
python ./manage.py run_analysis_full --window_length 500 --window_start 20
echo "25ms Window - 50% of attack\n"
python ./manage.py run_analysis_full --window_length 25 --window_start 50
echo "100ms Window - 50% of attack\n"
python ./manage.py run_analysis_full --window_length 100 --window_start 50
echo "250ms Window - 50% of attack\n"
python ./manage.py run_analysis_full --window_length 250 --window_start 50
echo "500ms Window - 50% of attack\n"
python ./manage.py run_analysis_full --window_length 500 --window_start 50
echo "25ms Window - 100% of attack\n"
python ./manage.py run_analysis_full --window_length 25 --window_start 100
echo "100ms Window - 100% of attack\n"
python ./manage.py run_analysis_full --window_length 100 --window_start 100
echo "250ms Window - 100% of attack\n"
python ./manage.py run_analysis_full --window_length 250 --window_start 100
echo "500ms Window - 100% of attack\n"
python ./manage.py run_analysis_full --window_length 500 --window_start 100
echo "Full Sample Length\n"
python ./manage.py run_analysis_full


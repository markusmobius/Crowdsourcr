cd src
start cmd /k python app.py --port=8101 --environment=production --db_name=news_crowdsourcing_a --make_payments=True
timeout /t 1
start cmd /k python app.py --port=8102 --environment=production --db_name=news_crowdsourcing_a --make_payments=False

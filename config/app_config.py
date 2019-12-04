superadmins = []

google = {}

port = 8080
db_name="news_crowdsourcing"
make_payments = True

aws={}

def populate_config(filename):
    global superadmins
    global google
    global port
    global db_name
    global make_payments
    global aws

    import json
    with open("../config/"+filename) as json_file: 
        data = json.load(json_file)
        superadmins=data["superadmins"]
        google=data["google"]
        port=data["port"]
        db_name=data["db_name"]
        make_payments=data["make_payments"]
        aws=data["aws"]
       
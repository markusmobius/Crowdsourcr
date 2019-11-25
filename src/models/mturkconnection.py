import os
import boto3
import xmltodict
import json
import datetime

#QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer

class MTurkConnection(object):
    def __init__(self, 
                 access_key=None, 
                 secret_key=None, 
                 email=None, 
                 hitpayment="0.01", 
                 running=False, 
                 hitid=None, 
                 title="News Classification Task", 
                 description="Classify a set of news articles as part of an academic research study.",
                 keywords="news, classification, research, academic",
                 environment="development",
                 bonus=0.0,
                 **kwargs):
        self.title = title
        self.description = description
        self.keywords = keywords
        self.access_key = access_key
        self.secret_key = secret_key
        self.email = email
        self.running = running
        self.hitpayment = hitpayment
        self.host = 'mechanicalturk.amazonaws.com' if environment == 'production' else 'mechanicalturk.sandbox.amazonaws.com'
        self.admin_host = 'https://requester.mturk.com' if environment == 'production' else 'https://requestersandbox.mturk.com'
        self.bonus = float(bonus)
        environments = {
            "production": {
                "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
                "preview": "https://www.mturk.com/mturk/preview",
                "manage": "https://requester.mturk.com/mturk/manageHITs"
            },
            "sandbox": {
                "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                "preview": "https://workersandbox.mturk.com/mturk/preview",
                "manage": "https://requestersandbox.mturk.com/mturk/manageHITs"
            },
        }
        self.mturk_environment = environments["production"] if environment == 'production' else environments["sandbox"]
        self.client = boto3.client('mturk',
            endpoint_url = self.mturk_environment['endpoint'], 
            region_name = 'us-east-1', 
            aws_access_key_id = self.access_key, 
            aws_secret_access_key = self.secret_key)
        self.hit_id = hitid

    def try_auth(self):
        return True if self.get_balance() else False

    def get_balance(self):
        try:
            balance = self.client.get_account_balance()['AvailableBalance']
            print("Account balance: %s" % (balance))
            #print("Account balance: %d" % (balance['AvailableBalance']))
            return balance
        except:
            print("Problem getting account balance")
            return None

    def get_all_hits(self):
        return [hit['HITId'] for hit in self.client.list_hits()['HITs']]
    
    def serialize(self):
        return { 'access_key' : self.access_key,
                 'secret_key' : self.secret_key,
                 'email' : self.email,
                 'running' : self.running,
                 'admin_host': self.admin_host,
                 'hitpayment' : self.hitpayment,
                 'hitid' : self.hit_id,
                 'title' : self.title,
                 'description' : self.description,
                 'keywords' : self.keywords,
                 'bonus' : self.bonus}
    @classmethod
    def deserialize(cls, d):
        return MTurkConnection(**d)

    def begin_run(self, max_assignments=1, url="https://www.google.com"):
        question_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
          <ExternalURL>QUESTION_URL</ExternalURL>
          <FrameHeight>0</FrameHeight>
        </ExternalQuestion>
        """
        hitinfo = self.client.create_hit(
            MaxAssignments=max_assignments,
            Title=self.title,
            Description=self.description,
            LifetimeInSeconds=14400,
            AssignmentDurationInSeconds=60 * 60 * 2,
            Keywords=self.keywords,
            Reward=self.hitpayment,
            QualificationRequirements=[{
                    'QualificationTypeId': '00000000000000000071',
                    'Comparator': 'EqualTo',
                    'LocaleValues': [{
                            'Country': 'US',
                    }]
            }],
            Question = question_xml.replace("QUESTION_URL", url)
            # Question='<p>'+self.description+' To begin, navigate to the following url: <a href="'+url+'">%('+url+')s</a>.</p>'
        )

        self.hit_type_id = hitinfo['HIT']['HITTypeId']
        self.hit_id = hitinfo['HIT']['HITId']
        print("\nCreated HIT: %s" % self.hit_id)
        print("You can view the HIT here: ")
        print(self.mturk_environment['preview'] + "?groupId={}".format(self.hit_type_id))
        print("And manage the results here: ")
        print(self.mturk_environment['manage'])

        # qc1 = boto.mturk.question.QuestionContent()
        # qc1.append_field('Title','Secret Code')
        # qc1.append_field('Text', 'Enter the 16 character secret code that you will receive after you complete this task.')
        # fta1 = boto.mturk.question.FreeTextAnswer()
        # q1 = boto.mturk.question.Question(identifier='secretcode',
        #                                   content=qc1,
        #                                   answer_spec=boto.mturk.question.AnswerSpecification(fta1),
        #                                   is_required=True)

        self.running = True
        return True

    def end_run(self, bonus={}, already_paid=[], hit_id = None):
        if not self.hit_id or not self.running:
            return []
        if hit_id is None:
            hit_id = self.hit_id 
        paid_bonus = []
        try:
            worker_assignments = {}
            next_token=None
            while True:
                if next_token is None:
                    response = self.client.list_assignments_for_hit(HITId = hit_id, MaxResults = 100)
                else:
                    response = self.client.list_assignments_for_hit(HITId=hit_id, NextToken = next_token, MaxResults=100)

                for a in response['Assignments'] :
                    if a['WorkerId'] not in already_paid :
                        worker_assignments[a['WorkerId']] = a['AssignmentId']

                if 'NextToken' in response.keys():
                    next_token = response['NextToken']
                else:
                    break
                
            for workerid, assignmentid in worker_assignments.iteritems() :
                if workerid not in bonus :
                    print "Error in end_run: worker_id %s present on mturk but not in bonus dict." % workerid
                else :
                    bonus_amt = min(10, max(0.05, round(bonus[workerid] * self.bonus, 2)))
                    self.client.send_bonus(WorkerId=workerid,
                                           BonusAmount=str(bonus_amt),
                                           AssignmentId=assignmentid,
                                           Reason='Bonus for completion of task.')
                    paid_bonus.append({'workerid' : workerid,
                                       'percent' : bonus[workerid],
                                       'amount' : bonus_amt,
                                       'assignmentid' : assignmentid})
            try:
                self.client.delete_hit(HITId=hit_id)
                print("Deleted hit: ", hit_id)
            except:
                self.client.update_expiration_for_hit(HITId = hit_id, ExpireAt = datetime.datetime(2019, 1, 1))
                print("Expired hit: ", hit_id)
        except:
            print "Error caught when trying to end run."
            raise
        self.running = False
        return paid_bonus

    def get_payments_to_make(self):
        if not self.hit_id or not self.running:
            return []
        else:
            all_assignments = []
            next_token = None 
            while True :
                try:
                    if next_token is None:
                        response = self.client.list_assignments_for_hit(HITId = self.hit_id, MaxResults = 100)
                    else:
                        response = self.client.list_assignments_for_hit(HITId=self.hit_id, NextToken = next_token, MaxResults=100)
        
                    all_assignments = [[a['AssignmentId'], a['WorkerId'], a['Answer']] for a in response['Assignments'] if a['AssignmentStatus'] == 'Submitted']
                    if 'NextToken' in response.keys():
                        next_token = response['NextToken']
                    else:
                        break
                except:
                    raise 
            
            return all_assignments

    def make_payments(self, assignment_ids=[]) :
        for assignmentid in assignment_ids:
            try:
                self.client.approve_assignment(AssignmentId=assignmentid)
            except:
                continue


if __name__=='__main__':
    mturk = MTurkConnection(access_key="KEYHERE", secret_key="SECRETHERE")
    mturk.try_auth()
    mturk.begin_run()
    print("Payments to make: ", mturk.get_payments_to_make())
    mturk.end_run()

    hits = mturk.client.list_hits()['HITs']
    if True:
        for hit in hits:
            hitid = hit['HITId']
            title = hit['Title']
            creation_date = hit['CreationTime']
            status = hit['HITStatus']
            print(hitid, title, creation_date, status)

            if status == "Reviewable":
                print("Deleting hit.", hitid)
                mturk.client.delete_hit(HITId = hitid)
            else:
                try:
                    mturk.client.update_expiration_for_hit(HITId = hitid, ExpireAt = datetime.datetime(2015, 1, 1))
                    mturk.client.delete_hit(HITId = hitid)
                    print("Expiring and deleting hit.", hitid)
                except:
                    print("Could not expire and delete hit ", hitid)

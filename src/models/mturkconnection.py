import os
import boto.mturk.connection

class MTurkConnection(object):
    def __init__(self, access_key=None, secret_key=None, email=None, hitpayment=1.0, running=False):
        self.access_key = access_key
        self.secret_key = secret_key
        self.email = email
        self.running = running
        self.hitpayment = hitpayment
        self.mturk_conn = boto.mturk.connection.MTurkConnection(self.access_key,
                                                                self.secret_key)
    def try_auth(self, access_key=None, secret_key=None):
        return True if self.get_balance else False

    def get_balance(self):
        try:
            return self.mturk_conn.get_account_balance()
        except:
            return None

    def get_all_hits(self):
        return [hit.HITId for hit in self.mturk_conn.get_all_hits()]
    
    def serialize(self):
        return { 'access_key' : self.access_key,
                 'secret_key' : self.secret_key,
                 'email' : self.email,
                 'running' : self.running,
                 'hitpayment' : self.hitpayment }
    @classmethod
    def deserialize(cls, d):
        return MTurkConnection(access_key=d['access_key'],
                               secret_key=d['secret_key'],
                               email=d['email'],
                               hitpayment=d['hitpayment'],
                               running=d['running'])
    def begin_run(self, max_assignments):
        self.mturk_conn.create_hit(questions=open(os.path.join(os.path.dirname(__file__), 'question_form.xml'), 'r').read(),
                                   title="News article classification.", 
                                   description="Classify a set of news articles as part of an academic research study.", 
                                   keywords="news classification research academic", 
                                   reward="<Reward><Amount>%f</Amount><CurrencyCode>USD</CurrencyCode></Reward>" % self.hitpayment,
                                   max_assignments=max_assignments)
        return True

            

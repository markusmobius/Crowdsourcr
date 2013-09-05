import models

class XMLTaskController(object):
    def __init__(self, db):
        self.db = db
    def xml_upload(self, xml_path=None) :
        self.db.ctasks.drop()
        self.db.ctypes.drop()
        self.db.cresponses.drop()
        self.db.chits.drop()
        self.db.cdocs.drop()
        self.db.chitloads.drop()
        self.db.currentstatus.drop()
        self.db.workerpings.drop()
        return models.XMLTask(xml_path)

"""
        for module in xmltask.get_modules():
            CTypeController.create(module)
        all_tasks = xmltask.get_tasks()
        all_hits = xmltask.get_hits()
        all_modules = xmltask.get_modules()
        print all_tasks
        print all_hits
        print all_modules
        for task in all_tasks:
            print task
        for hit in all_hits:
            print hit
        for module in all_modules:
            print module

"""

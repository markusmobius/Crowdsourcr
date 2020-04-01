import pycountry

class CountryTools:
    def check(self,code):
        if len(code)==2:               
            if pycountry.countries.get(alpha_2=code):
                return True
            else:
                return False
        else:
            if pycountry.subdivisions.get(code=code):
                return True
            else:
                return False

    def checkList(self,codeList):
        frags=codeList.split(',')
        for f in frags:
            if not self.check(f.strip()):
                return False
        return True

    def createLocales(self,codeList):
        locales=[]
        frags=codeList.split(',')
        for f in frags:
            f=f.strip()
            if self.check(f):
                ff=f.split('-')
                if len(ff)==2:
                    locales.append({"Country":ff[0],"Subdivision":ff[1]})
                else:
                    locales.append({"Country":ff[0]})
        return locales

            

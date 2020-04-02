import pycountry

class CountryTools:
    def check(self,code):
        if len(code)==2:               
            if pycountry.countries.get(alpha_2=code):
                return None
            else:
                return "Country code "+code+" is not a valid ISO 3166 code."
        else:
            if pycountry.subdivisions.get(code=code):
                return None
            else:
                return "Country/subdivision code "+code+ " is not a valid ISO 3166 country/subdivision code."

    def checkList(self,codeList):
        frags=codeList.split(',')
        for f in frags:
            error=self.check(f.strip())
            if error!=None:
                return error
        return None

    def createLocales(self,codeList):
        locales=[]
        frags=codeList.split(',')
        for f in frags:
            f=f.strip()
            if self.check(f)==None:
                ff=f.split('-')
                if len(ff)==2:
                    locales.append({"Country":ff[0],"Subdivision":ff[1]})
                else:
                    locales.append({"Country":ff[0]})
        return locales

            

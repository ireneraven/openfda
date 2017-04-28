
#The MIT License (MIT)

#Copyright (c) 2017 Irene Raven Garcia

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

# LIBRERIAS
import http.server
import http.client
import json

# CLASE
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'

    def get_event(self, limite):
        # GET EVENT
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit=' + limite)
        r1 = conn.getresponse() #almacena la respuesta
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_drugs_from_events(self, events):

        medicamentos = []
        results = events['results']
        for event in results:
            medicamentos += [event['patient']['drug'][0]['medicinalproduct']]
        return medicamentos

    def get_incognita(self):

        incognita = self.path.split('=')[1]
        return incognita

    def get_events_search(self):

        incognita = self.get_incognita()
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+incognita+'&limit=10')
        r1 = conn.getresponse() #almacena la respuesta
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_empresas(self):

        events= self.get_events_search()
        empresas = []
        results = events['results']
        for event in results:
            empresas += [event['companynumb']]
        return empresas

    def get_companies_from_events(self,events):

        companies = []
        results = events['results']
        for event in results:
            companies += [event["companynumb"]]
        return companies

    def get_incognita2(self):

        incognita = self.path.split('=')[1]
        return incognita

    def get_events_search_companies(self):

        incognita = self.get_incognita2()
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=companynumb:'+incognita+'&limit=10')
        r1 = conn.getresponse() #almacena la respuesta
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_drugs(self):
        events= self.get_events_search_companies()
        companies = []
        results = events['results']
        for event in results:
            companies += [event["patient"]["drug"][0]["medicinalproduct"]]
        return companies

    def get_limit(self):
        limite=self.path.split('=')[1]
        if limite == "":
            limite=10
        limite = str(limite)
        return limite

    def get_gender_list(self,events):
        gender = []
        for event in events:
            gender += [event["patient"]["patientsex"]]
        return gender
        """
        print(len(events))
        for event in events:
            try:
                print (event["patient"])
                gender += [event["patient"]["patientsex"]]
            except:
                print("EXCEPCIONNNNN")
                print(event)
        return gender
"""
    def get_main_page(self):
        # get main page
        html = """
        <html>
            <head>
            </head>
            <body>

                <form method="get" action="listDrugs">
                    </input>
                    <input type = "submit" value="Drug List: Send to OpenFDA">
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>

                <form method="get" action="searchDrug">
                    </input>
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Drug Search LYRICA: Send to OpenFDA">
                </form>

                <form method="get" action="listCompanies">
                    </input>
                    <input type = "submit" value="Companie List: Send to OpenFDA">
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>

                <form method="get" action="searchCompany">
                    </input>
                    <input type = "text" name = "Company"></input>
                    <input type = "submit" value="Company Search: Send to OpenFDA">
                </form>

                <form method="get" action = "listGender">
                    </input>
                    <input type = "text" name = "Gender"></input>
                    <input type = "submit" value="Gender list">
                </form>

            </body>
        </html>
        """
        return html

    def get_list_drugs(self, medicamentos):

        s = ''
        for med in medicamentos:
            s += '<li>' +med+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Medicinal Product</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_list_companies(self, companies):
        s = ''
        for comp in companies:
            s += '<li>' +comp+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Companies</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html


    def do_GET(self):
        # GET



        code = 200



        # Write content as utf-8 data
        if self.path== "/":
            html2 = self.get_main_page()

        elif 'listDrugs' in self.path:
            limite=self.get_limit()
            events = self.get_event(limite)
            medicamentos = self.get_drugs_from_events(events)
            event = self.get_event(limite)
            html2 = self.get_list_drugs(medicamentos)

        elif 'searchDrug' in self.path:
            empresas = self.get_empresas()
            html2 = self.get_list_drugs(empresas)


        elif 'listCompanies' in self.path:
            limite=self.get_limit()
            event = self.get_event(limite)
            companies = self.get_companies_from_events(event)
            html2 = self.get_list_companies(companies)

        elif 'searchCompany' in self.path:
            drugs = self.get_drugs()
            html2 = self.get_list_companies(drugs)


        elif 'listGender' in self.path:
            limite=self.get_limit()
            events = self.get_event(limite)
            results = events['results']
            gender= self.get_gender_list(results)
            html2 = self.get_list_companies(gender)

        elif '/secret' in self.path: #para que te pida nombre y usuario
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm= "My realm"')
            self.end_headers()

        elif '/redirect' in self.path: #para que se te vuelva a cargar la pagina
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()




        else:
            code = 404
            html2 = """
            404
            """

        self.send_response(code)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if not '/redirect' in self.path and not '/secret' in self.path:

            self.wfile.write(bytes(html2, "utf8"))




        return

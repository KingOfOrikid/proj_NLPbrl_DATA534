import requests

class Data():
    def __init__(self):
        #key1 "ad9765417caa9e2fd304e0aea0e2d24f"
        #key2 "4ccf98ac9854f73e845a16a9e300daeb"
        self.headers = {
            "content-type": "application/json",
            "X-RosetteAPI-Key": "4ccf98ac9854f73e845a16a9e300daeb",
            "X-RapidAPI-Key":
            "bc44666f27msh0cea06e275c5146p185e39jsnb306b7888971",
            "X-RapidAPI-Host": "rosetteapi-rosette-v1.p.rapidapi.com"
        }
        self.payload = {}

    def get_token(self, text):
        self.payload = {}
        url = "https://rosetteapi-rosette-v1.p.rapidapi.com/tokens"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)['tokens']

    def get_lang(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/language"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)["languageDetections"][0]['language']

    def get_vec(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/semantics/vector"
        self.payload['content'] = text
        self.payload['options'] = {"perToken": True}
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return {
            'documentEmbedding': eval(response.text)['documentEmbedding'],
            'tokenEmbeddings': eval(response.text)['tokenEmbeddings']
        }

    def get_posTag(self, text):
        self.payload = {}
        null = ''
        url = "https://rosetteapi-rosette-v1.p.rapidapi.com/morphology/complete"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)

        return {
            "tokens": eval(response.text)["tokens"],
            "posTags": eval(response.text)["posTags"]
        }

    def get_senTag(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/sentences"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)['sentences']
    
    def get_relation(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/relationships"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)['relationships']

    def get_classification(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/categories"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)["categories"]
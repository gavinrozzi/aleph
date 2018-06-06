import pandas as pd
import ahocorasick
import string



class geo_Extract(object):

    def __init__(self, geo_corpus_path):
        # download geonames at http://download.geonames.org/export/dump/allCountries.zip and unzip before import

        # will cut down the geonames import corpus to essentials for implementation
        all_geonames_cols = ['geonameid',
            'name',
            'asciiname',
            'alternatenames',
            'latitude',
            'longitude',
            'feature class',
            'feature code',
            'country code',
            'cc2',
            'admin1 code',
            'admin2 code',
            'admin3 code',
            'admin4 code',
            'population',
            'elevation',
            'dem',
            'timezone',
            'modification date']

        all_geonames = pd.read_csv(geo_corpus_path,delimiter='\t',
                            encoding='utf8', header = None)
        all_geonames.columns = all_geonames_cols

        countries = all_countries.loc[(all_countries['feature code'] == 'PCLI')].reset_index()[['country code','asciiname']].values.tolist()
        alt_countries = all_countries.loc[(all_countries['feature code'] == 'PCLI')].reset_index()[['country code','alternatenames']].values.tolist()

        adm_areas = all_countries.loc[(all_countries['feature code'] == 'ADM1')].reset_index()[['country code','asciiname']].values.tolist()
        alt_adm_areas = all_countries.loc[(all_countries['feature code'] == 'ADM1')].reset_index()[['country code','alternatenames']].values.tolist()

        self.country_automaton = ahocorasick.Automaton()
        strip_punc = str.maketrans('', '', string.punctuation)

        for n in countries:
            self.country_automaton.add_word(str(n[1]), (str(n[0]),str(n[1])))

        for n_alt in alt_countries:
            for alt in str.split(n_alt[1],','):
                self.country_automaton.add_word(str(alt), (str(n_alt[0]),str(alt)))


        for n in adm_areas:
            self.country_automaton.add_word(str(n[1]), (str(n[0]),str(n[1])))

        for n_alt in alt_adm_areas:
            for alt in str.split(str(n_alt[1]),','):
                self.country_automaton.add_word(str(alt), (str(n_alt[0]),str(alt)))

        self.country_automaton.make_automaton()


    def clean_str(self, s):
        strip_punct = str.maketrans('', '', string.punctuation)
#         return s.translate(strip_punct).lower()
        return s.translate(strip_punct)


    def ngrams(self, doc_in, n):
        doc_in = doc_in.split(' ')
        output = []
        for i in range(len(input)-n+1):
            output.append(' '.join(input[i:i+n]))
        return output


    def extract(self, doc):
        strings = []
        indeces = []
        values = []
        for s in str.split(doc,' '):
            for index, value in self.country_automaton.iter(s):
                if self.clean_str(s) == self.clean_str(str(value[1])):
                    strings.append(s)
                    indeces.append(index)
                    values.append(value)

        # look for matches over a certain range of n-grams within the doc
        for i in range(2,7):
            doc_ngram = ngrams(doc, i)

            for s_n in doc_ngram:
                for index, value in self.country_automaton.iter(s_n):
                    if self.clean_str(s_n) == self.clean_str(str(value[1])):
                        strings.append(s_n)
                        indeces.append(index)
                        values.append(value)


        return strings, indeces, values

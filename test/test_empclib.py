import unittest
from .. epmclib.getPMCID import getPMCID
from .. epmclib.getPMID import getPMID
from .. epmclib.exceptions import *


class EPMClibTester(unittest.TestCase):

    def test_getpmcid_resolves(self):
        pmcid = getPMCID('PMC288264')
        result = pmcid.resolves()
        self.assertEqual(True, result)

    def test_getpmcid_does_not_resolve(self):
        pmcid = getPMCID('PMC2882643532')
        result = pmcid.resolves()
        self.assertEqual(False, result)

    def test_get_pmcid_lite_data(self):
        pmcid = getPMCID('PMC288264')
        pmcid.liteQuery()
        result = pmcid.rawresults
        idealresult = {'resultList': {'result': [
            {'hasReferences': 'Y', 'pageInfo': '1243-1252',
             'isOpenAccess': 'N', 'journalTitle': 'J Clin Invest', 'citedByCount': 114,
             'authorString': 'Miyata T, Oda O, Inagi R, Iida Y, Araki N, Yamada N, Horiuchi S, Taniguchi N,'
                             ' Maeda K, Kinoshita T.',
             'issue': '3', 'pubYear': '1993',
             'title': 'beta 2-Microglobulin modified with advanced glycation end products is a major component of hemod'
                      'ialysis-associated amyloidosis.',
             'inEPMC': 'Y', 'pmcid': 'PMC288264', 'doi': '10.1172/jci116696',
             'hasLabsLinks': 'Y', 'pubType': 'journal article; research-article',
             'source': 'MED', 'id': '8376584', 'journalVolume': '92', 'journalIssn': '0021-9738',
             'hasTextMinedTerms': 'Y', 'pmid': '8376584', 'inPMC': 'N', 'hasPDF': 'Y', 'hasDbCrossReferences': 'N',
             'hasBook': 'N', 'luceneScore': 'NaN', 'hasTMAccessionNumbers': 'N'}]},
            'request': {'resultType': 'lite', 'pageSize': 25, 'query': 'PMCID:PMC288264', 'synonym': False, 'page': 1},
            'version': '4.4.0', 'hitCount': 1}

        self.assertEqual(idealresult, result)

    def test_get_pmcid_core_data(self):
        pmcid = getPMCID('PMC288264')
        pmcid.coreQuery()
        result = pmcid.rawresults
        idealresult = {'resultList': {'result':
                                          [{'id': '8376584',
                                            'title': 'beta 2-Microglobulin modified with advanced glycation end product'
                                                     's is a major component of hemodialysis-associated amyloidosis.',
                                            'issue': '3', 'hasReferences': 'Y', 'hasBook': 'N', 'pubYear': '1993',
                                            'isOpenAccess': 'N', 'source': 'MED', 'citedByCount': 114,
                                            'pageInfo': '1243-1252', 'doi': '10.1172/jci116696',
                                            'journalTitle': 'J Clin Invest', 'hasPDF': 'Y', 'hasTextMinedTerms': 'Y',
                                            'hasDbCrossReferences': 'N', 'journalVolume': '92',
                                            'journalIssn': '0021-9738', 'luceneScore': 'NaN',
                                            'hasTMAccessionNumbers': 'N',
                                            'authorString': 'Miyata T, Oda O, Inagi R, Iida Y, Araki N, Yamada N,'
                                                            ' Horiuchi S, Taniguchi N, Maeda K, Kinoshita T.',
                                            'inEPMC': 'Y', 'inPMC': 'N', 'pmcid': 'PMC288264',
                                            'pubType': 'journal article; research-article', 'pmid': '8376584',
                                            'hasLabsLinks': 'Y'}]},
                       'request': {'resultType': 'lite', 'page': 1, 'synonym': False, 'query': 'PMCID:PMC288264',
                                   'pageSize': 25}, 'hitCount': 1, 'version': '4.4.0'}
        print(result)
        self.assertEqual(idealresult, result)

    def test_get_pmcid_title_only(self):
        pmcid = getPMCID('PMC288264')
        pmcid.getTitle()
        result = pmcid.title
        self.assertEquals('beta 2-Microglobulin modified with advanced glycation end product'
                          's is a major component of hemodialysis-associated amyloidosis.', result)

    def test_raise_id_not_found_exception(self):
        pmcid = getPMCID('PMC2882643532')
        self.assertRaises(IDNotResolvedException, pmcid.getTitle)

    def test_no_prefix_on_pmcid_is_added(self):
        pmcid = getPMCID('2882643532')
        self.assertEquals(pmcid.query[6:],'PMC2882643532')

    def test_query_string_pmid(self):
        pmid = getPMID('1219350')
        self.assertEquals(pmid.query, 'ext_id:1219350 src:med')


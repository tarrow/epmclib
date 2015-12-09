import unittest
from mock import patch
import os.path, json
from .. epmclib.getPMCID import getPMCID
from .. epmclib.getPMID import getPMID
from .. epmclib.exceptions import *


class EPMClibTester(unittest.TestCase):

    def test_getpmcid_resolves(self):
        "Test resolves returns True for a real PMCID"
        pmcid = getPMCID('PMC288264')
        result = pmcid.resolves()
        self.assertEqual(True, result)

    def test_getpmcid_does_not_resolve(self):
        """Test resolves returns False for a fake pmcid"""
        pmcid = getPMCID('PMC2882643532')
        result = pmcid.resolves()
        self.assertEqual(False, result)

    def test_get_pmcid_lite_data(self):
        """Test lite query against inline json"""
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
        """Test the json of a core data query"""
        pmcid = getPMCID('PMC288264')
        pmcid.coreQuery()
        result = pmcid.rawresults
        testfile = open(os.path.normpath('resources/coretest.json'), 'r')
        idealresult = json.load(testfile)
        self.assertEqual(idealresult, result)

    def test_get_pmcid_title_only(self):
        """Test the title of a pmcid for known result"""
        pmcid = getPMCID('PMC288264')
        pmcid.getTitle()
        result = pmcid.title
        self.assertEquals('beta 2-Microglobulin modified with advanced glycation end product'
                          's is a major component of hemodialysis-associated amyloidosis.', result)
    def test_get_pmcid_basic_metadata(self):
        """Test basic metatdata for known result against hardcoded dict"""
        pmcid = getPMCID('PMC288264')
        pmcid.getBBasicMetadata()
        result = pmcid.metadata
        idealresult = {'authors': ['Miyata T',
                                   'Oda O',
                                   'Inagi R',
                                   'Iida Y',
                                   'Araki N',
                                   'Yamada N',
                                   'Horiuchi S',
                                   'Taniguchi N',
                                   'Maeda K',
                                   'Kinoshita T'],
                       'date': '1993-09-01',
                       'doi': '10.1172/jci116696',
                       'issn': '0021-9738',
                       'issue': '3',
                       'journal': 'The Journal of clinical investigation',
                       'orcids': {},
                       'pages': '1243-1252',
                       'pmcid': 'PMC288264',
                       'pmid': '8376584',
                       'title': 'beta 2-Microglobulin modified with advanced glycation end products is a major component of hemodialysis-associated amyloidosis.',
                       'volume': '92'}
        self.assertEquals(result, idealresult)

    def test_raise_id_not_found_exception(self):
        """Check IDNotResolvedException is raised for known failer"""
        pmcid = getPMCID('PMC2882643532')
        self.assertRaises(IDNotResolvedException, pmcid.getTitle)

    def test_no_prefix_on_pmcid_is_added(self):
        """Tests PMC prefix is added if PMCid is not given one EuropePMC requires this to be there"""
        pmcid = getPMCID('2882643532')
        self.assertEquals(pmcid.query[6:],'PMC2882643532')

    def test_query_string_pmid(self):
        """Test correct query string is added for PMIDS"""
        pmid = getPMID('1219350')
        self.assertEquals(pmid.query, 'ext_id:1219350 src:med')



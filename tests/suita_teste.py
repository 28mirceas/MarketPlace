import unittest
import HtmlTestRunner
from test_user import TestUser
from test_product import TestProduct
from test_category import TestCategory
from test_order import TestOrder

class TestSuite(unittest.TestCase):
    def test_suite(self):
        # Creăm o suită de teste
        teste_de_rulat = unittest.TestSuite()

        # Adăugăm testele din fiecare clasă
        teste_de_rulat.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestUser))
        teste_de_rulat.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestProduct))
        teste_de_rulat.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCategory))
        teste_de_rulat.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestOrder))

        # Definim un runner pentru a genera raportul HTML
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_name="Rezultate teste",
            report_title="Titlu raport executie"
        )

        # Rulăm testele
        runner.run(teste_de_rulat)
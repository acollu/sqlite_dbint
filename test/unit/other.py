import itertools
import random
import unittest
from ...sqlite_dbint.sqlite_dbint import SqliteDatabaseInterface

# class under test
db = SqliteDatabaseInterface("test_database.db")

class TestSqliteDatabaseInterface(unittest.TestCase):

    # Testing call

    def test_call(self):
        for valid_field in mapping.data_mapping:
            self.assertEqual(mapping(valid_field), mapping.data_mapping[valid_field])
        with self.assertRaises(KeyError):
            for non_valid_field in [10, "a non valid field", 5.5, None, ""]:
                mapping(non_valid_field)

    # Public method testing

    def test_is_valid_field(self):
        for valid_field in mapping.data_mapping:
            self.assertTrue(mapping.is_valid_field(valid_field))
        for non_valid_field in [10, "a non valid field", 5.5, None, ""]:
            self.assertFalse(mapping.is_valid_field(non_valid_field))

    def test_get_mapping(self):
        for valid_field in mapping.data_mapping:
            self.assertEqual(mapping.get_mapping(valid_field), mapping.data_mapping[valid_field])
        with self.assertRaises(KeyError):
            for non_valid_field in [10, "a non valid field", 5.5, None, ""]:
                mapping.get_mapping(non_valid_field)


# class under test
fmp = Fmp("../../../../../json_data/")


class TestFmp(unittest.TestCase):
    # Testing data structures

    def test_data(self):
        self.assertEqual(fmp.relative_urls.keys(), fmp.data_structures.keys())
        self.assertEqual(fmp.relative_urls.keys(), fmp.periods.keys())
        for datafield in fmp.mapping.data_mapping.values():
            self.assertTrue(fmp._datafield_exists_in(datafield, fmp.data_structures))
        for document_name in fmp.periods:
            self.assertTrue(all([period in ["annual", "quarter"] for period in fmp.periods[document_name]]))

    # Testing private methods

    def test_current_data(self):
        for symbol, price in fmp.current_data.items():
            self.assertIsInstance(symbol, str)
            self.assertIsInstance(price, float)

    def test_field_exists_in(self):
        test_data_structure = {"key_left": {"key_upper": [{"key": ""}, {"other_key": ""}]}, "key_right": {"key": ""}}
        for valid_field in ["key_left", "key_right", "key_upper", "key", "other_key"]:
            self.assertTrue(fmp._field_exists_in(valid_field, test_data_structure))
        for non_valid_field in [10, "a non valid field", 5.5, None, ""]:
            self.assertFalse(fmp._field_exists_in(non_valid_field, test_data_structure))

    def test_datafield_exists_in(self):
        test_data_structure = {"key_left": "", "key_upper": [{"key": ""}], "key_right": [{"other_key": ""}]}
        for valid_field in ["key", "other_key"]:
            self.assertTrue(fmp._datafield_exists_in(valid_field, test_data_structure))
        for non_valid_field in [10, "a non valid field", 5.5, None, "", "key_left"]:
            self.assertFalse(fmp._datafield_exists_in(non_valid_field, test_data_structure))

    # Public method testing

    def test_get_symbols(self):
        self.assertEqual(fmp.get_symbols(), sorted(list(fmp.current_data)))

    def test_is_available_symbol(self):
        for valid_symbol in fmp.current_data:
            self.assertTrue(fmp.is_available_symbol(valid_symbol))
        for non_valid_symbol in [10, "a non valid symbol", 5.5, None, ""]:
            self.assertFalse(fmp.is_available_symbol(non_valid_symbol))

    def test_get_price(self):
        for valid_symbol in fmp.current_data:
            self.assertEqual(fmp.get_price(valid_symbol), fmp.current_data[valid_symbol])
        with self.assertRaises(UnknownSymbol):
            for non_valid_symbol in [10, "a non valid symbol", 5.5, None, ""]:
                fmp.get_price(non_valid_symbol)

    def test_get_url(self):
        valid_symbol = ""
        valid_period = ""
        valid_document_name = ""
        for i in range(1000):
            valid_symbol = list(fmp.current_data.keys())[random.randint(0, len(fmp.current_data.keys()) - 1)]
            valid_document_name = list(fmp.relative_urls.keys())[random.randint(0, len(fmp.relative_urls.keys()) - 1)]
            valid_period = fmp.periods[valid_document_name][random.randint(0, len(fmp.periods[valid_document_name]) - 1)]
            url = fmp.base_url + fmp.relative_urls[valid_document_name] + valid_symbol + "?period=" + valid_period
            self.assertEqual(fmp.get_url(valid_symbol, valid_period, valid_document_name), url)
        with self.assertRaises(UnknownSymbol):
            for non_valid_symbol in [10, "a non valid symbol", 5.5, None, ""]:
                fmp.get_url(non_valid_symbol, valid_period, valid_document_name)
            fmp.get_url("non valid symbol", "non valid period", valid_document_name)
            fmp.get_url("non valid symbol", "non valid period", "non valid document name")
            fmp.get_url("non valid symbol", valid_period, "non valid document name")
        with self.assertRaises(InvalidPeriod):
            for non_valid_period in [10, "a non valid period", 5.5, None, ""]:
                fmp.get_url(valid_symbol, non_valid_period, valid_document_name)
            fmp.get_url(valid_symbol, "non valid period", valid_document_name)
            fmp.get_url(valid_symbol, "non valid period", "non valid document name")
        with self.assertRaises(UnknownFinancialDocument):
            for non_valid_document_name in [10, "a non valid symbol", 5.5, None, ""]:
                fmp.get_url(valid_symbol, valid_period, non_valid_document_name)

    def test_get_document_name_containing(self):
        datafields_list = [list(fmp.data_structures[document_name]["financials"][0].keys()) for document_name in fmp.data_structures if "financials" in fmp.data_structures[document_name]]
        datafields = list(itertools.chain(*datafields_list))
        for datafield in datafields:
            document_name = None
            for dname in fmp.data_structures:
                if fmp._field_exists_in(datafield, fmp.data_structures[dname]):
                    document_name = dname
                    break
            self.assertEqual(fmp.get_document_name_containing(datafield), document_name)
        with self.assertRaises(UnknownDatafield):
            for datafield in [10, "a non valid datafield", 5.5, None, ""]:
                fmp.get_document_name_containing(datafield)

    def test_get_documents_datafields_dict(self):
        datafields_list = [list(fmp.data_structures[document_name]["financials"][0].keys()) for document_name in fmp.data_structures if "financials" in fmp.data_structures[document_name]]
        datafields = sorted(list(itertools.chain(*datafields_list)))
        documents_datafields_dict = fmp.get_documents_datafields_dict(datafields)
        self.assertIsInstance(documents_datafields_dict, dict)
        datafields_output = []
        for document_name in documents_datafields_dict:
            self.assertIsInstance(documents_datafields_dict[document_name], list)
            for datafield in documents_datafields_dict[document_name]:
                self.assertIn(datafield, fmp.data_structures[document_name]["financials"][0].keys())
            datafields_output.extend(list(documents_datafields_dict[document_name]))
        datafields_output = sorted(datafields_output)
        self.assertEqual(datafields, datafields_output)
        with self.assertRaises(UnknownDatafield):
            fmp.get_documents_datafields_dict([10, "a non valid datafield", 5.5, None, ""])

    def test_get_document_data_from_url(self):
        pass

    def read_document_data_from_file(self):
        pass

    def get_periodic_data(self):
        pass


if __name__ == '__main__':
    unittest.main()

import unittest
import modified_r2


class TestR2(unittest.TestCase):

    def test_date_validation(self):
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('1889-12-31'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('1990-01-01'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2100-12-31'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2101-01-01'))

        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-06-31'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-06-30'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-05-32'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-05-31'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-05-00'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-05-01'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-06-00'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-06-01'))

        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-13-07'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-12-07'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-00-07'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-01-07'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-25-03'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('25-03-2022'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('YYYY-MM-DD'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('-199-11-11'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022--11-05'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-11--5'))

        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2022-02-29'))
        with self.subTest():
            self.assertFalse(modified_r2.validate_date('2022-02-30'))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date(' 2 0 2 2 - 0 7 - 1 1 '))
        with self.subTest():
            self.assertTrue(modified_r2.validate_date('2000-11-18'))


    def test_name_validation(self):
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('Person1'), ['Person1'])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('Person1;'), ['Person1'])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('Person1;;'), ['Person1', ''])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('Person1; ;'), ['Person1', ''])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('Person1;; person3;'), ['Person1', '', 'person3'])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('Person1;; person3;;'), ['Person1', '', 'person3', ''])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name(';; person3;;;;person7'), ['', '', 'person3', '', '', '', 'person7'])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name(';;;;person5;;'), ['', '', '', '', 'person5', ''])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name(';  ;  ;'), None)
        with self.subTest():
            self.assertEqual(modified_r2.validate_name(';person2'), ['', 'person2'])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name('; ; person3 ;   '), ['', '', 'person3'])
        with self.subTest():
            self.assertEqual(modified_r2.validate_name(';;;;;;;;;person10;'), ['', '', '', '', '', '', '', '', '', 'person10'])


if __name__ == "__main__":
    unittest.main()
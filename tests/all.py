import unittest

import minervapy.session
import minervapy.configuration
import minervapy.conversion
import minervapy.files

base_url = "https://minerva-dev.lcsb.uni.lu/minerva/api/"
user_name = "test_user"
password = "test_password"


def prepare(log_in=True):
    minervapy.session.set_base_url(base_url)
    if log_in:
        response = minervapy.session.log_in(user_name, password)


class TestSession(unittest.TestCase):
    def test_set_base_url(self):
        minervapy.session.set_base_url(base_url)
        self.assertEqual(minervapy.session.get_base_url(), base_url)

    def test_log_in(self):
        prepare(log_in=False)
        response = minervapy.session.log_in(user_name, password)
        self.assertEqual(response.json()["info"], "Login successful.")

    def test_is_session_valid_true(self):
        prepare()
        valid = minervapy.session.is_session_valid()
        self.assertTrue(valid)

    def test_is_session_valid_false(self):
        prepare()
        minervapy.session.log_out()
        valid = minervapy.session.is_session_valid()
        self.assertFalse(valid)

    def test_log_out_logged_in(self):
        prepare()
        response = minervapy.session.log_out()
        self.assertEqual(response.json()["status"], "OK")

    def test_log_out_logged_out(self):
        prepare()
        minervapy.session.log_out()
        self.assertRaises(Exception, minervapy.session.log_out)


class TestConfiguration(unittest.TestCase):
    def test_get_configuration(self):
        prepare()
        minervapy.configuration.get_configuration()

    def test_get_options(self):
        prepare()
        minervapy.configuration.get_options()


class TestConversion(unittest.TestCase):
    def test_get_formats(self):
        prepare()
        inputs, outputs = minervapy.conversion.get_formats()

    def test_convert(self):
        prepare()
        minervapy.conversion.convert(
            "input_celldesigner_map.xml",
            "celldesigner",
            "output_celldesigner_image.png",
            "png",
        )


class TestFiles(unittest.TestCase):
    def test_create_new_file(self):
        prepare()
        file = minervapy.files.create_new_file("test_file", 1)

    def test_upload_file(self):
        prepare()
        file = minervapy.files.upload_file(
            "input_celldesigner_map.xml", "test_file2"
        )

    def test_get_file(self):
        prepare()
        file = minervapy.files.create_new_file("test_file", 1)
        file = minervapy.files.get_file(file.id)


if __name__ == "__main__":
    unittest.main()

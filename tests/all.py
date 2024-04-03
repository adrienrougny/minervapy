import unittest

import minervapy.session
import minervapy.configuration
import minervapy.conversion
import minervapy.files
import minervapy.project
import minervapy.map

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
            "png",
            "output_celldesigner_image.png",
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


class TestProject(unittest.TestCase):

    def test_get_projects(self):
        prepare()
        projects = minervapy.project.get_projects()

    def test_get_project(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        project = minervapy.project.get_project(project.projectId)

    def test_download_source_from_project_id(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        project = minervapy.project.download_source(project.projectId)

    def test_download_source_from_project(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        data = minervapy.project.download_source(project.projectId)

    def test_download_source_from_project_id_with_output_file(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        data = minervapy.project.download_source(
            project.projectId, "output_source.xml"
        )

    def test_get_statistics_from_project_id(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        statistics = minervapy.project.get_statistics(project.projectId)

    def test_get_statistics_from_project(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        statistics = minervapy.project.get_statistics(project)


class TestMaps(unittest.TestCase):
    def test_get_maps_from_project_id(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project.projectId)

    def test_get_maps_from_project(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)

    def test_get_map_from_project_id(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project.projectId)
        map = maps[0]
        map = minervapy.map.get_map(map.idObject, project.projectId)

    def test_get_map_from_project(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)
        map = maps[0]
        map = minervapy.map.get_map(map.idObject, project)

    def test_download_map_from_map_id_and_project_id_as_celldesigner(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)
        map = maps[0]
        data = minervapy.map.download_map(
            map.idObject,
            project_or_project_id=project.projectId,
            format="celldesigner",
            output_file_path="output_celldesigner_map.xml",
        )

    def test_download_map_from_map_as_celldesigner(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)
        map = maps[0]
        data = minervapy.map.download_map(
            map,
            format="celldesigner",
            output_file_path="output_celldesigner_map.xml",
        )

    def test_download_map_from_map_as_png(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)
        map = maps[0]
        data = minervapy.map.download_map(
            map,
            format="png",
            output_file_path="output_celldesigner_map.png",
        )

    def test_download_map_from_map_as_png_with_zoom_level_5(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)
        map = maps[0]
        data = minervapy.map.download_map(
            map,
            format="png",
            output_file_path="output_celldesigner_map.png",
            zoom_level=5.0,
        )

    def test_map_download_as_celldesigner(self):
        prepare()
        projects = minervapy.project.get_projects()
        project = projects[0]
        maps = minervapy.map.get_maps(project)
        map = maps[0]
        data = map.download(
            format="celldesigner",
            output_file_path="output_celldesigner_map.xml",
        )


if __name__ == "__main__":
    unittest.main()

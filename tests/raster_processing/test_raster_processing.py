import unittest
import os
import rasterio

import raster_processing
import handler


class TestReproject(unittest.TestCase):

    def test_reproject(self):
        self.in_file = '../data/input/pre/MO-2/2008/200804_missouri_west_mo_0x6000m_utm_clr/vol056/3709460ne.tif'
        self.dest_file = '../data/output/resample.tif'
        self.result = raster_processing.reproject(self.in_file, self.dest_file)
        self.test = rasterio.open(self.result).crs
        self.assertEqual('EPSG:4326', self.test)


class TestCreateMosaic(unittest.TestCase):

    def setUp(self):
        self.files = handler.get_files('../data/input/pre')
        self.out_file = os.path.abspath('../data/output/test_mosaic.tif')
        try:
            os.remove(self.out_file)
        except:
            pass

        self.result = raster_processing.create_mosaic(self.files, out_file=self.out_file)

    def test_output_exists(self):
        self.assertTrue(os.path.isfile(self.result))

    def test_correct_resolution(self):
        self.src = rasterio.open(self.result)
        self.assertEqual((0.6, 0.6), self.src.res)

    def test_correct_extent(self):
        self.src = rasterio.open(self.result)
        self.assertEqual((355207.8, 4110082.2), self.src.transform * (0, 0))


class TestGetIntersect(unittest.TestCase):

    def test_intersect_extent(self):
        self.assertEqual((364950.125, 4102656.6, 366951.60000000003, 4105049.875), raster_processing.get_intersect(
            '/Users/lb/Documents/PycharmProjects/xView2_FDNY/tests/data/input/pre/MO-2/2008/200804_missouri_west_mo_0x6000m_utm_clr/vol056/3709460ne.tif',
            '/Users/lb/Documents/PycharmProjects/xView2_FDNY/tests/data/input/post/jpg/may24C365000e4105000n.jpg'
        ))


class TestGetIntersectWin(unittest.TestCase):

    def test_get_intersect_win(self):
        self.intersect = (-94.62862733666518, 36.997318285256874, -94.55892307170559, 37.06518001454033)
        self.mosaic = '/Users/lb/Documents/PycharmProjects/xView2_FDNY/tests/data/output/test_mosaic.tif'
        self.test = 'Window(col_off=211, row_off=10114, width=10853, height=11148)'
        self.result = raster_processing.get_intersect_win(self.mosaic, self.intersect)
        self.assertEqual(self.test, self.result)


# class TestCreateChips(unittest.TestCase):
#
#     def setUp(self):
#         self.out_dir = '../data/output/chips/test_chips'
#         self.mosaic = TestCreateMosaic()
#         self.in_mosaic = self.mosaic.result
#
#     def test_chip_exist(self):
#         self.assertEqual(0, len())
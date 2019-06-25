import unittest

from get_iplayer_python.mpd_data_extractor import get_programme_duration, get_programme_periods, \
    get_programme_adaptation_sets, get_adaption_info, get_programme_representation, prepare_initialization_template, \
    prepare_media_template, calculate_number_of_segments, create_fragments
from get_iplayer_python.tests.test_data import mpd_file


def fake_xml_getter(xml):
    def name(url: str):
        return xml
    return name


class TestMpdDataExtractor(unittest.TestCase):
    test_url = "http://aod-dash-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/9ab037-m0005zsl/vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2.ism/iptv_hd_abr_v1_uk_dash_master.mpd?__gda__=1561337815_34e5a9c6508c400847508c4146389241"

    def test_that_can_get_duration(self):
        expected = 7199.844375
        actual = get_programme_duration(self.test_url, fake_xml_getter(mpd_file))
        self.assertEqual(expected, actual)

    def test_can_retrieve_periods(self):
        expected = 1
        actual = get_programme_periods(self.test_url, fake_xml_getter(mpd_file))
        self.assertEqual(expected, len(actual))

    def test_can_get_adaptation_tests_for_period(self):
        period = get_programme_periods(self.test_url, fake_xml_getter(mpd_file))[0]
        expected = 2
        actual = get_programme_adaptation_sets(period)
        self.assertEqual(expected, len(actual))

    def test_can_get_adaptation_info(self):
        expected = {
            "start_number": 1,
            "timescale": 48000,
            "segment_duration": 307200.0,
            "media": 'vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$-$Number$.m4s',
            "initialization": 'vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$.dash'
        }
        period = get_programme_periods(self.test_url, fake_xml_getter(mpd_file))[0]
        adaptation_set = get_programme_adaptation_sets(period)[0]
        actual = get_adaption_info(adaptation_set)
        self.assertEqual(expected, actual)

    def test_can_get_representation_from_adaptation(self):
        expected = 2
        period = get_programme_periods(self.test_url, fake_xml_getter(mpd_file))[0]
        adaptation_set = get_programme_adaptation_sets(period)[0]
        actual = get_programme_representation(adaptation_set)
        self.assertEqual(expected, len(actual))

    def test_can_get_initialization_template(self):
        expected = 'vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-audio_eng=128000.dash'
        initialization_url = "vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$.dash"
        representation_id = "audio_eng=128000"
        actual = prepare_initialization_template(initialization_url, representation_id)
        self.assertEqual(expected, actual)

    def test_can_calculate_number_of_segments(self):
        expected = 1125
        segment_duration = 307200.0
        period_duration = 7199.844375
        timescale = 48000
        actual = calculate_number_of_segments(segment_duration, period_duration, timescale)
        self.assertEqual(expected, actual)

    def test_can_create_media_template(self):
        expected = 'vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-audio_eng=128000-%(Number)d.m4s'
        media_url = 'vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$-$Number$.m4s'
        representation_id = "audio_eng=128000"
        actual = prepare_media_template(media_url, representation_id)
        self.assertEqual(expected, actual)

    def test_can_create_fragments(self):
        expected = 1125
        actual = create_fragments(
            "path",
            1,
            1125,
            6.4,
            128000,
            "vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-audio_eng=128000-%(Number)d.m4s"
        )
        self.assertEqual(expected, len(actual))

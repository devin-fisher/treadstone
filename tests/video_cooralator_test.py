import unittest
import os
import sys
from unittest import skip
import json
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(main_dir)
from lib.timeline_analysis.video_cooralator import video_event_translator


class SimplisticTest(unittest.TestCase):

    def test_full_test_case(self):
        with open("fodder/video_cooralator_test_case_1.json", 'r') as f:
            test_case_data = json.loads(f.read())
        video_event_translator(test_case_data['time_line_events'], test_case_data['video_analysis'])
        self.assertTrue(True)

    def test_start_only(self):
        video_break = {"start": 120, "shifts": []}
        event = [{"startTime": 30, "endTime": 40}]
        correlated = video_event_translator(event, video_break)
        expected = {'video_start': 150, 'video_end': 160, 'game_start': 30, 'game_end': 40}
        self.assertDictContainsSubset(expected, correlated[0])

    def test_no_effect_shift(self):
        video_break = {"start": 120, "shifts": [{
            "start_game_time": 10,
            "start_time": 130,
            "did_shift": False,
            "end_game_time": 15,
            "end_time": 135
         }]}
        event = [{"startTime": 30, "endTime": 40}]
        correlated = video_event_translator(event, video_break)
        expected = {'video_start': 150, 'video_end': 160, 'game_start': 30, 'game_end': 40}
        self.assertDictContainsSubset(expected, correlated[0])

    def test_with_shift(self):
        video_break = {"start": 120, "shifts": [{
            "start_game_time": 10,
            "start_time": 130,
            "did_shift": True,
            "end_game_time": 20,
            "end_time": 135
         }]}
        event = [{"startTime": 30, "endTime": 40}]
        correlated = video_event_translator(event, video_break)
        expected = {'video_start': 145, 'video_end': 155, 'game_start': 30, 'game_end': 40}
        self.assertDictContainsSubset(expected, correlated[0])

    def test_event_in_break(self):
        video_break = {"start": 120, "shifts": [{
            "start_game_time": 20,
            "start_time": 140,
            "did_shift": False,
            "end_game_time": 31,
            "end_time": 151
         }]}
        event = [{"startTime": 30, "endTime": 40}]
        correlated = video_event_translator(event, video_break)
        expected = {'video_start': 151.5, 'video_end': 160, 'game_start': 31.5, 'game_end': 40}
        self.assertDictContainsSubset(expected, correlated[0])

    def test_event_in_break_with_shift(self):
        video_break = {
            "start": 120,
            "shifts": [{
                "start_game_time": 20,
                "start_time": 140,
                "did_shift": True,
                "end_game_time": 33,
                "end_time": 151
            }]}
        event = [{"startTime": 30, "endTime": 40}]
        correlated = video_event_translator(event, video_break)
        expected = {'video_start': 151.5, 'video_end': 158, 'game_start': 33.5, 'game_end': 40}
        self.assertDictContainsSubset(expected, correlated[0])

    def test_event_with_two_breaks(self):
        video_break = {
            "start": 5,
            "shifts": [
                {
                    "start_game_time": 5,
                    "start_time": 10,
                    "did_shift": True,
                    "end_game_time": 21,
                    "end_time": 20
                },
                {
                    "start_game_time": 33,
                    "start_time": 32,
                    "did_shift": False,
                    "end_game_time": 38,
                    "end_time": 37
                }
            ]}
        event = [{"startTime": 20, "endTime": 35},{"startTime": 40, "endTime": 50}]
        correlated = video_event_translator(event, video_break)
        expected = {'video_start': 20.5, 'video_end': 31.5, 'game_start': 21.5, 'game_end': 32.5}
        self.assertDictContainsSubset(expected, correlated[0])
        expected = {'video_start': 39, 'video_end': 49, 'game_start': 40, 'game_end': 50}
        self.assertDictContainsSubset(expected, correlated[1])

if __name__ == '__main__':
    unittest.main()

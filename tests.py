import unittest

from starlette.testclient import TestClient

import yaas


class SmokeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(yaas.app)

    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_video(self):
        video_url = 'https://www.youtube.com/watch?v=mNFx28NGLfI'
        r = self.client.get('/details', params={'url': video_url})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('error', r.text)

    def test_playlist(self):
        playlist_url = 'https://www.youtube.com/watch?v=1AGCX41FV3A&list=PLED86AD896A3CF401'
        r = self.client.get('/details', params={'url': playlist_url})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('error', r.text)

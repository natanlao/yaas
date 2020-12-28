import unittest

import yaas


class SmokeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = yaas.app.test_client()

    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_video(self):
        video_url = 'https://www.youtube.com/watch?v=mNFx28NGLfI'
        r = self.client.get('/details', query_string={'url': video_url})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('error', r.data.decode())

    def test_playlist(self):
        playlist_url = 'https://www.youtube.com/watch?v=1AGCX41FV3A&list=PLED86AD896A3CF401'
        r = self.client.get('/details', query_string={'url': playlist_url})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('error', r.data.decode())

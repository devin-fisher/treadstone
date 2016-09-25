import falcon
from PIL import Image
from inmemory_zip import InMemoryZip
import numpy



class Report(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id):
        imz = InMemoryZip()
        imz.append("test.txt", "Another test").append("test2.txt", "Still another")
        imarray = numpy.random.rand(100, 100, 3) * 255
        image = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
        imz.append_image("test2.jpg", image)
        resp.data = imz.read()
        resp.content_type = "application/zip"
        resp.append_header('Content-Disposition', 'attachment; filename=complete_report.zip')





from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4


def create_name_tag(names, doc_name):

    canv = Canvas(doc_name + '.pdf', pagesize=A4)
    img = ImageReader('static/name.jpg')
    registerFont(TTFont('optima', 'static/OPTIMA.TTF'))
    registerFont(TTFont('optima-bold', 'static/OPTIMA-BOLD.TTF'))

    # now begin the work
    for index, name in enumerate(names):

        x = 20 * mm
        y = 250 * mm
        w = 75 * mm
        h = 25 * mm

        if index % 2 == 0:
            x = 100 * mm

        if index >= 2:
            y = y - 40 * mm

        if index >= 4:
            y = y - 50 * mm

        if index >= 6:
            y = y - 60 * mm

        canv.drawImage(img, x, y, w, h, anchor='sw', anchorAtXY=True, showBoundary=False)
        if len(name['name']) >= 8:
            canv.setFont('optima-bold', 15)
        else:
            canv.setFont('optima-bold', 18)
        canv.setFillColor(HexColor('#742013'))  # change the text color
        canv.drawCentredString(x + w * 0.5, y + h * 0.5, name['name'].upper())
        canv.setFont('optima', 10)
        canv.drawCentredString(x + w * 0.5, y + h * 0.35, name['position'])
        print(x, index)
        print(y, index)

    canv.save()

from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


# ----------------------------------------------------------------------
def create_barcodes(barcode):
    """
    Create barcode examples and embed in a PDF
    """
    c = canvas.Canvas(barcode + ".pdf", pagesize=A4)

    barcode128 = code128.Code128(barcode, barHeight=30, barWidth=1.3)

    codes = []
    for i in range(33):
        codes.append(barcode128)

    x = 5 * mm
    y = 270 * mm

    for index, code in enumerate(codes):
        code.drawOn(c, x, y)
        c.drawString(x + 50, y - 13, str(barcode))
        c.rect(x, y - 25, width=190, height=70, stroke=1, fill=0)

        y = y - 24.5 * mm

        if index == 10:
            x = 72 * mm
            y = 270 * mm

        if index == 21:
            x = 139 * mm
            y = 270 * mm
            print(y, index)

    c.save()


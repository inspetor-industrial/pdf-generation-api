import io
import json
import os
import datetime
import time

import PyPDF2 as pdf2
from flask import typing as ft, Response, request
from flask.views import View
from playwright.sync_api import sync_playwright

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from src.utils.logger import logger


class CalibrationValve(View):
    methods = ['GET']

    def __init__(self, *args, **kwargs):
        super(CalibrationValve, self).__init__(*args, **kwargs)
        self._report_path = None

    def dispatch_request(self) -> ft.ResponseReturnValue:
        report_id = request.args.get('report_id')

        try:
            logger.info("Validating Calibration Valve")
        except Exception as e:
            logger.error("Calibration Valve validation failed")
            logger.error(str(e))

        base_url = os.getenv('INSPETOR_URL')
        report_url = f"{base_url}/reports/valve/preview/{report_id}?download=true"

        logger.info(f"Calibration Valve URL: {report_url}")
        with sync_playwright() as p:
            logger.info("Initiating browser session")
            browser = p.chromium.launch()

            try:
                page = browser.new_page()
                page.goto(report_url)

                logger.info(f"waiting networkidle, timout = {30_000}")
                time.sleep(10)

                logger.info("take pdf buffer")
                pdf_file_first_page = page.pdf(
                    format="A4",
                    print_background=True,
                )

                pdf_rest = page.pdf(
                    format="A4",
                    print_background=True,
                    margin={'top': '80px', 'bottom': '30px'},
                )

                logger.info("closing browser with buffer")
                browser.close()

            except Exception as e:
                logger.error("Network idle timeout")
                logger.error(str(e))
                browser.close()

                return Response(
                    response=json.dumps({
                        "message": 'An error occurred.',
                        "error": str(e)
                    }),
                    status=500,
                )

            try:
                logger.info("applying styles")
                first_reader = pdf2.PdfReader(io.BytesIO(pdf_file_first_page))
                rest_reader = pdf2.PdfReader(io.BytesIO(pdf_rest))

                final_pdf = pdf2.PdfWriter()
                final_pdf.add_page(first_reader.pages[0])

                for _, page in enumerate(rest_reader.pages[1:]):
                    final_pdf.add_page(page)

                packet = io.BytesIO()

                logger.info("inserting page numbers and vertical lines")
                can = canvas.Canvas(packet, pagesize=letter)
                width, height = letter

                quantity_of_pages = len(final_pdf.pages)

                background_color = colors.HexColor("#819fad")
                # background_color = colors.HexColor("#FFFFFF")

                for page_number in range(quantity_of_pages - 1):
                    page = final_pdf.pages[page_number]
                    can.setPageSize((page.mediabox.width, page.mediabox.height))
                    can.setFillColor(background_color)
                    can.rect(0, height - 10, 40, 30, fill=True, stroke=False)

                    text = f"N° {page_number + 1}"
                    style = getSampleStyleSheet()["BodyText"]
                    style.textColor = colors.white
                    style.fontName = "Helvetica-Bold"

                    p = Paragraph(text, style)
                    p.wrapOn(can, 70, 20)
                    p.drawOn(can, 10, height)

                    x_position = width - 40
                    line_height = height
                    for j in range(3):
                        can.setStrokeColor(colors.black)
                        can.setLineWidth(1)
                        can.line(x_position, line_height + 60, x_position, 0)

                        x_position -= 10

                    can.setFillColor(colors.black)
                    can.drawString((width // 2) - 30, 10, str(datetime.date.today().year))

                    can.showPage()
                can.save()
                packet.seek(0)

                logger.info("merging styles into original pdf")
                response_pdf = pdf2.PdfWriter()
                for page_index in range(quantity_of_pages):
                    page = final_pdf.pages[page_index]

                    if page_index > 0:
                        page.merge_page(pdf2.PdfReader(packet).pages[page_index - 1])
                    response_pdf.add_page(page)

                buffer = io.BytesIO()
                response_pdf.write_stream(buffer)

                response = Response(buffer.getvalue(), headers={
                    'Content-Type': 'application/pdf',
                    'Content-Disposition': f"attachment;filename = {report_id}.pdf"
                })

                return response
            except Exception as e:
                logger.error("Network idle timeout")
                logger.error(str(e))

                return Response(
                    response=json.dumps({
                        "message": 'An error occurred.',
                        "error": str(e)
                    }),
                    status=500,
                )

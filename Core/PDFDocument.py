import os
from pathlib import Path

from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from tqdm import tqdm

from Core.Logger import Logger

class PDFDocument:
    title: str
    auther: str | None
    pages: list[Path]
    logger: Logger

    def __init__(self, title: str, logger: Logger, author: str | None = None):
        self.title = title
        self.auther = author
        self.logger = logger
        self.pages = []

    def append_page(self, file_path: Path):
        self.pages.append(file_path)

    def save_pdf(self, path: Path):
        canvas = self._create_canvas(path)

        self.logger.log(f"Generating PDF...")
        for page in tqdm(self.pages):
            image = Image.open(page)
            canvas.setPageSize(image.size)
            canvas.drawImage(page, 0, 0)
            canvas.showPage()
        canvas.save()

        self.logger.log(f"PDF generated at '{path}'.")

        return path

    def _create_canvas(self, filepath: Path) -> Canvas:
        canvas = Canvas(str(filepath))

        if self.auther is not None: canvas.setAuthor(self.auther)
        if self.title is not None: canvas.setTitle(self.title)

        return canvas

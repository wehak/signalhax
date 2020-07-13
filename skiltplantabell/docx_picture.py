from docx.shared import Inches
from docx import Document

document = Document()
document.add_picture('basic_shapes.svg', width=Inches(1.0))
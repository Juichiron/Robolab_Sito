from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import mm
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
import os
from PIL import Image
def make_barcode_transparent(png_path):
    img = Image.open(png_path).convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(png_path, "PNG")
    
    
def make_circular_image(image_path):
    from PIL import Image, ImageDraw
    
    # Open and convert image to RGBA
    img = Image.open(image_path).convert('RGBA')
    
    # Create a new image with alpha channel
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw a white circle that will be used as mask
    draw.ellipse((0, 0) + img.size, fill=255)
    
    # Apply the circular mask
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    # Save temporary circular image
    temp_path = image_path.replace('.png', '_circular.png')
    output.save(temp_path, 'PNG')
    return temp_path    

def draw_ticket(title_text, nome, cognome, identifier, event_date, aula_text, piano_text):
    width = 250 * mm
    height = 100 * mm
    filename = f"{nome}{cognome}{identifier}.pdf"
    c = canvas.Canvas(filename, pagesize=(width, height))

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # --- SFONDO BIANCO ---
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # --- TITOLO E DATA IN ALTO A SINISTRA ---
    title_x = 5 * mm
    title_y = height - 20 * mm
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(black)
    c.drawString(title_x, title_y, title_text)
    c.setFont("Helvetica-Bold", 22)
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 32)
    c.drawString(title_x + title_width + 6*mm, title_y, event_date)

    title_y -= 10 * mm
    
    # --- NOME E COGNOME SOTTO IL TITOLO ---
    c.setFont("Helvetica-Bold", 26)
    c.drawString(title_x, title_y - 18 * mm, f"{nome} {cognome}")

        # --- LOGO UNIBA IN BASSO A SINISTRA ---
    circle_x = 0 * mm
    circle_y = 0 * mm
    circle_r = 15 * mm
    
    # Carica e posiziona il logo Uniba
    logo_uniba = os.path.join(base_dir, "./generaBiglietto/img", "logoUniba.png")
    logo_size = circle_r * 2  # Diametro del cerchio
    c.drawImage(logo_uniba, 
                circle_x, 
                circle_y, 
                width=logo_size, 
                height=logo_size, 
                mask='auto')

    # --- DIPARTIMENTO, AULA, PIANO ACCANTO AL CERCHIO ---
    dep_x = circle_x + 2 * circle_r + 5 * mm
    dep_y = circle_y + 2 * circle_r - 11 * mm
    c.setFont("Helvetica", 11)
    c.drawString(dep_x, dep_y, "Dipartimento di informatica")
    dep_y -= 5 * mm
    c.setFont("Helvetica", 10)
    c.drawString(dep_x, dep_y - 8 * mm, f"{aula_text} | {piano_text}º piano")

    # --- RETTANGOLO CENTRALE VERTICALE ---
    rect_w = 54 * mm
    rect_h = 86 * mm
    rect_x = ((width - rect_w) / 2)+30*mm
    rect_y = (height - rect_h) / 2
    c.setLineWidth(2)
    c.setStrokeColor(black)
    c.rect(rect_x, rect_y, rect_w, rect_h, stroke=1, fill=0)

    # --- LOGO ROBOLAB IN ALTO NEL RETTANGOLO ---
    logo_robolab = os.path.join(base_dir, "./generaBiglietto/img", "logoRobolab.png")
    logo_h = 30 * mm
    logo_w = 30 * mm
    circular_robolab = make_circular_image(logo_robolab)
    c.drawImage(circular_robolab, rect_x + (rect_w - logo_w )/2, rect_y + 4 * mm+ rect_h - logo_h - 5*mm, width=logo_w, height=logo_h, mask='auto')

    # --- X GRANDE AL CENTRO DEL RETTANGOLO ---
    c.setStrokeColor(black)
    c.setLineWidth(3)
    x_center = rect_x + rect_w / 2
    x_y = rect_y + rect_h / 2
    size_x = 8 * mm
    c.line(x_center - size_x, x_y - size_x, x_center + size_x, x_y + size_x)
    c.line(x_center - size_x, x_y + size_x, x_center + size_x, x_y - size_x)

    # --- LOGO PROVA IN BASSO NEL RETTANGOLO ---
    logo_prova = os.path.join(base_dir, "./generaBiglietto/img", "logoRobolab.png")
    logo_p_h = 30 * mm
    logo_p_w = 30 * mm
    circular_prova = make_circular_image(logo_prova)
    try:
        c.drawImage(circular_prova, 
                    rect_x + (rect_w - logo_p_w)/2, 
                    rect_y + 1*mm, 
                    width=logo_p_w, 
                    height=logo_p_h, 
                    mask='auto')
    finally:
        if os.path.exists(circular_prova):
            os.remove(circular_prova)
    # --- BARRETTE NERE VERTICALI IN ALTO E IN BASSO A DESTRA ---
    bar_w = 8 * mm
    bar_h = 15 * mm
    bar_x = width - bar_w - 40*mm
    # Barretta in alto
    c.setFillColor(black)
    c.rect(bar_x, height - bar_h, bar_w, bar_h, fill=1, stroke=0)
    # Barretta in basso
    c.rect(bar_x, 0, bar_w, bar_h, fill=1, stroke=0)

        # --- BARCODE VERTICALE DOPO LE BARRETTE ---
    barcode_data = f"{title_text}-{nome}{cognome}-{identifier}"
    barcode_generator = Code128(barcode_data, writer=ImageWriter())
    barcode_filename = f"temp_barcode_{identifier}"
    barcode_path = f"{barcode_filename}.png"
    barcode_options = {
        'module_height': 40.0,  # Ridotto da 30.0
        'module_width': 0.5,    # Ridotto da 0.6
        'quiet_zone': 0,
        'write_text': False,
        'background': 'white',
        'foreground': '#23291a'
    }
    try:
        barcode_generator.save(barcode_filename, options=barcode_options)
        make_barcode_transparent(barcode_path)
        barcode_width = 25 * mm  # Ridotto da 30 mm
        barcode_height = height - (bar_h * 1.5)  # Aumentato il margine
        c.saveState()
        c.rotate(90)
        barcode_x = bar_h - 5*mm
        barcode_y = -243*mm
        c.drawImage(barcode_path,
                    barcode_x,
                    barcode_y,
                    width=barcode_height,
                    height=barcode_width,
                    mask='auto')
        c.restoreState()
    finally:
        if os.path.exists(barcode_path):
            os.remove(barcode_path)

    c.save()
    print(f"Biglietto generato: {filename}")

# Esempio di utilizzo
draw_ticket("Prova", "Piero", "Motocaro", "123456", "15/04/2025", aula_text="Aula 1", piano_text="1")

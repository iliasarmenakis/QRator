import qrcode
import os

def generate_qr_code(content, filename):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    # Create PIL image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img_path = os.path.join(os.path.dirname(__file__), filename)
    img.save(img_path)

    print(f"QR code saved as {img_path}")

if __name__ == "__main__":
    # Example usage:
    content = "http://localhost:8080"  # Your content here (e.g., URL)
    filename = "qr_code.png"  # Your desired filename here
    generate_qr_code(content, filename)

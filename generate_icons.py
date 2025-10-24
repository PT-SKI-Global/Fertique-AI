from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon(size, output_path):
    img = Image.new('RGB', (size, size), color='#2E7D32')
    
    draw = ImageDraw.Draw(img)
    
    emoji_size = int(size * 0.6)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", emoji_size)
    except:
        font = ImageFont.load_default()
    
    text = "🌾"
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    circle_radius = int(size * 0.45)
    circle_center = (size // 2, size // 2)
    draw.ellipse(
        [
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ],
        fill='#4CAF50'
    )
    
    draw.text((x, y), text, fill='white', font=font)
    
    img.save(output_path, 'PNG', quality=95, optimize=True)
    print(f"Created icon: {output_path} ({size}x{size})")

os.makedirs('static', exist_ok=True)

icon_sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in icon_sizes:
    create_app_icon(size, f'static/icon-{size}x{size}.png')

print("✅ All app icons created successfully!")
print("\nNext steps:")
print("1. Replace generated icons with professionally designed ones")
print("2. Add screenshots for app store listings")
print("3. Test PWA installation on mobile devices")

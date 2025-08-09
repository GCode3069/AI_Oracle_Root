"""
Effects Library for Oracle Horror
Visual horror effects: glitch, matrix rain, neon overlays, VHS corruption
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Tuple, List, Optional
import random
import os
from pathlib import Path

class EffectsLibrary:
    def __init__(self):
        self.color_schemes = {
            "dark_neon": {
                "primary": (0, 255, 65),    # Matrix green
                "secondary": (0, 150, 40),
                "background": (0, 10, 0),
                "accent": (0, 255, 200)
            },
            "blood_red": {
                "primary": (255, 0, 0),     # Blood red
                "secondary": (150, 0, 0),
                "background": (20, 0, 0),
                "accent": (255, 100, 100)
            },
            "cyber_blue": {
                "primary": (0, 212, 255),   # Cyber blue
                "secondary": (0, 100, 150),
                "background": (0, 5, 15),
                "accent": (100, 255, 255)
            }
        }
        
        self.matrix_chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    
    def test_effects(self) -> bool:
        """Test all visual effects"""
        try:
            # Test basic image generation
            test_img = self.generate_background((1920, 1080), "dark_neon")
            
            # Test matrix rain
            matrix_img = self.add_matrix_rain(test_img, "medium")
            
            # Test glitch effect
            glitch_img = self.add_screen_glitch(matrix_img, "high")
            
            # Test text overlay
            final_img = self.add_horror_text(glitch_img, "Test Horror Text", "glitch_neon")
            
            print("✅ All visual effects tested successfully")
            return True
            
        except Exception as e:
            print(f"❌ Effects test failed: {e}")
            return False
    
    def generate_background(self, size: Tuple[int, int], color_scheme: str) -> Image.Image:
        """Generate horror background image"""
        width, height = size
        colors = self.color_schemes.get(color_scheme, self.color_schemes["dark_neon"])
        
        # Create base image
        img = Image.new('RGB', size, colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Add subtle gradient
        for y in range(height):
            gradient_intensity = int(255 * (y / height) * 0.1)
            gradient_color = tuple(min(255, c + gradient_intensity) for c in colors["background"])
            draw.line([(0, y), (width, y)], fill=gradient_color)
        
        # Add random noise pattern
        self._add_digital_noise(img, colors, intensity=0.05)
        
        # Add circuit-like patterns
        if color_scheme in ["dark_neon", "cyber_blue"]:
            self._add_circuit_patterns(img, colors)
        
        return img
    
    def add_matrix_rain(self, img: Image.Image, intensity: str = "medium") -> Image.Image:
        """Add Matrix-style falling code rain"""
        width, height = img.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Determine rain parameters based on intensity
        intensity_params = {
            "low": {"columns": 20, "speed": 1, "opacity": 100},
            "medium": {"columns": 40, "speed": 2, "opacity": 150}, 
            "high": {"columns": 80, "speed": 3, "opacity": 200}
        }
        
        params = intensity_params.get(intensity, intensity_params["medium"])
        
        # Try to load a monospace font, fallback to default
        try:
            font_size = max(12, width // 100)
            font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Generate falling code columns
        column_width = width // params["columns"]
        
        for col in range(params["columns"]):
            x = col * column_width
            
            # Random column height and position
            column_height = random.randint(height // 4, height)
            y_start = random.randint(-column_height // 2, height // 4)
            
            # Draw characters in column
            char_height = font_size + 2 if font else 14
            for i in range(0, column_height, char_height):
                y = y_start + i
                if 0 <= y < height:
                    char = random.choice(self.matrix_chars)
                    
                    # Color intensity decreases towards bottom of trail
                    trail_pos = i / column_height
                    alpha = int(params["opacity"] * (1 - trail_pos))
                    color = (0, 255, 65, alpha)  # Matrix green with alpha
                    
                    if font:
                        draw.text((x, y), char, font=font, fill=color)
                    else:
                        draw.text((x, y), char, fill=color)
        
        # Composite overlay onto original image
        result = Image.alpha_composite(img.convert('RGBA'), overlay)
        return result.convert('RGB')
    
    def add_screen_glitch(self, img: Image.Image, frequency: str = "medium") -> Image.Image:
        """Add screen glitch and VHS corruption effects"""
        width, height = img.size
        
        # Convert to numpy for easier manipulation
        img_array = np.array(img)
        
        # Determine glitch parameters
        frequency_params = {
            "low": {"scan_lines": 5, "shifts": 3, "noise": 0.02},
            "medium": {"scan_lines": 15, "shifts": 8, "noise": 0.05},
            "high": {"scan_lines": 30, "shifts": 15, "noise": 0.1}
        }
        
        params = frequency_params.get(frequency, frequency_params["medium"])
        
        # Add horizontal scan line effects
        for _ in range(params["scan_lines"]):
            y = random.randint(0, height - 5)
            line_height = random.randint(2, 10)
            
            # Create RGB shift effect
            if y + line_height < height:
                # Shift red channel
                img_array[y:y+line_height, :, 0] = np.roll(
                    img_array[y:y+line_height, :, 0], 
                    random.randint(-5, 5), axis=1
                )
                # Shift blue channel opposite direction
                img_array[y:y+line_height, :, 2] = np.roll(
                    img_array[y:y+line_height, :, 2], 
                    random.randint(-3, 3), axis=1
                )
        
        # Add random pixel shifts
        for _ in range(params["shifts"]):
            x1, y1 = random.randint(0, width-50), random.randint(0, height-20)
            x2, y2 = random.randint(0, width-50), random.randint(0, height-20)
            w, h = random.randint(20, 100), random.randint(10, 30)
            
            if (x1 + w < width and y1 + h < height and 
                x2 + w < width and y2 + h < height):
                # Copy block from one location to another
                img_array[y2:y2+h, x2:x2+w] = img_array[y1:y1+h, x1:x1+w]
        
        # Add digital noise
        noise = np.random.normal(0, params["noise"] * 255, img_array.shape)
        img_array = np.clip(img_array + noise, 0, 255)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def add_horror_text(self, img: Image.Image, text: str, style: str = "glitch_neon") -> Image.Image:
        """Add horror-styled text overlay with animations"""
        width, height = img.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Text styling based on style type
        if style == "glitch_neon":
            color = (0, 255, 65, 255)  # Matrix green
            shadow_color = (0, 100, 30, 200)
        elif style == "blood_red":
            color = (255, 0, 0, 255)
            shadow_color = (100, 0, 0, 200)
        elif style == "cyber_blue":
            color = (0, 212, 255, 255)
            shadow_color = (0, 100, 150, 200)
        else:
            color = (255, 255, 255, 255)
            shadow_color = (100, 100, 100, 200)
        
        # Try to load a suitable font
        font_size = max(48, width // 30)
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Calculate text position (center)
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 10  # Rough estimate
            text_height = 20
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Add glitch effect to text
        if "glitch" in style:
            # Draw multiple offset copies for glitch effect
            offsets = [(0, 0), (-2, -1), (2, 1), (-1, 2), (1, -2)]
            colors = [color, shadow_color, (255, 0, 0, 100), (0, 255, 0, 100), (0, 0, 255, 100)]
            
            for offset, glitch_color in zip(offsets, colors):
                if font:
                    draw.text((x + offset[0], y + offset[1]), text, font=font, fill=glitch_color)
                else:
                    draw.text((x + offset[0], y + offset[1]), text, fill=glitch_color)
        else:
            # Draw shadow first
            if font:
                draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
                draw.text((x, y), text, font=font, fill=color)
            else:
                draw.text((x + 2, y + 2), text, fill=shadow_color)
                draw.text((x, y), text, fill=color)
        
        # Composite overlay onto original image
        result = Image.alpha_composite(img.convert('RGBA'), overlay)
        return result.convert('RGB')
    
    def add_neon_overlay(self, img: Image.Image, pattern: str = "circuit") -> Image.Image:
        """Add neon overlay patterns"""
        width, height = img.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        if pattern == "circuit":
            # Draw circuit-like patterns
            self._draw_neon_circuits(draw, width, height)
        elif pattern == "grid":
            # Draw neon grid
            self._draw_neon_grid(draw, width, height)
        elif pattern == "border":
            # Draw neon border
            self._draw_neon_border(draw, width, height)
        
        # Apply glow effect
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Composite overlay onto original image
        result = Image.alpha_composite(img.convert('RGBA'), overlay)
        return result.convert('RGB')
    
    def add_vhs_corruption(self, img: Image.Image, intensity: str = "medium") -> Image.Image:
        """Add VHS-style corruption and artifacts"""
        width, height = img.size
        img_array = np.array(img)
        
        intensity_params = {
            "low": {"tracking": 2, "chroma": 0.1, "noise": 0.02},
            "medium": {"tracking": 5, "chroma": 0.2, "noise": 0.05},
            "high": {"tracking": 10, "chroma": 0.4, "noise": 0.1}
        }
        
        params = intensity_params.get(intensity, intensity_params["medium"])
        
        # Add tracking errors (horizontal lines)
        for _ in range(params["tracking"]):
            y = random.randint(0, height - 1)
            width_shift = random.randint(-10, 10)
            
            if width_shift != 0:
                img_array[y] = np.roll(img_array[y], width_shift, axis=0)
        
        # Add chroma noise (color bleeding)
        chroma_noise = np.random.normal(0, params["chroma"] * 50, (height, width, 3))
        img_array = np.clip(img_array + chroma_noise, 0, 255)
        
        # Add vertical sync issues
        if random.random() < 0.3:  # 30% chance of vertical sync issues
            sync_shift = random.randint(-20, 20)
            img_array = np.roll(img_array, sync_shift, axis=0)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _add_digital_noise(self, img: Image.Image, colors: dict, intensity: float = 0.05):
        """Add digital noise pattern to image"""
        width, height = img.size
        pixels = img.load()
        
        for _ in range(int(width * height * intensity)):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Random color from scheme
            noise_color = random.choice([colors["primary"], colors["secondary"], colors["accent"]])
            alpha = random.randint(10, 50)
            
            # Blend with existing pixel
            existing = pixels[x, y]
            blended = tuple(min(255, int(existing[i] + noise_color[i] * alpha / 255)) for i in range(3))
            pixels[x, y] = blended
    
    def _add_circuit_patterns(self, img: Image.Image, colors: dict):
        """Add circuit-like patterns to background"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Draw random circuit lines
        for _ in range(20):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            
            color = colors["secondary"]
            draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
            
            # Add junction points
            if random.random() < 0.3:
                draw.ellipse([x1-3, y1-3, x1+3, y1+3], fill=colors["accent"])
    
    def _draw_neon_circuits(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw neon circuit patterns"""
        neon_color = (0, 255, 65, 150)  # Semi-transparent green
        
        # Draw horizontal lines
        for y in range(0, height, height // 10):
            draw.line([(0, y), (width, y)], fill=neon_color, width=2)
        
        # Draw vertical lines
        for x in range(0, width, width // 15):
            draw.line([(x, 0), (x, height)], fill=neon_color, width=2)
        
        # Add circuit nodes
        for _ in range(20):
            x, y = random.randint(0, width), random.randint(0, height)
            draw.ellipse([x-5, y-5, x+5, y+5], fill=neon_color)
    
    def _draw_neon_grid(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw neon grid pattern"""
        neon_color = (0, 212, 255, 100)  # Semi-transparent cyan
        
        grid_size = min(width, height) // 20
        
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=neon_color, width=1)
        
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=neon_color, width=1)
    
    def _draw_neon_border(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw neon border"""
        neon_color = (255, 0, 100, 200)  # Semi-transparent pink
        
        # Outer border
        draw.rectangle([10, 10, width-10, height-10], outline=neon_color, width=3)
        
        # Inner border
        draw.rectangle([20, 20, width-20, height-20], outline=neon_color, width=2)
        
        # Corner accents
        corner_size = 50
        corners = [(20, 20), (width-70, 20), (20, height-70), (width-70, height-70)]
        
        for x, y in corners:
            draw.rectangle([x, y, x+corner_size, y+corner_size], outline=neon_color, width=3)
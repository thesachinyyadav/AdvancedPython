import dearpygui.dearpygui as dpg
import numpy as np
import math
from PIL import Image, ImageDraw
import io
import requests
from urllib.request import urlopen
import os

class WorldMapVisualization:
    def __init__(self):
        self.width = 1200
        self.height = 600
        self.world_map_texture = None
        self.b2_bomber_texture = None
        
        # Strategic locations (longitude, latitude)
        self.locations = {
            "Iran": (53.688, 32.4279),  # Tehran
            "USA_Diego_Garcia": (72.4131, -7.3167),  # Diego Garcia Base
            "USA_Guam": (144.7937, 13.4443),  # Andersen AFB Guam
            "USA_Qatar": (51.5310, 25.2760),  # Al Udeid Air Base
            "USA_Turkey": (35.4264, 39.0494),  # Incirlik Air Base
            "USA_Kuwait": (47.9774, 29.3759),  # Ali Al Salem Air Base
        }
        
        # Attack routes (from, to, route_name)
        self.attack_routes = [
            ("USA_Diego_Garcia", "Iran", "Diego Garcia Route"),
            ("USA_Guam", "Iran", "Pacific Route"),
            ("USA_Qatar", "Iran", "Gulf Route"),
            ("USA_Turkey", "Iran", "Northern Route"),
            ("USA_Kuwait", "Iran", "Direct Gulf Route"),
        ]
        
    def lon_lat_to_pixel(self, lon, lat):
        """Convert longitude/latitude to pixel coordinates"""
        x = int((lon + 180) * self.width / 360)
        y = int((90 - lat) * self.height / 180)
        return x, y
    
    def create_world_map_texture(self):
        """Create a simple world map texture"""
        # Create a basic world map
        img = Image.new('RGB', (self.width, self.height), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw continents (simplified)
        continents = [
            # North America
            [(40, 150), (200, 100), (250, 150), (220, 250), (150, 280), (100, 200)],
            # South America
            [(180, 350), (220, 320), (240, 400), (200, 500), (160, 480), (150, 380)],
            # Europe
            [(450, 120), (520, 100), (540, 140), (500, 160), (460, 150)],
            # Africa
            [(480, 200), (550, 180), (580, 300), (560, 450), (500, 470), (460, 350), (470, 250)],
            # Asia
            [(550, 80), (750, 60), (900, 100), (950, 200), (900, 250), (700, 280), (600, 200), (570, 120)],
            # Australia
            [(800, 400), (900, 380), (920, 420), (880, 450), (820, 440)],
        ]
        
        for continent in continents:
            draw.polygon(continent, fill='darkgreen', outline='black')
        
        # Convert to bytes for DearPyGui
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    def create_b2_bomber_texture(self):
        """Create a simple B2 bomber silhouette"""
        size = 64
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw B2 bomber shape (triangular stealth design)
        bomber_points = [
            (size//2, size//8),      # nose
            (size//8, size*3//4),    # left wing tip
            (size//2, size*5//8),    # center back
            (size*7//8, size*3//4),  # right wing tip
        ]
        
        draw.polygon(bomber_points, fill='black', outline='red', width=2)
        
        # Convert to bytes for DearPyGui
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    def setup_dpg(self):
        """Setup DearPyGui"""
        dpg.create_context()
        
        # Create textures
        map_data = self.create_world_map_texture()
        bomber_data = self.create_b2_bomber_texture()
        
        with dpg.texture_registry():
            self.world_map_texture = dpg.add_raw_texture(
                width=self.width, 
                height=self.height, 
                default_value=map_data, 
                format=dpg.mvFormat_Float_rgba
            )
            
            self.b2_bomber_texture = dpg.add_raw_texture(
                width=64, 
                height=64, 
                default_value=bomber_data, 
                format=dpg.mvFormat_Float_rgba
            )
    
    def draw_attack_routes(self, draw_list):
        """Draw attack routes on the map"""
        colors = [
            [255, 0, 0, 255],    # Red
            [0, 255, 0, 255],    # Green
            [0, 0, 255, 255],    # Blue
            [255, 255, 0, 255],  # Yellow
            [255, 0, 255, 255],  # Magenta
        ]
        
        for i, (from_loc, to_loc, route_name) in enumerate(self.attack_routes):
            from_coords = self.locations[from_loc]
            to_coords = self.locations[to_loc]
            
            from_x, from_y = self.lon_lat_to_pixel(from_coords[0], from_coords[1])
            to_x, to_y = self.lon_lat_to_pixel(to_coords[0], to_coords[1])
            
            # Draw route line
            color = colors[i % len(colors)]
            dpg.draw_line(draw_list, [from_x, from_y], [to_x, to_y], 
                         color=color, thickness=3)
            
            # Draw direction arrow
            dx = to_x - from_x
            dy = to_y - from_y
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                # Normalize
                dx /= length
                dy /= length
                
                # Arrow head
                arrow_length = 20
                arrow_x = to_x - dx * arrow_length
                arrow_y = to_y - dy * arrow_length
                
                # Arrow wings
                perp_x = -dy * 10
                perp_y = dx * 10
                
                arrow_points = [
                    [to_x, to_y],
                    [arrow_x + perp_x, arrow_y + perp_y],
                    [arrow_x - perp_x, arrow_y - perp_y]
                ]
                
                for j in range(len(arrow_points)):
                    next_j = (j + 1) % len(arrow_points)
                    dpg.draw_line(draw_list, arrow_points[j], arrow_points[next_j], 
                                 color=color, thickness=2)
    
    def draw_locations(self, draw_list):
        """Draw strategic locations on the map"""
        for loc_name, (lon, lat) in self.locations.items():
            x, y = self.lon_lat_to_pixel(lon, lat)
            
            if loc_name == "Iran":
                # Draw target (Iran) as a red circle
                dpg.draw_circle(draw_list, [x, y], 15, color=[255, 0, 0, 255], 
                               fill=[255, 100, 100, 128], thickness=3)
                dpg.draw_text(draw_list, [x + 20, y - 10], "IRAN (TARGET)", 
                             color=[255, 0, 0, 255], size=12)
            else:
                # Draw US bases as blue squares
                dpg.draw_rectangle(draw_list, [x-8, y-8], [x+8, y+8], 
                                 color=[0, 0, 255, 255], fill=[100, 100, 255, 128], 
                                 thickness=2)
                dpg.draw_text(draw_list, [x + 15, y - 5], loc_name.replace("USA_", ""), 
                             color=[0, 0, 255, 255], size=10)
    
    def draw_bombers(self, draw_list):
        """Draw B2 bombers at strategic locations"""
        bomber_locations = ["USA_Diego_Garcia", "USA_Guam", "USA_Qatar"]
        
        for loc_name in bomber_locations:
            if loc_name in self.locations:
                lon, lat = self.locations[loc_name]
                x, y = self.lon_lat_to_pixel(lon, lat)
                
                # Draw bomber icon
                dpg.draw_image(draw_list, self.b2_bomber_texture, 
                              [x-16, y-16], [x+16, y+16])
    
    def create_main_window(self):
        """Create the main window with the map"""
        with dpg.window(label="B2 Bomber Strategic Attack Routes to Iran", 
                       width=self.width + 50, height=self.height + 100):
            
            # Information panel
            dpg.add_text("B2 BOMBER STRATEGIC ANALYSIS", color=[255, 255, 0])
            dpg.add_text("Potential Attack Routes to Iran from US Military Bases")
            dpg.add_separator()
            
            # Legend
            with dpg.group(horizontal=True):
                dpg.add_text("Legend: ", color=[255, 255, 255])
                dpg.add_text("■ US Bases", color=[0, 0, 255])
                dpg.add_text("● Iran (Target)", color=[255, 0, 0])
                dpg.add_text("✈ B2 Bombers", color=[255, 255, 255])
            
            dpg.add_separator()
            
            # Map canvas
            with dpg.drawlist(width=self.width, height=self.height):
                # Draw world map background
                dpg.draw_image(self.world_map_texture, [0, 0], [self.width, self.height])
                
                # Draw attack routes
                self.draw_attack_routes(dpg.last_item())
                
                # Draw locations
                self.draw_locations(dpg.last_item())
                
                # Draw bombers
                self.draw_bombers(dpg.last_item())
            
            dpg.add_separator()
            
            # Strategic analysis
            dpg.add_text("STRATEGIC ANALYSIS:", color=[255, 255, 0])
            
            analysis_text = """
1. DIEGO GARCIA ROUTE (Red): Longest range, requires multiple air-to-air refueling
   - Distance: ~3,500 miles | Flight Time: ~7-8 hours | Refueling: 2-3 times
   
2. PACIFIC ROUTE FROM GUAM (Green): Extremely long, crosses entire Asia
   - Distance: ~6,000 miles | Flight Time: ~12+ hours | Refueling: 4-5 times
   
3. GULF ROUTE FROM QATAR (Blue): Shortest and most direct
   - Distance: ~600 miles | Flight Time: ~1.5 hours | Refueling: None required
   
4. NORTHERN ROUTE FROM TURKEY (Yellow): Medium range, crosses Iraq
   - Distance: ~800 miles | Flight Time: ~2 hours | Refueling: None required
   
5. DIRECT GULF FROM KUWAIT (Magenta): Very short and direct
   - Distance: ~400 miles | Flight Time: ~1 hour | Refueling: None required

OPTIMAL ROUTES: Qatar or Kuwait bases provide the most efficient attack vectors
with minimal refueling requirements and maximum stealth effectiveness.
            """
            
            dpg.add_text(analysis_text, wrap=self.width - 20)

def main():
    """Main function to run the visualization"""
    app = WorldMapVisualization()
    app.setup_dpg()
    
    app.create_main_window()
    
    dpg.create_viewport(title="B2 Bomber Strategic Analysis", width=1300, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    
    dpg.set_primary_window(dpg.last_item(), True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
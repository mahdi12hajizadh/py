import tkinter as tk
from models.shapes import Shape, ShapeType
from models.arrows import Arrow

class CanvasManager:
    def __init__(self, flowchart):
        self.flowchart = flowchart
        self.canvas = None
        self.selected_item = None
        self.dragging = False
        self.drag_offset = (0, 0)
        self.arrow_start = None
        self.state_manager = None
        self.drag_data = {"item": None, "x": 0, "y": 0, "shape": None}
        
    def set_canvas(self, canvas):
        self.canvas = canvas
        self.render()
        
    def create_shape(self, shape_type, x, y):
        """ایجاد شکل جدید در کانواس"""
        print(f"Creating shape: {shape_type} at ({x}, {y})")
        shape = Shape(shape_type, x, y)
        self.flowchart.add_node(shape)
        self._save_state()
        self.render()
        return shape
        
    def render(self):
        """رندر مجدد همه اشکال و فلش‌ها"""
        if not self.canvas:
            return
            
        print(f"Rendering: {len(self.flowchart.nodes)} nodes")
        self.canvas.delete("all")
        
        # رسم فلش‌ها
        for edge in self.flowchart.edges:
            self._draw_arrow(edge)
            
        # رسم شکل‌ها
        for node in self.flowchart.nodes:
            self._draw_shape(node)
            
    def _draw_shape(self, shape):
        """رسم یک شکل با tag مناسب برای جابجایی"""
        if not self.canvas:
            return
            
        x, y = shape.position
        width, height = 120, 60
        
        shape_type = shape.type
        color = self._get_shape_color(shape_type)
        
        # ایجاد شکل با tag درست - اضافه کردن "shape" به tags
        if shape_type == ShapeType.START:
            item = self.canvas.create_oval(
                x, y, x + width, y + height,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )
        elif shape_type == ShapeType.PROCESS:
            item = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )
        elif shape_type == ShapeType.DECISION:
            points = [
                x + width//2, y,
                x + width, y + height//2,
                x + width//2, y + height,
                x, y + height//2
            ]
            item = self.canvas.create_polygon(
                *points,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )
        elif shape_type == ShapeType.INPUT_OUTPUT:
            points = [
                x + 20, y,
                x + width - 20, y,
                x + width, y + height,
                x, y + height
            ]
            item = self.canvas.create_polygon(
                *points,
                fill=color, outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )
        else:
            item = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill="#D3D3D3", outline="black", width=2,
                tags=("draggable", "shape", f"shape_{shape.id}")
            )
            
        # متن شکل
        text_item = self.canvas.create_text(
            x + width//2, y + height//2,
            text=shape.text or "Shape",
            font=("Arial", 10, "bold"),
            fill="black",
            tags=("draggable", "text", f"text_{shape.id}")
        )
        
        # ذخیره آیتم‌ها در shape برای جابجایی
        shape.items = [item, text_item]
        
    def _draw_arrow(self, edge):
        """رسم فلش بین دو شکل"""
        if not self.canvas:
            return
            
        from_shape = self.flowchart.get_node(edge.from_id)
        to_shape = self.flowchart.get_node(edge.to_id)
        
        if not from_shape or not to_shape:
            return
            
        from_x = from_shape.position[0] + 60
        from_y = from_shape.position[1] + 30
        to_x = to_shape.position[0] + 60
        to_y = to_shape.position[1] + 30
        
        self.canvas.create_line(
            from_x, from_y, to_x, to_y,
            arrow=tk.LAST, width=2, fill="white", 
            arrowshape=(10, 12, 5), tags="arrow"
        )
        
    def _get_shape_color(self, shape_type):
        colors = {
            ShapeType.START: "#90EE90",
            ShapeType.PROCESS: "#87CEEB",
            ShapeType.DECISION: "#FFD700",
            ShapeType.INPUT_OUTPUT: "#FFB6C1",
        }
        return colors.get(shape_type, "#D3D3D3")
        
    def select_item(self, x, y):
        """انتخاب یک شکل با کلیک"""
        if not self.canvas:
            return False
            
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        for item in items:
            tags = self.canvas.gettags(item)
            if "shape" in tags:
                self.selected_item = item
                self.canvas.itemconfig(item, outline="red", width=3)
                return True
        return False
        
    def deselect_all(self):
        """لغو انتخاب همه اشکال"""
        if self.selected_item:
            try:
                self.canvas.itemconfig(self.selected_item, outline="black", width=2)
            except:
                pass
            self.selected_item = None
            
    def move_shape(self, shape_id, dx, dy):
        """جابجایی روان شکل - بدون رندر مجدد"""
        shape = self.flowchart.get_node(shape_id)
        if not shape:
            return
            
        # آپدیت موقعیت در مدل
        old_x, old_y = shape.position
        new_x = old_x + dx
        new_y = old_y + dy
        shape.position = (new_x, new_y)
        
        # جابجایی آیتم‌های کانواس
        if hasattr(shape, 'items'):
            for item in shape.items:
                try:
                    self.canvas.move(item, dx, dy)
                except:
                    pass
        
        # به‌روزرسانی فلش‌های متصل
        self.update_arrows_for_shape(shape)
            
    def update_arrows_for_shape(self, shape):
        """به‌روزرسانی فلش‌های متصل به شکل"""
        if not self.canvas:
            return
            
        # پیدا کردن فلش‌های متصل به این شکل
        for edge in self.flowchart.edges:
            if edge.from_id == shape.id or edge.to_id == shape.id:
                # حذف فلش قدیمی
                items_to_delete = self.canvas.find_withtag(f"arrow_{edge.id}")
                for item in items_to_delete:
                    self.canvas.delete(item)
                
                # رسم فلش جدید
                self._draw_arrow(edge)
            
    def add_arrow(self, from_id, to_id):
        """اضافه کردن فلش بین دو شکل"""
        print(f"Adding arrow from {from_id} to {to_id}")
        
        if from_id and to_id and from_id != to_id:
            # چک کن فلش تکراری نباشه
            for edge in self.flowchart.edges:
                if edge.from_id == from_id and edge.to_id == to_id:
                    print("Arrow already exists!")
                    return None
                    
            edge = Arrow(from_id, to_id)
            self.flowchart.add_edge(edge)
            self._save_state()
            self.render()
            print(f"Arrow added successfully")
            return edge
        print("Invalid arrow: from_id or to_id is None or same")
        return None
        
    def delete_selected(self):
        """حذف شکل انتخاب شده"""
        if self.selected_item:
            tags = self.canvas.gettags(self.selected_item)
            for tag in tags:
                if tag.startswith("shape_"):
                    shape_id = tag.replace("shape_", "")
                    self.flowchart.remove_node(shape_id)
                    
                    edges_to_remove = []
                    for edge in self.flowchart.edges:
                        if edge.from_id == shape_id or edge.to_id == shape_id:
                            edges_to_remove.append(edge)
                    for edge in edges_to_remove:
                        self.flowchart.remove_edge(edge)
                    
                    self._save_state()
                    self.render()
                    self.selected_item = None
                    return True
        return False
        
    def _save_state(self):
        """ذخیره وضعیت برای Undo"""
        try:
            if self.state_manager:
                self.state_manager.save_state()
                return True
            elif self.canvas:
                master = self.canvas.master
                for _ in range(10):
                    if hasattr(master, 'state_manager'):
                        master.state_manager.save_state()
                        return True
                    if hasattr(master, 'master'):
                        master = master.master
                    else:
                        break
            return False
        except Exception as e:
            print(f"Error saving state: {e}")
            return False
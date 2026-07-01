from models.shapes import ShapeType

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
        self.visited_nodes = set()
        self.flowchart = None
        
    def generate(self, flowchart):
        """Generate Python code from flowchart"""
        self.flowchart = flowchart
        self.code_lines = []
        self.visited_nodes = set()
        self.indent_level = 0
        
        if not flowchart.nodes:
            return "# No shapes to generate code from"
            
        # Find start node
        start_nodes = [n for n in flowchart.nodes if n.type == ShapeType.START]
        if not start_nodes:
            return "# No start node found"
            
        start_node = start_nodes[0]
        
        # Add header
        self.code_lines.append("# Generated code from FlowPy Studio")
        self.code_lines.append("")
        
        # Generate code from start node
        self._generate_from_node(start_node)
        
        return "\n".join(self.code_lines)
        
    def _generate_from_node(self, node):
        """Recursively generate code from a node"""
        if node.id in self.visited_nodes:
            return
            
        self.visited_nodes.add(node.id)
        
        # Get outgoing edges
        outgoing = [e for e in self.flowchart.edges if e.from_id == node.id]
        
        # Generate code for this node
        indent = "    " * self.indent_level
        
        if node.type == ShapeType.START:
            # Skip start node
            pass
            
        elif node.type == ShapeType.PROCESS:
            self.code_lines.append(f"{indent}{node.text}")
            
        elif node.type == ShapeType.INPUT_OUTPUT:
            # Handle input/output
            if "input" in node.text.lower():
                self.code_lines.append(f"{indent}{node.text}")
            else:
                self.code_lines.append(f"{indent}print({node.text})")
                
        elif node.type == ShapeType.DECISION:
            # Generate if statement
            condition = node.text
            self.code_lines.append(f"{indent}if {condition}:")
            self.indent_level += 1
            
            # Find true branch (first edge)
            if outgoing:
                true_edge = outgoing[0]
                true_node = self.flowchart.get_node(true_edge.to_id)
                if true_node:
                    self._generate_from_node(true_node)
                    
            self.indent_level -= 1
            
            # Find false branch (second edge)
            if len(outgoing) > 1:
                false_edge = outgoing[1]
                self.code_lines.append(f"{indent}else:")
                self.indent_level += 1
                false_node = self.flowchart.get_node(false_edge.to_id)
                if false_node:
                    self._generate_from_node(false_node)
                self.indent_level -= 1
                
        # Process outgoing edges (for non-decision nodes)
        if node.type != ShapeType.DECISION:
            for edge in outgoing:
                next_node = self.flowchart.get_node(edge.to_id)
                if next_node:
                    self._generate_from_node(next_node) 

import xml.etree.ElementTree as ET
import random
import string
from datetime import datetime, timezone

class DrawioRack():
    def __init__(self):
        self._createBaseElement()
        self.firstRackX = 120
        self.firstRackY = 60
        self.rackMarginTop = 21
        self.rackMarginBottom = 22
        
        self.rackSpace = 120

        self.rackUnitHeight = 15
        self.rackWidth = 204

        self.rackTable = {}

    def saveToFile(self):
        tree = ET.ElementTree(self.root)
        tree.write("rack_diagram.drawio", encoding="utf-8", xml_declaration=True)
        print("Draw.io 文件已生成：rack_diagram.drawio")

    def _generate_random_id(self, length = 8):
        characters = string.ascii_letters + string.digits
        return '' . join(random.choice(characters) for _ in range(length))

    def _createBaseElement(self):
        self.root = ET.Element("mxfile")
        self.root.set("host", "lszhang.com")
        now = datetime.now(timezone.utc)
        iso_format = now.replace(microsecond=0).isoformat()
        iso_format_z = iso_format.replace("+00:00", "Z")
        self.root.set("modified", iso_format_z)
        self.root.set("agent", "Python Script")
        self.root.set("version", "26.0.9")
        
        diagram = ET.SubElement(self.root, "diagram")
        diagram.set("name", "Rack Diagram")
        diagram.set("id", "rack-diagram")

        mx_graph_model = ET.SubElement(diagram, "mxGraphModel")
        mx_graph_model.set("dx", "1100")
        mx_graph_model.set("dy", "810")
        mx_graph_model.set("grid", "1")
        mx_graph_model.set("gridSize", "5")
        mx_graph_model.set("guides", "1")
        mx_graph_model.set("tooltips", "1")
        mx_graph_model.set("connect", "1")
        mx_graph_model.set("arrows", "1")
        mx_graph_model.set("fold", "1")
        mx_graph_model.set("page", "1")
        mx_graph_model.set("pageScale", "1")
        mx_graph_model.set("pageWidth", "1169")
        mx_graph_model.set("pageHeight", "827")
        mx_graph_model.set("math", "0")
        mx_graph_model.set("shadow", "0")

        self.root_element = ET.SubElement(mx_graph_model, "root")

        id0 = ET.SubElement(self.root_element, "mxCell")
        id0.set("id", "0")

        id1 = ET.SubElement(self.root_element, "mxCell")
        id1.set("id", "1")
        id1.set("parent", "0")

    def createRack(self, rackName = "Rack", unitCount = 42):
        # 计算这个机柜应该在位置
        rackCountInDraw = len(self.rackTable)
        rackX = self.firstRackX + rackCountInDraw * (self.rackWidth + self.rackSpace)
        rackY = self.firstRackY
        
        random_id = "rack_" + self._generate_random_id()
        self.rackTable[rackName] = [random_id, unitCount]
        rack = ET.SubElement(self.root_element, "mxCell")
        rack.set("id", random_id)
        rack.set("value", rackName)
        style = "strokeColor=#666666;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;outlineConnect=0;shadow=0;dashed=0;shape=mxgraph.rackGeneral.rackCabinet3;fillColor2=#f4f4f4;container=1;collapsible=0;childLayout=rack;allowGaps=1;marginLeft=33;marginRight=9;"
        style = style + "marginTop=" + str(self.rackMarginTop) + ";marginBottom=" + str(self.rackMarginBottom) + ";textColor=#666666;numDisp=descend;"
        style = style + "rackUnitSize=" + str(self.rackUnitHeight) + ";"
        rack.set("style", style)
        rack.set("vertex", "1")
        rack.set("parent", "1")
        rack_geometry = ET.SubElement(rack, "mxGeometry")
        rack_geometry.set("x", str(rackX))
        rack_geometry.set("y", str(rackY))
        rack_geometry.set("width", str(self.rackWidth))
        rackHeight = self.rackUnitHeight * unitCount + 43
        rack_geometry.set("height", str(rackHeight))
        rack_geometry.set("as", "geometry")

    def createServer(self, serverName, rackName, floorInRack, height):
        # 检查机柜是否已经存在
        if rackName not in self.rackTable:
            self.createRack(rackName)
        server = ET.SubElement(self.root_element, "mxCell")
        server.set("id", "server_" + self._generate_random_id())
        server.set("value", serverName)
        style = "strokeColor=#666666;html=1;labelPosition=right;align=left;spacingLeft=15;shadow=0;dashed=0;outlineConnect=0;"
        if height == 1:
            style = style + "shape=mxgraph.rack.general.1u_rack_server;"
        else:
            style = style + "shape=mxgraph.rack.general.2u_rack_server;"
        server.set("style", style)
        server.set("vertex", "1")
        server_geometry = ET.SubElement(server, "mxGeometry")
        server_geometry.set("x", "33")
        thisRackUnitCount = self.rackTable[rackName][1]
        y = self.rackMarginTop + (thisRackUnitCount - floorInRack - height + 1) * self.rackUnitHeight
        server_geometry.set("y", str(y))
        server_geometry.set("width", "162")
        server_geometry.set("height", str(height * self.rackUnitHeight))
        server_geometry.set("as", "geometry")

        server.set("parent", self.rackTable[rackName][0])

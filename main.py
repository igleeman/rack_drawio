from lib_rack_drawio import DrawioRack
import csv

racks = []
with open('racks.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        try:
            height = int(row['机柜高度'].strip())
        except ValueError:
            height = 42  # 或者设置为其他默认值
            
        rack_info = {
            'RackName': row['机柜名'].strip(),
            'RackHeight': height
        }
        racks.append(rack_info)

servers = []
with open('servers.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        try:
            height = int(row['高度'].strip())
        except ValueError:
            height = 1  # 或者设置为其他默认值
        try:
            unit = int(row['机柜内位置'].strip())
        except ValueError:
            unit = 1  # 或者设置为其他默认值
            
        server_info = {
            'ServerName': row['服务器名'].strip(),
            'Rack': row['所在机柜'].strip(),
            'Unit': unit,
            'Height': height
        }
        servers.append(server_info)

drawio = DrawioRack()

for rack in racks:
    drawio.createRack(rack['RackName'], rack['RackHeight'])

for server in servers:
    drawio.createServer(server['ServerName'], server['Rack'], server['Unit'], server['Height'])

drawio.saveToFile()

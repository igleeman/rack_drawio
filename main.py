from lib_rack_drawio import DrawioRack
import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process racks and servers CSV files.")
    parser.add_argument('-r', '--racks', help="Path to the racks CSV file", default='racks.csv')
    parser.add_argument('-s', '--servers', help="Path to the servers CSV file", default='servers.csv')
    parser.add_argument('-o', '--output', help="Path to the output file", default='datacenter.drawio')
    args = parser.parse_args()

    try:
        racks = []
        with open(args.racks, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    height = int(row['机柜高度'].strip())
                except ValueError:
                    height = 42
                    
                rack_info = {
                    'RackName': row['机柜名'].strip(),
                    'RackHeight': height
                }
                racks.append(rack_info)
    except FileNotFoundError:
        print(f"Error: The file {args.racks} does not exist.")

    try:
        servers = []
        with open(args.servers, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                def get_value(value, default = ''):
                    return default if value is None else value.strip()
                
                server_info = {
                    'ServerName': get_value(row.get('服务器名')),
                    'Rack': get_value(row.get('所在机柜')),
                    'Unit': int(get_value(row.get('机柜内位置'), '1')),
                    'Height': int(get_value(row.get('高度'), '1')),
                    'IP': get_value(row.get('IP')),
                    '用途': get_value(row.get('用途')),
                    '状态': get_value(row.get('状态'),),
                    '其他属性': get_value(row.get('其他属性'))
                }
                servers.append(server_info) 
    except FileNotFoundError:
        print(f"Error: The file {args.servers} does not exist.")

    drawio = DrawioRack()

    for rack in racks:
        drawio.create_rack(rack['RackName'], rack['RackHeight'])

    for server in servers:
        drawio.create_server(server['ServerName'], server['Rack'], server['Unit'], server['Height'], server['IP'], server['用途'], server['状态'], server['其他属性'])

    drawio.save_to_file(args.output)

if __name__ == "__main__":
    main()
import asyncio
from bleak import BleakClient

address = "8c:aa:b5:84:db:52"
# 읽기/쓰기용 캐릭터리스틱 uuid
read_write_charcteristic_uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        # 서비스내에 있는 캐릭터리스틱 정보 보기
        for service in services:
            print(service)                
            print('\tuuid:', service.uuid)
            print('\tcharacteristic list:')
            for characteristic in service.characteristics:
                print('\t\t', characteristic)
                print('\t\tuuid:', characteristic.uuid)
                print('\t\tdescription :', characteristic.description)
                # ['write-without-response', 'write', 'read', 'notify']
                print('\t\tproperties :', characteristic.properties)
        
        # 읽기/쓰기 캐릭터리스틱 uuid를 이용해 데이터 읽기
        # 해당 캐릭터리스틱의 속성에는 read가 존재해야만 읽기가 가능하다.
        read_data = await client.read_gatt_char(read_write_charcteristic_uuid)
        # 읽근 데이터 출력
        print('read_data: ',read_data)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')


"""
#캐릭터리스틱을 통해 읽기
import asyncio
from bleak import BleakClient

address = "8c:aa:b5:84:db:52"
read_write_charcteristic_uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                # 각 캐릭터리스틱의 uuid를 읽기용 캐릭터리스틱 uuid와 비교
                if characteristic.uuid == read_write_charcteristic_uuid:
                    # 해당 캐릭터리스틱에 읽기 속성이 있는지 확인
                    if 'read' in characteristic.properties:
                        # 데이터 읽기
                        read_data = await client.read_gatt_char(characteristic)
                        print('read_data: ',read_data)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')
[출처] 파이썬(Python) - BLE 통신하기(블루투스 저전력) 3. 읽고 쓰기(read, write) 편 bleak|작성자 천동이
"""
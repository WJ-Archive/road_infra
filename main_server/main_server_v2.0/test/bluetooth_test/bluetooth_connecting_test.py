#기본 Connect 예제
import asyncio
from bleak import BleakClient

# 위에서 얻은 BLE 장치의 주소
address = "00:12:F3:30:41:C4"

# 장치와 연결해제시 발생하는 콜백 이벤트
def on_disconnect(client):
    print("Client with address {} got disconnected!".format(client.address))

async def run(address):
    # 장치 주소를 이용해 client 클래스 생성
    client = BleakClient(address)
    try:
        # 장치 연결 해제 콜백 함수 등록
        client.set_disconnected_callback(on_disconnect)
        # 장치 연결 시작
        await client.connect()
        print('connected')    
    except Exception as e:
        # 연결 실패시 발생
        print('error: ', e, end='')        
    finally:
        print('start disconnect')
        # 장치 연결 해제
        await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')

"""
#BLE 서비스정보 얻기
import asyncio
from bleak import BleakClient

address = "8c:aa:b5:84:db:52"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        # 연결한 장치의 서비스 정보 얻기
        services = await client.get_services()
        # 리턴 받은 services의 타입 확인
        print("Services:", type(services))
        # 루프를 돌면서 출력
        for service in services:
            print(service)
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')
"""

"""
#캐릭터리스틱 정보 얻기
import asyncio
from bleak import BleakClient

address = "8c:aa:b5:84:db:52"
async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            print(service)             
            # 서비스의 UUID 출력   
            print('\tuuid:', service.uuid)
            print('\tcharacteristic list:')
            # 서비스의 모든 캐릭터리스틱 출력용
            for characteristic in service.characteristics:
                # 캐릭터리스틱 클래스 변수 전체 출력
                print('\t\t', characteristic)
                # UUID 
                print('\t\tuuid:', characteristic.uuid)
                # decription(캐릭터리스틱 설명)
                print('\t\tdescription :', characteristic.description)
                # 캐릭터리스틱의 속성 출력
                # 속성 값 : ['write-without-response', 'write', 'read', 'notify']
                print('\t\tproperties :', characteristic.properties)

    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')
[출처] 파이썬(Python) - BLE 통신하기(블루투스 저전력) 2. 연결(connect) 편 bleak|작성자 천동이

"""
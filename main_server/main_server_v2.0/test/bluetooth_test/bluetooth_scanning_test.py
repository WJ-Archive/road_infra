#pip install bleak (파이썬 3.9.6 설치 확인)

#문제점 . Thread랑 asyncio 를 같이 써도 문제 없을지 걱정되긴함

import asyncio # 비동기화 모듈
from bleak import BleakScanner # BLE 검색 모듈


# 비동기 형태로 BLE 장치 검색
async def run():
    # 검색 시작 (검색이 종료될때까지 대기)
    # 기본 검색 시간은 5초이다.
    devices = await BleakScanner.discover()
    # 검색된 장치들 리스트 출력
    for d in devices:
        print(d)

# 비동기 이벤트 루프 생성
loop = asyncio.get_event_loop()
# 비동기 형태로 run(검색)함수 실행
# 완료될때까지 대기
loop.run_until_complete(run())


"""
import asyncio
from bleak import BleakScanner

async def run():
    # 검색 시작(with 사용)
    async with BleakScanner() as scanner:
        # 5초간 대기
        await asyncio.sleep(5.0)
        # 검색된 장치 얻어오기
        devices = await scanner.get_discovered_devices()
    # 리스트 출력
    for d in devices:
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
"""


"""
#콜백(callback)을 등록 후 장치 검색(start)/중지(stop)로 장치 검색

import asyncio
from bleak import BleakScanner

'''
 장치가 검색되면 호출되는 콜백 함수
 device: 장치 정보(bleak.backends.device.BLEDevice)
 advertisement_data: 장치에서 송출하는 데이터
'''
def detection_callback(device, advertisement_data):
    # 장치 주소와 신호세기, 그리고 어드버타이징 데이터를 출력한다.
    print(device.address, "RSSI:", device.rssi, advertisement_data)

async def run():
    # 검색 클래스 생성
    scanner = BleakScanner()
    # 콜백 함수 등록
    scanner.register_detection_callback(detection_callback)
    # 검색 시작
    await scanner.start()
    # 5초간 대기 이때 검색된 장치들이 있다면 등록된 콜백함수가 호출된다.
    await asyncio.sleep(5.0)
    # 검색 중지
    await scanner.stop()
    # 지금까지 찾은 장치들 가져오기
    devices = await scanner.get_discovered_devices()
    # 지금까지 찾은 장치 리스트 출력
    for d in devices:
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

#[출처] 파이썬(Python) - BLE 통신하기(블루투스 저전력) 1. 검색(scan) 편 bleak|작성자 천동이
"""
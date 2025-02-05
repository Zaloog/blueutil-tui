import pytest


@pytest.fixture
def test_device_output():
    return """[
    {
        "address":"f0-04-e1-db-ea-42",
        "recentAccessDate":"2025-02-05T18:22:14+01:00",
        "paired":true,
        "RSSI":0,
        "rawRSSI":0,
        "favourite":false,
        "connected":true,
        "name":"AirPods Pro",
        "slave":false
        },
    {
        "address":"d8-b2-20-49-83-7b",
        "recentAccessDate":"2025-02-05T18:22:14+01:00",
        "favourite":false,
        "name":"Air75 BT5.0 ",
        "connected":false,
        "paired":true
        },
    {
        "address":"dd-a5-06-a5-dd-24",
        "recentAccessDate":"2025-02-05T18:22:14+01:00",
        "paired":true,
        "RSSI":0,
        "rawRSSI":0,
        "favourite":false,
        "connected":true,
        "name":"NuPhy Air75 V2-1",
        "slave":false
        }
]"""

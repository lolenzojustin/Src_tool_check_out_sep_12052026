# Lấy thông tin profile bằng API GPM
# import requests
# import json
# LOCAL_URL = "http://localhost:9495"  # Thay bằng Local URL của GPM nếu khác
# url = f"{LOCAL_URL}/api/v1/profiles"
# params = {
#     "page": 1,
#     "per_page": 30,
#     "search": "",
#     "sort": 0
# }
# try:
#     response = requests.get(url, params=params, timeout=30)

#     print("Request URL:", response.url)
#     print("Status code:", response.status_code)

#     response.raise_for_status()

#     data = response.json()

#     print(json.dumps(data, indent=4, ensure_ascii=False))

# except requests.exceptions.RequestException as e:
#     print("Lỗi request API:", e)



#  Tạo profile mới bằng API GPM
# import requests
# import json
# BASE_URL = "http://localhost:9495"

# url = f"{BASE_URL}/api/v1/profiles/create"
# payload = {
#     "name": "Test profile from api",
#     "group_id": None,
#     "raw_proxy": "socks5://127.0.0.1:5000",
#     "browser_type": 1,
#     "browser_version": "147.0.7727.56",
#     "os_type": 1,
#     "custom_user_agent": None,
#     "task_bar_title": "abc",
#     "webrtc_mode": None,
#     "fixed_webrtc_public_ip": "",
#     "geolocation_mode": None,
#     "canvas_mode": None,
#     "client_rects_mode": None,
#     "webgl_image_mode": None,
#     "webgl_metadata_mode": None,
#     "audio_mode": None,
#     "font_mode": None,
#     "timezone_based_on_ip": True,
#     "timezone": None,
#     "is_language_based_on_ip": True,
#     "fixed_language": None
# }
# headers = {
#     "Content-Type": "application/json"
# }
# try:
#     response = requests.post(url, json=payload, headers=headers, timeout=30)
#     print("Status code:", response.status_code)
#     # print("Response:")
#     # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
# except Exception as e:
#     print("Lỗi:", e)



# Mở profile bằng API GPM
import requests
import json

API_URL = "http://localhost:9495"

PROFILE_ID = "0ecdd509-1a62-4987-9a50-9ca402ef32f1"  # Thay bằng UUID profile của bạn

url = f"{API_URL}/api/v1/profiles/start/{PROFILE_ID}"

params = {
    "remote_debugging_port": 40444,
    "window_scale": 0.8,
    "window_pos": "100,100",
    "window_size": "800,600",
    "addition_args": ""
}

try:
    response = requests.get(url, params=params, timeout=60)

    print("Status code:", response.status_code)

    try:
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception:
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Lỗi request API:", e)
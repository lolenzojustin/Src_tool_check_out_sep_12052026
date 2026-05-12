import requests
import time
import shutil
import os
import subprocess
API_URL = "http://127.0.0.1:18439"   # sửa theo port GPM của bạn
class Gpm:
    def __init__(self) -> None:
        pass
    def get_new_payload(self,proxy):
                
        payload = {
            "profile_name": "Check out sep",
            "group_name": "All",
            "browser_core": "chromium",
            "browser_name": "Chrome",
            "browser_version": "139.0.7258.139",
            "is_random_browser_version": False,
            "raw_proxy": proxy,               # IP:Port:User:Pass hoặc tm://API_KEY|True,False ...
            "startup_urls": "",            # "https://google.com,https://facebook.com"
            "is_masked_font": True,
            "is_noise_canvas": False,
            "is_noise_webgl": False,
            "is_noise_client_rect": False,
            "is_noise_audio_context": True,
            "is_random_screen": False,
            "is_masked_webgl_data": True,
            "is_masked_media_device": True,
            "is_random_os": False,
            "os": "Windows 11",
            "webrtc_mode": 2,              # 1: Off, 2: Base on IP
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/139.0.0.0 Safari/537.36"
        }
        return payload
    def get_new_payload_2(self):
                
        payload = {
            "profile_name": "Check out sep",
            "group_name": "All",
            "browser_core": "chromium",
            "browser_name": "Chrome",
            "browser_version": "139.0.7258.139",
            "is_random_browser_version": False,
            "raw_proxy": "",               # IP:Port:User:Pass hoặc tm://API_KEY|True,False ...
            "startup_urls": "",            # "https://google.com,https://facebook.com"
            "is_masked_font": True,
            "is_noise_canvas": False,
            "is_noise_webgl": False,
            "is_noise_client_rect": False,
            "is_noise_audio_context": True,
            "is_random_screen": False,
            "is_masked_webgl_data": True,
            "is_masked_media_device": True,
            "is_random_os": False,
            "os": "Windows 11",
            "webrtc_mode": 2,              # 1: Off, 2: Base on IP
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/139.0.0.0 Safari/537.36"
        }
        return payload    
    def create_profile(self,apiurl_Gpm,proxy):
        new_payload = self.get_new_payload(proxy)
        response = requests.post(
            apiurl_Gpm + "/api/v3/profiles/create",
            json=new_payload,
            timeout=30
        ).json()
        id_profile = response["data"]["id"]
        print("tạo id_profile là",id_profile)
        return id_profile
    def create_profile_2(self,apiurl_Gpm):
        new_payload = self.get_new_payload_2()
        response = requests.post(
            apiurl_Gpm + "/api/v3/profiles/create",
            json=new_payload,
            timeout=30
        ).json()
        id_profile = response["data"]["id"]
        print("tạo id_profile là",id_profile)
        return id_profile    
    def open_profile(self,apiurl_Gpm, id_profile, win_pos, win_size):
        # Thư mục chứa extension (có file manifest.json bên trong)
        extension_dir = r"C:\Users\PC\Desktop\nopecha"
        # extension_dir = r"C:\Users\PC\Desktop\dknlfmjaanfblgfdfebhijalfmhmjjjo"
        # Tham số truyền cho Chrome
        add_args = f'--load-extension="{extension_dir}"'
        params_open_profile = {
            "addination_args": add_args,
            # các param khác nếu muốn:
            "win_scale": 1.0,
            "win_pos": win_pos,
            "win_size": win_size,
        }

        url = f"{apiurl_Gpm}/api/v3/profiles/start/{id_profile}"

        response = requests.get(url, params=params_open_profile).json()

        # response = requests.post(API_URL+"/api/v3/profiles/start/"+id_profile+f"?win_scale=1.0&win_pos={win_pos}&win_size={win_size}",timeout=30).json()

        # response = requests.post(API_URL+"/api/v3/profiles/start/"+id_profile+f"?win_scale=1.0&win_pos={win_pos}&win_size={win_size}",timeout=30).json()
        # Lấy remote_debugging_address
        remote_debugging_address = response["data"]["remote_debugging_address"]
        return remote_debugging_address

    def close_profile(self,apiurl_Gpm,id_profile):
        response = requests.get(apiurl_Gpm+"/api/v3/profiles/close/"+id_profile,timeout=30).json()
    def update_profile(self,apiurl_Gpm,id_profile):
        response = requests.post(apiurl_Gpm+"/api/v3/profiles/update/"+id_profile,timeout=30).json()
    def delete_profile(self,apiurl_Gpm,id_profile):
        response = requests.get(apiurl_Gpm+"/api/v3/profiles/delete/"+id_profile+"?mode=2",timeout=30).json()
        print("xóa id_profile là",id_profile)    
# if __name__ == "__main__":
#     g = GpmApi()
#     # Bước 1: Tạo
#     id = g.create_profile()
#     print("đã tạo profile")
#     time.sleep(2)
#     # Bước 2: Mở để gologin tự tạo thư mục profile
#     g.open_profile(id_profile=id)
#     print("đã mở profile vừa tạo",)
#     time.sleep(2)
#     g.close_profile(id_profile=id)
#     print("đã đóng profile vừa tạo")
#     time.sleep(2)
#     g.update_profile(id_profile=id)
#     print("đã update profile vừa tạo")
#     time.sleep(2)
#     g.delete_profile(id_profile=id)
#     print("đã xóa profile vừa tạo")
#     time.sleep(1000)

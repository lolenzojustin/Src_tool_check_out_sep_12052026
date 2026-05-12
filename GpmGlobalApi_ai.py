from __future__ import annotations  # Cho phép dùng kiểu dữ liệu hiện đại và tránh lỗi forward reference

import socket  # Dùng để kiểm tra port local có đang trống hay không
import threading  # Dùng để tạo khóa chống trùng port khi chạy đa luồng
from typing import Any, Dict, Optional  # Dùng để khai báo kiểu dữ liệu cho code rõ ràng hơn
from urllib.parse import urlparse  # Dùng để tách host từ API URL

import requests  # Dùng để gửi request HTTP đến GPM Global API


API_URL = "http://localhost:9495"  # URL mặc định của GPM Global API trên máy local

DEBUG_PORT_START = 40444  # Port bắt đầu để tìm remote debugging port
DEBUG_PORT_END = 49999  # Port cuối để tìm remote debugging port
_NEXT_DEBUG_PORT = DEBUG_PORT_START  # Biến lưu port tiếp theo sẽ thử dùng
_PORT_LOCK = threading.Lock()  # Khóa chống nhiều luồng lấy trùng port cùng lúc


def _is_port_free(port: int) -> bool:  # Hàm kiểm tra một port có đang trống không
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Tạo socket TCP để test port
        try:  # Bắt đầu thử bind vào port
            sock.bind(("127.0.0.1", port))  # Thử chiếm port trên localhost
            return True  # Nếu bind được thì port đang trống
        except OSError:  # Nếu bind lỗi nghĩa là port đang được dùng
            return False  # Trả về False vì port không trống


def _get_free_debug_port() -> int:  # Hàm lấy một remote debugging port còn trống
    global _NEXT_DEBUG_PORT  # Cho phép sửa biến port tiếp theo ở phạm vi global

    with _PORT_LOCK:  # Khóa lại để tránh nhiều luồng lấy trùng port
        total_ports = DEBUG_PORT_END - DEBUG_PORT_START + 1  # Tính tổng số port có thể thử

        for _ in range(total_ports):  # Lặp qua toàn bộ dải port cho phép
            port = _NEXT_DEBUG_PORT  # Lấy port hiện tại để kiểm tra
            _NEXT_DEBUG_PORT += 1  # Tăng port lên để lần sau thử port tiếp theo

            if _NEXT_DEBUG_PORT > DEBUG_PORT_END:  # Nếu vượt quá port cuối
                _NEXT_DEBUG_PORT = DEBUG_PORT_START  # Quay lại port bắt đầu

            if _is_port_free(port):  # Kiểm tra port hiện tại có trống không
                return port  # Nếu trống thì trả về port này

    raise RuntimeError("Không tìm được remote_debugging_port còn trống.")  # Báo lỗi nếu không còn port trống


class Gpm:  # Class chính dùng để làm việc với GPM Global API
    def __init__(  # Hàm khởi tạo object Gpm
        self,  # Đại diện cho object hiện tại
        api_url: str = API_URL,  # API URL mặc định của GPM Global
        profile_name: str = "Check out sep",  # Tên profile mặc định khi tạo mới
        browser_version: str = "147.0.7727.56",  # Phiên bản trình duyệt mặc định
        timeout: int = 30,  # Thời gian chờ request tối đa tính bằng giây
    ) -> None:  # Hàm không trả về dữ liệu
        self.api_url = api_url.rstrip("/")  # Lưu API URL và xóa dấu / ở cuối nếu có
        self.profile_name = profile_name  # Lưu tên profile mặc định
        self.browser_version = browser_version  # Lưu phiên bản browser mặc định
        self.timeout = timeout  # Lưu timeout dùng cho request API

    def _base_url(self, apiurl_Gpm: Optional[str] = None) -> str:  # Hàm lấy base URL để gọi API
        base = (apiurl_Gpm or self.api_url or API_URL).strip().rstrip("/")  # Lấy URL ưu tiên từ tham số, sau đó đến self.api_url, cuối cùng là API_URL

        if not base:  # Kiểm tra URL có bị rỗng không
            raise ValueError("API URL đang rỗng. Ví dụ: http://localhost:9495")  # Báo lỗi nếu URL rỗng

        return base  # Trả về base URL hợp lệ

    def _host_from_apiurl(self, apiurl_Gpm: Optional[str] = None) -> str:  # Hàm lấy host từ API URL
        host = urlparse(self._base_url(apiurl_Gpm)).hostname or "127.0.0.1"  # Tách hostname từ URL, nếu không có thì dùng 127.0.0.1

        if host in ["localhost", "0.0.0.0"]:  # Nếu host là localhost hoặc 0.0.0.0
            return "127.0.0.1"  # Đổi về 127.0.0.1 để Playwright/CDP dễ kết nối

        return host  # Trả về host đã lấy được

    def _request(  # Hàm request chung để gọi GPM API
        self,  # Đại diện cho object hiện tại
        method: str,  # Method HTTP như GET hoặc POST
        url: str,  # URL API cần gọi
        strict: bool = True,  # Nếu True thì gặp success=False sẽ báo lỗi
        **kwargs,  # Nhận thêm params, json hoặc các tùy chọn request khác
    ) -> Dict[str, Any]:  # Trả về dữ liệu JSON dạng dictionary
        try:  # Bắt đầu gọi API và xử lý lỗi
            res = requests.request(method, url, timeout=self.timeout, **kwargs)  # Gửi HTTP request đến GPM API
            res.raise_for_status()  # Báo lỗi nếu HTTP status là 4xx hoặc 5xx
            data = res.json()  # Chuyển response JSON thành dictionary Python

        except requests.RequestException as e:  # Bắt lỗi khi gọi request thất bại
            raise RuntimeError(f"Lỗi gọi GPM Global API: {e}") from e  # Báo lỗi rõ ràng hơn

        except ValueError as e:  # Bắt lỗi khi response không phải JSON
            raise RuntimeError(f"GPM Global trả về không phải JSON: {res.text}") from e  # Báo lỗi kèm nội dung response

        if strict and isinstance(data, dict) and data.get("success") is False:  # Nếu bật strict và API trả success=False
            raise RuntimeError(f"GPM Global API báo lỗi: {data}")  # Báo lỗi API trả về

        return data  # Trả về dữ liệu JSON đã xử lý

    def _data(self, response_json: Dict[str, Any]) -> Any:  # Hàm lấy phần data trong response JSON
        return response_json.get("data")  # Trả về giá trị trong key data

    def get_new_payload(self, proxy: Optional[str] = "") -> Dict[str, Any]:  # Hàm tạo payload để tạo profile mới
        raw_proxy = "" if proxy in [None, "", "0", 0] else str(proxy).strip()  # Xử lý proxy rỗng thành chuỗi rỗng, còn lại thì ép sang string

        return {  # Trả về dictionary payload tạo profile
            "name": self.profile_name,  # Tên profile sẽ tạo
            "group_id": None,  # Không gán group_id, để mặc định
            "raw_proxy": raw_proxy,  # Proxy thô truyền vào profile
            "browser_type": 1,  # Chọn browser type là Chrome
            "browser_version": self.browser_version,  # Phiên bản browser dùng cho profile
            "os_type": 1,  # Chọn hệ điều hành Windows
            "custom_user_agent": None,  # Không set user agent tùy chỉnh
            "task_bar_title": self.profile_name,  # Tiêu đề hiển thị trên taskbar
            "webrtc_mode": None,  # Để GPM tự xử lý WebRTC mặc định
            "fixed_webrtc_public_ip": "",  # Không cố định IP WebRTC
            "geolocation_mode": None,  # Để GPM tự xử lý geolocation mặc định
            "canvas_mode": None,  # Để GPM tự xử lý canvas mặc định
            "client_rect_mode": None,  # Để GPM tự xử lý client rect mặc định
            "webgl_image_mode": None,  # Để GPM tự xử lý WebGL image mặc định
            "webgl_metadata_mode": None,  # Để GPM tự xử lý WebGL metadata mặc định
            "audio_mode": None,  # Để GPM tự xử lý audio fingerprint mặc định
            "font_mode": None,  # Để GPM tự xử lý font fingerprint mặc định
            "timezone_base_on_ip": True,  # Tự lấy timezone theo IP
            "timezone": None,  # Không set timezone thủ công
            "is_language_base_on_ip": True,  # Tự lấy ngôn ngữ theo IP
            "fixed_language": None,  # Không cố định ngôn ngữ thủ công
        }  # Kết thúc payload tạo profile

    def get_new_payload_2(self) -> Dict[str, Any]:  # Hàm tạo payload không dùng proxy
        return self.get_new_payload("")  # Gọi lại get_new_payload với proxy rỗng

    def list_profiles(  # Hàm lấy danh sách profile
        self,  # Đại diện cho object hiện tại
        apiurl_Gpm: Optional[str] = None,  # API URL tùy chỉnh nếu muốn dùng khác mặc định
        page: int = 1,  # Trang cần lấy
        per_page: int = 30,  # Số profile trên mỗi trang
        search: str = "",  # Từ khóa tìm kiếm profile
        sort: int = 0,  # Kiểu sắp xếp danh sách profile
    ) -> Dict[str, Any]:  # Trả về response dạng dictionary
        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles"  # Tạo URL API lấy danh sách profile

        params = {  # Tạo query params gửi lên API
            "page": page,  # Truyền số trang
            "per_page": per_page,  # Truyền số lượng profile mỗi trang
            "search": search,  # Truyền từ khóa tìm kiếm
            "sort": sort,  # Truyền kiểu sắp xếp
        }  # Kết thúc params

        return self._request("GET", url, params=params)  # Gọi API GET để lấy danh sách profile

    def get_profile(self, apiurl_Gpm: Optional[str], id_profile: str) -> Dict[str, Any]:  # Hàm lấy thông tin một profile theo ID
        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/{id_profile}"  # Tạo URL API lấy profile theo ID

        return self._request("GET", url)  # Gọi API GET để lấy thông tin profile

    def create_profile(self, apiurl_Gpm: Optional[str] = None, proxy: str = "") -> str:  # Hàm tạo profile mới có thể kèm proxy
        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/create"  # Tạo URL API tạo profile
        payload = self.get_new_payload(proxy)  # Tạo payload tạo profile với proxy truyền vào

        response_json = self._request("POST", url, json=payload)  # Gọi API POST để tạo profile
        data = self._data(response_json)  # Lấy phần data từ response

        if not isinstance(data, dict) or "id" not in data:  # Kiểm tra response có chứa id profile không
            raise RuntimeError(f"Không lấy được id_profile từ response: {response_json}")  # Báo lỗi nếu không lấy được id

        id_profile = data["id"]  # Lấy id profile vừa tạo
        print("Tạo id_profile là", id_profile)  # In id profile ra màn hình

        return id_profile  # Trả về id profile vừa tạo

    def create_profile_2(self, apiurl_Gpm: Optional[str] = None) -> str:  # Hàm tạo profile mới không dùng proxy
        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/create"  # Tạo URL API tạo profile
        payload = self.get_new_payload_2()  # Tạo payload không có proxy

        response_json = self._request("POST", url, json=payload)  # Gọi API POST để tạo profile
        data = self._data(response_json)  # Lấy phần data từ response

        if not isinstance(data, dict) or "id" not in data:  # Kiểm tra response có chứa id profile không
            raise RuntimeError(f"Không lấy được id_profile từ response: {response_json}")  # Báo lỗi nếu không lấy được id

        id_profile = data["id"]  # Lấy id profile vừa tạo
        print("Tạo id_profile là", id_profile)  # In id profile ra màn hình

        return id_profile  # Trả về id profile vừa tạo

    def update_profile(  # Hàm cập nhật profile
        self,  # Đại diện cho object hiện tại
        apiurl_Gpm: Optional[str] = None,  # API URL tùy chỉnh nếu muốn dùng khác mặc định
        id_profile: Optional[str] = None,  # ID profile cần cập nhật
        payload: Optional[Dict[str, Any]] = None,  # Dữ liệu cần cập nhật cho profile
    ) -> Dict[str, Any]:  # Trả về response dạng dictionary
        if not id_profile:  # Kiểm tra có truyền id_profile chưa
            raise ValueError("Thiếu id_profile")  # Báo lỗi nếu thiếu id_profile

        if payload is None:  # Nếu không truyền payload cập nhật
            print("Không truyền payload update_profile -> bỏ qua update.")  # Thông báo bỏ qua update

            return {  # Trả về response giả để code cũ không bị lỗi
                "success": True,  # Đánh dấu thành công
                "data": None,  # Không có dữ liệu trả về
                "message": "skip update because payload is None",  # Ghi rõ lý do bỏ qua update
            }  # Kết thúc response giả

        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/update/{id_profile}"  # Tạo URL API update profile

        return self._request("POST", url, json=payload)  # Gọi API POST để cập nhật profile

    def delete_profile(  # Hàm xóa profile
        self,  # Đại diện cho object hiện tại
        apiurl_Gpm: Optional[str] = None,  # API URL tùy chỉnh nếu muốn dùng khác mặc định
        id_profile: Optional[str] = None,  # ID profile cần xóa
        mode: str = "hard",  # Chế độ xóa, soft hoặc hard
    ) -> Dict[str, Any]:  # Trả về response dạng dictionary
        if not id_profile:  # Kiểm tra có truyền id_profile chưa
            raise ValueError("Thiếu id_profile")  # Báo lỗi nếu thiếu id_profile

        if mode not in ["soft", "hard"]:  # Kiểm tra mode có hợp lệ không
            raise ValueError("mode chỉ được là 'soft' hoặc 'hard'")  # Báo lỗi nếu mode sai

        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/delete/{id_profile}"  # Tạo URL API xóa profile

        response_json = self._request(  # Gọi API xóa profile
            "GET",  # Dùng method GET theo API của GPM
            url,  # Truyền URL xóa profile
            strict=False,  # Không bắt lỗi success=False để tránh crash khi GPM trả response không chuẩn
            params={"mode": mode},  # Truyền chế độ xóa soft hoặc hard
        )  # Kết thúc gọi API xóa profile

        print("Xóa id_profile là", id_profile)  # In id profile đã xóa ra màn hình

        return response_json  # Trả về response từ API

    def open_profile(  # Hàm mở profile và lấy remote debugging address
        self,  # Đại diện cho object hiện tại
        apiurl_Gpm: Optional[str] = None,  # API URL tùy chỉnh nếu muốn dùng khác mặc định
        id_profile: Optional[str] = None,  # ID profile cần mở
        win_pos: str = "100,100",  # Vị trí cửa sổ browser khi mở
        win_size: str = "800,600",  # Kích thước cửa sổ browser khi mở
        remote_debugging_port: Optional[int] = None,  # Port remote debugging muốn dùng
        window_scale: float = 1.0,  # Tỉ lệ scale cửa sổ browser
        addition_args: str = "",  # Tham số Chrome mở rộng nếu cần
    ) -> str:  # Trả về remote debugging address dạng host:port
        if not id_profile:  # Kiểm tra có truyền id_profile chưa
            raise ValueError("Thiếu id_profile")  # Báo lỗi nếu thiếu id_profile

        if not remote_debugging_port:  # Nếu chưa truyền remote debugging port
            remote_debugging_port = _get_free_debug_port()  # Tự lấy một port còn trống

        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/start/{id_profile}"  # Tạo URL API mở profile

        params = {  # Tạo params gửi lên API mở profile
            "remote_debugging_port": remote_debugging_port,  # Truyền port debug để Playwright/Selenium kết nối
            "window_scale": window_scale,  # Truyền tỉ lệ scale cửa sổ
            "window_pos": win_pos,  # Truyền vị trí cửa sổ
            "window_size": win_size,  # Truyền kích thước cửa sổ
            "addition_args": addition_args or "",  # Truyền tham số mở rộng cho browser nếu có
        }  # Kết thúc params

        response_json = self._request("GET", url, params=params)  # Gọi API GET để mở profile
        data = self._data(response_json)  # Lấy phần data từ response

        port = data.get("remote_debugging_port") if isinstance(data, dict) else None  # Lấy remote_debugging_port từ data

        if not port:  # Kiểm tra có lấy được port không
            raise RuntimeError(f"Không lấy được remote_debugging_port: {response_json}")  # Báo lỗi nếu không có port

        remote_debugging_address = f"{self._host_from_apiurl(apiurl_Gpm)}:{port}"  # Ghép host và port thành địa chỉ CDP

        print("remote_debugging_address là", remote_debugging_address)  # In địa chỉ CDP ra màn hình

        return remote_debugging_address  # Trả về địa chỉ CDP dạng host:port

    def close_profile(  # Hàm đóng profile đang chạy
        self,  # Đại diện cho object hiện tại
        apiurl_Gpm: Optional[str] = None,  # API URL tùy chỉnh nếu muốn dùng khác mặc định
        id_profile: Optional[str] = None,  # ID profile cần đóng
    ) -> Dict[str, Any]:  # Trả về response dạng dictionary
        if not id_profile:  # Kiểm tra có truyền id_profile chưa
            raise ValueError("Thiếu id_profile")  # Báo lỗi nếu thiếu id_profile

        url = f"{self._base_url(apiurl_Gpm)}/api/v1/profiles/stop/{id_profile}"  # Tạo URL API stop profile

        return self._request("GET", url, strict=False)  # Gọi API đóng profile và không crash nếu success=False

    def start_profile(self, *args, **kwargs) -> str:  # Alias để gọi open_profile bằng tên start_profile
        return self.open_profile(*args, **kwargs)  # Gọi lại hàm open_profile

    def stop_profile(self, *args, **kwargs) -> Dict[str, Any]:  # Alias để gọi close_profile bằng tên stop_profile
        return self.close_profile(*args, **kwargs)  # Gọi lại hàm close_profile


if __name__ == "__main__":  # Chỉ chạy đoạn test này khi chạy trực tiếp file Python
    gpm = Gpm(api_url=API_URL)  # Tạo object Gpm dùng API URL mặc định

    profile_id = gpm.create_profile_2()  # Tạo profile mới không dùng proxy
    print("Đã tạo profile:", profile_id)  # In ID profile vừa tạo

    remote = gpm.open_profile(  # Mở profile vừa tạo
        id_profile=profile_id,  # Truyền ID profile cần mở
        win_pos="100,100",  # Đặt vị trí cửa sổ browser
        win_size="800,600",  # Đặt kích thước cửa sổ browser
    )  # Kết thúc gọi hàm mở profile

    print("CDP URL:", f"http://{remote}/json/version")  # In URL CDP dùng để kết nối Playwright/Selenium

    # gpm.close_profile(id_profile=profile_id)  # Bỏ dấu # nếu muốn đóng profile sau khi test
    # gpm.delete_profile(id_profile=profile_id, mode="hard")  # Bỏ dấu # nếu muốn xóa hẳn profile sau khi test
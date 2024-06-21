"""
提供windows macos系统设置网路代理的行为
"""
import platform

__all__ = ['NetProxyUtils']


class NetProxyUtils():

    @staticmethod
    def which_os() -> str:
        """
        @return: macOS or Windows or Other
        """
        os_name = platform.system()
        if os_name == "Darwin":
            return "macOS"
        elif os_name == "Windows":
            return "Windows"
        else:
            return "Other"

    @staticmethod
    def enable_proxy(server: str, port: str) -> bool:
        which_os = NetProxyUtils.which_os()
        if which_os == "macOS":
            return NetProxyUtils.__private_macos_set_proxy("Wi-Fi", server, port)
        elif which_os == "Windows":
            return NetProxyUtils.__private_win_set_proxy(server, port)
        else:
            return False

    @staticmethod
    def disable_proxy() -> bool:
        which_os = NetProxyUtils.which_os()
        if which_os == "macOS":
            return NetProxyUtils.__private_macos_disable_proxy("Wi-Fi")
        elif which_os == "Windows":
            return NetProxyUtils.__private_win_disable_proxy()
        else:
            return False

    @staticmethod
    def __private_win_set_proxy(server: str, port: str):
        try:
            import winreg as reg
            # 打开注册表项
            internet_settings = reg.OpenKey(reg.HKEY_CURRENT_USER,
                                            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                            0, reg.KEY_ALL_ACCESS)

            # 启用代理
            reg.SetValueEx(internet_settings, 'ProxyEnable', 0, reg.REG_DWORD, 1)

            # 设置代理服务器和端口
            proxy_server = f"{server}:{port}"
            reg.SetValueEx(internet_settings, 'ProxyServer', 0, reg.REG_SZ, proxy_server)

            # 通知系统代理设置已更改
            import ctypes
            INTERNET_OPTION_SETTINGS_CHANGED = 39
            INTERNET_OPTION_REFRESH = 37

            ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)

            print(f"Windows Proxy set to {proxy_server}")

            return True

        except Exception as e:
            print(f"Windows Failed to set proxy: {e}")
            return False

    @staticmethod
    def __private_win_disable_proxy() -> bool:
        try:
            import winreg as reg
            # 打开注册表项
            internet_settings = reg.OpenKey(reg.HKEY_CURRENT_USER,
                                            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                            0, reg.KEY_ALL_ACCESS)

            # 禁用代理
            reg.SetValueEx(internet_settings, 'ProxyEnable', 0, reg.REG_DWORD, 0)

            # 通知系统代理设置已更改
            import ctypes
            INTERNET_OPTION_SETTINGS_CHANGED = 39
            INTERNET_OPTION_REFRESH = 37

            ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)

            return True

        except Exception as e:
            print(f"Failed to disable proxy: {e}")
            return False

    @staticmethod
    def __private_macos_set_proxy(network_service: str, server: str, port: str) -> bool:
        try:
            import subprocess
            # 设置HTTP代理
            subprocess.run(["networksetup", "-setwebproxy", network_service, server, port], check=True)

            # 设置HTTPS代理
            subprocess.run(["networksetup", "-setsecurewebproxy", network_service, server, port], check=True)

            # 启用HTTP代理
            subprocess.run(["networksetup", "-setwebproxystate", network_service, "on"], check=True)

            # 启用HTTPS代理
            subprocess.run(["networksetup", "-setsecurewebproxystate", network_service, "on"], check=True)

            print(f"MacOs Proxy set to {server}:{port} for {network_service}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"MacOs Failed to set proxy: {e}")
            return False

    @staticmethod
    def __private_macos_disable_proxy(network_service: str) -> bool:
        try:
            import subprocess
            # 禁用HTTP代理
            subprocess.run(["networksetup", "-setwebproxystate", network_service, "off"], check=True)

            # 禁用HTTPS代理
            subprocess.run(["networksetup", "-setsecurewebproxystate", network_service, "off"], check=True)

            print(f"Proxy disabled for {network_service}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Failed to disable proxy: {e}")
            return False


if __name__ == "__main__":
    network_service = "Wi-Fi"  # 或者其他网络服务名称，如 "Ethernet"
    server = "127.0.0.1"
    port = "9999"

    NetProxyUtils.enable_proxy(server, port)
    input("Press Enter to disable the proxy...")  # 等待用户输入以禁用代理

    NetProxyUtils.disable_proxy()

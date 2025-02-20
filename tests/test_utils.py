from login_history_too.utils import get_ip_info


def test_get_ip_info():
    ip_address = "8.8.8.8"
    result = get_ip_info(ip_address)
    assert isinstance(result, dict)
    assert "ip" in result

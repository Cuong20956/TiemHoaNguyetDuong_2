from datetime import datetime


DATE_FORMAT = "%d/%m/%Y"


def parse_date(text):
    """
    Chuyển chuỗi dd/mm/yyyy thành datetime.
    """

    try:
        return datetime.strptime(
            text.strip(),
            DATE_FORMAT
        )

    except (
        ValueError,
        AttributeError
    ):
        return None


def kiem_tra_ngay(
    ngay_dat,
    ngay_giao
):
    """
    Ngày giao phải >= ngày đặt.
    """

    dat = parse_date(
        ngay_dat
    )

    giao = parse_date(
        ngay_giao
    )

    if dat is None or giao is None:
        return False

    return giao >= dat


def kiem_tra_so_dien_thoai(
    sdt
):
    """
    SĐT phải gồm 9 đến 11 chữ số.
    """

    sdt = str(
        sdt
    ).strip()

    return (
        sdt.isdigit()
        and 9 <= len(sdt) <= 11
    )


def kiem_tra_so_nguyen_duong(
    value
):
    try:
        return int(value) > 0

    except (
        ValueError,
        TypeError
    ):
        return False


def kiem_tra_so_thuc_duong(
    value
):
    try:
        return float(value) > 0

    except (
        ValueError,
        TypeError
    ):
        return False


def tinh_tong_tien(
    so_luong,
    don_gia,
    phi_giao,
    phu_phi_gap
):
    """
    Tổng tiền =
    số lượng * đơn giá
    + phí giao
    + phụ phí gấp
    """

    return (
        int(so_luong)
        * float(don_gia)
        + float(phi_giao)
        + float(phu_phi_gap)
    )


def dinh_dang_tien(
    value
):
    try:
        return f"{float(value):,.0f} đ"

    except (
        ValueError,
        TypeError
    ):
        return "0 đ"
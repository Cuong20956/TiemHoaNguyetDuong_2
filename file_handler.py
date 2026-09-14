from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

FILE_KHACH_HANG = DATA_DIR / "khach_hang.txt"


def doc_khach_hang():
    """
    Đọc danh sách khách hàng từ file TXT.

    Cấu trúc:
    ma_khach|ten_khach|sdt|dia_chi
    """

    danh_sach = []

    try:
        with open(
            FILE_KHACH_HANG,
            "r",
            encoding="utf-8"
        ) as file:

            for dong in file:

                dong = dong.strip()

                # Bỏ qua dòng trống
                if not dong:
                    continue

                du_lieu = dong.split("|")

                # Một khách phải có đúng 4 trường
                if len(du_lieu) != 4:
                    continue

                khach_hang = {
                    "ma_khach": du_lieu[0].strip(),
                    "ten_khach": du_lieu[1].strip(),
                    "sdt": du_lieu[2].strip(),
                    "dia_chi": du_lieu[3].strip()
                }

                danh_sach.append(khach_hang)

    except FileNotFoundError:

        print(
            "Không tìm thấy file:",
            FILE_KHACH_HANG
        )

    except UnicodeDecodeError:

        print(
            "File khach_hang.txt không đúng UTF-8."
        )

    except Exception as e:

        print(
            "Lỗi đọc file khách hàng:",
            e
        )

    return danh_sach
def tim_kiem_khach_hang(tu_khoa):

    ket_qua = []

    tu_khoa = tu_khoa.lower().strip()

    danh_sach = doc_khach_hang()

    for khach in danh_sach:

        if (
            tu_khoa in khach["ma_khach"].lower()
            or tu_khoa in khach["ten_khach"].lower()
            or tu_khoa in khach["sdt"]
        ):
            ket_qua.append(khach)

    return ket_qua
FILE_HOA = DATA_DIR / "hoa.txt"
# ==========================================
# ĐỌC DANH SÁCH HOA
# ==========================================
def doc_hoa():

    danh_sach = []

    try:
        with open(
            FILE_HOA,
            "r",
            encoding="utf-8"
        ) as file:

            for dong in file:

                dong = dong.strip()

                if not dong:
                    continue

                du_lieu = dong.split("|")

                if len(du_lieu) != 6:
                    continue

                try:
                    hoa = {
                        "ma_hoa": du_lieu[0].strip(),
                        "ten_hoa": du_lieu[1].strip(),
                        "so_luong": int(du_lieu[2]),
                        "gia": float(du_lieu[3]),
                        "trang_thai": du_lieu[4].strip(),
                        "hinh_anh": du_lieu[5].strip()
                    }

                    danh_sach.append(hoa)

                except ValueError:
                    print(
                        "Dòng dữ liệu hoa không hợp lệ:",
                        dong
                    )

    except FileNotFoundError:

        print(
            "Không tìm thấy file hoa.txt"
        )

    except Exception as e:

        print(
            "Lỗi đọc file hoa:",
            e
        )

    return danh_sach


# ==========================================
# GHI TOÀN BỘ DANH SÁCH HOA
# ==========================================
def ghi_hoa(danh_sach):

    try:
        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            FILE_HOA,
            "w",
            encoding="utf-8"
        ) as file:

            for hoa in danh_sach:

                dong = (
                    f'{hoa["ma_hoa"]}|'
                    f'{hoa["ten_hoa"]}|'
                    f'{hoa["so_luong"]}|'
                    f'{hoa["gia"]}|'
                    f'{hoa["trang_thai"]}|'
                    f'{hoa["hinh_anh"]}\n'
                )

                file.write(dong)

        return True

    except Exception as e:

        print(
            "Lỗi ghi file hoa:",
            e
        )

        return False


# ==========================================
# TÌM HOA THEO MÃ
# ==========================================
def tim_hoa_theo_ma(ma_hoa):

    danh_sach = doc_hoa()

    for hoa in danh_sach:

        if hoa["ma_hoa"] == ma_hoa:
            return hoa

    return None


# ==========================================
# TÌM KIẾM HOA
# ==========================================
def tim_kiem_hoa(tu_khoa):

    tu_khoa = tu_khoa.lower().strip()

    ket_qua = []

    for hoa in doc_hoa():

        if (
            tu_khoa in hoa["ma_hoa"].lower()
            or tu_khoa in hoa["ten_hoa"].lower()
            or tu_khoa in hoa["trang_thai"].lower()
        ):
            ket_qua.append(hoa)

    return ket_qua


# ==========================================
# THÊM HOA
# ==========================================
def them_hoa(hoa_moi):

    danh_sach = doc_hoa()

    # Kiểm tra trùng mã
    for hoa in danh_sach:

        if hoa["ma_hoa"] == hoa_moi["ma_hoa"]:

            return (
                False,
                "Mã hoa đã tồn tại."
            )

    # Tự xác định trạng thái
    if hoa_moi["so_luong"] > 0:
        hoa_moi["trang_thai"] = "Còn hàng"
    else:
        hoa_moi["trang_thai"] = "Hết hàng"

    danh_sach.append(
        hoa_moi
    )

    if ghi_hoa(danh_sach):

        return (
            True,
            "Thêm hoa thành công."
        )

    return (
        False,
        "Không thể ghi dữ liệu."
    )


# ==========================================
# SỬA HOA
# ==========================================
def sua_hoa(ma_hoa, du_lieu_moi):

    danh_sach = doc_hoa()

    tim_thay = False

    for hoa in danh_sach:

        if hoa["ma_hoa"] == ma_hoa:

            hoa["ten_hoa"] = (
                du_lieu_moi["ten_hoa"]
            )

            hoa["so_luong"] = int(
                du_lieu_moi["so_luong"]
            )

            hoa["gia"] = float(
                du_lieu_moi["gia"]
            )

            hoa["hinh_anh"] = (
                du_lieu_moi["hinh_anh"]
            )

            if hoa["so_luong"] > 0:
                hoa["trang_thai"] = "Còn hàng"
            else:
                hoa["trang_thai"] = "Hết hàng"

            tim_thay = True

            break

    if not tim_thay:

        return (
            False,
            "Không tìm thấy hoa."
        )

    if ghi_hoa(danh_sach):

        return (
            True,
            "Cập nhật hoa thành công."
        )

    return (
        False,
        "Không thể ghi dữ liệu."
    )


# ==========================================
# XÓA HOA
# ==========================================
def xoa_hoa(ma_hoa):

    danh_sach = doc_hoa()

    danh_sach_moi = []

    tim_thay = False

    for hoa in danh_sach:

        if hoa["ma_hoa"] == ma_hoa:

            tim_thay = True

        else:

            danh_sach_moi.append(
                hoa
            )

    if not tim_thay:

        return (
            False,
            "Không tìm thấy hoa."
        )

    if ghi_hoa(danh_sach_moi):

        return (
            True,
            "Xóa hoa thành công."
        )

    return (
        False,
        "Không thể ghi dữ liệu."
    )


# ==========================================
# NHẬP THÊM TỒN KHO
# ==========================================
def nhap_them_hoa(
    ma_hoa,
    so_luong_nhap
):

    danh_sach = doc_hoa()

    for hoa in danh_sach:

        if hoa["ma_hoa"] == ma_hoa:

            hoa["so_luong"] += int(
                so_luong_nhap
            )

            if hoa["so_luong"] > 0:
                hoa["trang_thai"] = "Còn hàng"

            if ghi_hoa(danh_sach):

                return (
                    True,
                    "Nhập thêm hoa thành công."
                )

            return (
                False,
                "Không thể ghi file."
            )

    return (
        False,
        "Không tìm thấy hoa."
    )


# ==========================================
# TRỪ TỒN KHO KHI TẠO ĐƠN
# ==========================================
def tru_ton_kho(
    ma_hoa,
    so_luong_dat
):

    danh_sach = doc_hoa()

    for hoa in danh_sach:

        if hoa["ma_hoa"] == ma_hoa:

            so_luong_dat = int(
                so_luong_dat
            )

            if so_luong_dat <= 0:

                return (
                    False,
                    "Số lượng phải lớn hơn 0."
                )

            if so_luong_dat > hoa["so_luong"]:

                return (
                    False,
                    "Không đủ hoa trong kho."
                )

            hoa["so_luong"] -= (
                so_luong_dat
            )

            if hoa["so_luong"] == 0:
                hoa["trang_thai"] = "Hết hàng"
            else:
                hoa["trang_thai"] = "Còn hàng"

            if ghi_hoa(danh_sach):

                return (
                    True,
                    "Đã cập nhật tồn kho."
                )

            return (
                False,
                "Không thể ghi file."
            )

    return (
        False,
        "Không tìm thấy mã hoa."
    )
FILE_DON_HANG = DATA_DIR / "don_hang.txt"
def doc_don_hang():

    danh_sach = []

    try:
        with open(
            FILE_DON_HANG,
            "r",
            encoding="utf-8"
        ) as file:

            for dong in file:

                dong = dong.strip()

                if not dong:
                    continue

                du_lieu = dong.split("|")

                if len(du_lieu) != 11:
                    print(
                        "Bỏ qua dòng sai:",
                        dong
                    )
                    continue

                try:
                    don = {
                        "ma_don": du_lieu[0].strip(),
                        "ma_khach": du_lieu[1].strip(),
                        "ma_hoa": du_lieu[2].strip(),
                        "so_luong": int(du_lieu[3]),
                        "dip": du_lieu[4].strip(),
                        "ngay_dat": du_lieu[5].strip(),
                        "ngay_giao": du_lieu[6].strip(),
                        "dia_chi": du_lieu[7].strip(),
                        "phi_giao": float(du_lieu[8]),
                        "phu_phi_gap": float(du_lieu[9]),
                        "trang_thai": du_lieu[10].strip()
                    }

                    danh_sach.append(don)

                except ValueError:

                    print(
                        "Dữ liệu đơn không hợp lệ:",
                        dong
                    )

    except FileNotFoundError:

        print(
            "Không tìm thấy don_hang.txt"
        )

    except Exception as e:

        print(
            "Lỗi đọc đơn hàng:",
            e
        )

    return danh_sach
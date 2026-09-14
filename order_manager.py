import sqlite3

from database import get_connection

from utils import (
    tinh_tong_tien
)


# =========================================
# HOA
# =========================================
def lay_danh_sach_hoa():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM hoa
            ORDER BY ten_hoa ASC
        """)

        return cursor.fetchall()

    finally:
        conn.close()


def lay_hoa_theo_ma(
    ma_hoa
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM hoa
            WHERE ma_hoa = ?
        """, (
            ma_hoa,
        ))

        return cursor.fetchone()

    finally:
        conn.close()


# =========================================
# ĐƠN HÀNG
# =========================================
def lay_danh_sach_don(
    keyword="",
    loai="ma_don",
    sort=""
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM don_hang
        """

        params = []

        # ==============================
        # TÌM KIẾM
        # ==============================
        if keyword:

            if loai == "ten_khach":

                sql += """
                    WHERE ten_khach
                    LIKE ?
                """

            elif loai == "dip":

                sql += """
                    WHERE dip
                    LIKE ?
                """

            elif loai == "mau_hoa":

                sql += """
                    WHERE mau_hoa
                    LIKE ?
                """

            else:

                sql += """
                    WHERE ma_don
                    LIKE ?
                """

            params.append(
                f"%{keyword}%"
            )

        # ==============================
        # SẮP XẾP
        # ==============================
        if sort == "ngay_asc":

            sql += """
                ORDER BY
                substr(ngay_giao, 7, 4),
                substr(ngay_giao, 4, 2),
                substr(ngay_giao, 1, 2)
                ASC
            """

        elif sort == "ngay_desc":

            sql += """
                ORDER BY
                substr(ngay_giao, 7, 4),
                substr(ngay_giao, 4, 2),
                substr(ngay_giao, 1, 2)
                DESC
            """

        elif sort == "tong_asc":

            sql += """
                ORDER BY
                (
                    so_luong * don_gia
                    + phi_giao
                    + phu_phi_gap
                ) ASC
            """

        elif sort == "tong_desc":

            sql += """
                ORDER BY
                (
                    so_luong * don_gia
                    + phi_giao
                    + phu_phi_gap
                ) DESC
            """

        else:

            sql += """
                ORDER BY ma_don DESC
            """

        cursor.execute(
            sql,
            params
        )

        rows = cursor.fetchall()

        danh_sach = []

        for row in rows:

            don = dict(row)

            don["tong_tien"] = (
                tinh_tong_tien(
                    don["so_luong"],
                    don["don_gia"],
                    don["phi_giao"],
                    don["phu_phi_gap"]
                )
            )

            danh_sach.append(
                don
            )

        return danh_sach

    finally:
        conn.close()


def lay_don_theo_ma(
    ma_don
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM don_hang
            WHERE ma_don = ?
        """, (
            ma_don,
        ))

        row = cursor.fetchone()

        if row is None:
            return None

        don = dict(row)

        don["tong_tien"] = (
            tinh_tong_tien(
                don["so_luong"],
                don["don_gia"],
                don["phi_giao"],
                don["phu_phi_gap"]
            )
        )

        return don

    finally:
        conn.close()


# =========================================
# THÊM ĐƠN
# =========================================
def them_don(
    data
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Lấy hoa
        cursor.execute("""
            SELECT *
            FROM hoa
            WHERE ma_hoa = ?
        """, (
            data["ma_hoa"],
        ))

        hoa = cursor.fetchone()

        if hoa is None:
            return (
                False,
                "Không tìm thấy hoa."
            )

        so_luong = int(
            data["so_luong"]
        )

        if so_luong > hoa["so_luong"]:
            return (
                False,
                "Số lượng hoa trong kho không đủ."
            )

        # Kiểm tra mã đơn trùng
        cursor.execute("""
            SELECT ma_don
            FROM don_hang
            WHERE ma_don = ?
        """, (
            data["ma_don"],
        ))

        if cursor.fetchone():
            return (
                False,
                "Mã đơn đã tồn tại."
            )

        # Thêm đơn
        cursor.execute("""
            INSERT INTO don_hang (
                ma_don,
                ten_khach,
                sdt,

                ma_hoa,
                mau_hoa,

                so_luong,
                don_gia,

                dip,
                ngay_dat,
                ngay_giao,

                dia_chi,

                phi_giao,
                phu_phi_gap,

                trang_thai
            )

            VALUES (
                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?, ?,
                ?,
                ?, ?,
                ?
            )
        """, (
            data["ma_don"],
            data["ten_khach"],
            data["sdt"],

            hoa["ma_hoa"],
            hoa["ten_hoa"],

            so_luong,
            hoa["gia"],

            data["dip"],
            data["ngay_dat"],
            data["ngay_giao"],

            data["dia_chi"],

            data["phi_giao"],
            data["phu_phi_gap"],

            "Chưa giao"
        ))

        # Trừ tồn kho
        so_luong_con = (
            hoa["so_luong"]
            - so_luong
        )

        trang_thai_hoa = (
            "Còn hàng"
            if so_luong_con > 0
            else "Hết hàng"
        )

        cursor.execute("""
            UPDATE hoa

            SET
                so_luong = ?,
                trang_thai = ?

            WHERE ma_hoa = ?
        """, (
            so_luong_con,
            trang_thai_hoa,
            hoa["ma_hoa"]
        ))

        conn.commit()

        return (
            True,
            "Thêm đơn thành công."
        )

    except sqlite3.Error as e:

        conn.rollback()

        return (
            False,
            f"Lỗi database: {e}"
        )

    finally:
        conn.close()


# =========================================
# XÓA ĐƠN
# =========================================
def xoa_don(
    ma_don
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM don_hang
            WHERE ma_don = ?
        """, (
            ma_don,
        ))

        don = cursor.fetchone()

        if don is None:
            return False

        # Hoàn lại tồn kho
        cursor.execute("""
            UPDATE hoa

            SET
                so_luong =
                    so_luong + ?,

                trang_thai =
                    'Còn hàng'

            WHERE ma_hoa = ?
        """, (
            don["so_luong"],
            don["ma_hoa"]
        ))

        # Xóa đơn
        cursor.execute("""
            DELETE FROM don_hang
            WHERE ma_don = ?
        """, (
            ma_don,
        ))

        conn.commit()

        return True

    except sqlite3.Error:

        conn.rollback()

        return False

    finally:
        conn.close()


# =========================================
# TRẠNG THÁI ĐƠN
# =========================================
def cap_nhat_trang_thai(
    ma_don,
    trang_thai
):
    if trang_thai not in [
        "Chưa giao",
        "Đang giao",
        "Đã giao"
    ]:
        return False

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE don_hang

            SET trang_thai = ?

            WHERE ma_don = ?
        """, (
            trang_thai,
            ma_don
        ))

        conn.commit()

        return (
            cursor.rowcount > 0
        )

    except sqlite3.Error:

        conn.rollback()

        return False

    finally:
        conn.close()


def cap_nhat_don(ma_don, data):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Lấy đơn cũ
        cursor.execute("""
            SELECT *
            FROM don_hang
            WHERE ma_don = ?
        """, (ma_don,))

        don_cu = cursor.fetchone()

        if don_cu is None:
            return False, "Không tìm thấy đơn hàng."

        # Lấy hoa mới
        cursor.execute("""
            SELECT *
            FROM hoa
            WHERE ma_hoa = ?
        """, (data["ma_hoa"],))

        hoa_moi = cursor.fetchone()

        if hoa_moi is None:
            return False, "Không tìm thấy hoa."

        so_luong_moi = int(data["so_luong"])

        # =============================
        # HOÀN KHO HOA CŨ
        # =============================
        cursor.execute("""
            UPDATE hoa
            SET so_luong = so_luong + ?,
                trang_thai = 'Còn hàng'
            WHERE ma_hoa = ?
        """, (
            don_cu["so_luong"],
            don_cu["ma_hoa"]
        ))

        # Đọc lại tồn kho hoa mới
        cursor.execute("""
            SELECT *
            FROM hoa
            WHERE ma_hoa = ?
        """, (data["ma_hoa"],))

        hoa_moi = cursor.fetchone()

        if so_luong_moi > hoa_moi["so_luong"]:
            conn.rollback()

            return (
                False,
                "Số lượng hoa trong kho không đủ."
            )

        so_luong_con = (
            hoa_moi["so_luong"]
            - so_luong_moi
        )

        trang_thai_hoa = (
            "Còn hàng"
            if so_luong_con > 0
            else "Hết hàng"
        )

        # =============================
        # TRỪ KHO HOA MỚI
        # =============================
        cursor.execute("""
            UPDATE hoa

            SET
                so_luong = ?,
                trang_thai = ?

            WHERE ma_hoa = ?
        """, (
            so_luong_con,
            trang_thai_hoa,
            data["ma_hoa"]
        ))

        # =============================
        # CẬP NHẬT ĐƠN
        # =============================
        cursor.execute("""
            UPDATE don_hang

            SET
                ten_khach = ?,
                sdt = ?,
                ma_hoa = ?,
                mau_hoa = ?,
                so_luong = ?,
                don_gia = ?,
                dip = ?,
                ngay_dat = ?,
                ngay_giao = ?,
                dia_chi = ?,
                phi_giao = ?,
                phu_phi_gap = ?

            WHERE ma_don = ?
        """, (
            data["ten_khach"],
            data["sdt"],
            hoa_moi["ma_hoa"],
            hoa_moi["ten_hoa"],
            so_luong_moi,
            hoa_moi["gia"],
            data["dip"],
            data["ngay_dat"],
            data["ngay_giao"],
            data["dia_chi"],
            data["phi_giao"],
            data["phu_phi_gap"],
            ma_don
        ))

        conn.commit()

        return (
            True,
            "Cập nhật đơn hàng thành công."
        )

    except sqlite3.Error as e:
        conn.rollback()

        return (
            False,
            f"Lỗi database: {e}"
        )

    finally:
        conn.close()
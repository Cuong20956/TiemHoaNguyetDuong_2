def hoa_to_dict(row):
    """
    Chuyển một dòng hoa từ SQLite thành dictionary.
    """

    if row is None:
        return None

    return {
        "ma_hoa": row["ma_hoa"],
        "ten_hoa": row["ten_hoa"],
        "so_luong": row["so_luong"],
        "gia": row["gia"],
        "trang_thai": row["trang_thai"],
        "hinh_anh": row["hinh_anh"]
    }


def don_hang_to_dict(row):
    """
    Chuyển một dòng đơn hàng thành dictionary.
    """

    if row is None:
        return None

    return {
        "ma_don": row["ma_don"],
        "ten_khach": row["ten_khach"],
        "sdt": row["sdt"],

        "ma_hoa": row["ma_hoa"],
        "mau_hoa": row["mau_hoa"],

        "so_luong": row["so_luong"],
        "don_gia": row["don_gia"],

        "dip": row["dip"],
        "ngay_dat": row["ngay_dat"],
        "ngay_giao": row["ngay_giao"],

        "dia_chi": row["dia_chi"],

        "phi_giao": row["phi_giao"],
        "phu_phi_gap": row["phu_phi_gap"],

        "trang_thai": row["trang_thai"]
    }
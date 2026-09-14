import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "tiem_hoa.db"


def get_connection():
    """
    Tạo kết nối tới SQLite.
    """
    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DATABASE_FILE
    )

    conn.row_factory = sqlite3.Row

    return conn


def create_tables():
    """
    Tạo bảng hoa và bảng đơn hàng nếu chưa tồn tại.
    """

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # ==============================
        # BẢNG HOA
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hoa (
                ma_hoa TEXT PRIMARY KEY,
                ten_hoa TEXT NOT NULL,
                so_luong INTEGER NOT NULL,
                gia REAL NOT NULL,
                trang_thai TEXT NOT NULL,
                hinh_anh TEXT
            )
        """)

        # ==============================
        # BẢNG ĐƠN HÀNG
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS don_hang (
                ma_don TEXT PRIMARY KEY,
                ten_khach TEXT NOT NULL,
                sdt TEXT NOT NULL,

                ma_hoa TEXT,
                mau_hoa TEXT NOT NULL,

                so_luong INTEGER NOT NULL,
                don_gia REAL NOT NULL,

                dip TEXT,
                ngay_dat TEXT,
                ngay_giao TEXT,

                dia_chi TEXT NOT NULL,

                phi_giao REAL DEFAULT 30000,
                phu_phi_gap REAL DEFAULT 0,

                trang_thai TEXT DEFAULT 'Chưa giao',

                FOREIGN KEY (ma_hoa)
                    REFERENCES hoa(ma_hoa)
            )
        """)

        conn.commit()

    except sqlite3.Error as e:
        print(
            "Lỗi tạo bảng:",
            e
        )

    finally:
        conn.close()


def them_du_lieu_hoa_mau():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM hoa"
        )

        so_luong = cursor.fetchone()[0]

        if so_luong > 0:
            return

        danh_sach_hoa = [

            (
                "MH001",
                "Hoa hồng đỏ",
                50,
                15000,
                "Còn hàng",
                "hoa_hong_do.jpg"
            ),

            (
                "MH002",
                "Hoa hồng trắng",
                40,
                16000,
                "Còn hàng",
                "hoa_hong_trang.jpg"
            ),

            (
                "MH003",
                "Hoa hồng vàng",
                45,
                17000,
                "Còn hàng",
                "hoa_hong_vang.jpg"
            ),

            (
                "MH004",
                "Hoa hồng phấn",
                35,
                18000,
                "Còn hàng",
                "hoa_hong_phan.jpg"
            ),

            (
                "MH005",
                "Hoa tulip đỏ",
                30,
                30000,
                "Còn hàng",
                "hoa_tulip_do.jpg"
            ),

            (
                "MH006",
                "Hoa tulip trắng",
                25,
                32000,
                "Còn hàng",
                "hoa_tulip_trang.jpg"
            ),

            (
                "MH007",
                "Hoa hướng dương",
                40,
                25000,
                "Còn hàng",
                "hoa_huong_duong.jpg"
            ),

            (
                "MH008",
                "Hoa baby trắng",
                50,
                12000,
                "Còn hàng",
                "hoa_baby_trang.jpg"
            ),

            (
                "MH009",
                "Hoa ly",
                25,
                35000,
                "Còn hàng",
                "hoa_ly.jpg"
            ),

            (
                "MH010",
                "Hoa cẩm tú cầu",
                20,
                45000,
                "Còn hàng",
                "hoa_cam_tu_cau.jpg"
            ),

            (
                "MH011",
                "Hoa cẩm chướng",
                30,
                18000,
                "Còn hàng",
                "hoa_cam_chuong.jpg"
            ),

            (
                "MH012",
                "Hoa lan hồ điệp",
                18,
                80000,
                "Còn hàng",
                "hoa_lan_ho_diep.jpg"
            ),

            (
                "MH013",
                "Hoa đồng tiền",
                35,
                20000,
                "Còn hàng",
                "hoa_dong_tien.jpg"
            ),

            (
                "MH014",
                "Hoa mẫu đơn",
                20,
                65000,
                "Còn hàng",
                "hoa_mau_don.jpg"
            ),

            (
                "MH015",
                "Hoa lavender",
                30,
                28000,
                "Còn hàng",
                "hoa_lavender.jpg"
            ),

            (
                "MH016",
                "Hoa sen",
                25,
                30000,
                "Còn hàng",
                "hoa_sen.jpg"
            ),

            (
                "MH017",
                "Hoa cúc họa mi",
                35,
                22000,
                "Còn hàng",
                "hoa_cuc_hoa_mi.jpg"
            ),

            (
                "MH018",
                "Hoa thạch thảo",
                30,
                18000,
                "Còn hàng",
                "hoa_thach_thao.jpg"
            ),

            (
                "MH019",
                "Hoa salem",
                25,
                20000,
                "Còn hàng",
                "hoa_salem.jpg"
            ),

            (
                "MH020",
                "Hoa ping pong",
                30,
                26000,
                "Còn hàng",
                "hoa_ping_pong.jpg"
            )
        ]

        cursor.executemany("""
            INSERT INTO hoa (
                ma_hoa,
                ten_hoa,
                so_luong,
                gia,
                trang_thai,
                hinh_anh
            )

            VALUES (
                ?, ?, ?, ?, ?, ?
            )
        """, danh_sach_hoa)

        conn.commit()

        print(
            "Đã tạo 20 loại hoa mẫu."
        )

    except sqlite3.Error as e:

        print(
            "Lỗi thêm dữ liệu hoa:",
            e
        )

    finally:
        conn.close()
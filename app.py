from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    create_tables,
    them_du_lieu_hoa_mau
)
from order_manager import (
    lay_danh_sach_hoa,
    lay_danh_sach_don,
    lay_don_theo_ma,
    them_don,
    xoa_don,
    cap_nhat_trang_thai,
    cap_nhat_don,
)

from utils import (
    kiem_tra_so_dien_thoai,
    kiem_tra_so_nguyen_duong,
    kiem_tra_so_thuc_duong,
    kiem_tra_ngay
)

from file_handler import (
    doc_khach_hang,
    tim_kiem_khach_hang,
    tim_kiem_hoa,
    tim_hoa_theo_ma,
    them_hoa,
    sua_hoa,
    xoa_hoa
)


app = Flask(__name__)

app.secret_key = "tiem-hoa-nguyet-duong-dev"


# ==========================================
# KHỞI TẠO DATABASE
# ==========================================
create_tables()
them_du_lieu_hoa_mau()


# ==========================================
# TRANG CHỦ / DASHBOARD
# ==========================================
@app.route("/")
def index():
    danh_sach_don = lay_danh_sach_don()

    trang_thai = {
        "Chưa giao": 0,
        "Đang giao": 0,
        "Đã giao": 0
    }
    thong_ke_hoa = {}
    thong_ke_dip = {}

    for don in danh_sach_don:
        if don["trang_thai"] in trang_thai:
            trang_thai[don["trang_thai"]] += 1

        thong_ke_hoa[don["mau_hoa"]] = (
            thong_ke_hoa.get(don["mau_hoa"], 0)
            + don["so_luong"]
        )

        if don["dip"]:
            thong_ke_dip[don["dip"]] = (
                thong_ke_dip.get(don["dip"], 0)
                + 1
            )

    hoa_ban_chay = (
        max(thong_ke_hoa, key=thong_ke_hoa.get)
        if thong_ke_hoa
        else "Chưa có dữ liệu"
    )
    dip_pho_bien = (
        max(thong_ke_dip, key=thong_ke_dip.get)
        if thong_ke_dip
        else "Chưa có dữ liệu"
    )
    tong_doanh_thu = sum(
        don["tong_tien"]
        for don in danh_sach_don
        if don["trang_thai"] == "Đã giao"
    )

    return render_template(
        "index.html",
        tong_don=len(danh_sach_don),
        chua_giao=trang_thai["Chưa giao"],
        dang_giao=trang_thai["Đang giao"],
        da_giao=trang_thai["Đã giao"],
        tong_doanh_thu=tong_doanh_thu,
        hoa_ban_chay=hoa_ban_chay,
        dip_pho_bien=dip_pho_bien,
        don_gan_day=danh_sach_don[:5]
    )


@app.route("/menu-hoa")
def menu_hoa():
    return render_template(
        "menu_hoa.html",
        danh_sach_hoa=lay_danh_sach_hoa()
    )


@app.route(
    "/don-hang/<ma_don>/sua",
    methods=["GET", "POST"]
)
def sua_don_route(ma_don):

    don = lay_don_theo_ma(ma_don)

    if don is None:
        flash(
            "Không tìm thấy đơn hàng.",
            "danger"
        )

        return redirect(
            url_for("don_hang")
        )

    danh_sach_hoa = lay_danh_sach_hoa()

    if request.method == "POST":

        ten_khach = request.form.get(
            "ten_khach",
            ""
        ).strip()

        sdt = request.form.get(
            "sdt",
            ""
        ).strip()

        ma_hoa = request.form.get(
            "ma_hoa",
            ""
        ).strip()

        so_luong = request.form.get(
            "so_luong",
            ""
        ).strip()

        dip = request.form.get(
            "dip",
            ""
        ).strip()

        ngay_dat = request.form.get(
            "ngay_dat",
            ""
        ).strip()

        ngay_giao = request.form.get(
            "ngay_giao",
            ""
        ).strip()

        dia_chi = request.form.get(
            "dia_chi",
            ""
        ).strip()

        phi_giao = request.form.get(
            "phi_giao",
            "30000"
        ).strip()

        giao_gap = request.form.get(
            "giao_gap"
        )

        phu_phi_gap = 0

        if giao_gap == "on":

            if ngay_dat != ngay_giao:
                flash(
                    "Giao gấp chỉ áp dụng trong ngày.",
                    "danger"
                )

                return render_template(
                    "sua_don.html",
                    don=don,
                    danh_sach_hoa=danh_sach_hoa
                )

            phu_phi_gap = 50000

        if not ten_khach:
            flash(
                "Tên khách không được để trống.",
                "danger"
            )

            return redirect(
                request.url
            )

        if not kiem_tra_so_dien_thoai(sdt):
            flash(
                "SĐT phải có từ 9 đến 11 chữ số.",
                "danger"
            )

            return redirect(
                request.url
            )

        if not kiem_tra_so_nguyen_duong(so_luong):
            flash(
                "Số lượng phải lớn hơn 0.",
                "danger"
            )

            return redirect(
                request.url
            )

        if not kiem_tra_ngay(
            ngay_dat,
            ngay_giao
        ):
            flash(
                "Ngày giao không hợp lệ.",
                "danger"
            )

            return redirect(
                request.url
            )

        if not dia_chi:
            flash(
                "Địa chỉ không được để trống.",
                "danger"
            )

            return redirect(
                request.url
            )

        data = {
            "ten_khach": ten_khach,
            "sdt": sdt,
            "ma_hoa": ma_hoa,
            "so_luong": int(so_luong),
            "dip": dip,
            "ngay_dat": ngay_dat,
            "ngay_giao": ngay_giao,
            "dia_chi": dia_chi,
            "phi_giao": float(phi_giao),
            "phu_phi_gap": phu_phi_gap
        }

        thanh_cong, thong_bao = cap_nhat_don(
            ma_don,
            data
        )

        flash(
            thong_bao,
            "success" if thanh_cong else "danger"
        )

        if thanh_cong:
            return redirect(
                url_for("don_hang")
            )

    return render_template(
        "sua_don.html",
        don=don,
        danh_sach_hoa=danh_sach_hoa
    )


# ==========================================
# DANH SÁCH ĐƠN HÀNG
# ==========================================
@app.route("/don-hang")
def don_hang():
    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    loai = request.args.get(
        "loai",
        "ma_don"
    )

    sort = request.args.get(
        "sort",
        ""
    )

    danh_sach_don = lay_danh_sach_don(
        keyword=keyword,
        loai=loai,
        sort=sort
    )

    return render_template(
        "don_hang.html",

        danh_sach_don=danh_sach_don,

        keyword=keyword,
        loai=loai,
        sort=sort
    )


# ==========================================
# THÊM ĐƠN
# ==========================================
@app.route(
    "/don-hang/them",
    methods=[
        "GET",
        "POST"
    ]
)
def them_don_route():

    danh_sach_hoa = lay_danh_sach_hoa()

    if request.method == "POST":

        # ==============================
        # LẤY DỮ LIỆU TỪ FORM
        # ==============================
        ma_don = request.form.get(
            "ma_don",
            ""
        ).strip()

        ten_khach = request.form.get(
            "ten_khach",
            ""
        ).strip()

        sdt = request.form.get(
            "sdt",
            ""
        ).strip()

        ma_hoa = request.form.get(
            "ma_hoa",
            ""
        ).strip()

        so_luong = request.form.get(
            "so_luong",
            ""
        ).strip()

        dip = request.form.get(
            "dip",
            ""
        ).strip()

        ngay_dat = request.form.get(
            "ngay_dat",
            ""
        ).strip()

        ngay_giao = request.form.get(
            "ngay_giao",
            ""
        ).strip()

        dia_chi = request.form.get(
            "dia_chi",
            ""
        ).strip()

        phi_giao = request.form.get(
            "phi_giao",
            "30000"
        ).strip()

        giao_gap = request.form.get(
            "giao_gap"
        )

        # ==============================
        # PHỤ PHÍ GIAO GẤP
        # ==============================
        phu_phi_gap = 0

        if giao_gap == "on":

            if ngay_dat != ngay_giao:

                flash(
                    "Giao gấp chỉ áp dụng khi ngày giao bằng ngày đặt.",
                    "danger"
                )

                return render_template(
                    "them_don.html",
                    danh_sach_hoa=danh_sach_hoa
                )

            phu_phi_gap = 50000

        # ==============================
        # VALIDATE
        # ==============================
        if not ma_don:

            flash(
                "Mã đơn không được để trống.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not ten_khach:

            flash(
                "Tên khách không được để trống.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not kiem_tra_so_dien_thoai(
            sdt
        ):

            flash(
                "Số điện thoại phải có từ 9 đến 11 chữ số.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not ma_hoa:

            flash(
                "Vui lòng chọn hoa.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not kiem_tra_so_nguyen_duong(
            so_luong
        ):

            flash(
                "Số lượng phải lớn hơn 0.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not kiem_tra_so_thuc_duong(
            phi_giao
        ):

            flash(
                "Phí giao phải lớn hơn 0.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not kiem_tra_ngay(
            ngay_dat,
            ngay_giao
        ):

            flash(
                "Ngày giao không được nhỏ hơn ngày đặt.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        if not dia_chi:

            flash(
                "Địa chỉ không được để trống.",
                "danger"
            )

            return render_template(
                "them_don.html",
                danh_sach_hoa=danh_sach_hoa
            )

        # ==============================
        # DATA GỬI SANG ORDER_MANAGER
        # ==============================
        data = {
            "ma_don": ma_don,
            "ten_khach": ten_khach,
            "sdt": sdt,
            "ma_hoa": ma_hoa,

            "so_luong": int(
                so_luong
            ),

            "dip": dip,

            "ngay_dat": ngay_dat,
            "ngay_giao": ngay_giao,

            "dia_chi": dia_chi,

            "phi_giao": float(
                phi_giao
            ),

            "phu_phi_gap": phu_phi_gap
        }

        thanh_cong, thong_bao = them_don(
            data
        )

        if thanh_cong:

            flash(
                thong_bao,
                "success"
            )

            return redirect(
                url_for(
                    "don_hang"
                )
            )

        else:

            flash(
                thong_bao,
                "danger"
            )

    return render_template(
        "them_don.html",
        danh_sach_hoa=danh_sach_hoa
    )


# ==========================================
# XÓA ĐƠN
# ==========================================
@app.route(
    "/don-hang/<ma_don>/xoa",
    methods=[
        "POST"
    ]
)
def xoa_don_route(
    ma_don
):
    ket_qua = xoa_don(
        ma_don
    )

    if ket_qua:

        flash(
            "Xóa đơn hàng thành công.",
            "success"
        )

    else:

        flash(
            "Không thể xóa đơn hàng.",
            "danger"
        )

    return redirect(
        url_for(
            "don_hang"
        )
    )


# ==========================================
# CẬP NHẬT TRẠNG THÁI
# ==========================================
@app.route(
    "/don-hang/<ma_don>/trang-thai",
    methods=[
        "POST"
    ]
)
def trang_thai_don(
    ma_don
):
    trang_thai = request.form.get(
        "trang_thai"
    )

    ket_qua = cap_nhat_trang_thai(
        ma_don,
        trang_thai
    )

    if ket_qua:

        flash(
            "Cập nhật trạng thái thành công.",
            "success"
        )

    else:

        flash(
            "Không thể cập nhật trạng thái.",
            "danger"
        )

    return redirect(
        url_for(
            "don_hang"
        )
    )


# ==========================================
# TRA CỨU ĐƠN
# ==========================================
@app.route(
    "/tra-cuu",
    methods=[
        "GET",
        "POST"
    ]
)
def tra_cuu():

    don = None

    da_tim = False

    if request.method == "POST":

        ma_don = request.form.get(
            "ma_don",
            ""
        ).strip()

        da_tim = True

        if ma_don:

            don = lay_don_theo_ma(
                ma_don
            )

            if don is None:

                flash(
                    "Không tìm thấy đơn hàng.",
                    "warning"
                )

        else:

            flash(
                "Vui lòng nhập mã đơn.",
                "warning"
            )

    return render_template(
        "tra_cuu.html",
        don=don,
        da_tim=da_tim
    )


# ==========================================
# THỐNG KÊ
# ==========================================
@app.route("/thong-ke")
def thong_ke():

    danh_sach_don = lay_danh_sach_don()

    tong_doanh_thu = 0

    thong_ke_hoa = {}
    thong_ke_dip = {}

    trang_thai = {
        "Chưa giao": 0,
        "Đang giao": 0,
        "Đã giao": 0
    }

    doanh_thu_ngay = {}
    doanh_thu_thang = {}

    for don in danh_sach_don:

        # ==============================
        # TRẠNG THÁI
        # ==============================
        if don["trang_thai"] in trang_thai:

            trang_thai[
                don["trang_thai"]
            ] += 1

        # ==============================
        # HOA ĐẶT NHIỀU
        # ==============================
        ten_hoa = don["mau_hoa"]

        thong_ke_hoa[ten_hoa] = (
            thong_ke_hoa.get(
                ten_hoa,
                0
            )
            + don["so_luong"]
        )

        # ==============================
        # DỊP PHỔ BIẾN
        # ==============================
        dip = don["dip"]

        if dip:

            thong_ke_dip[dip] = (
                thong_ke_dip.get(
                    dip,
                    0
                )
                + 1
            )

        # ==============================
        # DOANH THU
        # CHỈ TÍNH ĐƠN ĐÃ GIAO
        # ==============================
        if don["trang_thai"] == "Đã giao":

            tong_doanh_thu += (
                don["tong_tien"]
            )

            ngay = don["ngay_giao"]

            doanh_thu_ngay[ngay] = (
                doanh_thu_ngay.get(
                    ngay,
                    0
                )
                + don["tong_tien"]
            )

            # dd/mm/yyyy
            parts = ngay.split("/")

            if len(parts) == 3:

                thang = (
                    parts[1]
                    + "/"
                    + parts[2]
                )

                doanh_thu_thang[
                    thang
                ] = (
                    doanh_thu_thang.get(
                        thang,
                        0
                    )
                    + don["tong_tien"]
                )

    # ==============================
    # HOA BÁN CHẠY
    # ==============================
    if thong_ke_hoa:

        hoa_ban_chay = max(
            thong_ke_hoa,
            key=thong_ke_hoa.get
        )

        so_luong_hoa_ban_chay = (
            thong_ke_hoa[
                hoa_ban_chay
            ]
        )

    else:

        hoa_ban_chay = (
            "Chưa có dữ liệu"
        )

        so_luong_hoa_ban_chay = 0

    # ==============================
    # DỊP PHỔ BIẾN
    # ==============================
    if thong_ke_dip:

        dip_pho_bien = max(
            thong_ke_dip,
            key=thong_ke_dip.get
        )

        so_don_dip = (
            thong_ke_dip[
                dip_pho_bien
            ]
        )

    else:

        dip_pho_bien = (
            "Chưa có dữ liệu"
        )

        so_don_dip = 0

    return render_template(
        "thong_ke.html",

        tong_doanh_thu=tong_doanh_thu,

        hoa_ban_chay=hoa_ban_chay,
        so_luong_hoa_ban_chay=so_luong_hoa_ban_chay,

        dip_pho_bien=dip_pho_bien,
        so_don_dip=so_don_dip,

        trang_thai=trang_thai,

        doanh_thu_ngay=doanh_thu_ngay,
        doanh_thu_thang=doanh_thu_thang
    )


# ==========================================
# KHÁCH HÀNG
# ==========================================
@app.route("/khach-hang")
def khach_hang():
    tu_khoa = request.args.get(
        "q",
        ""
    ).strip()

    if tu_khoa:
        danh_sach = tim_kiem_khach_hang(
            tu_khoa
        )
    else:
        danh_sach = doc_khach_hang()

    return render_template(
        "khach_hang.html",
        danh_sach=danh_sach,
        tu_khoa=tu_khoa
    )


# ==========================================
# QUẢN LÝ HOA TỪ FILE TXT
# ==========================================
@app.route("/quan-ly-hoa")
def quan_ly_hoa():
    tu_khoa = request.args.get("q", "").strip()
    danh_sach = tim_kiem_hoa(tu_khoa)

    return render_template(
        "quan_ly_hoa.html",
        danh_sach=danh_sach,
        tu_khoa=tu_khoa
    )


@app.route("/hoa/them", methods=["GET", "POST"])
def them_hoa_route():
    if request.method == "POST":
        try:
            hoa_moi = {
                "ma_hoa": request.form.get("ma_hoa", "").strip(),
                "ten_hoa": request.form.get("ten_hoa", "").strip(),
                "so_luong": int(request.form.get("so_luong", "0")),
                "gia": float(request.form.get("gia", "0")),
                "hinh_anh": request.form.get("hinh_anh", "").strip()
            }

            if not hoa_moi["ma_hoa"] or not hoa_moi["ten_hoa"]:
                raise ValueError

            if hoa_moi["so_luong"] < 0 or hoa_moi["gia"] < 0:
                raise ValueError

            thanh_cong, thong_bao = them_hoa(hoa_moi)
        except (TypeError, ValueError):
            thanh_cong = False
            thong_bao = "Vui lòng nhập dữ liệu hoa hợp lệ."

        flash(thong_bao, "success" if thanh_cong else "danger")

        if thanh_cong:
            return redirect(url_for("quan_ly_hoa"))

    return render_template("them_hoa.html")


@app.route("/hoa/<ma_hoa>/sua", methods=["GET", "POST"])
def sua_hoa_route(ma_hoa):
    hoa = tim_hoa_theo_ma(ma_hoa)

    if hoa is None:
        flash("Không tìm thấy hoa.", "danger")
        return redirect(url_for("quan_ly_hoa"))

    if request.method == "POST":
        try:
            du_lieu_moi = {
                "ten_hoa": request.form.get("ten_hoa", "").strip(),
                "so_luong": int(request.form.get("so_luong", "0")),
                "gia": float(request.form.get("gia", "0")),
                "hinh_anh": request.form.get("hinh_anh", "").strip()
            }

            if not du_lieu_moi["ten_hoa"]:
                raise ValueError

            if du_lieu_moi["so_luong"] < 0 or du_lieu_moi["gia"] < 0:
                raise ValueError

            thanh_cong, thong_bao = sua_hoa(ma_hoa, du_lieu_moi)
        except (TypeError, ValueError):
            thanh_cong = False
            thong_bao = "Vui lòng nhập dữ liệu hoa hợp lệ."

        flash(thong_bao, "success" if thanh_cong else "danger")

        if thanh_cong:
            return redirect(url_for("quan_ly_hoa"))

        hoa = dict(hoa)
        hoa.update(du_lieu_moi)

    return render_template("sua_hoa.html", hoa=hoa)


@app.route("/hoa/<ma_hoa>/xoa", methods=["POST"])
def xoa_hoa_route(ma_hoa):
    thanh_cong, thong_bao = xoa_hoa(ma_hoa)
    flash(thong_bao, "success" if thanh_cong else "danger")
    return redirect(url_for("quan_ly_hoa"))


# ==========================================
# CHẠY APP
# ==========================================
if __name__ == "__main__":
    app.run(
        debug=True
    )
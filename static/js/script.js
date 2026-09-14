function toggleMenu() {
    const nav = document.getElementById("navLinks");

    if (nav) {
        nav.classList.toggle("show");
    }
}


function confirmDelete() {
    return confirm(
        "Bạn có chắc chắn muốn xóa đơn hàng này?"
    );
}


// =============================
// CHỌN HOA
// =============================

const flowerSelect =
    document.getElementById("flowerSelect");

const displayPrice =
    document.getElementById("displayPrice");

const stockText =
    document.getElementById("stockText");

const quantity =
    document.getElementById("quantity");


function formatMoney(value) {
    return new Intl.NumberFormat(
        "vi-VN"
    ).format(value) + "đ";
}


function updateFlowerInfo() {

    if (!flowerSelect) {
        return;
    }

    const option =
        flowerSelect.options[
            flowerSelect.selectedIndex
        ];

    if (!option || !option.value) {

        if (displayPrice) {
            displayPrice.value = "0đ";
        }

        if (stockText) {
            stockText.textContent =
                "Vui lòng chọn hoa";
        }

        return;
    }

    const price = Number(
        option.dataset.price || 0
    );

    const stock = Number(
        option.dataset.stock || 0
    );

    if (displayPrice) {
        displayPrice.value =
            formatMoney(price);
    }

    if (stockText) {
        stockText.textContent =
            "Kho hiện còn: "
            + stock
            + " sản phẩm";
    }

    if (quantity) {
        quantity.max = stock;
    }
}


if (flowerSelect) {

    flowerSelect.addEventListener(
        "change",
        updateFlowerInfo
    );

    updateFlowerInfo();
}


// =============================
// KIỂM TRA SỐ LƯỢNG
// =============================

if (quantity && flowerSelect) {

    quantity.addEventListener(
        "input",
        function () {

            const option =
                flowerSelect.options[
                    flowerSelect.selectedIndex
                ];

            if (!option) {
                return;
            }

            const stock = Number(
                option.dataset.stock || 0
            );

            const value = Number(
                quantity.value
            );

            if (value > stock) {

                alert(
                    "Số lượng đặt vượt quá số lượng tồn kho!"
                );

                quantity.value = stock;
            }

        }
    );
}


// =============================
// TỰ ẨN FLASH MESSAGE
// =============================

setTimeout(
    function () {

        const alerts =
            document.querySelectorAll(
                ".alert"
            );

        alerts.forEach(
            function (alert) {

                alert.style.opacity = "0";

                setTimeout(
                    function () {
                        alert.remove();
                    },
                    300
                );

            }
        );

    },
    5000
);
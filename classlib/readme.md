# location class
________
## 1. Cách dùng
**Debug mode:**
- Đổi giá trị TEST_CLASS = 0 sang TEST_CLASS = 1
- Đổi các tham số LocationNameGet để chọn level lấy thông tin khu vực
- Cần debug sâu hơn, bật tham số debug class LocationManager(debug = 1)

**run mode:**
- Thiết lập giá trị TEST_CLASS = 0
- Khởi tạo class LocationManager(debug = 0)
## 2. Trả về
- LocationNameGet(): list có thông tin như sau
```
[
    {
        "name":"khu phố 1, phường 12, quận Tân Bình, TPHCM",
        "locationid":"8479677001002"
        "maxlevel":4
    },
    {
        "name":"phường 13, quận Tân Bình, TP HCM",
        "locationid":"8479677002",
        "maxlevel":3
    }
    ......
]
```

## 3. Trường hợp sử dụng
- Lấy thông tin hiển thị các khu vực quản lý tương ứng với userid trên web.
- Khi web cần lấy thông tin lập lịch để hiển thị lên web thì gửi ngược về giá trị locationid và maxlevel để lấy chính xác nội dung lập lịch.

____
# mongo class 

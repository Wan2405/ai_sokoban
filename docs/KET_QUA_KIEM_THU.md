# Kết quả kiểm tra bản ghép

Ngày kiểm tra: 02/10/2026.
Môi trường: Python 3.12.14, Linux, `pygame-ce==2.5.8`.
Các kiểm tra GUI dùng trình hiển thị giả lập của SDL, không mở cửa sổ thật.

## Kết quả

| Kiểm tra | Kết quả |
| --- | --- |
| `python -m unittest discover -s tests -v` | 15/15 đạt: 7 kiểm thử core và 8 kiểm thử tích hợp GUI/agent |
| `python -m tests.check_requirements` | Đạt: menu, phát lại, nút/phím, va chạm, giành điểm và giới hạn lượt của hai tác nhân |
| `python -m tests.check_presentation` | Đạt: bố cục, đổi kích thước, hình ảnh, hiệu ứng, hướng dẫn và hoàn thành map |
| `python main.py --frames 2` | Khởi động và thoát sau hai khung hình |
| `python main_cli.py` | Chạy độc lập bằng thư viện chuẩn, lời giải East/East/East, chi phí 3 |
| Tọa độ và chuyển trạng thái | Core và mô hình GUI cho cùng vị trí sau từng hành động của lời giải |
| Giải sau khi đi tay | Map nhỏ đã đi East: lời giải còn hai hành động; bộ đếm bàn chơi cuối cùng là ba bước |
| Người chơi đứng trên đích | Đích vẫn được giữ khi chuyển dữ liệu từ GUI sang core |
| Map đã hoàn thành | Trả danh sách rỗng, chi phí 0, GUI chấp nhận lời giải |
| Không có lời giải | GUI hiển thị thông báo, không ghi đè trạng thái bàn chơi |

## Bốn map gốc

| Map | Chi phí UCS | Chi phí A* | Phát lại và tiến/lùi trong GUI |
| --- | ---: | ---: | --- |
| `map_test.txt` | 3 | 3 | Đạt |
| `map_two_boxes.txt` | 8 | 8 | Đạt |
| `example_map.txt` | 34 | 34 | Đạt |
| `map_already_solved.txt` | 0 | 0 | Đạt |

So sánh trực tiếp dữ liệu file với ZIP core gốc: cả bốn file map giống nhau từng byte.
Các ảnh PNG của GUI cũng giống nhau từng byte. Logic thuật toán UCS, A*, heuristic,
luật di chuyển của `Board`, phát lại và luật hai tác nhân được giữ;
đường dẫn nhập các mô-đun được đổi theo cấu trúc mới.

Sau khi chuyển `gui_model.py` và `solver_bridge.py` sang Req 5, các bộ kiểm thử trên
được chạy lại. Req 1 chỉ còn ba file core, Req 2 chỉ còn năm file tìm kiếm, cùng `__init__.py`.

Map nháp “Kho gạch nhỏ” có thùng bị kẹt ngay từ đầu. Kiểm tra độc lập bằng duyệt BFS
trên luật GUI đã xét hết 47 trạng thái đạt được và không gặp đích. Map nháp “Sân tập”
có lời giải chi phí 6. Hai map này được giữ để tham khảo/kiểm thử, không thay bộ map mặc định.

## Những gì chưa được xác nhận

- Chưa chạy GUI trong cửa sổ thật trên Windows hoặc macOS 13.7.8 Intel của nhóm.
- Chưa kiểm tra mọi map có thể tạo. Kết quả trên xác nhận các map và trường hợp đã thử.
- Req 3 và 4 chưa có mã nguồn trong bản ghép.
- Req 7 và 8 đã được kiểm tra riêng bằng arena, runner giới hạn thời gian, hai agent
  BFS/DLS, fixture agent ngoài và luồng chọn agent trong GUI; chưa có kiểm thử Windows
  với cửa sổ thật (các kiểm thử GUI dùng SDL dummy).

Nhóm nên chạy lại ba lệnh kiểm thử và thử phím/chuột/font tiếng Việt trên máy trình bày.

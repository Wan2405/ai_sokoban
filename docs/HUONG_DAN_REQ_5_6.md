# Giao diện và luật hai tác nhân

## Req 5

Chạy từ thư mục ngoài cùng: `python main.py`.
Chương trình dùng `pygame-ce==2.5.8`, mã nguồn nhập thư viện bằng `import pygame`.
Giữ các ảnh trong `source/task1_sokoban/req_5/assets/` bên cạnh `renderer.py`.

Ứng dụng mặc định đã nối `app.solver` với `solve_board()` trong `req_5/solver_bridge.py`.
Hàm này gọi mô hình bài toán ở Req 1 và thuật toán tìm kiếm ở Req 2.
Giao diện gửi bàn chơi hiện tại và tên `"UCS"` hoặc `"A*"`.
Hàm giải trả `(actions, total_cost)`, ví dụ `(["East", "East", "East"], 3)`.

`Replay` chỉ chấp nhận danh sách hành động hợp lệ, chi phí nguyên bằng số hành động,
và trạng thái cuối đã hoàn thành. Lời giải lỗi không ghi đè lịch sử bàn chơi đang sử dụng.
Khi người dùng đã đi tay, chi phí lời giải là số hành động **còn phải thực hiện**;
bộ đếm bước đi của bàn chơi vẫn bao gồm các bước tay trước đó.

Space phát/tạm dừng; ←/→ lùi/tiến một bước. Khi hết lời giải, phát tự động dừng và
không tự đổi map. R đặt lại map để bắt đầu tìm một lời giải khác.

## Req 6

Ở menu, chọn 2 tác nhân, nhập số lượt n > 0 rồi bấm Bắt đầu.
Chế độ này dùng map “Kho đôi” gốc riêng; không thay đổi bốn map một tác nhân.
Người 1 dùng W/A/S/D, người 2 dùng mũi tên. Bàn chơi chờ đủ hai hướng rồi xử lý một lượt.

- Mỗi lượt lấy hai hành động từ cùng một trạng thái trước lượt.
- Không cho hai người chung ô, đổi chỗ trực tiếp hoặc xuyên qua nhau.
- Xung đột cùng đẩy một thùng, đẩy về cùng ô, hoặc đẩy lên vị trí người chơi được hủy
  theo luật của `CompetitiveBoard.step()`.
- Đẩy một thùng lên đích giúp người đó sở hữu điểm tại đích. Đẩy thùng ra khỏi đích
  làm mất quyền sở hữu; người kia có thể đẩy lại để giành điểm.
- Thùng có sẵn trên đích ban đầu chưa được gán điểm cho bên nào.
- Mỗi cặp hành động tiêu thụ một lượt, kể cả khi bị chặn. Đủ n lượt thì so sánh điểm;
  bằng nhau là hòa. Luật này khác chi phí mỗi hành động hợp lệ trong tìm kiếm một tác nhân.
- Undo/redo và đặt lại giữ nguyên hành vi của GUI gốc.

Có thể chạy mô hình hai tác nhân riêng trong Terminal:

```powershell
python -m source.task1_sokoban.req_6.competition --steps 20
```

Req 6 trong bản này cung cấp luật và giao diện thao tác tay. Thuật toán điều khiển hai
tác nhân tự động chưa được cài. Các kiểm thử của GUI kiểm tra va chạm, hai lần đẩy độc lập,
giành lại điểm, giới hạn lượt và đối xứng khi đổi tên tác nhân.

## Kiểm tra trên giao diện

Chạy `main.py`, chọn lần lượt chế độ một tác nhân và hai tác nhân, sau đó kiểm tra
các nút, menu, phát lại, cửa sổ ở nhiều kích thước, hiệu ứng và luật hai tác nhân.
Việc kiểm tra trên giao diện không thay thế thử phím, chuột và font tiếng Việt trên
máy thật của nhóm.

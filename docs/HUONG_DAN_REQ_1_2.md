# Hướng dẫn đọc code và chuẩn bị vấn đáp

## 1. Luồng hoạt động tổng quát

1. `MapLoader` đọc từng ký tự trong file bản đồ.
2. Dữ liệu cố định được lưu trong `SokobanMap`: tường, đích và các ô có thể đi.
3. Dữ liệu thay đổi được lưu trong `SokobanState`: vị trí người chơi và các thùng.
4. `SokobanProblem` xác định hành động hợp lệ, trạng thái kế tiếp, goal test và chi phí.
5. UCS hoặc A* lấy các trạng thái từ frontier để tìm lời giải.
6. `SearchNode` lưu parent và action để truy vết danh sách hành động.
7. `SearchResult` trả kết quả chung cho terminal, GUI và benchmark.

## 2. Vì sao state chỉ gồm người chơi và các thùng?

Tường và đích không thay đổi trong lúc chơi nên được lưu một lần trong `SokobanMap`. Nếu chép chúng vào mọi state, chương trình sẽ tốn thêm bộ nhớ nhưng không cung cấp thông tin mới.

## 3. Vì sao dùng `frozenset` cho vị trí thùng?

Thứ tự các thùng không quan trọng. Hai state có cùng vị trí người chơi và cùng tập vị trí thùng phải được xem là giống nhau. `frozenset` không thay đổi sau khi tạo và có thể được dùng trong `set` hoặc làm khóa của `dict`.

Khi cần đẩy thùng, chương trình tạo một `set` mới, cập nhật vị trí rồi tạo `SokobanState` mới. State cũ không bị sửa.

## 4. State khác SearchNode như thế nào?

- `SokobanState` mô tả một cấu hình của trò chơi.
- `SearchNode` chứa state cùng với `parent`, `action` và `path_cost`.

Nhiều node có thể dẫn tới cùng một state qua các đường đi khác nhau. Search engine chỉ giữ đường có chi phí tốt nhất.

## 5. UCS hoạt động như thế nào?

UCS dùng priority queue và ưu tiên node có giá trị nhỏ nhất:

```text
priority = g(n)
```

Trong dự án, mỗi hành động có chi phí 1 nên `g(n)` bằng số hành động đã thực hiện. Goal test được kiểm tra khi node được lấy ra khỏi frontier. Lúc đó UCS đã tìm được đường có chi phí nhỏ nhất đến node này.

## 6. A* khác UCS ở đâu?

Cấu trúc hai thuật toán gần giống nhau. Điểm khác biệt chính là độ ưu tiên:

```text
UCS: priority = g(n)
A*:  priority = g(n) + h(n)
```

`g(n)` là chi phí đã trả. `h(n)` là chi phí còn lại được ước lượng.

## 7. Heuristic của dự án là gì?

Từ mỗi đích, chương trình chạy BFS theo chiều ngược của thao tác đẩy thùng. Một vị trí trước đó chỉ hợp lệ khi:

- Ô chứa thùng là ô sàn.
- Ô phía sau thùng, nơi người chơi cần đứng để đẩy, cũng là ô sàn.

Sau đó chương trình thử ghép mỗi thùng với một đích khác nhau và chọn tổng khoảng cách nhỏ nhất.

Heuristic không dùng công thức Manhattan hoặc Euclidean. Khoảng cách được tạo bằng BFS trên cấu trúc thật của bản đồ và có xét tường.

## 8. Vì sao heuristic là một cận dưới?

Khi ước lượng, chương trình bỏ qua sự cản trở của các thùng khác và giả sử người chơi có thể đi tới vị trí cần thiết để đẩy. Bài toán được đơn giản hóa nên chi phí ước lượng không lớn hơn chi phí thật.

Mỗi bước đẩy thùng cần ít nhất một hành động. Tổng số lần đẩy tối thiểu vì vậy không thể lớn hơn tổng số hành động thật của lời giải.

## 9. `explored` và `best_path_cost` dùng để làm gì?

- `explored` chứa các state đã được mở rộng.
- `best_path_cost[state]` lưu chi phí nhỏ nhất đã tìm thấy để đi tới state.

Nếu tìm thấy cùng state bằng một đường đắt hơn, node mới không cần được thêm vào frontier. Cách này tránh vòng lặp và giảm số node phải lưu.

## 10. Vì sao heap lưu thêm `entry_number`?

Mỗi phần tử frontier có dạng:

```text
(priority, entry_number, node)
```

Nếu hai node có cùng priority, Python dùng `entry_number` để xác định thứ tự. Nhờ vậy Python không phải so sánh trực tiếp hai đối tượng `SearchNode`.

## 11. Deadlock tĩnh là gì?

Nếu một thùng nằm ở vị trí mà ngay cả khi bỏ qua các thùng khác nó vẫn không thể được đẩy đến bất kỳ đích nào, state đó chắc chắn không có lời giải. Ví dụ phổ biến là thùng nằm trong một góc không phải đích.

`SokobanProblem` tính trước các ô mà thùng có thể đi đến đích. State có thùng nằm ngoài tập này sẽ không được đưa vào frontier.

## 12. Vì sao GUI có thể dùng lại phần Core?

GUI chỉ cần:

1. Tạo `SokobanProblem`.
2. Gọi `search()` của UCS hoặc A*.
3. Đọc `result.actions`.
4. `Replay` kiểm tra hành động bằng mô hình bàn chơi, rồi GUI tiến/lùi qua các trạng thái đã lưu.

Search engine không import Pygame nên có thể được kiểm thử độc lập trên terminal.

## 13. Kết quả kiểm thử hiện tại

Với bản đồ nhỏ:

```text
Actions = [East, East, East]
Total cost = 3
```

Với bản đồ ví dụ trong đề, cả UCS và A* đều tìm được lời giải có chi phí 34. A* mở rộng ít node hơn UCS vì được heuristic định hướng.


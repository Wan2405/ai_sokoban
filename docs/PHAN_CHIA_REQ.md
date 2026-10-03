# Phân chia mã nguồn theo Req và cách các phần gọi nhau

## Req 1 — Mô hình hóa bài toán

Thư mục: `source/task1_sokoban/req_1/`.

| File | Làm gì? | Thành phần chính |
| --- | --- | --- |
| `state.py` | Lưu vị trí người chơi và tập vị trí thùng; so sánh trạng thái, tránh xét lặp | `SokobanState` |
| `map_loader.py` | Đọc ký tự map; tách tường, sàn, đích và trạng thái ban đầu | `MapLoader.load()`, `SokobanMap` |
| `sokoban_problem.py` | Xác định hướng hợp lệ, chuyển trạng thái, kiểm tra đích và chi phí 1; loại thùng kẹt tĩnh | `SokobanProblem` |

Core dùng tọa độ `(hàng, cột)`. Mô hình GUI gốc dùng `(cột, hàng)` hay `(x, y)`.
Mô hình GUI được giữ trong Req 5 để dùng lại phần giao diện của bạn trong nhóm.
File cầu nối trong Req 5 chuyển đổi tọa độ giữa hai mô hình.
Kiểm thử kết nối so sánh chuyển trạng thái ở hai mô hình.
`gui_model.py` cùng lịch sử trong `Board` thuộc Req 5. Req 1 chỉ chứa ba file core gốc.

Sáu thành phần mô hình hóa: trạng thái `(player_position, box_positions)`; trạng thái ban đầu
đọc từ map; hành động bốn hướng; kết quả đi/đẩy hợp lệ; đích khi mọi thùng nằm trên đích;
chi phí mỗi hành động bằng 1 và chi phí đường đi bằng tổng số hành động.

## Req 2 — UCS, A* và heuristic

Thư mục: `source/task1_sokoban/req_2/`.

| File | Làm gì? | Thành phần chính |
| --- | --- | --- |
| `uniform_cost_search.py` | Lấy nút có chi phí đã đi `g` nhỏ nhất, tìm lời giải | `UniformCostSearch.search()` |
| `a_star_search.py` | Lấy nút có `f = g + h` nhỏ nhất | `AStarSearch.search()` |
| `heuristic.py` | Duyệt BFS ngược từ đích, ghép mỗi thùng với một đích riêng để ước lượng tổng số lần đẩy tối thiểu | `BoxGoalDistanceHeuristic.calculate()` |
| `search_node.py` | Lưu trạng thái, nút cha, hành động và chi phí; truy vết lời giải | `SearchNode.get_solution_actions()` |
| `search_result.py` | Đóng gói việc tìm thấy lời giải, hành động, chi phí và số liệu | `SearchResult` |

Heuristic không sử dụng Euclid/Manhattan. Nó bỏ qua các thùng khác và đường đi của người chơi
để tạo bài toán dễ hơn, vì vậy ước lượng là một cận dưới của số hành động còn lại.
`h` là **ước lượng** số lần đẩy, không phải số bước thật chắc chắn cần để giải.

## Req 5 — Giao diện và phát lại

Thư mục: `source/task1_sokoban/req_5/`.

| File / thư mục | Làm gì? |
| --- | --- |
| `gui_model.py` | Mô hình bàn chơi và lịch sử của GUI: `Level`, `Board`, `Snapshot`, `load_default_levels()`; chuyển từ `model.py` của bạn làm GUI |
| `solver_bridge.py` | File thêm khi ghép: đổi tọa độ, lấy trạng thái hiện tại, gọi core Req 1–2 và trả kết quả GUI cần |
| `app.py` | Tạo cửa sổ, xử lý nút/phím, menu, chọn thuật toán, gọi core và điều khiển phát lại |
| `renderer.py` | Vẽ tường, sàn, đích, thùng, người chơi và hiệu ứng chuyển bước |
| `replay.py` | Kiểm tra toàn bộ lời giải và tổng chi phí trước khi nạp vào lịch sử phát lại |
| `assets/` | Các ảnh PNG của GUI gốc, giữ nguyên dữ liệu |
| `__main__.py` | Cho phép chạy gói bằng `python -m source.task1_sokoban.req_5` |

Req 1–2 là phần core của bạn. Hai file phục vụ GUI nêu trên được đặt trong Req 5
để thể hiện rõ phân công. Việc chuyển vị trí file không thay đổi thuật toán tìm kiếm.

## Req 6 — Luật hai tác nhân

Thư mục: `source/task1_sokoban/req_6/`.

`competition.py` chứa `CompetitiveState` và `CompetitiveBoard`: hai vị trí người chơi,
thùng, quyền sở hữu điểm, hai hành động đồng thời, xử lý va chạm, giới hạn n lượt và kết quả.
Giao diện ở Req 5 chỉ nhận thao tác rồi hiển thị trạng thái của mô hình này.

Core một tác nhân của Req 2 chưa điều khiển hai người chơi. Thuật toán điều khiển cạnh tranh
là phần riêng của nhóm; không coi việc chuyển UCS một tác nhân sang đây là đủ.

## Req 7 — Giao ước và thực thi agent

Thư mục: `source/task1_sokoban/req_7/`.

`agent_api.py` định nghĩa `AgentView`, nạp agent từ module hoặc file `.py`, và
`AgentRunner` chạy quyết định trên thread riêng với giới hạn 1000 ms. Agent lỗi,
quá giờ hoặc trả hướng không hợp lệ không làm dừng trận; runner dùng lại hướng
trước đó. `arena.py` chạy hai agent không cần GUI và báo điểm, thời gian, timeout
và lỗi.

`agent_greedy.py` là agent BFS tham lam, `agent_lookahead.py` là agent
DLS/IDS; `agent_tools.py` cung cấp BFS khoảng cách đi bộ và reverse BFS số
lần đẩy. `arena.py` chạy hai agent không cần GUI và báo điểm, thời gian,
timeout và lỗi. GUI Req 5 cho phép chuyển từng tác nhân giữa Người và AI để
chạy thử hai agent đấu với nhau.

## Req 8 — Tích hợp agent nhóm khác

Thư mục: `source/task1_sokoban/req_8/`.

`agent_external_test.py` là fixture agent ngoài tối giản, có `NAME` và
`choose_action(view, time_limit)` đúng giao ước Req 7. Fixture này dùng để
kiểm tra đường đi đầy đủ từ import module, chạy arena đến chọn và hiển thị
agent trong GUI. Agent thật của nhóm khác cũng được nạp qua đường dẫn file
`.py` hoặc tên module bằng các tùy chọn `--agent1` và `--agent2`.

## Luồng khi bấm UCS hoặc A*

1. `main.py` gọi `main()` trong `req_5/app.py`.
2. `main()` đọc bốn map bằng `req_5/gui_model.py → load_default_levels()`.
3. `SokobanApp` tạo `Board`, `BoardRenderer`, nối `self.solver = solve_board`.
4. Người dùng bấm UCS hoặc A*. `SokobanApp.act()` tạo bản sao bàn chơi hiện tại,
   chạy `req_5/solver_bridge.py → solve_board(candidate, self.algorithm)` ở luồng nền
   và hiển thị loading; môi trường không có cửa sổ dùng luồng chính để kiểm thử.
5. `create_map_from_board()` đổi tọa độ, lấy tường/đích/sàn và vị trí hiện tại, tạo `SokobanMap`.
6. `solve_board()` tạo `SokobanProblem`, rồi gọi `UniformCostSearch.search()` hoặc
   `AStarSearch.search()` cùng heuristic.
7. Thuật toán lấy nút ưu tiên nhất, kiểm tra đích, sinh các trạng thái kế tiếp từ Req 1.
   Đạt đích thì truy theo nút cha để lấy danh sách hành động; trả `SearchResult`.
8. Cầu nối lấy `result.actions` và `result.total_cost` trả về GUI. Nếu không tìm được
   lời giải, cầu nối báo lỗi có nội dung tiếng Việt để GUI hiển thị.
9. `load_solution()` tạo `Replay`. `Replay` kiểm tra từng hành động hợp lệ, chi phí bằng
   số hành động và trạng thái cuối đạt đích rồi mới nạp lịch sử.
10. Space phát tự động. → dùng `Board.redo()`; ← dùng `Board.undo()`.
    `BoardRenderer` vẽ trạng thái tại bước hiện tại. Thuật toán không phải tính lại mỗi bước.

Thuật toán tìm kiếm xét nhiều trạng thái trong bộ nhớ trước khi GUI phát lại. Người chơi
trên màn hình không tự đi theo từng trạng thái mà thuật toán đang xét; nó thực hiện
danh sách hành động cuối cùng khi người dùng bấm phát hoặc tiến bước.

## Luồng khi chạy Terminal

`main_cli.py` đọc map bằng `MapLoader.load()`, tạo `SokobanProblem`, gọi thuật toán và
in `SearchResult`. Luồng này không nhập Pygame, không cần mở cửa sổ.

## Những thay đổi khi ghép

- Chuyển các file vào thư mục Req và đổi đường dẫn `import`.
- Thêm `solver_bridge.py`, `main.py`, kiểm thử kết nối và hướng dẫn theo cấu trúc mới.
- Đổi `main.py` core cũ thành `main_cli.py`, chỉnh đường dẫn map mặc định.
- GUI mặc định nạp bốn map core, bỏ qua dòng rỗng cuối file khi đọc.
- Giữ nguyên logic UCS, A*, heuristic, luật đi/đẩy, luật hai tác nhân và hình ảnh gốc.
- Các kiểm tra GUI ghi ảnh vào `output/gui_checks/` để không làm bẩn thư mục mã.
- `gui_model.py` và `solver_bridge.py` nằm trong Req 5; Req 1–2 chỉ giữ phần core gốc.

Không có Req 3, 4, 7 giả lập trong ZIP; nhóm bổ sung các phần đó khi có nguồn thật.

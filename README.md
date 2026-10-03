# AI Midterm — Sokoban, chia theo từng Req
<img width="2488" height="3312" alt="image" src="https://github.com/user-attachments/assets/79f38e1d-830a-4840-8204-b9a7e30a853b" />


Bản này ghép core UCS/A* với giao diện Pygame và giữ luật hai tác nhân của GUI.
Mỗi hành động hợp lệ có chi phí **1**. Bốn file map gốc của core được giữ nguyên nội dung.

## 1. Chạy trên VS Code / Windows

1. Giải nén ZIP. Mở thư mục **AI_midterm** bằng **File → Open Folder**.
   Thư mục đang mở phải chứa `main.py`, `requirements.txt`, `source` và `tests`.
2. Dùng Python **3.10 trở lên**; có thể dùng Python 3.12.
3. Mở **Terminal → New Terminal** và chạy lần lượt:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Không cần kích hoạt môi trường ảo bằng `Activate.ps1`; các lệnh trên dùng trực tiếp
Python của `.venv` nên tránh lỗi chính sách chạy script trong PowerShell.
Trong VS Code, chọn **Ctrl+Shift+P → Python: Select Interpreter → .venv**.
Nếu máy chỉ nhận lệnh `py`, dùng `py -3 -m venv .venv` cho lệnh đầu tiên.

Chương trình mở menu **1 tác nhân / 2 tác nhân**. Chọn **1 tác nhân** để dùng core của bạn.
Trong chế độ **1 tác nhân**, bấm trực tiếp **UCS** hoặc **A*** để tìm lời giải;
giao diện sẽ hiện loading trong lúc tính toán.

| Thao tác | Phím hoặc nút |
| --- | --- |
| Đi tay | Mũi tên hoặc W/A/S/D |
| Phát / tạm dừng lời giải | Space hoặc nút phát |
| Tiến / lùi một bước trong lời giải | → / ← hoặc hai nút cạnh nút phát |
| Đặt lại map | R hoặc nút chơi lại |
| Đổi map | Page Up / Page Down hoặc hai nút trên cùng |
| Hướng dẫn | H hoặc F1 |

Sau khi tìm được lời giải, người chơi ở bước đầu của lượt phát lại.
Bấm Space hoặc → để thực hiện các hành động. Có thể đi tay trước rồi mới tìm lời giải;
thuật toán sẽ giải từ trạng thái hiện tại.

## 2. Cây thư mục theo Req

Các đường dẫn trong bảng là đường dẫn tính từ thư mục `AI_midterm`.

| Thư mục / file | Trách nhiệm |
| --- | --- |
| `main.py` | Mở GUI đã nối với core |
| `main_cli.py` | Chạy core trong Terminal, không cần Pygame |
| `source/task1_sokoban/req_1/` | Core của bạn: bản đồ, trạng thái, hành động, chuyển trạng thái, đích và chi phí |
| `source/task1_sokoban/req_2/` | Core của bạn: UCS, A*, heuristic, nút tìm kiếm và kết quả |
| `source/task1_sokoban/req_5/` | Phần GUI: mô hình bàn chơi, cầu nối tới core, giao diện, vẽ hình và phát lại; `assets/` nằm trong thư mục này |
| `source/task1_sokoban/req_6/` | Trạng thái và luật cạnh tranh của hai tác nhân |
| `source/task1_sokoban/req_7/` | Giao ước agent, AgentRunner, arena, agent BFS và agent IDS/DLS |
| `source/task1_sokoban/req_8/` | Fixture agent ngoài và luồng import agent của nhóm khác |
| `source/task1_sokoban/maps/` | Bốn map gốc của core; map mẫu của GUI nằm riêng trong `gui_drafts/` |
| `tests/` | Kiểm thử core, GUI và việc kết nối |
| `docs/` | Phân chia Req, giải thích core và hướng dẫn GUI / hai tác nhân |
| `output/` | Ảnh do các lệnh kiểm tra sinh ra; không đưa vào Git |

Xem nội dung từng file và luồng gọi hàm trong [docs/PHAN_CHIA_REQ.md](docs/PHAN_CHIA_REQ.md).
Các file `__init__.py` giúp Python nhận biết các thư mục mã là gói (package); hãy giữ chúng.

Req 1–2 chỉ chứa các file core gốc của bạn. `gui_model.py` được chuyển từ `model.py`
của bạn làm GUI; `solver_bridge.py` là file thêm khi ghép. Cả hai nằm trong Req 5.

## 3. Chạy core riêng trong Terminal

Không cần cài Pygame để chạy các lệnh này:

```powershell
.\.venv\Scripts\python.exe main_cli.py source/task1_sokoban/maps/map_test.txt ucs
.\.venv\Scripts\python.exe main_cli.py source/task1_sokoban/maps/map_test.txt astar
```

Nếu không truyền tham số, `main_cli.py` dùng `map_test.txt` và A*.
Kết quả gồm danh sách `North/East/West/South`, tổng chi phí và các số liệu tìm kiếm.
Heuristic dùng BFS ngược từ đích và ghép thùng với các đích khác nhau;
**không dùng khoảng cách Euclid hoặc Manhattan**.

## 4. Chạy kiểm thử

Chạy tại thư mục ngoài cùng có `main.py`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m tests.check_requirements
.\.venv\Scripts\python.exe -m tests.check_presentation
```

Lệnh đầu chạy toàn bộ kiểm thử core, tích hợp GUI và agent (hiện có 15 kiểm thử).
Hai lệnh sau kiểm tra thêm các nút, phát lại, kích thước cửa sổ, menu và luật hai tác nhân.
Ảnh kiểm chứng được ghi vào `output/gui_checks/`.

| Map | Tổng chi phí UCS | Tổng chi phí A* |
| --- | ---: | ---: |
| `map_test.txt` | 3 | 3 |
| `map_two_boxes.txt` | 8 | 8 |
| `example_map.txt` | 34 | 34 |
| `map_already_solved.txt` | 0 | 0 |

Có thể chỉ chạy core: `python -m unittest tests.test_core_search -v`.
Xem phạm vi kiểm tra của bản ZIP trong [docs/KET_QUA_KIEM_THU.md](docs/KET_QUA_KIEM_THU.md).

## 5. Đọc một map riêng hoặc kiểm tra khởi động

```powershell
.\.venv\Scripts\python.exe main.py --map source/task1_sokoban/maps/example_map.txt
.\.venv\Scripts\python.exe main.py --frames 2
.\.venv\Scripts\python.exe main.py --screenshot output/preview.png
```

Đường dẫn map do bạn truyền được tính từ thư mục Terminal hiện tại.
Bộ map mặc định và đường dẫn hình ảnh được tính theo vị trí mã nguồn.
File map dùng `%` (tường), `A` (người chơi), `B` (thùng), `C` (thùng trên đích),
`D` (đích), dấu cách (sàn). Không xóa dấu cách khi sửa map.

## 6. Ghép vào repo đã clone

ZIP không chứa lịch sử Git hoặc môi trường ảo. Nếu dùng repo đã clone:

1. Sao lưu thư mục repo trước khi thay cấu trúc.
2. Chép **nội dung bên trong thư mục AI_midterm của ZIP** vào thư mục repo;
   giữ thư mục `.git` của repo. Không lồng thêm một thư mục `AI_midterm` nữa.
3. Chạy lại kiểm thử từ cấu trúc mới. Các file GUI cũ ở ngoài cùng đã có vị trí mới trong
   `req_5`, `req_6`; chỉ giữ một bộ nguồn đang dùng để tránh nhầm bản.
4. Xem `git status`, `git diff`, rồi commit trên nhánh của bạn.

File `.gitignore` bỏ qua `.venv`, bộ nhớ đệm Python và ảnh kiểm thử sinh ra.
Req 3 và Req 4 chưa nằm trong phạm vi bản ghép này; Req 7 và Req 8 đã có trong
`source/task1_sokoban/req_7/` và `source/task1_sokoban/req_8/`.

## 7. Req 7 — Giao ước agent và chạy arena

Req 7 nằm trong `source/task1_sokoban/req_7/` và dùng trực tiếp luật cạnh tranh
đồng thời của Req 6. Agent chỉ cần cung cấp:

```python
NAME = "Tên ngắn"  # tùy chọn

def choose_action(view, time_limit):
    return "North"  # East, South hoặc West cũng hợp lệ
```

`AgentView` cung cấp vị trí hai tác nhân, thùng, đích, số lượt còn lại và trạng
thái hiện tại. `AgentRunner` gọi agent trên thread riêng, giới hạn mặc định
1000 ms; agent bị timeout, lỗi hoặc trả action sai sẽ lặp action trước để trận
tiếp tục an toàn.

Chạy hai agent từ terminal:

```powershell
.\.venv\Scripts\python.exe -m source.task1_sokoban.req_7.arena `
  --agent1 path\to\agent1.py --agent2 path\to\agent2.py --steps 40
```

Hai agent của nhóm đã được tích hợp trong Req 7: `agent_greedy` dùng BFS để
tìm đường tới vị trí đẩy tốt, còn `agent_lookahead` dùng DLS/IDS. Ở màn hình
**2 tác nhân**, bấm nút `1: Người` hoặc `2: Người` để đổi từng bên thành AI,
sau đó bấm tiếp để luân phiên qua các agent đã đăng ký, trong đó có
`req_8.agent_external_test` đại diện cho agent nhóm khác. Bấm **Bắt đầu** để
cho hai agent tự đấu. Có thể truyền agent thật khác bằng `--agent1` và
`--agent2`; GUI sẽ hiện `NAME` của agent đó trong nút chọn và thanh trạng thái
trận.

### Chiến thuật của hai agent

- Khoảng cách đi bộ được tính bằng BFS trên các ô có thể đi qua.
- Khoảng cách đẩy được tính bằng reverse BFS từ các đích; ô không có khoảng
  cách được xem là ô chết và không được chọn làm vị trí đẩy.
- `agent_greedy` chọn vị trí đứng đẩy có điểm đánh giá thấp nhất dựa trên
  khoảng cách đi bộ và số lần đẩy còn lại.
- `agent_lookahead` dùng DLS/IDS để tìm đường trong giới hạn độ sâu.
- Cả hai agent có thể chọn thùng chưa thuộc mình, nên hỗ trợ chiến thuật
  **cướp thùng của đối thủ**.
- Khi ô đứng đẩy bị đối thủ chiếm, `approach_spot()` tìm waypoint lân cận
  để agent thoát thế kẹt và tiếp cận lại mục tiêu. Cách này xử lý trường hợp
  hai agent bị đứng sau khi đẩy thùng trong trận `n=40`.

Heuristic của Req 2 và chiến thuật Req 7 không dùng chung nguyên xi:
heuristic Req 2 là cận dưới toàn cục cho A* và ghép thùng với các đích;
Req 7 là đánh giá chiến thuật cục bộ, có xét vị trí người chơi, vị trí đứng
đẩy, quyền sở hữu và khả năng cướp thùng.

## 8. Req 8 — Tích hợp agent nhóm khác

Thư mục `source/task1_sokoban/req_8/` chứa fixture
`agent_external_test.py`, mô phỏng agent của nhóm khác nhưng vẫn tuân thủ giao
ước của Req 7. Fixture này chỉ dùng để kiểm tra việc import, chạy arena và
hiển thị tên agent trong GUI; nó không đại diện cho thuật toán thi đấu chính.
Agent thật của nhóm khác có thể là module hoặc file `.py`, được nạp bằng
`--agent1` và `--agent2` như hướng dẫn ở trên.

Trong GUI, nút chọn từng tác nhân luân phiên qua Người, BFS, IDS/DLS và
`TeamOther-Test`. Chọn AI cho cả hai bên rồi bấm **Bắt đầu** để chạy chế độ
AI-vs-AI. Tên agent và thời gian phản hồi gần nhất được hiển thị trên giao diện.

Ví dụ chạy fixture agent ngoài đấu với BFS:

```powershell
.\.venv\Scripts\python.exe -m source.task1_sokoban.req_7.arena `
  --agent1 source.task1_sokoban.req_8.agent_external_test `
  --agent2 source.task1_sokoban.req_7.agent_greedy --steps 40
```

Agent ngoài phải có dạng:

```python
NAME = "Ten agent"

def choose_action(view, time_limit):
    return "East"  # North, East, South hoặc West
```

## 9. Phạm vi và giới hạn

- Req 1–2 là tìm kiếm cho **một tác nhân**. Req 6 giữ luật hai tác nhân; các
  agent cạnh tranh của Req 7 dùng giao ước riêng, không chuyển UCS/A* một tác
  nhân thành thuật toán thi đấu.
- Hai agent cạnh tranh được chạy nền trong GUI, nên agent chậm không làm treo
  cửa sổ; timeout, lỗi hoặc hành động sai sẽ lặp lại hành động trước.
- Luật Req 6 xử lý lượt đi đồng thời, va chạm, đẩy thùng, giành/cướp thùng,
  ghi nhận chủ sở hữu thùng trên đích và giới hạn số lượt `n`.
- Req 7 đã được kiểm tra bằng trận BFS-vs-IDS/DLS 40 lượt và luồng AI-vs-AI
  trong GUI. Req 8 đã được kiểm tra bằng fixture agent ngoài trong arena và
  bằng việc chọn/hiển thị agent đó trong GUI.
- Hai map nháp gốc vẫn được giữ trong `LEVELS` để chạy kiểm tra GUI. Map “Kho gạch nhỏ”
  có một thùng bị kẹt nên không có lời giải; nó không nằm trong bộ map mặc định của ứng dụng.
- Việc tìm kiếm chạy cùng luồng với GUI. Với map lớn, cửa sổ có thể tạm chờ trong lúc tìm.
- Bản ghép được kiểm tra trên Python 3.12 / Linux với `pygame-ce==2.5.8` bằng chế độ
  không mở cửa sổ. Chưa kiểm tra trực tiếp trên máy Windows hoặc macOS của nhóm.
"# ai_sokoban" 

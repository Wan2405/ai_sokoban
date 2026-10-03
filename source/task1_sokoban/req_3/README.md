So sánh UCS và A*
## 1. Mục tiêu
Req 3 thực hiện thực nghiệm để so sánh Uniform Cost Search (UCS) và A*
trên cùng tập bản đồ Sokoban. Việc so sánh dựa trên thời gian tìm kiếm,
chi phí lời giải và số lượng trạng thái/nút được xử lý trong quá trình
tìm kiếm.

## 2. Cách chạy
Chạy từ thư mục gốc của project:

python -m source.task1_sokoban.req_3.benchmark
Không dùng đường dẫn kiểu Windows như source\task1_sokoban\... để bảo
đảm lệnh có thể chạy trên macOS/Linux.

Thư viện cần thiết cho việc ghi Excel và vẽ biểu đồ:

pip install openpyxl matplotlib
Các thư viện đã được khai báo trong requirements.txt và cố định phiên bản
theo môi trường chạy của nhóm để các thành viên sử dụng cùng phiên bản
thư viện.

## 3. Phương pháp thực nghiệm
Tập dữ liệu
Benchmark sử dụng 4 map:

Map Mục đích

example_map.txt Map chính để quan sát rõ sự khác
biệt về số node giữa UCS và A*.

map_already_solved.txt Kiểm tra trường hợp trạng thái ban
đầu đã là trạng thái đích.

map_test.txt Kiểm tra trên một map có độ
khó/trạng thái khác với map ví dụ.

map_two_boxes.txt Kiểm tra trên map có hai box, giúp đánh giá thuật toán trên trạng thái phức tạp hơn.

Mỗi cặp (map, thuật toán) được chạy 5 lần. Việc lặp lại giúp
giảm ảnh hưởng của dao động thời gian đo giữa các lần chạy.

Hai thuật toán sử dụng cùng SokobanProblem và cùng cơ chế sinh trạng
thái kế tiếp. Vì vậy, khác biệt về số node được mở rộng/sinh ra chủ yếu
phản ánh cách UCS và A* lựa chọn trạng thái tiếp theo.

## 4. Các độ đo
Độ đo Ý nghĩa

Time_ms Thời gian tìm kiếm, tính bằng
mili-giây. Chỉ tính thời gian
search, không tính thời gian khởi
tạo heuristic.

Path_Cost Tổng chi phí của lời giải tìm được.

Expanded_Nodes Số node được lấy ra để mở rộng. Đây
là độ đo ít phụ thuộc vào tốc độ
của máy hơn thời gian chạy.

Generated_Nodes Số node được sinh ra trong quá
trình tìm kiếm. Đây cũng là độ đo
tương đối độc lập với phần cứng.

Max_Frontier_Size là phép đo không gian gián tiếp. Benchmark hiện
tại chưa đo trực tiếp số byte bộ nhớ mà chương trình sử dụng.

## 5. Kết quả
Kết quả tổng hợp được lấy từ sheet Summary trong file Excel sau lần
chạy benchmark cuối cùng.

Ở example_map, kết quả cho thấy UCS mở rộng khoảng 39.616 node,
trong khi A* mở rộng khoảng 6.211 node. Hai thuật toán vẫn tìm được
lời giải có cùng Path_Cost khoảng 34.

Lưu ý: thời gian (Time_ms) có thể thay đổi giữa các lần chạy do phụ
thuộc vào máy và môi trường thực thi. Vì vậy khi nộp báo cáo nên sử
dụng số liệu từ lần chạy cuối cùng.

## 6. Phân tích
Cả UCS và A* đều tìm được lời giải tối ưu trong các trường hợp được
kiểm tra.

Trên example_map, A* mở rộng ít node hơn đáng kể so với UCS và có xu
hướng giữ frontier nhỏ hơn. Điều này phù hợp với cơ chế của A*: ngoài
chi phí đã đi g(n), A* còn sử dụng heuristic để ước lượng phần chi phí
còn lại và ưu tiên những trạng thái có triển vọng hơn.

Tuy nhiên, số node ít hơn không đồng nghĩa thời gian chạy luôn nhỏ hơn.
Trên map lớn, mỗi node được xét bởi A* còn phải tính heuristic. Chi phí
tính heuristic có thể làm giảm hoặc triệt tiêu lợi thế về số node, nên
Time_ms cần được đánh giá riêng thay vì suy ra trực tiếp từ
Expanded_Nodes.

## 7. Hạn chế
Số lượng map còn ít nên chưa đại diện cho toàn bộ các dạng Sokoban.

Max_Frontier_Size chỉ đo gián tiếp mức sử dụng bộ nhớ; chưa có
phép đo bộ nhớ thực tế theo byte.

Time_ms phụ thuộc vào phần cứng, hệ điều hành và tải của máy tại
thời điểm chạy.

Nếu bổ sung map mới, cần cập nhật lại cả danh sách map trong phương
pháp thực nghiệm và bảng/kết quả trong README.

## 8. Các file trong thư mục
benchmark.py: chương trình chạy benchmark UCS và A*.

results/sokoban_results.csv: dữ liệu thô của từng lần chạy.

results/sokoban_results.xlsx: file Excel gồm:

Raw_Data: dữ liệu từng lần chạy.

Summary: số liệu tổng hợp theo từng (Map, Algorithm).
README Req 4 -- Phân tích heuristic

## 1. Mục tiêu

Req 4 nhằm thảo luận và kiểm chứng hai tính chất quan trọng của
heuristic trong A*: admissible và consistent. Việc kiểm chứng
được thực hiện trên các trạng thái được lấy mẫu từ các map Sokoban.

## 2. Mô tả heuristic

Heuristic được sử dụng để ước lượng chi phí còn lại từ trạng thái hiện
tại đến trạng thái đích. Heuristic trong bài không sử dụng trực tiếp
khoảng cách Manhattan hoặc khoảng cách Euclid.

Phần cài đặt heuristic nên được đọc cùng với heuristic.py để mô tả
chính xác công thức và cách xử lý từng trạng thái; README chỉ tóm tắt ý
tưởng thay vì chép lại code.

## 3. Định nghĩa

Admissible

Một heuristic h là admissible nếu với mọi trạng thái s:

h(s) ≤ h*(s)

trong đó h*(s) là chi phí thật nhỏ nhất từ s đến trạng thái đích.

Ngoài ra, tại trạng thái đích:

h(goal) = 0

Consistent

Một heuristic là consistent nếu với mọi cạnh chuyển trạng thái s -> s'
có chi phí c:

h(s) ≤ c + h(s')

và:

h(goal) = 0

Tính consistent mạnh hơn admissible: một heuristic consistent thì cũng
admissible khi các điều kiện thông thường của bài toán được thỏa mãn.

## 4. Thảo luận lý thuyết

Vì sao heuristic không được vượt quá chi phí thật?

Nếu h(s) lớn hơn chi phí tối ưu thật h*(s), heuristic có thể đánh
giá một trạng thái là đắt hơn thực tế. Khi đó A* có thể ưu tiên sai
trạng thái và tính tối ưu của tìm kiếm không còn được bảo đảm theo điều
kiện admissible.

Tính consistent

Điều kiện:

h(s) ≤ c(s, s') + h(s')

đảm bảo heuristic không giảm quá mức khi đi qua một cạnh. Có thể hiểu
rằng chênh lệch giữa hai giá trị heuristic không vượt quá chi phí của
bước chuyển.

Deadlock và trạng thái không giải được

Sokoban có các trạng thái deadlock, trong đó box có thể bị đẩy vào vị
trí khiến bài toán không còn lời giải. Khi phân tích heuristic, cần phân
biệt việc heuristic đánh giá một trạng thái với việc trạng thái đó thực
sự có lời giải hay không. Các trạng thái không giải được không nên được
dùng để kết luận rằng một giá trị heuristic hữu hạn chính là chi phí lời
giải thực tế.

## 5. Thiết kế thí nghiệm

Req 4 có 3 nhóm kiểm tra:

5.1. GoalZero

Kiểm tra:

h(goal) = 0

Kết quả hiện tại: 4/4 mẫu đạt điều kiện.

5.2. Admissibility

Với mỗi trạng thái được lấy mẫu, tính h(s) và so sánh với h*(s),
trong đó h*(s) được tính bằng UCS bắt đầu từ chính trạng thái đó.

Điều kiện kiểm tra:

h(s) ≤ h*(s)

Kết quả hiện tại: 94/94 mẫu đạt điều kiện.

5.3. Consistency

Kiểm tra trực tiếp trên từng cạnh chuyển trạng thái:

h(s) ≤ cost(s, s') + h(s')

Kết quả hiện tại: 334/334 cạnh đạt điều kiện.

Cách lấy mẫu

Các trạng thái được lấy bằng BFS, tối đa 40 trạng thái mỗi map.

## 6. Đọc file kết quả

CSV của Req 4 chứa các loại dòng phục vụ cho các phép kiểm tra khác
nhau. Vì vậy không phải cột nào cũng có ý nghĩa với mọi loại kiểm tra.

Cột                                 Ý nghĩa

Next_State                        Trạng thái kế tiếp, chủ yếu dùng
khi kiểm tra Consistency.

cost                              Chi phí cạnh s -> s', dùng cho
Consistency.

h_next                            Giá trị heuristic của trạng thái kế
tiếp, dùng cho Consistency.

map_already_solved là trường hợp đặc biệt: trạng thái ban đầu đã là
goal nên không có nước đi tiếp theo. Vì vậy map này không tạo ra dòng để
kiểm tra Consistency.

## 7. Kết luận và hạn chế

Trên các trạng thái và cạnh đã được lấy mẫu, không tìm thấy phản ví
dụ vi phạm điều kiện admissible hoặc consistent. Kết quả này là bằng
chứng thực nghiệm trên tập mẫu, không phải một chứng minh toán học rằng
heuristic luôn admissible hoặc consistent trên mọi trạng thái Sokoban.

Các hạn chế chính:

Số lượng trạng thái kiểm tra còn nhỏ.

Mẫu có xu hướng tập trung gần trạng thái ban đầu do cách lấy mẫu
BFS.

Vì vậy kết quả chưa thể đại diện cho toàn bộ không gian trạng thái
của Sokoban.

Về độ chặt, heuristic có thể còn khá lỏng vì bỏ qua một phần chi phí di
chuyển của người. Ví dụ có trường hợp h = 10 trong khi h* = 35;
heuristic vẫn admissible nhưng còn cách khá xa chi phí tối ưu thực tế.

## 8. Cách chạy và vị trí file kết quả

Req 4 dùng `openpyxl` để ghi bảng tính và `matplotlib` để tạo biểu đồ;
hai thư viện này đã được khai báo trong `requirements.txt`.

Chạy từ thư mục gốc của project:

python -m source.task1_sokoban.req_4.heuristic_test

Không dùng đường dẫn Windows trong README nếu mục tiêu là hỗ trợ cả
macOS/Linux.

Sau khi chạy, các file kết quả được lưu trong:

source/task1_sokoban/req_4/results/

bao gồm CSV và XLSX do chương trình Req 4 sinh ra.
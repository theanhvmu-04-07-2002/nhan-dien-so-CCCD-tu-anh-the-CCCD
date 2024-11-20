# thư viện xử lý ảnh và thị giác máy tính
import cv2
# thư viện nhận dạng ký tự quang học
import pytesseract

#1 Lấy ảnh từ webcam
cap = cv2.VideoCapture(0)

while True:
    #1 Đọc ảnh từ webcam
    ret, frame = cap.read()

    #2 Đổi màu hình ảnh. Chuyển không gian màu: BGR -> xám: giảm chiều dài vecter màu thành ma trận đơn giản.
       # -> giảm mức độ phức tạp khi xử lý ảnhqq
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #3 Áp dụng bộ lọc Gaussian để giảm nhiễu: loại bỏ nhiễu nhỏ, giảm thiểu ảnh hưởng nhiễu lớn trên hình ảnh
        # -> phân biệt rõ ràng các đối tượng
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #4 Áp dụng phép chuyển đổi ngưỡng để tách ký tự với nền :
        # tạo bản đồ nhị phân sử dụng kĩ thuật chuyển đổi ngưỡng threshold để tạo ra hình ảnh chỉ gồm 2 giá trị pixel : 0 và 255
        # -> tách đối tượng từ nền của hình ảnh -> dễ dàng nhận diện
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    #5 Xác định vùng chứa số căn cước công dân trên ảnh
        # sử dụng các biến x y w h để xác định tọa độ . tọa độ (x, y) có chiều rộng w và chiều cao h
    x, y, w, h = 100, 100, 400, 100
    roi = thresh[y:y + h, x:x + w]

    #6 Nhận dạng số căn cước công dân
        # mô hình nhận dạng kí tự được tích hợp sẵn trong thư viện pytesseract :
        # -> tìm và trích xuất các kí tự số thu được
    cccd = pytesseract.image_to_string(roi, config='--psm 6')

    #7 Loại bỏ các kí tự không phải số
        # hàm filter nhận đầu vào là hàm lambda và một list các kí tự đại diện cho chuỗi cần xử lý,
        # -> chỉ giữ lại kí tự là số
    cccd = ''.join(filter(lambda x: x.isdigit(), cccd))

    #8 Kiểm tra nếu có đúng 12 chữ số thì in ra
        # vì số CCCD là dãy gồm đúng 12 kí tự là số nên chỉ khi đọc được 12 kí tự mới hiển thị kq
        # nếu không thỏa mãn, không hiển thị gì cả
    if len(cccd) == 12:
        print(cccd)

    #9 Hiển thị ảnh
        # frame: hình ảnh BGR ban đầu : khung hình chụp được từ Camera
        # thresh : hình ảnh nhị phân gồm 2 vùng đen (đối tượng) và  trắng (nền)
        # -> theo dõi quá trình xử lý ảnh
    cv2.imshow('frame', frame)
    cv2.imshow('thresh', thresh)

    #10 Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#10 Giải phóng tài nguyên
    # giảm thiểu nguy cơ tiêu tốn bộ nhớ
    # giải phóng tài nguyên cho phần cứng
    # đóng tất cả cửa sổ của chương trình
cap.release()
cv2.destroyAllWindows()



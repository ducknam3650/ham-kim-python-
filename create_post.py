import os
from typing import List, Dict
from datetime import datetime

class create_post:
    def __init__(self):
        self.post_name = None
        self.post_text = None
        self.category = None
        self.post: List[Dict[str, str]] = []
        self.current_time = None
    
    def execute(self):
        self.post_name = input("글의 제목을 입력 해주세요: ")
        self.post_text = input("글의 내용을 입력 해주세요: ")
        self.category = self.select_category() 
        self.current_time = datetime.now()  
        self.current_time = self.current_time.strftime("%Y.%m.%d %H:%M:%S")  
        self.display_post()
        self.save_to_file()
        

    def select_category(self) -> str:
        while True:
            try:
                category = int(input("카테고리를 선택하세요 (1.매우 좋음, 2.좋음, 3.그냥저냥, 4.나쁨, 5.매우 나쁨, 6.기타): "))
                if category == 1:
                    return "매우 좋음"
                elif category == 2:
                    return "좋음"
                elif category == 3:
                    return "그냥저냥"
                elif category == 4:
                    return "나쁨"
                elif category == 5:
                    return "매우 나쁨"
                elif category == 6:
                    return "기타"
                else:
                    print("잘못된 선택입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")

    def display_post(self): 
        separator = "-" * 60
        print(f'시간: {self.current_time}')
        print(separator)
        print(f'제목: {self.post_name}')
        print(separator)
        print(f'내용: {self.post_text}')
        print(separator)
        print(f'카테고리: {self.category}')  
        print(separator)
        
    def save_to_file(self): 
        post_dir = 'blog_CRUD' 

        existing_files = [f for f in os.listdir(post_dir) if f.endswith('.txt')]
        next_num = 1
        if existing_files:
            numbers = []
            for f in existing_files:
                try:
                    num_str = f.split('.')[0]
                    if num_str.isdigit():
                        numbers.append(int(num_str))
                except ValueError:
                    continue
            if numbers:
                next_num = max(numbers) + 1
        
        file_name = f"{next_num}.txt"
        file_path = os.path.join(post_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'시간: {self.current_time}\n')
            file.write(f'제목: {self.post_name}\n')
            file.write(f'내용: {self.post_text}\n')
            file.write(f'카테고리: {self.category}\n')
            file.write('-' * 60 + '\n')

if __name__ == "__main__":  
    post_creator = create_post()
    post_creator.execute()

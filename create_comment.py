import os
from typing import List, Dict
from datetime import datetime 

class create_comment:
    def __init__(self):
        self.post_dir = 'blog_CRUD'
        os.makedirs(self.post_dir, exist_ok=True)
        self.existing_files = [f for f in os.listdir(self.post_dir) if f.endswith('.txt') and f.split('.')[0].isdigit()]
    
    def get_available_posts(self):
        if not self.existing_files:
            return []
        
        post_numbers = []
        for filename in self.existing_files:
            post_num = int(filename.split('.')[0])
            post_numbers.append(post_num)
        
        return sorted(post_numbers)
    
    def show_available_posts(self):
        if not self.existing_files:
            print("댓글을 달 수 있는 게시물이 없습니다.")
            return []
        
        print("\n--- 댓글 작성 가능한 게시물 목록 ---")
        post_info = {}
        
        for filename in sorted(self.existing_files, key=lambda x: int(x.split('.')[0])):
            file_path = os.path.join(self.post_dir, filename)
            post_num = int(filename.split('.')[0])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[1].replace('제목: ', '').strip() if len(lines) > 1 else '제목 없음'
                post_info[post_num] = {'filename': filename, 'title': title}
                print(f"[{post_num}] 제목: {title}")
        
        return post_info
    
    def execute(self):  
        self.write_comment()
    
    def write_comment(self):
        post_info = self.show_available_posts()
        
        if not post_info:
            return
        
        while True:
            try:
                post_num = int(input("\n댓글을 작성할 게시물 번호를 입력하세요: "))
                if post_num in post_info:
                    break
                else:
                    print("존재하지 않는 게시물 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")
        
        print(f"\n--- {post_num}번 게시물에 댓글 작성 ---")
        author = input("작성자 이름을 입력하세요: ")
        comment_text = input("댓글 내용을 입력하세요: ")
        
        current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        
        post_file = os.path.join(self.post_dir, f"{post_num}.txt")
        
        with open(post_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[댓글]\n")
            f.write(f"작성시간: {current_time}\n")
            f.write(f"작성자: {author}\n")
            f.write(f"내용: {comment_text}\n")
            f.write("=" * 40 + "\n")
        
        print("댓글이 성공적으로 작성되었습니다!")
        
        show_result = input("작성된 댓글을 확인하시겠습니까? (y/n): ")
        if show_result.lower() == 'y':
            self.show_post_with_comments(post_num)
    
    def show_post_with_comments(self, post_num):
        post_file = os.path.join(self.post_dir, f"{post_num}.txt")
        
        if not os.path.exists(post_file):
            print(f"{post_num}번 게시물이 존재하지 않습니다.")
            return
        
        print(f"\n{'='*60}")
        print(f"게시물 {post_num}번 (댓글 포함)")
        print('='*60)
        
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)

if __name__ == "__main__":
    comment_creator = create_comment()
    comment_creator.execute()
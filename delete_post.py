import os
from datetime import datetime

class delete_post:
    def execute(self):  
        self.delete_post()
    
    def delete_post(self): 
        post_dir = 'blog_CRUD'
        os.makedirs(post_dir, exist_ok=True)

        existing_files = [f for f in os.listdir(post_dir) if f.endswith('.txt') and f.split('.')[0].isdigit()]

        if not existing_files:
            print("삭제할 게시물이 없습니다.")
            return

        print("\n--- 게시물 삭제 ---")
        print("삭제 가능한 게시물 목록:")
        file_map = {}
        for filename in sorted(existing_files, key=lambda x: int(x.split('.')[0])):
            file_path = os.path.join(post_dir, filename)
            post_num = int(filename.split('.')[0])
            file_map[post_num] = filename
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[1].replace('제목: ', '').strip() if len(lines) > 1 else '제목 없음'
                print(f"[{post_num}] 제목: {title}")
        
        while True:
            try:
                post_to_delete = int(input("삭제할 게시물 번호를 입력하세요: "))
                if post_to_delete in file_map:
                    break
                else:
                    print("잘못된 게시물 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")
        
        try:
            target_file_path = os.path.join(post_dir, file_map[post_to_delete])
            os.remove(target_file_path)
            print(f"게시물 {post_to_delete}번이 삭제되었습니다.")
        except OSError as e:
            print(f"파일 삭제 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    deleter = delete_post()
    deleter.execute()

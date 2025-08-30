import os
from datetime import datetime

class modify_post:
    def execute(self):
        self.modify_post()

    def modify_post(self):  
        post_dir = 'blog_CRUD'
        os.makedirs(post_dir, exist_ok=True)
        existing_files = [f for f in os.listdir(post_dir) if f.endswith('.txt') and f.split('.')[0].isdigit()]
        
        if not existing_files:
            print("수정할 게시물이 없습니다.")
            return

        print("\n--- 게시물 수정 ---")
        print("수정 가능한 게시물 목록:")
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
                post_to_update = int(input("수정할 게시물 번호를 입력하세요: "))
                if post_to_update in file_map:
                    break
                else:
                    print("잘못된 게시물 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")
        
        target_file_path = os.path.join(post_dir, file_map[post_to_update])
        
        with open(target_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print("\n--- 게시물 내용 수정 ---")
        new_post_name = input(f"새로운 제목을 입력하세요 (현재: {lines[1].replace('제목: ', '').strip()}): ")
        new_post_text = input(f"새로운 내용을 입력하세요 (현재: {lines[2].replace('내용: ', '').strip()}): ")

        lines[1] = f'제목: {new_post_name}\n'
        lines[2] = f'내용: {new_post_text}\n'
        
        with open(target_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"게시물 {post_to_update}번이 수정되었습니다.")

if __name__ == "__main__":
    modifier = modify_post()
    modifier.execute()
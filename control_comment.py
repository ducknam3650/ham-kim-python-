import os
from datetime import datetime

class control_comment:
    def execute(self):
        self.modify_comment()
    
    def get_available_posts(self):
        post_dir = 'blog_CRUD'
        os.makedirs(post_dir, exist_ok=True)
        existing_files = [f for f in os.listdir(post_dir) if f.endswith('.txt') and f.split('.')[0].isdigit()]
        
        if not existing_files:
            return []
        
        posts_with_comments = []
        for filename in existing_files:
            post_num = int(filename.split('.')[0])
            file_path = os.path.join(post_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '[댓글]' in content:
                    posts_with_comments.append(post_num)
        
        return sorted(posts_with_comments)
    
    def show_available_posts(self):
        post_dir = 'blog_CRUD'
        posts_with_comments = self.get_available_posts()
        
        if not posts_with_comments:
            print("수정할 댓글이 있는 게시물이 없습니다.")
            return {}
        
        print("\n--- 댓글 수정 가능한 게시물 목록 ---")
        post_info = {}
        
        for post_num in posts_with_comments:
            filename = f"{post_num}.txt"
            file_path = os.path.join(post_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[1].replace('제목: ', '').strip() if len(lines) > 1 else '제목 없음'
                post_info[post_num] = {'filename': filename, 'title': title}
                print(f"[{post_num}] 제목: {title}")
        
        return post_info
    
    def get_comments_from_post(self, post_num):
        post_dir = 'blog_CRUD'
        post_file = os.path.join(post_dir, f"{post_num}.txt")
        comments = []
        
        with open(post_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        comment_started = False
        current_comment = {}
        comment_index = 0
        
        for i, line in enumerate(lines):
            line = line.rstrip()
            
            if line == "[댓글]":
                comment_started = True
                if current_comment:  
                    current_comment['end_line'] = i - 1
                    comments.append(current_comment)
                current_comment = {'start_line': i, 'index': comment_index}
                comment_index += 1
                continue
            
            if comment_started and line.startswith("작성시간: "):
                current_comment['time'] = line.replace("작성시간: ", "")
            elif comment_started and line.startswith("작성자: "):
                current_comment['author'] = line.replace("작성자: ", "")
            elif comment_started and line.startswith("내용: "):
                current_comment['content'] = line.replace("내용: ", "")
            elif comment_started and line.startswith("=" * 40):
                current_comment['end_line'] = i
                comments.append(current_comment)
                current_comment = {}
                comment_started = False
        
        if current_comment and 'start_line' in current_comment:
            current_comment['end_line'] = len(lines) - 1
            comments.append(current_comment)
        
        return comments
    
    def show_comments_list(self, post_num):
        comments = self.get_comments_from_post(post_num)
        
        if not comments:
            print(f"{post_num}번 게시물에 댓글이 없습니다.")
            return []
        
        print(f"\n--- {post_num}번 게시물의 댓글 목록 ---")
        for i, comment in enumerate(comments):
            time_info = comment.get('time', '')
            author_info = comment.get('author', '알 수 없음')
            content_info = comment.get('content', '내용 없음')[:30]
            print(f"[{i + 1}] 시간: {time_info} | 작성자: {author_info} | 내용: {content_info}...")
        
        return comments
    
    def modify_comment(self):  
        post_info = self.show_available_posts()
        
        if not post_info:
            return

        while True:
            try:
                post_num = int(input("\n댓글을 수정할 게시물 번호를 입력하세요: "))
                if post_num in post_info:
                    break
                else:
                    print("존재하지 않는 게시물 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")
        
        comments = self.show_comments_list(post_num)
        if not comments:
            return
        
        while True:
            try:
                comment_index = int(input("수정할 댓글 번호를 입력하세요: "))
                if 1 <= comment_index <= len(comments):
                    selected_comment = comments[comment_index - 1]
                    break
                else:
                    print("잘못된 댓글 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")
        
        print(f"\n--- 현재 댓글 내용 ---")
        print(f"작성시간: {selected_comment.get('time', '')}")
        print(f"작성자: {selected_comment.get('author', '')}")
        print(f"내용: {selected_comment.get('content', '')}")
        
        new_author = input(f"새로운 작성자 이름 (현재: {selected_comment.get('author', '')}): ").strip()
        new_content = input(f"새로운 댓글 내용 (현재: {selected_comment.get('content', '')}): ").strip()
        
        if not new_author:
            new_author = selected_comment.get('author', '')
        if not new_content:
            new_content = selected_comment.get('content', '')
        
        self.update_comment_in_file(post_num, selected_comment, new_author, new_content)
        
        print(f"댓글이 성공적으로 수정되었습니다!")
        
        show_result = input("수정된 댓글을 확인하시겠습니까? (y/n): ")
        if show_result.lower() == 'y':
            self.show_post_with_comments(post_num)
    
    def update_comment_in_file(self, post_num, selected_comment, new_author, new_content): 
        post_dir = 'blog_CRUD'
        post_file = os.path.join(post_dir, f"{post_num}.txt")
        current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        
        with open(post_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = selected_comment['start_line']
        end_line = selected_comment['end_line']
        
        new_comment_lines = [
            "[댓글]\n",
            f"작성시간: {current_time}\n",
            f"작성자: {new_author}\n",
            f"내용: {new_content}\n",
            "=" * 40 + "\n"
        ]
        
        lines[start_line:end_line + 1] = new_comment_lines
        
        with open(post_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    def show_post_with_comments(self, post_num):
        post_dir = 'blog_CRUD'
        post_file = os.path.join(post_dir, f"{post_num}.txt")
        
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
    comment_controller = control_comment()
    comment_controller.execute()

from create_post import create_post
from modify_post import modify_post
from delete_post import delete_post
from create_comment import create_comment
from control_comment import control_comment


class BlogMenu:
    def select_menu(self) -> int:
        print("메뉴를 선택하세요: ")
        print("1. 글쓰기")
        print("2. 글목록") # 미구현
        print("3. 글수정")
        print("4. 글삭제")
        print("5. 댓글쓰기") 
        print("6. 댓글수정")  
        print("7. 댓글삭제") 
        print("8. 종료")
        return int(input("선택: "))
        
    def menu_choice(self, choice): 
        if choice == 1:
            post_creator = create_post()
            post_creator.execute()
        elif choice == 2:
            pass
        elif choice == 3:
            modifier = modify_post()
            modifier.execute()
        elif choice == 4:
            deleter = delete_post()
            deleter.execute()
        elif choice == 5:
            comment_creator = create_comment()
            comment_creator.execute()
        elif choice == 6:
            comment_controller = control_comment()
            comment_controller.execute()
        elif choice == 7:
            self._view_post_with_comments("댓글을 확인할")
        elif choice == 8:
            print("프로그램을 종료합니다.")
            exit()
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")
    
    def _view_post_with_comments(self, action_text: str):
        comment_viewer = create_comment()
        available_posts = comment_viewer.get_available_posts()
        
        if available_posts:
            print("사용 가능한 게시물 번호:", available_posts)
            try:
                post_num = int(input(f"{action_text} 게시물 번호 입력: "))
                if post_num in available_posts:
                    comment_viewer.show_post_with_comments(post_num)
                else:
                    print("존재하지 않는 게시물 번호입니다.")
            except ValueError:
                print("올바른 숫자를 입력하세요.")
        else:
            print("확인할 수 있는 게시물이 없습니다.")
            

if __name__ == "__main__":
    blogmenu = BlogMenu()
    while True:
        choice = blogmenu.select_menu()  
        blogmenu.menu_choice(choice)  
    
  




import pyinputplus as pyip

from controller import Controller


class CLI:
    def __init__(self):
        self.controller = Controller()
        self.current_menu = self.login
        self.running = True
        self.run_menus()

    @staticmethod
    def show_title(title):
        print('\n' + title)
        print('-' * len(title) + '\n')

    def run_menus(self):
        while self.running:
            self.current_menu = self.current_menu()

    def exit_menus(self):
        self.running = False
        print("Goodbye")

    def login(self):
        self.show_title('Login Screen')
        users = self.controller.get_user_names()
        menu_items = users  + ['Create a new account',
                       'Exit',
                       ]
        menu_choice = pyip.inputMenu(menu_items,
                                     prompt='Select user or create a new account\n',
                                     numbered=True,
                                     )
        if menu_choice.lower() == 'create a new account':
            next_menu = self.create_account
        elif menu_choice.lower() == 'exit':
            next_menu = self.exit_menus
        else:
            user_name = menu_choice
            self.controller.set_current_user_from_name(user_name)
            next_menu = self.user_home
        return next_menu

    def create_account(self, existing_users = None):
        self.show_title('Create Account Screen')
        print('Enter Account Details')
        user_name = pyip.inputStr('Username: ', blockRegexes=existing_users, strip=None)
        age = pyip.inputInt('Age: ', min=0, max=150, blank=True)
        gender = pyip.inputMenu(['male', 'female', 'other'], prompt='Gender: ', blank=True)
        nationality = pyip.inputStr('Nationality: ')
        self.controller.create_user(user_name, age, gender, nationality)
        return self.login

    def user_home(self):
        self.show_title(f'{self.controller.current_user.name} Home Screen')
        print(f'Name: {self.controller.current_user.name}')
        print(f'Age: {self.controller.current_user.age}')
        print(f'Nationality: {self.controller.current_user.nationality}')

        menu_items = {'Show your posts': lambda: self.show_posts(self.controller.current_user.name),
                      'Show posts from another user': self.show_posts,
                      'Add post': self.write_post,
                      'Logout': self.login,
                      }

        menu_choice = pyip.inputMenu(list(menu_items.keys()),
                                     prompt='\nSelect an action\n',
                                     numbered=True,
                                     )

        next_menu = menu_items[menu_choice]
        return next_menu

    def show_posts(self, user_name: str|None = None):
        if user_name is None:
            users = self.controller.get_user_names()
            menu_choice = pyip.inputMenu(users,
                                         prompt='Select a user\n',
                                         numbered=True,
                                         )
            user_name = menu_choice

        self.show_title(f"{user_name}'s Posts")
        self.controller.get_posts(user_name)

        for post in self.controller.current_posts:
            print(f'Title: {post.title}')
            print(f'Content: {post.description}')
            print(f'Likes: {post.number_of_likes}')
            self.show_comments(post.id)
        if not self.controller.current_posts:
            print('No Posts')

        menu_items = {'Like a post': self.select_like_post,
                      'Comment on a post': self.comment_on_post,
                      'Return to home': self.user_home,
                      }

        menu_choice = pyip.inputMenu(list(menu_items.keys()),
                                     prompt='\nSelect an action\n',
                                     numbered=True,
                                     )
        return menu_items[menu_choice]

    def show_comments(self, post_id: int):
        comments = self.controller.get_comments(post_id)
        if comments:
            print(f'Comments:')
            for comment in comments:
                print(f'\t{comment["author"]}: {comment["comment"]}')
        print()

    def write_post(self):
        title = input('Title: ')
        content = input('Content: ')
        self.controller.add_post(title, content)

        return self.user_home

    def select_like_post(self):
        self.show_title("Like posts")
        print("Select a post")
        posts = self.controller.current_posts
        menu_items = {post.description: post.id for post in posts}
        menu_items['Return to home'] = None
        menu_choice = pyip.inputMenu(list(menu_items.keys()),
                                     prompt='\nSelect an action\n',
                                     numbered=True,
                                     )
        if post_id := menu_items[menu_choice]:
            self.controller.like_post(post_id)
        return self.user_home

    def comment_on_post(self):
        print('Commenting not yet implemented')
        return self.user_home

if __name__ == '__main__':
    cli = CLI()
# controller = Controller()
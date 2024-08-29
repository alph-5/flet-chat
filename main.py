import flet as ft


class MessageContainer(ft.Container):
    def __init__(self, username, message):
        super().__init__()
        self.username = username
        self.message = message

        self.bgcolor = ft.colors.PRIMARY_CONTAINER
        self.border_radius = 10
        self.padding = 10

        self.content = ft.Column([
            ft.Row(
                controls=[
                    ft.Row([
                        ft.CircleAvatar(content=ft.Text(self.username[0]), bgcolor=ft.colors.random_color()),
                        ft.Text(self.username, theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
                    ]),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                icon=ft.icons.STAR_BORDER,
                                text="Add to favorites"
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Text(self.message)
        ])


def main(page: ft.Page):
    def on_recieve_post(message):
        page.add(message)

    def makenewpost(e):
        page.pubsub.send_all(MessageContainer(username=usernametextfield.value, message=posttextfield.value))
        page.close(newpostdialog)

    def chooseusername(e):
        if usernametextfield.value == "":
            usernametextfield.error_text = "Please enter your username"
            page.update()
        else:
            page.close(usernamemodal)

    def openpostdialog(e):
        posttextfield.value = ""
        page.open(newpostdialog)

    posttextfield = ft.TextField(
        hint_text="What do you want to post?",
        multiline=True
    )
    newpostdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("New post"),
        content=posttextfield,
        actions=[
            ft.TextButton("No", on_click=lambda e: page.close(newpostdialog)),
            ft.TextButton("Yes", on_click=makenewpost)
        ]
    )
    usernametextfield = ft.TextField(
        hint_text="Your username",
    )
    usernamemodal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Username"),
        content=usernametextfield,
        actions=[
            ft.TextButton("OK", on_click=chooseusername)
        ]
    )

    page.pubsub.subscribe(on_recieve_post)
    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=openpostdialog)
    page.update()

    page.open(usernamemodal)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)

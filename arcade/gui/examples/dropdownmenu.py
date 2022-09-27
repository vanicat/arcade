"""
Contribution from jans#1643

Still we have to think about a few things:

Which widgets should come with arcade (and will be maintained by us)
Can/should we combine this with the dropdown selection?
"""

import arcade
from arcade.gui import UIManager
from arcade.gui.widgets.dropdownmenu import UIDropDownMenu

if __name__ == '__main__':
    class MyView(arcade.View):
        def __init__(self):
            super().__init__()

            self.mng = UIManager()

            # Add button to UIManager, use UIAnchorWidget defaults to center on screen
            self.dropdown = UIDropDownMenu(
                "Hello",
            )
            for i in range(5):
                self.dropdown.add_option(f"test-{i}")

            self.dropdown.center_on_screen()
            self.mng.add(self.dropdown)

        def on_show_view(self):
            self.window.background_color = arcade.color.WHITE
            self.mng.enable()

        def on_hide_view(self):
            self.mng.disable()

        def on_draw(self):
            self.clear()
            self.mng.draw()


    window = arcade.Window()
    window.show_view(MyView())
    arcade.run()

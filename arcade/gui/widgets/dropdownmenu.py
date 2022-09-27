"""
Contribution from jans#1643

Still we have to think about a few things:

Which widgets should come with arcade (and will be maintained by us)
Can/should we combine this with the dropdown selection?
"""

from copy import deepcopy
from typing import Optional

import arcade
from arcade.experimental.uistyle import UIFlatButtonStyle_default
from arcade.gui import Rect, UIEvent, UIMousePressEvent
from arcade.gui.events import UIOnClickEvent
from arcade.gui.widgets import UILayout, UIWidget
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIBoxLayout


class UIDropDownMenu(UILayout):
    def __init__(self, text: str = None, width=100, height=32, default_option_heigth=25,
                 auto_close: bool = True, style=None, **kwargs):
        if style is None:
            style = {}

        super().__init__(width=width, height=height, style=style, **kwargs)

        self.default_option_heigth = default_option_heigth
        self.auto_close = auto_close
        self.button_style = deepcopy(UIFlatButtonStyle_default)

        self._title_button = UIFlatButton(text=text, width=self.width, height=self.height, style=self.button_style)
        self._title_button.on_click = self._on_dropdown_click  # type: ignore

        self._dropdown = UIBoxLayout()
        self._dropdown.visible = False

        self.total_rect = None

        self.add(self._title_button)
        self.add(self._dropdown)

        self.register_event_type("on_click")

    def add_option(self, text, heigth=None, style=None):
        button = self._dropdown.add(UIFlatButton(
            text=text,
            width=self.width,
            height=heigth or self.default_option_heigth,
            style=style or self.button_style
        ))
        button.on_click = self._on_option_click

    def add_divider(self):
        self._dropdown.add(UIWidget(width=self.width, height=2).with_background(color=arcade.color.GRAY))

    def _on_dropdown_click(self, event: UIOnClickEvent):
        self._dropdown.visible = not self._dropdown.visible

    def _on_option_click(self, event: UIOnClickEvent):
        self.dispatch_event("on_click", UIOnClickEvent(event.source, event.x, event.y))
        self.close()

    def do_layout(self):
        self.total_rect = Rect(self._title_button.rect.x, self._dropdown.rect.y,
                               self._title_button.rect.width + self._title_button.rect.x,
                               self._dropdown.rect.height + self._dropdown.rect.y)
        self._title_button.rect = self.rect

        self._dropdown.fit_content()  # resize layout to contain widgets
        self._dropdown.rect = self._dropdown.rect.align_top(self.bottom).align_left(
            self._title_button.left
        )

    def close(self):
        self._dropdown.visible = False

    @property
    def is_open(self):
        return self._dropdown.visible

    def open(self):
        self._dropdown.visible = True

    def on_click(self, event: UIOnClickEvent):
        pass

    def on_event(self, event: UIEvent) -> Optional[bool]:
        if self.auto_close:
            if self.is_open and isinstance(event, UIMousePressEvent) and not self.total_rect.collide_with_point(event.x, event.y):
                self.close()
        return super().on_event(event)


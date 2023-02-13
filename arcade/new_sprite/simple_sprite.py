from typing import TYPE_CHECKING, List, Optional, Tuple

from arcade import Texture
from arcade.arcade_types import RGBA, Point

if TYPE_CHECKING:
    from arcade.sprite_list import SpriteList


class SimpleSprite:
    """
    Class tat represent's a 'sprite' on-screen. This class is the bare minumum needed
    to draw a Sprite to the screen.
    """

    def __init__(
        self,
        texture: Texture,
        *,
        center_x: float = 0.0,
        center_y: float = 0.0,
        color: RGBA = (255, 255, 255, 255),
        angle: float = 0.0,
        scale_x: float = 1.0,
        scale_y: float = 1.0,
    ):
        self._position: Point = (center_x, center_y)
        self._color: RGBA = color
        self._angle = angle
        self._scale: Tuple[float, float] = (scale_x, scale_y)
        self._texture = texture

        self._width = self._texture.width * self._scale[0]
        self._height = self._texture.height * self._scale[1]

        self.sprite_lists: List["SpriteList"] = []
        self._sprite_list: Optional["SpriteList"] = None  # Used for SimpleSprite.draw()

    def _get_position(self) -> Point:
        """
        Get the center x and y coordinates of the sprite.

        Returns:
            (center_x, center_y)
        """
        return self._position

    def _set_position(self, new_value: Point):
        """
        Set the center x and y coordinates of the sprite.

        :param Point new_value: New position.
        """
        if new_value == self._position:
            return

        self._position = new_value

        for sprite_list in self.sprite_lists:
            sprite_list.update_location(self)

    position = property(_get_position, _set_position)

    def _get_center_x(self) -> float:
        """
        Get the center x coordinate of the sprite.

        Returns:
            center_x
        """
        return self._position[0]

    def _set_center_x(self, new_value: float):
        """
        Set the center x coordinate of the sprite.

        :param float new_value: New center X coordinate
        """
        if new_value == self._position[0]:
            return

        self._position = (new_value, self._position[1])

        for sprite_list in self.sprite_lists:
            sprite_list.update_location(self)

    center_x = property(_get_center_x, _set_center_x)

    def _get_center_y(self) -> float:
        """
        Get the center y coordinate of the sprite.

        Returns:
            center_y
        """
        return self._position[1]

    def _set_center_y(self, new_value: float):
        """
        Set the center y coordinate of the sprite.

        :param float new_value: New center Y coordinate
        """
        if new_value == self._position[1]:
            return

        self._position = (self._position[0], new_value)

        for sprite_list in self.sprite_lists:
            sprite_list.update_location(self)

    center_y = property(_get_center_y, _set_center_y)

    def _get_scale(self) -> Tuple[float, float]:
        """
        Get the x and y scale values for the Sprite

        Returns:
            (scale_x, scale_y)
        """
        return self._scale

    def _set_scale(self, new_value: Tuple[float, float]):
        """
        Set the x and y scale values of the sprite.

        :param Tuple[float, float] new_value: New scale
        """
        if new_value == self._scale:
            return

        self._scale = new_value
        self._width = self._texture.width * self._scale[0]
        self._height = self._texture.height * self._scale[1]

        for sprite_list in self.sprite_lists:
            sprite_list.update_size(self)

    scale = property(_get_scale, _set_scale)

    def _get_scale_x(self) -> float:
        """
        Get the x scale value for the Sprite

        Returns:
            scale_x
        """
        return self._scale[0]

    def _set_scale_x(self, new_value: float):
        """
        Set the x scale value for the Sprite

        :param float new_value: The new x scale
        """
        if new_value == self._scale[0]:
            return

        self._scale = (new_value, self._scale[1])
        self._width = self._texture.width * self._scale[0]

        for sprite_list in self.sprite_lists:
            sprite_list.update_size(self)

    scale_x = property(_get_scale_x, _set_scale_x)

    def _get_scale_y(self) -> float:
        """
        Get the y scale value for the Sprite

        Returns:
            scale_y
        """
        return self._scale[1]

    def _set_scale_y(self, new_value: float):
        """
        Set the y scale value for the Sprite

        :param float new_value: The new y scale
        """
        if new_value == self._scale[1]:
            return

        self._scale = (self._scale[0], new_value)
        self._height = self._texture.height * self._scale[1]

        for sprite_list in self.sprite_lists:
            sprite_list.update_size(self)

    scale_y = property(_get_scale_y, _set_scale_y)

    def _get_angle(self) -> float:
        """Get the angle of the sprite's rotation."""
        return self._angle

    def _set_angle(self, new_value: float):
        if new_value == self._angle:
            return

        self._angle = new_value

        for sprite_list in self.sprite_lists:
            sprite_list.update_angle(self)

    angle = property(_get_angle, _set_angle)

    def _get_color(self) -> RGBA:
        """
        Get the RGBA color associated with the sprite

        Returns:
            color
        """
        return self._color

    def _set_color(self, new_value: RGBA):
        """
        Set the RGB or RGBA color associated with the sprite

        :param RGBA new_value: The new RGB or RGBA tuple for the sprite's color
        """
        if new_value == self._color:
            return

        if len(new_value) == 3:
            # Mypy can't figure this out
            self._color = *new_value, self._color[3]  # type: ignore
        elif len(new_value) == 4:
            self._color = new_value
        else:
            raise ValueError("Color must be three or four ints from 0-255")

        for sprite_list in self.sprite_lists:
            sprite_list.update_color(self)

    color = property(_get_color, _set_color)

    def _get_alpha(self) -> int:
        """Return the alpha of the sprite"""
        return self._color[3]

    def _set_alpha(self, new_value: int):
        """
        Set the alpha value of the sprite.

        :param int new_value: The new alpha
        """
        if new_value == self._color[3]:
            return

        # Cast to int incase someone provies a float
        self._color = self._color[0], self._color[1], self._color[2], int(new_value)

        for sprite_list in self.sprite_lists:
            sprite_list.update_color(self)

    alpha = property(_get_alpha, _set_alpha)

    def _get_texture(self) -> Texture:
        return self._texture

    def _set_texture(self, texture: Texture):
        if texture == self._texture:
            return

        self._texture = texture
        self._width = self._texture.width * self._scale[0]
        self._height = self._texture.height * self._scale[1]

        for sprite_list in self.sprite_lists:
            sprite_list.update_texture(self)

    texture = property(_get_texture, _set_texture)

    def _get_top(self) -> float:
        return self.center_y + (self._height / 2)

    def _set_top(self, new_value: float):
        self.center_y += new_value - self.top

    top = property(_get_top, _set_top)

    def _get_bottom(self) -> float:
        return self.center_y - (self._height / 2)

    def _set_bottom(self, new_value: float):
        self.center_y += new_value - self.bottom

    bottom = property(_get_bottom, _set_bottom)

    def _get_left(self) -> float:
        return self.center_x - (self._width / 2)

    def _set_left(self, new_value: float):
        self.center_x += new_value - self.left

    left = property(_get_left, _set_left)

    def _get_right(self) -> float:
        return self.center_x + (self._width / 2)

    def _set_right(self, new_value: float):
        self.center_x += new_value - self.right

    right = property(_get_right, _set_right)

    def register_sprite_list(self, new_list: "SpriteList") -> None:
        self.sprite_lists.append(new_list)

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        if self._sprite_list is None:
            from arcade import SpriteList

            self._sprite_list = SpriteList(capacity=1)
            self._sprite_list.append(self)

        self._sprite_list.draw(
            filter=filter, pixelated=pixelated, blend_function=blend_function
        )

    def remove_from_sprite_lists(self) -> None:
        if len(self.sprite_lists) > 0:
            # We can't modify a list as we iterate though it, so creating a copy
            sprite_lists = self.sprite_lists.copy()
        else:
            # If only 1 list, no need to copy
            sprite_lists = self.sprite_lists

        for sprite_list in sprite_lists:
            if self in sprite_list:
                sprite_list.remove(self)

        self.sprite_lists.clear()

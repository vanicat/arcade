from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from arcade import Texture, load_texture
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
        texture_or_path: Union[Texture, str],
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

        if isinstance(texture_or_path, str):
            self._texture = load_texture(texture_or_path)
        elif isinstance(texture_or_path, Texture):
            self._texture = texture_or_path
        else:
            raise ValueError(
                "Value passed to SimpleSprite must be either a Texture or filepath string"
            )

        self._width = self._texture.width * self._scale[0]
        self._height = self._texture.height * self._scale[1]

        self.sprite_lists: List["SpriteList"] = []
        self._sprite_list: Optional["SpriteList"] = None  # Used for SimpleSprite.draw()

    @property
    def position(self) -> Point:
        """
        Get the center x and y coordinates of the sprite.

        Returns:
            (center_x, center_y)
        """
        return self._position

    @position.setter
    def position(self, new_value: Point):
        """
        Set the center x and y coordinates of the sprite.

        :param Point new_value: New position.
        """
        if new_value == self._position:
            return

        self._position = new_value

        for sprite_list in self.sprite_lists:
            sprite_list.update_location(self)

    @property
    def center_x(self) -> float:
        """
        Get the center x coordinate of the sprite.

        Returns:
            center_x
        """
        return self._position[0]

    @center_x.setter
    def center_x(self, new_value: float):
        """
        Set the center x coordinate of the sprite.

        :param float new_value: New center X coordinate
        """
        if new_value == self._position[0]:
            return

        self._position = (new_value, self._position[1])

        for sprite_list in self.sprite_lists:
            sprite_list.update_location(self)

    @property
    def center_y(self) -> float:
        """
        Get the center y coordinate of the sprite.

        Returns:
            center_y
        """
        return self._position[0]

    @center_x.setter
    def center_y(self, new_value: float):
        """
        Set the center y coordinate of the sprite.

        :param float new_value: New center Y coordinate
        """
        if new_value == self._position[1]:
            return

        self._position = (self._position[0], new_value)

        for sprite_list in self.sprite_lists:
            sprite_list.update_location(self)

    @property
    def scale(self) -> Tuple[float, float]:
        """
        Get the x and y scale values for the Sprite

        Returns:
            (scale_x, scale_y)
        """
        return self._scale

    @scale.setter
    def scale(self, new_value: Tuple[float, float]):
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

    @property
    def scale_x(self) -> float:
        """
        Get the x scale value for the Sprite

        Returns:
            scale_x
        """
        return self._scale[0]

    @scale_x.setter
    def scale_x(self, new_value: float):
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

    @property
    def scale_y(self) -> float:
        """
        Get the y scale value for the Sprite

        Returns:
            scale_y
        """
        return self._scale[1]

    @scale_y.setter
    def scale_y(self, new_value: float):
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

    @property
    def angle(self) -> float:
        """Get the angle of the sprite's rotation."""
        return self._angle

    @angle.setter
    def angle(self, new_value: float):
        if new_value == self._angle:
            return

        self._angle = new_value

        for sprite_list in self.sprite_lists:
            sprite_list.update_angle(self)

    @property
    def color(self) -> RGBA:
        """
        Get the RGBA color associated with the sprite

        Returns:
            color
        """
        return self._color

    @color.setter
    def color(self, new_value: RGBA):
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

    @property
    def alpha(self) -> int:
        """Return the alpha of the sprite"""
        return self._color[3]

    @alpha.setter
    def alpha(self, new_value: int):
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

    @property
    def texture(self) -> Texture:
        return self._texture

    @texture.setter
    def texture(self, texture: Texture):
        if texture == self._texture:
            return

        self._texture = texture
        self._width = self._texture.width * self._scale[0]
        self._height = self._texture.height * self._scale[1]

        for sprite_list in self.sprite_lists:
            sprite_list.update_texture(self)

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

    def kill(self) -> None:
        self.remove_from_sprite_lists

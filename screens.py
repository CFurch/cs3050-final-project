import arcade


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

SCREEN_TITLE = "2D Lethal Company"

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("resources/screens.jpeg")

    def on_show(self):
        pass

    def on_draw(self):
        arcade.start_render()
        # Draw your start screen graphics here
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw the start button
        arcade.draw_xywh_rectangle_filled(self.button_x - self.button_width // 2, self.button_y - self.button_height // 2,
                                          self.button_width, self.button_height, arcade.color.WHITE)
        # Draw text on the start button
        arcade.draw_text("Start", self.button_x, self.button_y,
                         arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle mouse click events here
        # Check if the mouse click is inside the start button
        if (self.button_x - self.button_width // 2 < x < self.button_x + self.button_width // 2 and
                self.button_y - self.button_height // 2 < y < self.button_y + self.button_height // 2):
            # Start the game when the button is clicked
            game_view = LethalCo()
            self.window.show_view(game_view)

    class GameView(arcade.View):
        def __init__(self):
            super().__init__()
        # Initialize the game view

    def on_key_press(self, key, modifiers):
        # Handle key press events here
        pass

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "My Game")
        self.start_view = StartScreen()

    def setup(self):
        # Initialize your game here
        pass

    def on_draw(self):
        # Render your game objects here
        pass

    def on_key_press(self, key, modifiers):
        # Handle key press events for the game
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle mouse click events for the game
        pass

    def switch_to_game(self):
        # Switch to the main game view
        self.window.show_view(self.main_game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Start Screen Example")
    start_view = StartScreen()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
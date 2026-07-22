import arcade

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
SCREEN_TITLE = "Test Arcade 3.0 - Balle, Ligne et Souris"

class MonJeu(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.AMAZON

        # --- Variables de la balle ---
        self.balle_x = 400
        self.balle_y = 300
        self.balle_vitesse_x = 5
        self.balle_vitesse_y = 3
        self.balle_rayon = 20

        # --- Variables de la souris ---
        self.souris_x = 0
        self.souris_y = 0

        # --- Optimisation Arcade 3.0 : L'objet Text ---
        # On le crée une seule fois dans l'init
        self.texte_info = arcade.Text(
            text="",
            x=10, 
            y=10,
            color=arcade.color.WHITE,
            font_size=14
        )

    def on_update(self, delta_time: float):
        # Déplacement de la balle
        self.balle_x += self.balle_vitesse_x
        self.balle_y += self.balle_vitesse_y

        # Rebond sur les murs
        if self.balle_x > SCREEN_WIDTH - self.balle_rayon or self.balle_x < self.balle_rayon:
            self.balle_vitesse_x *= -1
            
        if self.balle_y > SCREEN_HEIGHT - self.balle_rayon or self.balle_y < self.balle_rayon:
            self.balle_vitesse_y *= -1

        # Mise à jour du texte (on change juste la propriété .text de l'objet)
        self.texte_info.text = f"Balle: {self.balle_x}, {self.balle_y} | Souris: {self.souris_x}, {self.souris_y}"

    def on_draw(self):
        self.clear()

        # 1. On dessine une LIGNE entre la souris et la balle
        # Parfait pour modéliser tes "Connections" plus tard !
        arcade.draw_line(
            start_x=self.souris_x, 
            start_y=self.souris_y, 
            end_x=self.balle_x, 
            end_y=self.balle_y, 
            color=arcade.color.YELLOW, 
            line_width=2
        )

        # 2. On dessine la balle
        arcade.draw_circle_filled(
            center_x=self.balle_x,
            center_y=self.balle_y,
            radius=self.balle_rayon,
            color=arcade.color.CRIMSON
        )
        
        # 3. On affiche le texte
        self.texte_info.draw()

    # --- NOUVEAU : Interaction avec la souris ---
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """ Appelé automatiquement par Arcade à chaque fois que la souris bouge """
        self.souris_x = x
        self.souris_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Appelé quand on clique """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Si on fait un clic gauche, on téléporte la balle sur la souris
            self.balle_x = x
            self.balle_y = y

if __name__ == "__main__":
    fenetre = MonJeu()
    arcade.run()
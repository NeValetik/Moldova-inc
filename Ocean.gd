extends CanvasLayer

var game_started = false;
var starting_country;


func _on_color_rect_focus_entered():
	if Input.is_action_pressed("on_mouse_press"):
		$CountryButton.text = "World"

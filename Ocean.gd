extends CanvasLayer


func _on_color_rect_focus_entered():
	if Input.is_action_pressed("on_mouse_press"):
		%CountryButton.text = "Мир"

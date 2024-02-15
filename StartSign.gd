extends Sprite2D


var start_country;


func _on_button_pressed():
	start_country = get_parent().editor_description
	get_parent().game_started = true
	get_parent().get_parent().starting_country = start_country
	get_parent().get_parent().game_started = true
	self.queue_free()


func _on_button_mouse_entered():
	get_parent().on_sign = true


func _on_button_mouse_exited():
	get_parent().on_sign = false

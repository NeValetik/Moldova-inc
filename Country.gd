extends Panel

var focused = false

var game_started;




func _ready():
	self.process_priority = 1
	game_started = get_parent().game_started 

func _process(delta):
	game_started = get_parent().game_started 

func _on_focus_entered():
	if Input.is_action_pressed("on_mouse_press"):
		
		var countryName = self.editor_description
		$"../CountryButton".text = countryName
		
		if game_started == false:
			focused = true
			var start_sign = preload("res://gui/start_sign.tscn").instantiate()
			start_sign.global_position = get_local_mouse_position()
			add_child(start_sign)

var on_sign = false

func _on_focus_exited():
	if on_sign == false and game_started == false:
		self.get_child(0).queue_free()
		focused = false
	else:
		pass



func _on_gui_input(event):
	if focused == true and game_started == false:
		if event.is_action_pressed("on_mouse_press"):
			self.get_child(0).queue_free()
			var start_sign = preload("res://gui/start_sign.tscn").instantiate()
			start_sign.global_position = get_local_mouse_position()
			add_child(start_sign)

extends CanvasLayer

var pressed_again = false;

func _input(ev):
	#await get_tree().create_timer(0.1).timeout  
	if Input.is_key_pressed(KEY_ESCAPE) and pressed_again == false and %LoadingScreen.visible == false:
		self.visible = true
		get_tree().paused = true
		pressed_again = true
		process_mode = Node.PROCESS_MODE_WHEN_PAUSED
	elif Input.is_key_pressed(KEY_ESCAPE) and pressed_again == true and %LoadingScreen.visible == false:
		self.visible = false
		get_tree().paused = false
		pressed_again = false
		process_mode = Node.PROCESS_MODE_ALWAYS
		


func _on_resume_button_button_down():
	self.visible = false
	pressed_again = false
	get_tree().paused = false
	process_mode = Node.PROCESS_MODE_ALWAYS


func _on_exit_button_button_down():
	get_parent().get_tree().quit()

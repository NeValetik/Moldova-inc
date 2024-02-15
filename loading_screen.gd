extends CanvasLayer


func _on_exit_button_button_down():
	get_parent().get_tree().quit()

extends Button


func _on_button_down():
	$"../Asset".visible = true
	$"../Asset2".visible = false
	$"../Asset3".visible = false
	$"../Asset4".visible = false

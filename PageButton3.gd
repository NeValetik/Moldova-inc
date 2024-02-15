extends Button


func _on_button_down():
	$"../Asset".visible = false
	$"../Asset2".visible = false
	$"../Asset3".visible = true
	$"../Asset4".visible = false

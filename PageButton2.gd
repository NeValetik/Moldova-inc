extends Button



func _on_button_down():
	$"../Asset".visible = false
	$"../Asset2".visible = true
	$"../Asset3".visible = false
	$"../Asset4".visible = false

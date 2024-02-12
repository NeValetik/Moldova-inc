extends Node2D


func _ready():
	%LoadingScreen.visible = true



func _on_loading_screen_tree_exited():
	print()
	get_node(".").queue_free()

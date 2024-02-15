extends CanvasLayer

var country

func _on_country_button_button_down():
	self.visible = true
	country = $"../Ocean/CountryButton".text
	%CountryImg.texture = load("res://worldmap/%s.png"%country)


func _on_close_button_button_down():
	self.visible = false



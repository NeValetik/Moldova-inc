extends Panel

var db : SQLite
var db_name = "res://dataBase/CountryDataset.db"


func evaluate(command, variable_names = [], variable_values = []):
	var expression = Expression.new()
	var error = expression.parse(command, variable_names)
	if error != OK:
		push_error(expression.get_error_text())
		return

	var result = expression.execute(variable_values, self)

	if not expression.has_execute_failed():
		print(str(result))
		return result


#func _ready():
	#db = SQLite.new()
	#db.path = db_name
	#db.open_db()
	#var graph_links = db.select_rows("CountryData","ID",["ID","Country","Edges"])
	#print(self.get_meta("metadata/Index"))
	#self.editor_description = graph_links[self.get_meta("metadata/Index")]["Country"]
	#self.set_meta("links",evaluate(graph_links[self.get_meta("metadata/Index")]["Edges"]))


func _on_focus_entered():
	if Input.is_action_pressed("on_mouse_press"):
		var countryName = self.editor_description
		%CountryButton.text = countryName


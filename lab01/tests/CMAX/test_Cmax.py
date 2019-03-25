from Agregator_dir.Agregator_class import Agregator


correct_values = 31

def test_should_pass_if_Cmax_calculated_correctly(correct_values):
	agregator = Agregator("test.txt")
	assert agregator.Cmax_test() == correct_values
	print("PASSED - test_should_pass_if_Cmax_calculated_correctly")

test_should_pass_if_Cmax_calculated_correctly(correct_values)
from Agregator_dir.Agregator_class import Agregator


correct_values = [31, ]
files = ['test.txt',
]


def test_should_pass_if_Cmax_calculated_correctly(correct_values, files):
	for file in files:
		for cmax in correct_values:
			agregator = Agregator(file)
			assert agregator.Cmax_test() == cmax
			print("PASSED - test_should_pass_if_Cmax_calculated_correctly")

test_should_pass_if_Cmax_calculated_correctly(correct_values, files)
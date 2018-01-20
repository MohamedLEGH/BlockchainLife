from captchaSolver import captchaSolver



print("\ntest ---\n")
c_solver = captchaSolver("fd58e13e22604e820052b44611d61d6c")
print("current :" + c_solver.getCurrentKey())
temp = c_solver.getBalance()
print("test: " + str(temp))
print("___________________________________________________________________________")
solution = c_solver.solveCaptchaTextCaseSensitive("/home/testm2/Desktop/testcscr/php/pyhton/cap2.jpg")
print("\n\n**************************************\n\n")
print("Solution: " + str(solution))

print("\n\n***************************************\n\n\n")

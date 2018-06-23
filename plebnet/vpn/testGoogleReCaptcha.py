from reCaptchaSolver import reCaptchaSolver

print("\ntest ---\n")
rc_solver = reCaptchaSolver("fd58e13e22604e820052b44611d61d6c")
print("current :" + rc_solver.getCurrentKey())
temp = rc_solver.getBalance()
print("test: " + str(temp))
print("___________________________________________________________________________")
wUrl = "http://http.myjino.ru/recaptcha/test-get.php"
wKey = "6Lc_aCMTAAAAABx7u2W0WPXnVbI_v6ZdbM6rYf16"
rc_solution = rc_solver.solveGoogleReCaptcha(wUrl,wKey)
print("\n\n******* hash solution: ****** \n\n" + rc_solution + "\n\n*******\n\n")
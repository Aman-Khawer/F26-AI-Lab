# AI Lab 1: Introduction to AI & Paradigms

# TASK 1: AI Timeline:
# Timeline will be written in the Word report.

# TASK 2: Rule-Based Scholarship System:
def scholarship(score,document_completed,attendance,recommendation):
    if score >= 70 and document_completed and attendance and recommendation:
        return "review"
    else:
        return "hold"

print("TASK 2: SCHOLARSHIP SYSTEM")
tests= [
        ("pass",85,True,True,True,"review"),
        ("Attendance Fail",75,True,False,True,"hold"),
        (" No Recommendation",80,True,True,False,"hold"),
        ("Boundary Score",70,True,True,True,"review")
 ]
for name, score, complete, attendance, recommendation, expected in tests:
        actual = scholarship(score, complete, attendance, recommendation)

        print(
        ("Test:", name),
        ("Input:", score, complete, attendance, recommendation),
        ("Expected:", expected),
        ("Actual:", actual)
       )
        if actual == expected:
           print("Result: PASS")
        else: 
         print("Result: FAIL")

# TASK 3: Conversational Test

print("\nTASK 3: CONVERSATIONAL TEST")
print("A machine may talk like a human but still give wrong answers.")
print("So, conversation alone cannot prove general intelligence.")


    




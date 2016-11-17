import unittest

from racyon import run

class TestStringMethods(unittest.TestCase):

    def test_basics(self):
        self.assertEqual(run("(+ 1 1)"), 2)
        self.assertEqual(run("(> 3 (+ 1 1))"), True)

    def test_lambda(self):
        self.assertEqual(run("""((lambda (abs) (list (abs (- 5 7))
                                         (abs (- 7 5))))
                                (lambda (x) (if ( < x 0) (- 0 x) x)))"""), [2,2])

    def test_define(self):
        self.assertEqual(run("""(define abs (lambda (x) (if (< x 0) (- 0 x) x)))"""), None)
        self.assertEqual(run("(list (abs (- 7 5)) (abs (- 5 7)))"), [2,2])

    def test_logic(self):
        self.assertEqual(run("(and #true #true #true)"), True)
        self.assertEqual(run("(or #true #true #true)"), True)
        self.assertEqual(run("(and #true #false #true)"), False)
        self.assertEqual(run("(or #true #false #true)"), True)
        self.assertEqual(run("(or #false #false #false)"), False)

    def test_list_functions(self):
        self.assertEqual(run("(list 1 2 3 4)"), [1,2,3,4])
        self.assertEqual(run("(empty? empty)"), True)
        self.assertEqual(run("(cons 5 empty)"), [5])
        self.assertEqual(run("(rest (list 1 2 3 4))"), [2,3,4])
        self.assertEqual(run("(first (list 1 2 3 4))"), 1)
        self.assertEqual(run("(second (list 1 2 3 4))"), 2)
        self.assertEqual(run("(third (list 1 2 3 4))"), 3)

    def test_struct(self):
        self.assertEqual(run("(define-struct boat (capacity passengers))"), None)
        self.assertEqual(run("(define boat (make-boat 100 90))"), None)
        self.assertEqual(run("(boat-capacity boat)"), 100)
        self.assertEqual(run("(boat-passengers boat)"), 90)
        self.assertEqual(run("(boat? boat)"), True)
        self.assertEqual(run("(define-struct train (capacity passengers))"), None)
        self.assertEqual(run("(define train (make-train 100 90))"), None)
        self.assertEqual(run("(train-capacity train)"), 100)
        self.assertEqual(run("(train-passengers train)"), 90)
        self.assertEqual(run("(boat? train)"), False)
        self.assertEqual(run("(train? train)"), True)
        self.assertEqual(run("(train? boat)"), False)

if __name__ == '__main__':
    unittest.main()

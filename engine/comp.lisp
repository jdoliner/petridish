(defun make-gensyms (n)
  (cond
    ((= n 0) nil)
    (T (cons (gensym) (make-gensyms (- n 1))))))

(defun decl (f)
  (first (getf (symbol-plist f) 'SYSTEM::DEFINITION)))

(defun name (decl)
 (second decl))

(defun args (decl)
  (third decl))

(defun body (decl)
  (fourth decl))

(defun plus (x y)
  (+ x y))

;;rplc every instances of in body of orig with new
(defun rplc (orig new body)
  (cond
    ((eq body nil) nil)
    ((consp (first body)) (cons (rplc orig new (first body)) (rplc orig new (rest body))))
    ((eq orig (first body)) (cons new (rplc orig new (rest body))))
    (T (cons (first body) (rplc orig new (rest body))))))

(defun rplc-list (orig new body)
  (cond
    ((and orig new) (rplc-list (rest orig) (rest new) (rplc (first orig) (first new) body)))
    (T body)))

(defun hygienic-h (dcl argn)
 (cond
  ((> (+ argn 1) (length (third dcl))) dcl)
  (T  (let* ((dcl (hygienic-h dcl (+ argn 1)))
	     (orig (nth argn (args dcl)))
	     (new (gensym)))
	(list (first dcl) (name dcl) (rplc orig new (args dcl)) (rplc orig new (body dcl)))))))

(defun hygienic (decl)
 (let ((h-decl (hygienic-h decl 0)))
  (list (first h-decl) (gensym) (args h-decl) (body h-decl))))

;;insert list2 into list1 in place of element n
(defun insert (list1 n list2)
  (cond
    ((= n 0) (append list2 (rest list1)))
    (T (cons (first list1) (insert (rest list1) (- n 1) list2)))))

;;pipe decl2 into argument n of decl1
(defun pipe (newname decl1 n decl2)
  (cond
    ((> (+ n 1) (length (args decl1))) (list (first decl1) newname (args decl1) (body decl1)))
    (T (list (first decl1) newname (insert (args decl1) n (args decl2)) (rplc (nth n (args decl1)) (body decl2) (body decl1))))))

;;pinches a declaration, by associating
;;for example (pinch (decl 'plus) '(0 0)) will return (defun newname (x) (+ x x))
(defun pinch (newname decl pinch-list)
  (if (not (eq (length (args decl)) (length pinch-list)))
    (error "pinchlist is the wrong length")
    (let* ((num_args (+ (eval `(max ,@pinch-list)) 1))
	   (new-args (make-gensyms num_args)))
      (list (first decl) newname new-args (rplc-list (args decl) 
						     (mapcar (lambda (n) (nth n new-args)) pinch-list) 
						     (body decl))))))

(defun main(fname)
 (progn
  (load fname)
  (if (boundp 'operation)
  (cond
    ((eq operation 'pipe)
     (if (and (boundp 'newname) (boundp 'decl1) (boundp 'n) (boundp 'decl2))
       (pipe newname (hygienic decl1) n (hygienic decl2))
       (error "At least one of {newname, decl1 n decl2} was unspecified.")))
    ((eq operation 'pinch)
     (if (and (boundp 'newname) (boundp 'decl1) (boundp 'pinch-list))
       (pinch newname (hygienic decl1) pinch-list)
       (error "At least one of {newname decl1 pinch-list} was unspecified.")))
     (T (error "Invalid operation, supported operations are {pipe, pinch}.")))
   (error "no operation specified"))))

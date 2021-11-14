(defun determine-princess (size)
  (let* ((x nil) (y nil))
    (dotimes (fy size)
      (let ((fx (position #\p (read-line) :test #'equal)))
        (if fx (list (setf x fx) (setf y fy)))))
    (list x y)))

(defun delimiterp (c) (position c " "))

(defun my-split (string &key (delimiterp #'delimiterp))
  (loop :for beg = (position-if-not delimiterp string)
        :then (position-if-not delimiterp string :start (1+ end))
        :for end = (and beg (position-if delimiterp string :start beg))
        :when beg :collect (subseq string beg end)
        :while end))

(defun decide (dx dy)
  (cond
   ((and
     (> dx 0)
     (> (abs dx) (abs dy)))
    :right)
   ((and
     (< dx 0)
     (> (abs dx) (abs dy)))
    :left)
   ((> dy 0) :down)
   (t :up)))

(defun rescue-princess ()
  (let* ((size (parse-integer (read-line)))
         (l (my-split (read-line)))
         (b (list (parse-integer (second l)) (parse-integer (first l))))
         (p (determine-princess size))
         (v (mapcar (function -) p b)))
    (princ (symbol-name (apply (function decide) v)))))


(rescue-princess)


(print (+ 1 2))

(do 
    (print "hello world")
    (do 
        (print "another message")
        (return (return 3))
    )
    (print "escaped message")
)

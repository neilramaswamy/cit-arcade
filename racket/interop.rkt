#lang racket/base

(require pyffi)

; Initialization for the FFI
(initialize)
(post-initialize)

; We assume that this is being run from the cit-arcade root directory
(import game)
(import game.driver)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;  PIXEL GENERATION HELPERS  ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Generates a row of red pixels in increasing intensity
(define (generate-row num-cols)
  (define step (/ 255.0 num-cols))
  
  ; Helper function that keeps track of our current column
  (define (helper num-cols curr-col)
    (if (= num-cols 0)
        '()
        (cons (list (* step curr-col) 0 0) (helper (- num-cols 1) (+ curr-col 1)))))

  ; Call the helper
  (helper num-cols 0))


; Generates a matrix of pixels of shape (num-rows, num-cols)
(define (generate-pixels num-rows num-cols)
  (if (= num-rows 0)
      '()
      (cons (generate-row num-cols) (generate-pixels (- num-rows 1) num-cols))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   SCREEN INITIALIZATION   ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define driver (game.driver.InteropModeDriver))

(define py-dimensions (driver.initialize_screen))
(define dimensions (pytuple->vector py-dimensions))

(define rows (vector-ref dimensions 0))
(define cols (vector-ref dimensions 1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;     SCREEN PAINTING       ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(driver.paint_screen (generate-pixels rows cols))


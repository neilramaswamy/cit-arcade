#lang racket/base

(require pyffi)
(require 2htdp/image)

; Initialization for the FFI
(initialize)
(post-initialize)

; We assume that this is being run from the cit-arcade root directory
(import game)
(import game.driver)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;  PIXEL GENERATION HELPERS  ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Transforms a list of 2htdp/image/color into a flat list of [R, G, B]
(define (color-list-to-list clist)
  (map (lambda (kolor) (list (color-red kolor) (color-green kolor) (color-blue kolor))) clist))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   SCREEN INITIALIZATION   ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define driver (game.driver.InteropModeDriver))

(define py-dimensions (driver.initialize_screen))
(define dimensions (pytuple->vector py-dimensions))

(define num-rows (vector-ref dimensions 0))
(define num-cols (vector-ref dimensions 1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;     SCREEN PAINTING       ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; Loads a sequence of GIF frames in dir, assuming they are sorted alphabetically
; Returns a list of 2htdp/image.
(define (load-gif dir num-cols num-rows)
  ; They come back from the OS sorted
  (define frame-paths (map (lambda (x) (build-path dir x)) (directory-list dir)))

  (displayln (path->string (car frame-paths)))

  (map (lambda (path)
         (define img (bitmap/file (path->string path)))

         (define img-cols (image-width img))
         (define img-rows (image-height img))

         (define scaled-img (scale/xy (/ num-cols img-cols) (/ num-rows img-rows) img))

         scaled-img) frame-paths))

; Render a list of already-scaled 2htdp/image to the screen
(define (show-gif frames)
  (define color-lists (map (lambda (frame)
    (color-list-to-list (image->color-list (rotate 90 frame)))) frames))

  (map (lambda (color-list)
        (define t0 (current-inexact-monotonic-milliseconds))
         (driver.paint_screen_flat color-list)
         (define t1 (current-inexact-monotonic-milliseconds))
         (displayln (- t1 t0))) color-lists)

  ; Run indefinitely!
  (show-gif frames))

; Do the actual rendering
(define racket-frames (load-gif "racket/nightmare" num-rows num-cols))
(show-gif racket-frames)
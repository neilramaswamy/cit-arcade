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

; The alpha value for a fully transparent pixel
(define ALPHA_TRANSPARENT 0)
; The RGB value of an all-black pixel
(define BLACK_PIXEL (list 0 0 0))

; Transforms a list of 2htdp/image/color into a flat list of [R, G, B]
(define (color-list-to-list clist)
  (map (lambda (kolor)
          ; Transparent pixels should be black, the "nothing"/off color on our screen
          ; 
          ; I think we need this explicit check because image->color-list (or PNG?) gives transparent
          ; pixels an RGB of (255, 255, 255).
         (if (= (color-alpha kolor) ALPHA_TRANSPARENT)
              BLACK_PIXEL
             (list (color-red kolor) (color-green kolor) (color-blue kolor)))) clist))

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

  (map (lambda (path)
         (define img (bitmap/file (path->string path)))

         (define img-cols (image-width img))
         (define img-rows (image-height img))

         (define scaled-img (scale/xy (/ num-cols img-cols) (/ num-rows img-rows) img))

         scaled-img) frame-paths))

; Render a list of already-scaled 2htdp/image to the screen
(define (show-gif frames)
  ; A List of Lists, where the inner Lists are a sequence of pixels corresponding to a single frame
  ; Compute this up front so we don't have to repeat it ever
  (define list-of-frame-pixels (map (lambda (frame)
    (color-list-to-list (image->color-list frame))) frames))
  
  (define (show-frames)
    (map (lambda (color-list)
          (driver.paint_screen_flat color-list)) list-of-frame-pixels)
    ; Run indefinitely!
    (show-frames))
  
  (show-frames))

; Do the actual rendering
(define racket-frames (load-gif "game/assets/sonic" num-cols num-rows))
(show-gif racket-frames)